from uuid import UUID

from app.infrastructure.postgres.database import Database
from sqlalchemy import select

from app.modules.blueprints.academy.students.contracts.student_query import StudentDto
from app.infrastructure.postgres.academy_tables import StudentTable

class PostgresStudentQueryService:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_student(self, organization_id: UUID, student_id: UUID) -> StudentDto | None:
        async with self._db.session() as session:
            stmt = select(StudentTable).where(
                StudentTable.id == student_id,
                StudentTable.organization_id == organization_id,
            )
            result = await session.execute(stmt)
            student_row = result.scalar_one_or_none()

            if not student_row:
                return None

            return StudentDto(
                id=student_row.id,
                organization_id=student_row.organization_id,
                name=student_row.name,
                email=student_row.email,
                phone=student_row.phone,
            )
