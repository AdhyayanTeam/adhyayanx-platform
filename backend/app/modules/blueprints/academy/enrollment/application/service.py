from dataclasses import dataclass
from typing import Protocol, Any
from uuid import UUID, uuid4
from datetime import datetime, UTC

from app.infrastructure.postgres.database import Database
from app.foundation.exceptions.base import ValidationError
from app.modules.platform.events.publisher import Publisher
from app.modules.blueprints.academy.enrollment.domain.models import Enrollment, BatchAssignment
from app.modules.blueprints.academy.enrollment.domain.events import StudentEnrolled, StudentAssignedToBatch
from app.modules.blueprints.academy.catalog.contracts.course_query import CourseQueryContract
from app.modules.blueprints.academy.students.contracts.student_query import StudentQueryContract
from app.modules.blueprints.academy.delivery.contracts.batch_query import BatchQueryContract

@dataclass(frozen=True)
class EnrollStudentCommand:
    organization_id: UUID
    student_id: UUID
    course_id: UUID

@dataclass(frozen=True)
class AssignBatchCommand:
    organization_id: UUID
    enrollment_id: UUID
    batch_id: UUID

class EnrollmentRepository(Protocol):
    async def save(self, enrollment: Enrollment) -> None:
        ...

    async def get(self, organization_id: UUID, enrollment_id: UUID) -> Enrollment | None:
        ...

class EnrollmentRepositoryFactory(Protocol):
    def __call__(self, session: Any) -> EnrollmentRepository:
        ...

class EnrollmentService:
    def __init__(
        self,
        db: Database,
        publisher: Publisher,
        repo_factory: EnrollmentRepositoryFactory,
        course_query: CourseQueryContract,
        student_query: StudentQueryContract,
        batch_query: BatchQueryContract,
    ) -> None:
        self._db = db
        self._publisher = publisher
        self._repo_factory = repo_factory
        self._course_query = course_query
        self._student_query = student_query
        self._batch_query = batch_query

    async def enroll_student(self, cmd: EnrollStudentCommand) -> UUID:
        # Cross-module validation
        student = await self._student_query.get_student(cmd.organization_id, cmd.student_id)
        if not student:
            raise ValidationError("Student not found.")
            
        course = await self._course_query.get_course(cmd.organization_id, cmd.course_id)
        if not course:
            raise ValidationError("Course not found.")

        enrollment = Enrollment.create(
            id=uuid4(),
            organization_id=cmd.organization_id,
            student_id=cmd.student_id,
            course_id=cmd.course_id,
        )
        
        async with self._db.session() as session:
            repo = self._repo_factory(session)
            await repo.save(enrollment)
            
            for event in enrollment.pull_events():
                await self._publisher.publish(event, session)
            
        return enrollment.id

    async def assign_batch(self, cmd: AssignBatchCommand) -> UUID:
        async with self._db.session() as session:
            repo = self._repo_factory(session)
            
            enrollment = await repo.get(cmd.organization_id, cmd.enrollment_id)
            if not enrollment:
                raise ValidationError("Enrollment not found.")

            batch = await self._batch_query.get_batch(cmd.organization_id, cmd.batch_id)
            if not batch:
                raise ValidationError("Batch not found.")

            # Domain logic handles the invariants
            assignment = enrollment.assign_batch(
                batch_id=batch.id,
                batch_course_id=batch.course_id,
                batch_org_id=batch.organization_id
            )

            await repo.save(enrollment)
            
            for event in enrollment.pull_events():
                await self._publisher.publish(event, session)
            
            return assignment.id
