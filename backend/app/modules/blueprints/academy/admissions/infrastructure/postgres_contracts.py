from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, UTC

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.blueprints.academy.admissions.application.contracts import (
    StudentQueryContract,
    StudentCommandContract,
    EnrollmentCommandContract,
)
from app.infrastructure.postgres.academy_tables import StudentTable, EnrollmentTable

class PostgresStudentContracts(StudentQueryContract, StudentCommandContract):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_phone(self, org_id: UUID, phone: str) -> Optional[UUID]:
        result = await self._session.execute(
            select(StudentTable.id).where(
                StudentTable.organization_id == org_id,
                StudentTable.phone == phone,
            )
        )
        row = result.fetchone()
        return row[0] if row else None

    async def create_student(self, org_id: UUID, name: str, phone: str, email: Optional[str]) -> UUID:
        student_id = uuid4()
        model = StudentTable(
            id=student_id,
            organization_id=org_id,
            name=name,
            phone=phone,
            email=email,
        )
        self._session.add(model)
        await self._session.flush()
        return student_id

class PostgresEnrollmentContracts(EnrollmentCommandContract):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def enroll_student(self, org_id: UUID, student_id: UUID, course_id: UUID) -> UUID:
        enrollment_id = uuid4()
        model = EnrollmentTable(
            id=enrollment_id,
            organization_id=org_id,
            student_id=student_id,
            course_id=course_id,
            status="active",
        )
        self._session.add(model)
        await self._session.flush()
        return enrollment_id
