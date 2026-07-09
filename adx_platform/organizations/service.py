from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from adx_platform.events.publisher import Publisher
from adx_platform.organizations.commands import (
    CreateOrganizationCommand,
    DeleteOrganizationCommand,
    UpdateOrganizationCommand,
)
from adx_platform.organizations.events import (
    OrganizationCreated,
    OrganizationDeleted,
    OrganizationUpdated,
)
from foundation.exceptions.base import AggregateNotFoundError, ValidationError

if TYPE_CHECKING:
    from infrastructure.postgres.database import Database

logger = logging.getLogger("adx_platform.organizations")


class OrganizationService:
    """Domain service for organization operations."""

    def __init__(
        self,
        database: Database,
        publisher: Publisher,
    ) -> None:
        self._db = database
        self._publisher = publisher

    async def create(self, command: CreateOrganizationCommand) -> dict:
        async with self._db.session() as session:
            from infrastructure.postgres.organization_repository import (
                PostgresOrganizationRepository,
            )
            repo = PostgresOrganizationRepository(session)

            if await repo.exists_by_slug(command.slug):
                raise ValidationError(f"Organization with slug '{command.slug}' already exists")

            org = {
                "id": uuid4(),
                "name": command.name,
                "slug": command.slug,
                "lifecycle_state": "active",
                "version": 1,
                "metadata": command.metadata,
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }

            await repo.save(org)

            event = OrganizationCreated(
                aggregate_id=org["id"],
                data={"name": command.name, "slug": command.slug},
                metadata=command.metadata,
            )
            await self._publisher.publish(event, session)

            logger.info("Organization created: %s (%s)", org["id"], command.slug)
            return org

    async def get(self, organization_id: UUID) -> dict:
        async with self._db.session() as session:
            from infrastructure.postgres.organization_repository import (
                PostgresOrganizationRepository,
            )
            repo = PostgresOrganizationRepository(session)

            org = await repo.load(organization_id)
            if org is None:
                raise AggregateNotFoundError(f"Organization {organization_id} not found")
            return org

    async def update(self, command: UpdateOrganizationCommand) -> dict:
        async with self._db.session() as session:
            from infrastructure.postgres.organization_repository import (
                PostgresOrganizationRepository,
            )
            repo = PostgresOrganizationRepository(session)

            org = await repo.load(command.organization_id)
            if org is None:
                raise AggregateNotFoundError(f"Organization {command.organization_id} not found")

            if command.name is not None:
                org["name"] = command.name
            if command.slug is not None:
                org["slug"] = command.slug
            org["version"] += 1
            org["updated_at"] = datetime.now(UTC)

            await repo.save(org)

            event = OrganizationUpdated(
                aggregate_id=org["id"],
                data={"name": org["name"], "slug": org["slug"]},
                metadata=command.metadata,
            )
            await self._publisher.publish(event, session)

            logger.info("Organization updated: %s", org["id"])
            return org

    async def delete(self, command: DeleteOrganizationCommand) -> None:
        async with self._db.session() as session:
            from infrastructure.postgres.organization_repository import (
                PostgresOrganizationRepository,
            )
            repo = PostgresOrganizationRepository(session)

            org = await repo.load(command.organization_id)
            if org is None:
                raise AggregateNotFoundError(f"Organization {command.organization_id} not found")

            await repo.delete(command.organization_id)

            event = OrganizationDeleted(
                aggregate_id=command.organization_id,
                metadata=command.metadata,
            )
            await self._publisher.publish(event, session)

            logger.info("Organization deleted: %s", command.organization_id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[dict]:
        async with self._db.session() as session:
            from infrastructure.postgres.organization_repository import (
                PostgresOrganizationRepository,
            )
            repo = PostgresOrganizationRepository(session)
            return await repo.list(skip=skip, limit=limit)
