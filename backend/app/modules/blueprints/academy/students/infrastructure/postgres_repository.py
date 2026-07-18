from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.academy_tables import StudentTable
from app.modules.blueprints.academy.students.application.service import StudentRepository
from app.modules.blueprints.academy.students.domain.models import Student

class PostgresStudentRepository(StudentRepository):
    def __init__(self, session: Any) -> None:
        self._session: AsyncSession = session

    async def save(self, student: Student) -> None:
        table = StudentTable(
            id=student.id,
            organization_id=student.organization_id,
            name=student.name,
            email=student.email,
            phone=student.phone,
            created_at=student.created_at,
            updated_at=student.updated_at,
        )
        self._session.add(table)

    async def get(self, organization_id: UUID, student_id: UUID) -> Student | None:
        stmt = select(StudentTable).where(
            StudentTable.id == student_id,
            StudentTable.organization_id == organization_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Student(
            id=row.id,
            organization_id=row.organization_id,
            name=row.name,
            email=row.email,
            phone=row.phone,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
