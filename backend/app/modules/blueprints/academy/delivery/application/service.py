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

class SessionRepository(Protocol):
    async def save(self, session_entity: Session) -> None:
        ...
    async def get(self, organization_id: UUID, session_id: UUID) -> Session | None:
        ...

class AttendanceRepository(Protocol):
    async def save_many(self, records: list[AttendanceRecord]) -> None:
        ...
    async def get(self, organization_id: UUID, session_id: UUID, student_id: UUID) -> AttendanceRecord | None:
        ...
    async def save(self, record: AttendanceRecord) -> None:
        ...

class SessionRepositoryFactory(Protocol):
    def __call__(self, session: Any) -> SessionRepository:
        ...

class AttendanceRepositoryFactory(Protocol):
    def __call__(self, session: Any) -> AttendanceRepository:
        ...

class DeliveryService:
    def __init__(
        self, 
        db: Database, 
        publisher: Publisher,
        session_repo_factory: SessionRepositoryFactory,
        attendance_repo_factory: AttendanceRepositoryFactory,
        enrollment_query: EnrollmentQueryContract
    ) -> None:
        self._db = db
        self._publisher = publisher
        self._session_repo_factory = session_repo_factory
        self._attendance_repo_factory = attendance_repo_factory
        self._enrollment_query = enrollment_query

    async def create_session(self, cmd: CreateSessionCommand) -> UUID:
        now = datetime.now(UTC)
        session_entity = Session(
            id=uuid4(),
            organization_id=cmd.organization_id,
            batch_id=cmd.batch_id,
            starts_at=cmd.starts_at,
            ends_at=cmd.ends_at,
            status="scheduled",
            created_at=now,
            updated_at=now,
        )
        async with self._db.session() as db_session:
            repo = self._session_repo_factory(db_session)
            await repo.save(session_entity)
        return session_entity.id

    async def submit_attendance(self, cmd: SubmitAttendanceCommand) -> None:
        async with self._db.session() as db_session:
            session_repo = self._session_repo_factory(db_session)
            attendance_repo = self._attendance_repo_factory(db_session)
            
            session_entity = await session_repo.get(cmd.organization_id, cmd.session_id)
            if not session_entity:
                raise ValidationError("Session not found")
                
            enrolled_refs = await self._enrollment_query.get_students_assigned_to_batch(
                cmd.organization_id, session_entity.batch_id
            )
            enrolled_student_ids = {ref.student_id for ref in enrolled_refs}
            
            seen_students = set()
            records_to_save = []
            present_count = 0
            absent_count = 0
            now = datetime.now(UTC)
            
            for r in cmd.records:
                if r.student_id in seen_students:
                    raise ValidationError(f"Duplicate student ID in submission: {r.student_id}")
                if r.student_id not in enrolled_student_ids:
                    raise ValidationError(f"Student {r.student_id} is not enrolled in this batch.")
                
                seen_students.add(r.student_id)
                records_to_save.append(
                    AttendanceRecord(
                        session_id=cmd.session_id,
                        student_id=r.student_id,
                        organization_id=cmd.organization_id,
                        status=r.status,
                        created_at=now,
                        updated_at=now,
                    )
                )
                if r.status == "PRESENT":
                    present_count += 1
                else:
                    absent_count += 1
                    
            await attendance_repo.save_many(records_to_save)
            
            await self._publisher.publish(
                AttendanceSubmitted(
                    aggregate_type="academy.delivery.session",
                    aggregate_id=cmd.session_id,
                    organization_id=str(cmd.organization_id),
                    session_id=str(cmd.session_id),
                    batch_id=str(session_entity.batch_id),
                    submitted_by=str(cmd.submitted_by),
                    record_count=len(records_to_save),
                    present_count=present_count,
                    absent_count=absent_count,
                ),
                db_session
            )

    async def correct_attendance(self, cmd: CorrectAttendanceCommand) -> None:
        async with self._db.session() as db_session:
            attendance_repo = self._attendance_repo_factory(db_session)
            record = await attendance_repo.get(cmd.organization_id, cmd.session_id, cmd.student_id)
            if not record:
                raise ValidationError("Attendance record not found")
                
            prev_status = record.status
            record.status = cmd.new_status
            record.updated_at = datetime.now(UTC)
            
            await attendance_repo.save(record)
            
            await self._publisher.publish(
                AttendanceCorrected(
                    aggregate_type="academy.delivery.session",
                    aggregate_id=cmd.session_id,
                    organization_id=str(cmd.organization_id),
                    session_id=str(cmd.session_id),
                    student_id=str(cmd.student_id),
                    previous_status=prev_status,
                    new_status=cmd.new_status,
                    corrected_by=str(cmd.corrected_by),
                ),
                db_session
            )
