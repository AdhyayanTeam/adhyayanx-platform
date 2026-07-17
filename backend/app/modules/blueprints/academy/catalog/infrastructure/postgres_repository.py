from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.academy_tables import CourseTable
from app.modules.blueprints.academy.catalog.infrastructure.ports.catalog_repository import (
    CatalogRepository,
)


class PostgresCatalogRepository(CatalogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, course: dict[str, Any]) -> None:
        stmt = select(CourseTable).where(
            CourseTable.id == course["id"], CourseTable.organization_id == course["organization_id"]
        )
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.title = course.get("title", existing.title)
            existing.description = course.get("description", existing.description)
            existing.lifecycle_state = course.get("lifecycle_state", existing.lifecycle_state)
            existing.updated_at = course.get("updated_at", existing.updated_at)
        else:
            row = CourseTable(
                id=course["id"],
                organization_id=course["organization_id"],
                title=course["title"],
                description=course.get("description"),
                lifecycle_state=course["lifecycle_state"],
            )
            self._session.add(row)
            await self._session.flush()

    async def load(self, id: UUID, organization_id: UUID) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(CourseTable).where(
                CourseTable.id == id, CourseTable.organization_id == organization_id
            )
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def list(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(CourseTable)
            .where(CourseTable.organization_id == organization_id)
            .order_by(CourseTable.created_at)
            .offset(skip)
            .limit(limit)
        )
        return [self._to_dict(row) for row in result.scalars().all()]

    def _to_dict(self, row: CourseTable) -> dict[str, Any]:
        return {
            "id": row.id,
            "organization_id": row.organization_id,
            "title": row.title,
            "description": row.description,
            "lifecycle_state": row.lifecycle_state,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }
