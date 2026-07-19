from uuid import UUID
from sqlalchemy import text
from app.infrastructure.postgres.database import Database
from app.modules.blueprints.academy.enrollment.application.queries import EnrollmentQueryService, StudentEnrollmentView

class PostgresEnrollmentQueryService(EnrollmentQueryService):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_student_enrollments(self, org_id: UUID, student_id: UUID) -> list[StudentEnrollmentView]:
        query = text("""
            WITH LatestAssignment AS (
                SELECT 
                    a.enrollment_id, 
                    a.batch_id, 
                    b.name as batch_name,
                    ROW_NUMBER() OVER(PARTITION BY a.enrollment_id ORDER BY a.assigned_at DESC) as rn
                FROM academy_batch_assignments a
                JOIN academy_batches b ON a.batch_id = b.id
                WHERE a.organization_id = :org_id
            )
            SELECT 
                e.id as enrollment_id,
                e.course_id,
                c.title as course_title,
                e.status,
                e.created_at as enrolled_at,
                la.batch_id as current_batch_id,
                la.batch_name as current_batch_name
            FROM academy_enrollments e
            JOIN academy_courses c ON e.course_id = c.id
            LEFT JOIN LatestAssignment la ON e.id = la.enrollment_id AND la.rn = 1
            WHERE e.organization_id = :org_id AND e.student_id = :student_id
            ORDER BY e.created_at DESC
        """)

        async with self._db.session() as session:
            result = await session.execute(query, {"org_id": org_id, "student_id": student_id})
            rows = result.fetchall()
            
            return [
                StudentEnrollmentView(
                    enrollment_id=row.enrollment_id,
                    course_id=row.course_id,
                    course_title=row.course_title,
                    status=row.status,
                    enrolled_at=row.enrolled_at,
                    current_batch_id=row.current_batch_id,
                    current_batch_name=row.current_batch_name,
                )
                for row in rows
            ]
