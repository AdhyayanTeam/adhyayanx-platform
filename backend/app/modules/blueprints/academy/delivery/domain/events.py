from __future__ import annotations

from app.modules.platform.contracts.event import DomainEvent

class AttendanceSubmitted(DomainEvent):
    event_type: str = "academy.delivery.AttendanceSubmitted"
    organization_id: str
    session_id: str
    batch_id: str
    submitted_by: str
    record_count: int
    present_count: int
    absent_count: int

class AttendanceCorrected(DomainEvent):
    event_type: str = "academy.delivery.AttendanceCorrected"
    organization_id: str
    session_id: str
    student_id: str
    previous_status: str
    new_status: str
    corrected_by: str
