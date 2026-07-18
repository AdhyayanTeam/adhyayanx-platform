from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.academy_tables import BatchTable
from app.modules.blueprints.academy.delivery.application.service import BatchRepository
from app.modules.blueprints.academy.delivery.domain.models import Batch

class PostgresBatchRepository(BatchRepository):
    def __init__(self, session: Any) -> None:
        self._session: AsyncSession = session

    async def save(self, batch: Batch) -> None:
        table = BatchTable(
            id=batch.id,
            organization_id=batch.organization_id,
            course_id=batch.course_id,
            name=batch.name,
            start_date=batch.start_date,
            created_at=batch.created_at,
            updated_at=batch.updated_at,
        )
        self._session.add(table)

    async def get(self, organization_id: UUID, batch_id: UUID) -> Batch | None:
        stmt = select(BatchTable).where(
            BatchTable.id == batch_id,
            BatchTable.organization_id == organization_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Batch(
            id=row.id,
            organization_id=row.organization_id,
            course_id=row.course_id,
            name=row.name,
            start_date=row.start_date,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
