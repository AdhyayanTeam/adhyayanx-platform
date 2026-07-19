from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.academy_tables import BatchTable
from app.modules.blueprints.academy.delivery.application.service import BatchRepository
from app.modules.blueprints.academy.delivery.domain.models import Batch

class PostgresBatchRepository(BatchRepository):
    def __init__(self, session: Any) -> None:
        self._session: AsyncSession = session

    async def save(self, batch: Batch) -> None:
        table = BatchTable(
            id=batch.id,
            organization_id=batch.organization_id,
            course_id=batch.course_id,
            name=batch.name,
            start_date=batch.start_date,
            created_at=batch.created_at,
            updated_at=batch.updated_at,
        )
        self._session.add(table)

    async def get(self, organization_id: UUID, batch_id: UUID) -> Batch | None:
        stmt = select(BatchTable).where(
            BatchTable.id == batch_id,
            BatchTable.organization_id == organization_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Batch(
            id=row.id,
            organization_id=row.organization_id,
            course_id=row.course_id,
            name=row.name,
            start_date=row.start_date,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

from app.infrastructure.postgres.academy_tables import SessionTable, AttendanceRecordTable
from app.modules.blueprints.academy.delivery.application.service import SessionRepository, AttendanceRepository
from app.modules.blueprints.academy.delivery.domain.models import Session, AttendanceRecord

class PostgresSessionRepository(SessionRepository):
    def __init__(self, session: Any) -> None:
        self._session: AsyncSession = session

    async def save(self, session_entity: Session) -> None:
        table = SessionTable(
            id=session_entity.id,
            organization_id=session_entity.organization_id,
            batch_id=session_entity.batch_id,
            starts_at=session_entity.starts_at,
            ends_at=session_entity.ends_at,
            status=session_entity.status,
            attendance_submitted_at=session_entity.attendance_submitted_at,
            created_at=session_entity.created_at,
            updated_at=session_entity.updated_at,
        )
        await self._session.merge(table)

    async def get(self, organization_id: UUID, session_id: UUID) -> Session | None:
        stmt = select(SessionTable).where(
            SessionTable.id == session_id,
            SessionTable.organization_id == organization_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Session(
            id=row.id,
            organization_id=row.organization_id,
            batch_id=row.batch_id,
            starts_at=row.starts_at,
            ends_at=row.ends_at,
            status=row.status,
            attendance_submitted_at=row.attendance_submitted_at,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

class PostgresAttendanceRepository(AttendanceRepository):
    def __init__(self, session: Any) -> None:
        self._session: AsyncSession = session

    async def save_many(self, records: list[AttendanceRecord]) -> None:
        tables = [
            AttendanceRecordTable(
                session_id=r.session_id,
                student_id=r.student_id,
                organization_id=r.organization_id,
                status=r.status,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in records
        ]
        self._session.add_all(tables)

    async def get(self, organization_id: UUID, session_id: UUID, student_id: UUID) -> AttendanceRecord | None:
        stmt = select(AttendanceRecordTable).where(
            AttendanceRecordTable.session_id == session_id,
            AttendanceRecordTable.student_id == student_id,
            AttendanceRecordTable.organization_id == organization_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return AttendanceRecord(
            session_id=row.session_id,
            student_id=row.student_id,
            organization_id=row.organization_id,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def save(self, record: AttendanceRecord) -> None:
        table = AttendanceRecordTable(
            session_id=record.session_id,
            student_id=record.student_id,
            organization_id=record.organization_id,
            status=record.status,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
        await self._session.merge(table)
