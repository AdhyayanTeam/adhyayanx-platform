from typing import Protocol, Optional
from uuid import UUID

class StudentQueryContract(Protocol):
    async def find_by_phone(self, org_id: UUID, phone: str) -> Optional[UUID]:
        """Returns the student_id if found by exact phone match in the org."""
        ...

class StudentCommandContract(Protocol):
    async def create_student(self, org_id: UUID, name: str, phone: str, email: Optional[str]) -> UUID:
        """Creates a student and returns the new student_id."""
        ...

class EnrollmentCommandContract(Protocol):
    async def enroll_student(self, org_id: UUID, student_id: UUID, course_id: UUID) -> UUID:
        """Creates an enrollment and returns the new enrollment_id."""
        ...
