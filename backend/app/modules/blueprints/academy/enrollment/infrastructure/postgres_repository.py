from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.academy_tables import EnrollmentTable, BatchAssignmentTable
from app.modules.blueprints.academy.enrollment.application.service import EnrollmentRepository
from app.modules.blueprints.academy.enrollment.domain.models import Enrollment, BatchAssignment

class PostgresEnrollmentRepository(EnrollmentRepository):
    def __init__(self, session: Any) -> None:
        self._session: AsyncSession = session

    async def save(self, enrollment: Enrollment) -> None:
        # Check if enrollment already exists
        stmt = select(EnrollmentTable).where(EnrollmentTable.id == enrollment.id)
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.status = enrollment.status
            existing.updated_at = enrollment.updated_at
        else:
            table = EnrollmentTable(
                id=enrollment.id,
                organization_id=enrollment.organization_id,
                student_id=enrollment.student_id,
                course_id=enrollment.course_id,
                status=enrollment.status,
                created_at=enrollment.created_at,
                updated_at=enrollment.updated_at,
            )
            self._session.add(table)

        # Handle assignments
        # Simplest way for milestone 3: just insert new ones (we assume domain logic appends to the list)
        # To make it fully robust for updates we would track changes or do a merge, 
        # but for this specific flow, appending is sufficient.
        for assign in enrollment.assignments:
            assign_stmt = select(BatchAssignmentTable).where(BatchAssignmentTable.id == assign.id)
            assign_result = await self._session.execute(assign_stmt)
            existing_assign = assign_result.scalar_one_or_none()
            if existing_assign:
                existing_assign.ended_at = assign.ended_at
            else:
                new_assign = BatchAssignmentTable(
                    id=assign.id,
                    organization_id=assign.organization_id,
                    enrollment_id=enrollment.id,
                    batch_id=assign.batch_id,
                    assigned_at=assign.assigned_at,
                    ended_at=assign.ended_at,
                )
                self._session.add(new_assign)

    async def get(self, organization_id: UUID, enrollment_id: UUID) -> Enrollment | None:
        stmt = select(EnrollmentTable).where(
            EnrollmentTable.id == enrollment_id,
            EnrollmentTable.organization_id == organization_id,
        )
        # In a real ORM we would use selectinload to eagerly load assignments if we mapped relationships.
        # Since we are manually mapping, we fetch them separately or join.
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if not row:
            return None
            
        assign_stmt = select(BatchAssignmentTable).where(BatchAssignmentTable.enrollment_id == row.id)
        assign_result = await self._session.execute(assign_stmt)
        assign_rows = assign_result.scalars().all()
        
        assignments = [
            BatchAssignment(
                id=a.id,
                organization_id=a.organization_id,
                batch_id=a.batch_id,
                assigned_at=a.assigned_at,
                ended_at=a.ended_at,
            )
            for a in assign_rows
        ]

        return Enrollment(
            id=row.id,
            organization_id=row.organization_id,
            student_id=row.student_id,
            course_id=row.course_id,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
            assignments=assignments,
        )
