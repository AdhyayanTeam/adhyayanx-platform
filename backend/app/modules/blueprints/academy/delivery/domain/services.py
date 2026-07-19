from datetime import UTC, datetime
from uuid import UUID

from app.modules.blueprints.academy.delivery.domain.models import AttendanceRecord, Session
from app.modules.blueprints.academy.delivery.domain.events import AttendanceSubmitted

class DomainValidationError(ValueError):
    pass

def submit_session_attendance(
    session: Session,
    records: list[dict],
    enrolled_students: set[UUID],
    submitted_by: UUID,
) -> tuple[list[AttendanceRecord], AttendanceSubmitted]:
    """
    Business operation to submit attendance for a session.
    
    Validates that all submitted students are actually enrolled in the batch.
    Creates AttendanceRecord entities and the AttendanceSubmitted domain event.
    """
    attendance_records = []
    present_count = 0
    absent_count = 0
    
    # Track seen students to prevent duplicate submissions in the same request
    seen_students = set()

    for r in records:
        student_id = UUID(str(r["student_id"]))
        status = r["status"]
        
        if student_id in seen_students:
            raise DomainValidationError(f"Duplicate attendance submission for student {student_id}")
        seen_students.add(student_id)

        if student_id not in enrolled_students:
            raise DomainValidationError(f"Student {student_id} is not enrolled in the batch.")
            
        if status == "PRESENT":
            present_count += 1
        elif status == "ABSENT":
            absent_count += 1

        record = AttendanceRecord(
            session_id=session.id,
            student_id=student_id,
            organization_id=session.organization_id,
            status=status,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        attendance_records.append(record)
        
    now = datetime.now(UTC)
    
    event = AttendanceSubmitted(
        aggregate_type="academy.delivery.session",
        aggregate_id=session.id,
        session_id=str(session.id),
        organization_id=str(session.organization_id),
        batch_id=str(session.batch_id),
        record_count=len(attendance_records),
        present_count=present_count,
        absent_count=absent_count,
        submitted_by=str(submitted_by),
        occurred_at=now,
    )
    
    session.attendance_submitted_at = now
    session.updated_at = now
    
    return attendance_records, event
