from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.foundation.types import LifecycleState
from app.infrastructure.postgres.tables import OrganizationSubscriptionTable
from app.modules.platform.identity.ports.organization_subscription_repository import (
    OrganizationSubscriptionRepository,
)


class PostgresOrganizationSubscriptionRepository(OrganizationSubscriptionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, subscription: dict[str, Any]) -> None:
        row = OrganizationSubscriptionTable(
            id=subscription["id"],
            organization_id=subscription["organization_id"],
            blueprint_code=subscription["blueprint_code"],
            status=subscription.get("status", LifecycleState.ACTIVE),
            starts_at=subscription.get("starts_at"),
            ends_at=subscription.get("ends_at"),
            created_at=subscription.get("created_at"),
        )
        self._session.add(row)

    async def load_active_by_org(self, organization_id: UUID) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(OrganizationSubscriptionTable).where(
                OrganizationSubscriptionTable.organization_id == organization_id,
                OrganizationSubscriptionTable.status == LifecycleState.ACTIVE,
            )
        )
        return [self._to_dict(row) for row in result.scalars().all()]

    def _to_dict(self, row: OrganizationSubscriptionTable) -> dict[str, Any]:
        return {
            "id": row.id,
            "organization_id": row.organization_id,
            "blueprint_code": row.blueprint_code,
            "status": row.status,
            "starts_at": row.starts_at,
            "ends_at": row.ends_at,
            "created_at": row.created_at,
        }
