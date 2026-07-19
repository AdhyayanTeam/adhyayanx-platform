from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

@dataclass(frozen=True)
class StudentDto:
    id: UUID
    organization_id: UUID
    name: str
    email: str
    phone: str | None

class StudentQueryContract(Protocol):
    async def get_student(self, organization_id: UUID, student_id: UUID) -> StudentDto | None:
        """Fetch student details for cross-module validation."""
        ...

    async def list_students(self, organization_id: UUID) -> list[StudentDto]:
        """List all students for an organization."""
        ...
