from uuid import UUID

from app.infrastructure.postgres.database import Database
from sqlalchemy import select

from app.modules.blueprints.academy.catalog.contracts.course_query import CourseDto
from app.infrastructure.postgres.academy_tables import CourseTable

class PostgresCourseQueryService:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_course(self, organization_id: UUID, course_id: UUID) -> CourseDto | None:
        async with self._db.session() as session:
            stmt = select(CourseTable).where(
                CourseTable.id == course_id,
                CourseTable.organization_id == organization_id,
            )
            result = await session.execute(stmt)
            course_row = result.scalar_one_or_none()

            if not course_row:
                return None

            return CourseDto(
                id=course_row.id,
                organization_id=course_row.organization_id,
                title=course_row.title,
                lifecycle_state=course_row.lifecycle_state,
            )
