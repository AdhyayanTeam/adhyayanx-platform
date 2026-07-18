from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4

from app.foundation.exceptions.base import ValidationError


@dataclass
class BatchAssignment:
    id: UUID
    organization_id: UUID
    batch_id: UUID
    assigned_at: datetime
    ended_at: datetime | None = None


@dataclass
class Enrollment:
    id: UUID
    organization_id: UUID
    student_id: UUID
    course_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    assignments: list[BatchAssignment] = field(default_factory=list)

    def assign_batch(self, batch_id: UUID, batch_course_id: UUID, batch_org_id: UUID) -> BatchAssignment:
        if self.organization_id != batch_org_id:
            raise ValidationError("Cannot assign a batch from a different organization.")
        if self.course_id != batch_course_id:
            raise ValidationError("Cannot assign a batch for a different course.")
        
        # End any current active assignments
        now = datetime.now(UTC)
        for assignment in self.assignments:
            if assignment.ended_at is None:
                assignment.ended_at = now

        new_assignment = BatchAssignment(
            id=uuid4(),
            organization_id=self.organization_id,
            batch_id=batch_id,
            assigned_at=now,
        )
        self.assignments.append(new_assignment)
        self.updated_at = now
        return new_assignment
