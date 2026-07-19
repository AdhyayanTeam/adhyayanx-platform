from dataclasses import dataclass
from typing import Protocol, Optional
from uuid import UUID
from datetime import datetime

@dataclass
class StudentEnrollmentView:
    enrollment_id: UUID
    course_id: UUID
    course_title: str
    status: str
    enrolled_at: datetime
    current_batch_id: Optional[UUID]
    current_batch_name: Optional[str]

class EnrollmentQueryService(Protocol):
    async def get_student_enrollments(self, org_id: UUID, student_id: UUID) -> list[StudentEnrollmentView]:
        ...
