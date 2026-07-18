from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

@dataclass(frozen=True)
class BatchDto:
    id: UUID
    organization_id: UUID
    course_id: UUID
    name: str

class BatchQueryContract(Protocol):
    async def get_batch(self, organization_id: UUID, batch_id: UUID) -> BatchDto | None:
        """Fetch batch details for cross-module validation."""
        ...
