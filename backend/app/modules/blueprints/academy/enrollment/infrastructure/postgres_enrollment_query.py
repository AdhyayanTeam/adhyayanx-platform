from typing import Sequence
from uuid import UUID
from sqlalchemy import select

from app.infrastructure.postgres.database import Database
from app.infrastructure.postgres.academy_tables import EnrollmentTable, BatchAssignmentTable
from app.modules.blueprints.academy.enrollment.contracts.enrollment_query import EnrollmentQueryContract, BatchStudentRef

class PostgresEnrollmentQueryService(EnrollmentQueryContract):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_students_assigned_to_batch(
        self,
        organization_id: UUID,
        batch_id: UUID,
    ) -> Sequence[BatchStudentRef]:
        async with self._db.session() as session:
            stmt = (
                select(EnrollmentTable.student_id, EnrollmentTable.id)
                .join(BatchAssignmentTable, EnrollmentTable.id == BatchAssignmentTable.enrollment_id)
                .where(
                    EnrollmentTable.organization_id == organization_id,
                    BatchAssignmentTable.organization_id == organization_id,
                    BatchAssignmentTable.batch_id == batch_id,
                    BatchAssignmentTable.ended_at.is_(None)
                )
            )
            result = await session.execute(stmt)
            
            return [
                BatchStudentRef(
                    student_id=row.student_id,
                    organization_id=organization_id,
                    enrollment_id=row.id,
                )
                for row in result.fetchall()
            ]
