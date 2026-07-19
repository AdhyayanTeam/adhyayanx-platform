from dataclasses import dataclass
from typing import Protocol, Any
from uuid import UUID, uuid4
from datetime import datetime, UTC

from app.infrastructure.postgres.database import Database
from app.foundation.exceptions.base import ValidationError
from app.modules.blueprints.academy.delivery.domain.models import Batch

@dataclass(frozen=True)
class CreateBatchCommand:
    organization_id: UUID
    course_id: UUID
    name: str
    start_date: datetime | None = None

class BatchRepository(Protocol):
    async def save(self, batch: Batch) -> None:
        ...

    async def get(self, organization_id: UUID, batch_id: UUID) -> Batch | None:
        ...

class BatchRepositoryFactory(Protocol):
    def __call__(self, session: Any) -> BatchRepository:
        ...

class BatchService:
    def __init__(self, db: Database, repo_factory: BatchRepositoryFactory) -> None:
        self._db = db
        self._repo_factory = repo_factory

    async def create_batch(self, cmd: CreateBatchCommand) -> UUID:
        now = datetime.now(UTC)
        batch = Batch(
            id=uuid4(),
            organization_id=cmd.organization_id,
            course_id=cmd.course_id,
            name=cmd.name,
            start_date=cmd.start_date,
            created_at=now,
            updated_at=now,
        )
        async with self._db.session() as session:
            repo = self._repo_factory(session)
            await repo.save(batch)
        return batch.id

from app.modules.blueprints.academy.delivery.domain.models import Session, AttendanceRecord
from app.modules.platform.events.publisher import Publisher
from app.modules.blueprints.academy.enrollment.contracts.enrollment_query import EnrollmentQueryContract
from app.modules.blueprints.academy.delivery.domain.events import AttendanceSubmitted, AttendanceCorrected

@dataclass(frozen=True)
class CreateSessionCommand:
    organization_id: UUID
    batch_id: UUID
    starts_at: datetime
    ends_at: datetime

@dataclass(frozen=True)
class StudentAttendanceCmd:
    student_id: UUID
    status: str

@dataclass(frozen=True)
class SubmitAttendanceCommand:
    organization_id: UUID
    session_id: UUID
    submitted_by: UUID
    records: list[StudentAttendanceCmd]

@dataclass(frozen=True)
class CorrectAttendanceCommand:
    organization_id: UUID
    session_id: UUID
    student_id: UUID
    new_status: str
    corrected_by: UUID

from app.modules.blueprints.academy.delivery.contracts.session_repository import SessionRepository
from app.modules.blueprints.academy.delivery.contracts.attendance_repository import AttendanceRepository

from app.modules.blueprints.academy.delivery.application.uow import DeliveryUnitOfWork

class DeliveryService:
    def __init__(
        self, 
        uow: DeliveryUnitOfWork,
    ) -> None:
        self._uow = uow

    async def create_session(self, cmd: CreateSessionCommand) -> UUID:
        now = datetime.now(UTC)
        session_entity = Session(
            id=uuid4(),
            organization_id=cmd.organization_id,
            batch_id=cmd.batch_id,
            starts_at=cmd.starts_at,
            ends_at=cmd.ends_at,
            status="scheduled",
            attendance_submitted_at=None,
            created_at=now,
            updated_at=now,
        )
        async with self._uow as uow:
            await uow.sessions.save(session_entity)
            await uow.commit()
        return session_entity.id

    async def submit_attendance(self, cmd: SubmitAttendanceCommand) -> None:
        async with self._uow as uow:
            session_entity = await uow.sessions.get(cmd.organization_id, cmd.session_id)
            if not session_entity:
                raise ValidationError("Session not found")
                
            enrolled_refs = await uow.enrollment_query.get_students_assigned_to_batch(
                cmd.organization_id, session_entity.batch_id
            )
            enrolled_student_ids = {ref.student_id for ref in enrolled_refs}
            
            from app.modules.blueprints.academy.delivery.domain.services import submit_session_attendance, DomainValidationError
            
            # Map cmd.records to list[dict] as expected by domain service
            records_dicts = [{"student_id": r.student_id, "status": r.status} for r in cmd.records]
            
            try:
                attendance_records, event = submit_session_attendance(
                    session=session_entity,
                    records=records_dicts,
                    enrolled_students=enrolled_student_ids,
                    submitted_by=cmd.submitted_by
                )
            except DomainValidationError as e:
                raise ValidationError(str(e))
            
            await uow.attendance.save_many(attendance_records)
            await uow.sessions.save(session_entity)
            
            uow.record(event)
            await uow.commit()

    async def correct_attendance(self, cmd: CorrectAttendanceCommand) -> None:
        async with self._uow as uow:
            record = await uow.attendance.get(cmd.organization_id, cmd.session_id, cmd.student_id)
            if not record:
                raise ValidationError("Attendance record not found")
                
            prev_status = record.status
            record.status = cmd.new_status
            record.updated_at = datetime.now(UTC)
            
            await uow.attendance.save(record)
            
            from app.modules.blueprints.academy.delivery.domain.events import AttendanceCorrected
            event = AttendanceCorrected(
                aggregate_type="academy.delivery.session",
                aggregate_id=cmd.session_id,
                session_id=str(cmd.session_id),
                student_id=str(cmd.student_id),
                organization_id=str(cmd.organization_id),
                previous_status=prev_status,
                new_status=cmd.new_status,
                corrected_by=str(cmd.corrected_by),
                occurred_at=datetime.now(UTC),
            )
            uow.record(event)
            await uow.commit()
