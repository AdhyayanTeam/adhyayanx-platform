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


from app.modules.platform.contracts.event import DomainEvent
from app.modules.blueprints.academy.enrollment.domain.events import StudentEnrolled, StudentAssignedToBatch

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
    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    @classmethod
    def create(cls, id: UUID, organization_id: UUID, student_id: UUID, course_id: UUID) -> Enrollment:
        now = datetime.now(UTC)
        enrollment = cls(
            id=id,
            organization_id=organization_id,
            student_id=student_id,
            course_id=course_id,
            status="active",
            created_at=now,
            updated_at=now,
        )
        enrollment._events.append(
            StudentEnrolled(
                aggregate_type="academy.enrollment",
                aggregate_id=enrollment.id,
                enrollment_id=str(enrollment.id),
                organization_id=str(enrollment.organization_id),
                student_id=str(enrollment.student_id),
                course_id=str(enrollment.course_id),
            )
        )
        return enrollment

    def pull_events(self) -> list[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

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
        
        self._events.append(
            StudentAssignedToBatch(
                aggregate_type="academy.enrollment",
                aggregate_id=self.id,
                assignment_id=str(new_assignment.id),
                enrollment_id=str(self.id),
                organization_id=str(self.organization_id),
                batch_id=str(new_assignment.batch_id),
            )
        )
        
        return new_assignment
