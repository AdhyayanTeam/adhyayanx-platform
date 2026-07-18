from typing import Protocol, Sequence
from uuid import UUID
from dataclasses import dataclass

@dataclass
class BatchStudentRef:
    student_id: UUID
    organization_id: UUID
    enrollment_id: UUID

class EnrollmentQueryContract(Protocol):
    async def get_students_assigned_to_batch(
        self,
        organization_id: UUID,
        batch_id: UUID,
    ) -> Sequence[BatchStudentRef]:
        ...
