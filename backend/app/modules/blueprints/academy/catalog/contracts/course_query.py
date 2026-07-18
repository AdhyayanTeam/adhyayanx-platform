from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

@dataclass(frozen=True)
class CourseDto:
    id: UUID
    organization_id: UUID
    title: str
    lifecycle_state: str

class CourseQueryContract(Protocol):
    async def get_course(self, organization_id: UUID, course_id: UUID) -> CourseDto | None:
        """Fetch course details for cross-module validation."""
        ...
