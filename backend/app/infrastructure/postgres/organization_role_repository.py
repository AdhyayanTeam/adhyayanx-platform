from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.tables import OrganizationRoleTable
from app.modules.platform.identity.ports.organization_role_repository import (
    OrganizationRoleRepository,
)


class PostgresOrganizationRoleRepository(OrganizationRoleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def load(self, id: UUID) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(OrganizationRoleTable).where(OrganizationRoleTable.id == id)
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def create(self, role: dict[str, Any]) -> None:
        row = OrganizationRoleTable(
            id=role["id"],
            organization_id=role["organization_id"],
            name=role["name"],
            permissions=role.get("permissions", {}),
            created_at=role.get("created_at"),
        )
        self._session.add(row)
        await self._session.flush()

    async def load_by_name_and_org(self, name: str, organization_id: UUID) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(OrganizationRoleTable).where(
                OrganizationRoleTable.name == name,
                OrganizationRoleTable.organization_id == organization_id,
            )
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def list_for_org(self, organization_id: UUID) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(OrganizationRoleTable).where(
                OrganizationRoleTable.organization_id == organization_id
            )
        )
        return [self._to_dict(row) for row in result.scalars().all()]

    def _to_dict(self, row: OrganizationRoleTable) -> dict[str, Any]:
        return {
            "id": row.id,
            "organization_id": row.organization_id,
            "name": row.name,
            "permissions": row.permissions or {},
            "created_at": row.created_at,
        }
