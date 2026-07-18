from uuid import UUID

from app.infrastructure.postgres.database import Database
from sqlalchemy import select

from app.modules.blueprints.academy.delivery.contracts.batch_query import BatchDto
from app.infrastructure.postgres.academy_tables import BatchTable

class PostgresBatchQueryService:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_batch(self, organization_id: UUID, batch_id: UUID) -> BatchDto | None:
        async with self._db.session() as session:
            stmt = select(BatchTable).where(
                BatchTable.id == batch_id,
                BatchTable.organization_id == organization_id,
            )
            result = await session.execute(stmt)
            batch_row = result.scalar_one_or_none()

            if not batch_row:
                return None

            return BatchDto(
                id=batch_row.id,
                organization_id=batch_row.organization_id,
                course_id=batch_row.course_id,
                name=batch_row.name,
            )
