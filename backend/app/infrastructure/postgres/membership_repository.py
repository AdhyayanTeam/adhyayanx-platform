from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.tables import MembershipTable
from app.modules.platform.identity.ports.membership_repository import MembershipRepository


class PostgresMembershipRepository(MembershipRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, membership: dict[str, Any]) -> None:
        row = MembershipTable(
            id=membership["id"],
            user_id=membership["user_id"],
            organization_id=membership["organization_id"],
            role_id=membership["role_id"],
            created_at=membership.get("created_at"),
        )
        self._session.add(row)
        await self._session.flush()

    async def load_by_user_and_org(
        self, user_id: UUID, organization_id: UUID
    ) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(MembershipTable).where(
                MembershipTable.user_id == user_id,
                MembershipTable.organization_id == organization_id,
            )
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def list_for_user(self, user_id: UUID) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(MembershipTable).where(MembershipTable.user_id == user_id)
        )
        return [self._to_dict(row) for row in result.scalars().all()]

    def _to_dict(self, row: MembershipTable) -> dict[str, Any]:
        return {
            "id": row.id,
            "user_id": row.user_id,
            "organization_id": row.organization_id,
            "role_id": row.role_id,
            "created_at": row.created_at,
        }
