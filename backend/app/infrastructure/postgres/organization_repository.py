from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.foundation.types import LifecycleState
from app.infrastructure.postgres.tables import OrganizationTable
from app.modules.platform.organizations.ports.organization_repository import OrganizationRepository


class PostgresOrganizationRepository(OrganizationRepository):
    """PostgreSQL implementation of OrganizationRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def load(self, id: UUID) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(OrganizationTable).where(OrganizationTable.id == id)
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def load_by_slug(self, slug: str) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(OrganizationTable).where(OrganizationTable.slug == slug)
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def save(self, organization: dict[str, Any]) -> None:
        stmt = select(OrganizationTable).where(OrganizationTable.id == organization["id"])
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.name = organization.get("name", existing.name)
            existing.slug = organization.get("slug", existing.slug)
            existing.lifecycle_state = organization.get("lifecycle_state", existing.lifecycle_state)
            existing.version = organization.get("version", existing.version)
            existing.extra = organization.get("metadata", existing.extra)
            existing.updated_at = organization.get("updated_at", existing.updated_at)
        else:
            row = OrganizationTable(
                id=organization["id"],
                name=organization["name"],
                slug=organization["slug"],
                lifecycle_state=organization.get("lifecycle_state", LifecycleState.ACTIVE),
                version=organization.get("version", 1),
                extra=organization.get("metadata", {}),
                created_at=organization.get("created_at"),
                updated_at=organization.get("updated_at"),
            )
            self._session.add(row)
            await self._session.flush()

    async def create(self, organization: dict[str, Any]) -> None:
        row = OrganizationTable(
            id=organization["id"],
            name=organization["name"],
            slug=organization["slug"],
            lifecycle_state=organization.get("lifecycle_state", LifecycleState.ACTIVE),
            version=organization.get("version", 1),
            extra=organization.get("metadata", {}),
            created_at=organization.get("created_at"),
            updated_at=organization.get("updated_at"),
        )
        self._session.add(row)

    async def delete(self, id: UUID) -> None:
        result = await self._session.execute(
            select(OrganizationTable).where(OrganizationTable.id == id)
        )
        row = result.scalar_one_or_none()
        if row:
            await self._session.delete(row)

    async def exists(self, id: UUID) -> bool:
        result = await self._session.execute(
            select(OrganizationTable.id).where(OrganizationTable.id == id)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self._session.execute(
            select(OrganizationTable.id).where(OrganizationTable.slug == slug)
        )
        return result.scalar_one_or_none() is not None

    async def list(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(OrganizationTable)
            .order_by(OrganizationTable.created_at)
            .offset(skip)
            .limit(limit)
        )
        return [self._to_dict(row) for row in result.scalars().all()]

    def _to_dict(self, row: OrganizationTable) -> dict[str, Any]:
        return {
            "id": row.id,
            "name": row.name,
            "slug": row.slug,
            "lifecycle_state": row.lifecycle_state,
            "version": row.version,
            "metadata": row.extra or {},
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }
