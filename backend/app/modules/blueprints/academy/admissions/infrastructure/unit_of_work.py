from typing import Protocol

from app.modules.platform.contracts.event import DomainEvent
from app.modules.blueprints.academy.admissions.application.contracts import (
    StudentQueryContract,
    StudentCommandContract,
    EnrollmentCommandContract,
)
from app.modules.blueprints.academy.admissions.infrastructure.repository import AdmissionsRepository

class AdmissionsUnitOfWork(Protocol):
    repository: AdmissionsRepository
    student_queries: StudentQueryContract
    student_commands: StudentCommandContract
    enrollment_commands: EnrollmentCommandContract

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    def record(self, event: DomainEvent) -> None: ...
    async def __aenter__(self) -> "AdmissionsUnitOfWork": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
