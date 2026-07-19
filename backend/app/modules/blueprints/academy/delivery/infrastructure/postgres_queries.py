import zoneinfo
from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import select, func, and_, case
from sqlalchemy.orm import aliased

from app.infrastructure.postgres.database import Database
from app.infrastructure.postgres.tables import OrganizationTable
from app.infrastructure.postgres.academy_tables import (
    CourseTable,
    BatchTable,
    SessionTable,
    BatchAssignmentTable,
    StudentTable,
    AttendanceRecordTable,
    EnrollmentTable,
)
from app.modules.blueprints.academy.delivery.application.queries import (
    BatchOperationsQuery,
    TodaySessionView,
    BatchOverviewView,
    BatchRosterView,
    SessionAttendanceSheetView,
    BatchSessionSummaryView,
)


class PostgresBatchOperationsQuery(BatchOperationsQuery):
    def __init__(self, database: Database) -> None:
        self._database = database

    async def get_todays_sessions(self, org_id: UUID, local_date: date | None = None) -> list[TodaySessionView]:
        async with self._database.session() as session:
            # 1. Fetch Organization Timezone
            org_stmt = select(OrganizationTable.timezone).where(OrganizationTable.id == org_id)
            org_tz_str = await session.scalar(org_stmt)
            tz = zoneinfo.ZoneInfo(org_tz_str or "UTC")
            
            # 2. Determine local date boundaries
            target_date = local_date or datetime.now(tz).date()
            start_local = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=tz)
            end_local = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, 999999, tzinfo=tz)
            
            start_utc = start_local.astimezone(UTC)
            end_utc = end_local.astimezone(UTC)
            
            # 3. Query Sessions
            # We want session details, batch/course names, and assigned student count.
            # Assigned student count is a subquery or joined group.
            student_count_sq = (
                select(
                    BatchAssignmentTable.batch_id,
                    func.count(BatchAssignmentTable.id).label("assigned_count")
                )
                .where(BatchAssignmentTable.organization_id == org_id)
                .where(
                    and_(
                        BatchAssignmentTable.assigned_at <= start_utc,
                        (BatchAssignmentTable.ended_at == None) | (BatchAssignmentTable.ended_at > end_utc)
                    )
                )
                .group_by(BatchAssignmentTable.batch_id)
                .subquery()
            )
            
            stmt = (
                select(
                    SessionTable,
                    BatchTable.name.label("batch_name"),
                    CourseTable.title.label("course_title"),
                    func.coalesce(student_count_sq.c.assigned_count, 0).label("assigned_student_count")
                )
                .select_from(SessionTable)
                .join(BatchTable, SessionTable.batch_id == BatchTable.id)
                .join(CourseTable, BatchTable.course_id == CourseTable.id)
                .outerjoin(student_count_sq, SessionTable.batch_id == student_count_sq.c.batch_id)
                .where(
                    SessionTable.organization_id == org_id,
                    SessionTable.starts_at >= start_utc,
                    SessionTable.starts_at <= end_utc
                )
                .order_by(SessionTable.starts_at.asc())
            )
            
            result = await session.execute(stmt)
            
            views = []
            for row in result:
                s = row.SessionTable
                views.append(
                    TodaySessionView(
                        session_id=s.id,
                        batch_id=s.batch_id,
                        course_title=row.course_title,
                        batch_name=row.batch_name,
                        starts_at=s.starts_at,
                        ends_at=s.ends_at,
                        assigned_student_count=row.assigned_student_count,
                        attendance_submitted_at=s.attendance_submitted_at,
                    )
                )
            return views

    async def get_batch_overview(self, org_id: UUID, batch_id: UUID) -> BatchOverviewView | None:
        async with self._database.session() as session:
            now_utc = datetime.now(UTC)
            
            # Active student count for this batch
            count_stmt = (
                select(func.count(BatchAssignmentTable.id))
                .where(
                    BatchAssignmentTable.organization_id == org_id,
                    BatchAssignmentTable.batch_id == batch_id,
                    BatchAssignmentTable.ended_at == None
                )
            )
            assigned_count = await session.scalar(count_stmt) or 0
            
            # Next/Latest session
            # Try to find the next upcoming session
            next_session_stmt = (
                select(SessionTable)
                .where(
                    SessionTable.organization_id == org_id,
                    SessionTable.batch_id == batch_id,
                    SessionTable.starts_at >= now_utc
                )
                .order_by(SessionTable.starts_at.asc())
                .limit(1)
            )
            next_sess = await session.scalar(next_session_stmt)
            
            if not next_sess:
                # If no upcoming, find the most recent past session
                past_session_stmt = (
                    select(SessionTable)
                    .where(
                        SessionTable.organization_id == org_id,
                        SessionTable.batch_id == batch_id,
                        SessionTable.starts_at < now_utc
                    )
                    .order_by(SessionTable.starts_at.desc())
                    .limit(1)
                )
                next_sess = await session.scalar(past_session_stmt)
                
            # Batch and Course details
            batch_stmt = (
                select(BatchTable, CourseTable)
                .join(CourseTable, BatchTable.course_id == CourseTable.id)
                .where(BatchTable.id == batch_id, BatchTable.organization_id == org_id)
            )
            result = await session.execute(batch_stmt)
            row = result.first()
            
            if not row:
                return None
                
            b = row.BatchTable
            c = row.CourseTable
            
            return BatchOverviewView(
                batch_id=b.id,
                course_title=c.title,
                batch_name=b.name,
                assigned_student_count=assigned_count,
                next_session_id=next_sess.id if next_sess else None,
                next_session_starts_at=next_sess.starts_at if next_sess else None,
            )

    async def get_batch_roster(self, org_id: UUID, batch_id: UUID) -> list[BatchRosterView]:
        async with self._database.session() as session:
            stmt = (
                select(StudentTable)
                .join(EnrollmentTable, StudentTable.id == EnrollmentTable.student_id)
                .join(BatchAssignmentTable, EnrollmentTable.id == BatchAssignmentTable.enrollment_id)
                .where(
                    BatchAssignmentTable.organization_id == org_id,
                    BatchAssignmentTable.batch_id == batch_id,
                    BatchAssignmentTable.ended_at == None
                )
                .order_by(StudentTable.name.asc())
            )
            result = await session.execute(stmt)
            
            return [
                BatchRosterView(
                    student_id=s.id,
                    name=s.name,
                    email=s.email,
                )
                for s in result.scalars()
            ]

    async def get_session_attendance(self, org_id: UUID, session_id: UUID) -> list[SessionAttendanceSheetView]:
        async with self._database.session() as session:
            # Get session to know which batch it belongs to
            session_stmt = select(SessionTable).where(
                SessionTable.id == session_id,
                SessionTable.organization_id == org_id
            )
            sess = await session.scalar(session_stmt)
            if not sess:
                return []
                
            batch_id = sess.batch_id
            
            # Left join roster with attendance records for this session
            stmt = (
                select(StudentTable, AttendanceRecordTable.status)
                .select_from(StudentTable)
                .join(EnrollmentTable, StudentTable.id == EnrollmentTable.student_id)
                .join(BatchAssignmentTable, EnrollmentTable.id == BatchAssignmentTable.enrollment_id)
                .outerjoin(
                    AttendanceRecordTable,
                    and_(
                        AttendanceRecordTable.student_id == StudentTable.id,
                        AttendanceRecordTable.session_id == session_id
                    )
                )
                .where(
                    BatchAssignmentTable.organization_id == org_id,
                    BatchAssignmentTable.batch_id == batch_id,
                    BatchAssignmentTable.assigned_at <= sess.starts_at,
                    (BatchAssignmentTable.ended_at == None) | (BatchAssignmentTable.ended_at > sess.starts_at)
                )
                .order_by(StudentTable.name.asc())
            )
            result = await session.execute(stmt)
            
            views = []
            for row in result:
                s = row.StudentTable
                status = row.status
                views.append(
                    SessionAttendanceSheetView(
                        student_id=s.id,
                        name=s.name,
                        email=s.email,
                        status=status,
                    )
                )
            return views

    async def get_batch_attendance_summary(self, org_id: UUID, batch_id: UUID) -> list[BatchSessionSummaryView]:
        async with self._database.session() as session:
            stmt = (
                select(
                    SessionTable,
                    func.sum(case((AttendanceRecordTable.status == "PRESENT", 1), else_=0)).label("present_count"),
                    func.sum(case((AttendanceRecordTable.status == "ABSENT", 1), else_=0)).label("absent_count")
                )
                .select_from(SessionTable)
                .outerjoin(AttendanceRecordTable, SessionTable.id == AttendanceRecordTable.session_id)
                .where(
                    SessionTable.organization_id == org_id,
                    SessionTable.batch_id == batch_id,
                    SessionTable.attendance_submitted_at != None
                )
                .group_by(SessionTable.id)
                .order_by(SessionTable.starts_at.desc())
            )
            result = await session.execute(stmt)
            
            views = []
            for row in result:
                s = row.SessionTable
                views.append(
                    BatchSessionSummaryView(
                        session_id=s.id,
                        starts_at=s.starts_at,
                        present_count=row.present_count or 0,
                        absent_count=row.absent_count or 0,
                        attendance_submitted_at=s.attendance_submitted_at,
                    )
                )
            return views

    async def get_batches_for_course(self, org_id: UUID, course_id: UUID) -> list[BatchOverviewView]:
        async with self._database.session() as session:
            student_count_sq = (
                select(
                    BatchAssignmentTable.batch_id,
                    func.count(BatchAssignmentTable.id).label("assigned_count")
                )
                .where(BatchAssignmentTable.organization_id == org_id)
                .where(BatchAssignmentTable.ended_at == None)
                .group_by(BatchAssignmentTable.batch_id)
                .subquery()
            )
            
            # Subquery to find the next session
            next_session_sq = (
                select(
                    SessionTable.batch_id,
                    SessionTable.id,
                    SessionTable.starts_at,
                    func.row_number().over(
                        partition_by=SessionTable.batch_id,
                        order_by=SessionTable.starts_at.asc()
                    ).label("rn")
                )
                .where(
                    SessionTable.organization_id == org_id,
                    SessionTable.starts_at > datetime.now(UTC),
                )
                .subquery()
            )

            stmt = (
                select(
                    BatchTable.id.label("batch_id"),
                    CourseTable.title.label("course_title"),
                    BatchTable.name.label("batch_name"),
                    func.coalesce(student_count_sq.c.assigned_count, 0).label("assigned_student_count"),
                    next_session_sq.c.id.label("next_session_id"),
                    next_session_sq.c.starts_at.label("next_session_starts_at"),
                )
                .select_from(BatchTable)
                .join(CourseTable, BatchTable.course_id == CourseTable.id)
                .outerjoin(student_count_sq, BatchTable.id == student_count_sq.c.batch_id)
                .outerjoin(next_session_sq, and_(BatchTable.id == next_session_sq.c.batch_id, next_session_sq.c.rn == 1))
                .where(BatchTable.organization_id == org_id, BatchTable.course_id == course_id)
            )

            result = await session.execute(stmt)

            return [
                BatchOverviewView(
                    batch_id=row.batch_id,
                    course_title=row.course_title,
                    batch_name=row.batch_name,
                    assigned_student_count=row.assigned_student_count,
                    next_session_id=row.next_session_id,
                    next_session_starts_at=row.next_session_starts_at,
                )
                for row in result
            ]
