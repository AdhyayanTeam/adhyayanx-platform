from __future__ import annotations

from app.modules.platform.contracts.event import DomainEvent

class StudentEnrolled(DomainEvent):
    event_type: str = "academy.enrollment.StudentEnrolled"
    enrollment_id: str
    organization_id: str
    student_id: str
    course_id: str

class StudentAssignedToBatch(DomainEvent):
    event_type: str = "academy.enrollment.StudentAssignedToBatch"
    assignment_id: str
    enrollment_id: str
    organization_id: str
    batch_id: str
