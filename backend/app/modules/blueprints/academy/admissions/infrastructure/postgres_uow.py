from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.platform.contracts.event import DomainEvent
from app.infrastructure.postgres.database import Database
from app.modules.platform.events.publisher import Publisher
from app.modules.blueprints.academy.admissions.infrastructure.unit_of_work import AdmissionsUnitOfWork
from app.modules.blueprints.academy.admissions.infrastructure.repository import AdmissionsRepository, PostgresAdmissionsRepository
from app.modules.blueprints.academy.admissions.application.contracts import (
    StudentQueryContract,
    StudentCommandContract,
    EnrollmentCommandContract,
)
from app.modules.blueprints.academy.admissions.infrastructure.postgres_contracts import (
    PostgresStudentContracts,
    PostgresEnrollmentContracts,
)

class PostgresAdmissionsUnitOfWork(AdmissionsUnitOfWork):
    def __init__(
        self,
        db: Database,
        publisher: Publisher,
    ) -> None:
        self._db = db
        self._publisher = publisher
        
        self._session: AsyncSession | None = None
        self._events: list[DomainEvent] = []
        self._committed: bool = False

        self._repository: AdmissionsRepository | None = None
        self._student_queries: StudentQueryContract | None = None
        self._student_commands: StudentCommandContract | None = None
        self._enrollment_commands: EnrollmentCommandContract | None = None

    @property
    def repository(self) -> AdmissionsRepository:
        if not self._repository:
            raise RuntimeError("Unit of Work must be used within an async context manager.")
        return self._repository

    @property
    def student_queries(self) -> StudentQueryContract:
        if not self._student_queries:
            raise RuntimeError("Unit of Work must be used within an async context manager.")
        return self._student_queries

    @property
    def student_commands(self) -> StudentCommandContract:
        if not self._student_commands:
            raise RuntimeError("Unit of Work must be used within an async context manager.")
        return self._student_commands

    @property
    def enrollment_commands(self) -> EnrollmentCommandContract:
        if not self._enrollment_commands:
            raise RuntimeError("Unit of Work must be used within an async context manager.")
        return self._enrollment_commands

    async def __aenter__(self) -> "PostgresAdmissionsUnitOfWork":
        self._events = []
        self._committed = False
        
        self._session = self._db.session_factory()
        await self._session.begin()

        self._repository = PostgresAdmissionsRepository(self._session)
        student_contracts = PostgresStudentContracts(self._session)
        self._student_queries = student_contracts
        self._student_commands = student_contracts
        self._enrollment_commands = PostgresEnrollmentContracts(self._session)

        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if exc_type is not None or not self._committed:
                if self._session:
                    await self._session.rollback()
        finally:
            if self._session:
                await self._session.close()

        self._session = None
        self._repository = None
        self._student_queries = None
        self._student_commands = None
        self._enrollment_commands = None

    async def commit(self) -> None:
        if not self._session:
            raise RuntimeError("Cannot commit outside of a Unit of Work context.")
        
        if self._committed:
            return

        for event in self._events:
            await self._publisher.publish(event, self._session)
            
        await self._session.commit()
        
        self._committed = True
        self._events.clear()

    async def rollback(self) -> None:
        if self._session:
            await self._session.rollback()

    def record(self, event: DomainEvent) -> None:
        self._events.append(event)
