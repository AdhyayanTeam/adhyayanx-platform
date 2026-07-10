from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from app.foundation.exceptions.base import AggregateNotFoundError, ValidationError
from app.modules.platform.events.publisher import Publisher
from app.modules.platform.identity.commands import (
    CreateUserCommand,
    DeactivateUserCommand,
    ReactivateUserCommand,
)
from app.modules.platform.identity.events import UserCreated, UserDeactivated, UserReactivated

if TYPE_CHECKING:
    from app.infrastructure.postgres.database import Database

logger = logging.getLogger("app.modules.platform.identity")


class IdentityService:
    """Domain service for user identity operations."""

    def __init__(
        self,
        database: Database,
        publisher: Publisher,
    ) -> None:
        self._db = database
        self._publisher = publisher

    async def create_user(self, command: CreateUserCommand) -> dict[str, Any]:
        async with self._db.session() as session:
            from app.infrastructure.postgres.identity_repository import PostgresIdentityRepository

            repo = PostgresIdentityRepository(session)

            existing = await repo.load_by_email(command.email)
            if existing is not None:
                raise ValidationError(f"User with email '{command.email}' already exists")

            user_id = uuid4()
            user = {
                "id": user_id,
                "organization_id": command.organization_id,
                "email": command.email,
                "name": command.name,
                "lifecycle_state": "active",
                "auth_provider": command.auth_provider,
                "auth_provider_id": command.auth_provider_id,
                "version": 1,
                "metadata": command.metadata,
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }

            await repo.save(user)

            event = UserCreated(
                aggregate_id=user_id,
                data={
                    "email": command.email,
                    "name": command.name,
                    "organization_id": str(command.organization_id),
                },
                metadata=command.metadata,
            )
            await self._publisher.publish(event, session)

            logger.info("User created: %s (%s)", user["id"], command.email)
            return user

    async def get(self, user_id: UUID) -> dict[str, Any]:
        async with self._db.session() as session:
            from app.infrastructure.postgres.identity_repository import PostgresIdentityRepository

            repo = PostgresIdentityRepository(session)

            user = await repo.load(user_id)
            if user is None:
                raise AggregateNotFoundError(f"User {user_id} not found")
            return user

    async def get_by_email(self, email: str) -> dict[str, Any]:
        async with self._db.session() as session:
            from app.infrastructure.postgres.identity_repository import PostgresIdentityRepository

            repo = PostgresIdentityRepository(session)

            user = await repo.load_by_email(email)
            if user is None:
                raise AggregateNotFoundError(f"User with email '{email}' not found")
            return user

    async def deactivate(self, command: DeactivateUserCommand) -> dict[str, Any]:
        async with self._db.session() as session:
            from app.infrastructure.postgres.identity_repository import PostgresIdentityRepository

            repo = PostgresIdentityRepository(session)

            user = await repo.load(command.user_id)
            if user is None:
                raise AggregateNotFoundError(f"User {command.user_id} not found")

            user["lifecycle_state"] = "inactive"
            user["version"] += 1
            user["updated_at"] = datetime.now(UTC)

            await repo.save(user)

            event = UserDeactivated(
                aggregate_id=command.user_id,
                data={"organization_id": str(command.organization_id)},
                metadata=command.metadata,
            )
            await self._publisher.publish(event, session)

            logger.info("User deactivated: %s", command.user_id)
            return user

    async def reactivate(self, command: ReactivateUserCommand) -> dict[str, Any]:
        async with self._db.session() as session:
            from app.infrastructure.postgres.identity_repository import PostgresIdentityRepository

            repo = PostgresIdentityRepository(session)

            user = await repo.load(command.user_id)
            if user is None:
                raise AggregateNotFoundError(f"User {command.user_id} not found")

            user["lifecycle_state"] = "active"
            user["version"] += 1
            user["updated_at"] = datetime.now(UTC)

            await repo.save(user)

            event = UserReactivated(
                aggregate_id=command.user_id,
                data={"organization_id": str(command.organization_id)},
                metadata=command.metadata,
            )
            await self._publisher.publish(event, session)

            logger.info("User reactivated: %s", command.user_id)
            return user

    async def list(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        async with self._db.session() as session:
            from app.infrastructure.postgres.identity_repository import PostgresIdentityRepository

            repo = PostgresIdentityRepository(session)
            return await repo.list(organization_id, skip=skip, limit=limit)
