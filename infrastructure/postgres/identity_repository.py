from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from adx_platform.identity.ports.identity_repository import IdentityRepository
from infrastructure.postgres.tables import UserTable


class PostgresIdentityRepository(IdentityRepository):
    """PostgreSQL implementation of IdentityRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def load(self, id: UUID) -> dict | None:
        result = await self._session.execute(
            select(UserTable).where(UserTable.id == id)
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def load_by_email(self, email: str) -> dict | None:
        result = await self._session.execute(
            select(UserTable).where(UserTable.email == email)
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def save(self, user: dict) -> None:
        stmt = select(UserTable).where(UserTable.id == user["id"])
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.email = user.get("email", existing.email)
            existing.name = user.get("name", existing.name)
            existing.lifecycle_state = user.get("lifecycle_state", existing.lifecycle_state)
            existing.auth_provider = user.get("auth_provider", existing.auth_provider)
            existing.auth_provider_id = user.get("auth_provider_id", existing.auth_provider_id)
            existing.version = user.get("version", existing.version)
            existing.extra = user.get("metadata", existing.extra)
            existing.updated_at = user.get("updated_at", existing.updated_at)
        else:
            row = UserTable(
                id=user["id"],
                organization_id=user["organization_id"],
                email=user["email"],
                name=user["name"],
                lifecycle_state=user.get("lifecycle_state", "active"),
                auth_provider=user.get("auth_provider", "email"),
                auth_provider_id=user.get("auth_provider_id"),
                version=user.get("version", 1),
                extra=user.get("metadata", {}),
                created_at=user.get("created_at"),
                updated_at=user.get("updated_at"),
            )
            self._session.add(row)

    async def delete(self, id: UUID) -> None:
        result = await self._session.execute(
            select(UserTable).where(UserTable.id == id)
        )
        row = result.scalar_one_or_none()
        if row:
            await self._session.delete(row)

    async def exists(self, id: UUID) -> bool:
        result = await self._session.execute(
            select(UserTable.id).where(UserTable.id == id)
        )
        return result.scalar_one_or_none() is not None

    async def list(self, organization_id: UUID, skip: int = 0, limit: int = 100) -> list[dict]:
        result = await self._session.execute(
            select(UserTable)
            .where(UserTable.organization_id == organization_id)
            .order_by(UserTable.created_at)
            .offset(skip)
            .limit(limit)
        )
        return [self._to_dict(row) for row in result.scalars().all()]

    def _to_dict(self, row: UserTable) -> dict:
        return {
            "id": row.id,
            "organization_id": row.organization_id,
            "email": row.email,
            "name": row.name,
            "lifecycle_state": row.lifecycle_state,
            "auth_provider": row.auth_provider,
            "auth_provider_id": row.auth_provider_id,
            "version": row.version,
            "metadata": row.extra or {},
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }
