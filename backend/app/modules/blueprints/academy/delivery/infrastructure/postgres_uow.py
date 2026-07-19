from collections.abc import Callable
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.platform.contracts.event import DomainEvent
from app.infrastructure.postgres.database import Database
from app.modules.blueprints.academy.delivery.application.uow import DeliveryUnitOfWork, EnrollmentQueryFactory
from app.modules.blueprints.academy.delivery.contracts.attendance_repository import AttendanceRepository
from app.modules.blueprints.academy.delivery.contracts.session_repository import SessionRepository
from app.modules.blueprints.academy.delivery.infrastructure.postgres_repository import PostgresAttendanceRepository, PostgresSessionRepository
from app.modules.blueprints.academy.enrollment.contracts.enrollment_query import EnrollmentQueryContract
from app.modules.platform.events.publisher import Publisher


class PostgresDeliveryUnitOfWork(DeliveryUnitOfWork):
    """
    PostgreSQL-backed Unit of Work for the Delivery module.
    Manages exactly one AsyncSession and guarantees explicit transaction semantics.
    """

    def __init__(
        self,
        db: Database,
        publisher: Publisher,
        enrollment_query_factory: EnrollmentQueryFactory,
    ):
        self._db = db
        self._publisher = publisher
        self._enrollment_query_factory = enrollment_query_factory
        
        self._session: AsyncSession | None = None
        self._events: list[DomainEvent] = []
        self._committed: bool = False
        
        self._sessions: SessionRepository | None = None
        self._attendance: AttendanceRepository | None = None
        self._enrollment_query: EnrollmentQueryContract | None = None

    @property
    def sessions(self) -> SessionRepository:
        if not self._sessions:
            raise RuntimeError("Unit of Work must be used within an async context manager.")
        return self._sessions

    @property
    def attendance(self) -> AttendanceRepository:
        if not self._attendance:
            raise RuntimeError("Unit of Work must be used within an async context manager.")
        return self._attendance

    @property
    def enrollment_query(self) -> EnrollmentQueryContract:
        if not self._enrollment_query:
            raise RuntimeError("Unit of Work must be used within an async context manager.")
        return self._enrollment_query

    async def __aenter__(self) -> "PostgresDeliveryUnitOfWork":
        self._events = []
        self._committed = False
        
        self._session = self._db.session_factory()
        await self._session.begin()

        # Instantiate repositories bound to this transaction
        self._sessions = PostgresSessionRepository(self._session)
        self._attendance = PostgresAttendanceRepository(self._session)
        
        # Instantiate explicitly composed transaction-bound contracts
        self._enrollment_query = self._enrollment_query_factory(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        try:
            if exc_type is not None or not self._committed:
                # Explicit rollback if exception happened or commit was missed
                if self._session:
                    await self._session.rollback()
        finally:
            if self._session:
                await self._session.close()

        self._session = None
        self._sessions = None
        self._attendance = None
        self._enrollment_query = None

    async def commit(self) -> None:
        if not self._session:
            raise RuntimeError("Cannot commit outside of a Unit of Work context.")
        
        if self._committed:
            # Handle double commit idempotently
            return

        # 1. Flush/publish recorded events
        for event in self._events:
            await self._publisher.publish(event, self._session)
            
        # 2. Commit transaction
        await self._session.commit()
        
        self._committed = True
        self._events.clear()

    def record(self, event: DomainEvent) -> None:
        self._events.append(event)
