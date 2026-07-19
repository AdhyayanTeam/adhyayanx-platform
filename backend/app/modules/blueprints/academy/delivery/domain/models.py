from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Batch:
    id: UUID
    organization_id: UUID
    course_id: UUID
    name: str
    start_date: datetime | None
    created_at: datetime
    updated_at: datetime


@dataclass
class Session:
    id: UUID
    organization_id: UUID
    batch_id: UUID
    starts_at: datetime
    ends_at: datetime
    status: str
    attendance_submitted_at: datetime | None
    created_at: datetime
    updated_at: datetime

@dataclass
class AttendanceRecord:
    session_id: UUID
    student_id: UUID
    organization_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
