from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol
from uuid import UUID

@dataclass
class TodaySessionView:
    session_id: UUID
    batch_id: UUID
    course_title: str
    batch_name: str
    starts_at: datetime
    ends_at: datetime
    assigned_student_count: int
    attendance_submitted_at: datetime | None

@dataclass
class BatchOverviewView:
    batch_id: UUID
    course_title: str
    batch_name: str
    assigned_student_count: int
    next_session_id: UUID | None
    next_session_starts_at: datetime | None

@dataclass
class BatchRosterView:
    student_id: UUID
    name: str
    email: str

@dataclass
class SessionAttendanceSheetView:
    student_id: UUID
    name: str
    email: str
    status: str | None  # PRESENT, ABSENT, or None if not submitted

@dataclass
class BatchSessionSummaryView:
    session_id: UUID
    starts_at: datetime
    present_count: int
    absent_count: int
    attendance_submitted_at: datetime | None

class BatchOperationsQuery(Protocol):
    """
    CQRS Read Model Interface for Academy Batch Operations.
    Implemented directly against optimized SQL views/joins, bypassing the module domain layers.
    """
    async def get_todays_sessions(self, org_id: UUID, local_date: date | None = None) -> list[TodaySessionView]:
        ...

    async def get_batch_overview(self, org_id: UUID, batch_id: UUID) -> BatchOverviewView | None:
        ...

    async def get_batch_roster(self, org_id: UUID, batch_id: UUID) -> list[BatchRosterView]:
        ...

    async def get_session_attendance(self, org_id: UUID, session_id: UUID) -> list[SessionAttendanceSheetView]:
        ...

    async def get_batch_attendance_summary(self, org_id: UUID, batch_id: UUID) -> list[BatchSessionSummaryView]:
        ...
