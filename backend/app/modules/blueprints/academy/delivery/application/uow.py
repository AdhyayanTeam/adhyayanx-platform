from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable, Any

from app.modules.platform.contracts.event import DomainEvent
from app.modules.blueprints.academy.delivery.contracts.attendance_repository import AttendanceRepository
from app.modules.blueprints.academy.delivery.contracts.session_repository import SessionRepository
from app.modules.blueprints.academy.enrollment.contracts.enrollment_query import EnrollmentQueryContract

class EnrollmentQueryFactory(Protocol):
    def __call__(self, session: Any) -> EnrollmentQueryContract:
        ...

@runtime_checkable
class DeliveryUnitOfWork(Protocol):
    """
    Application-level boundary for Delivery operations.
    Coordinates transaction scope across repositories and outbox publisher.
    """

    @property
    def sessions(self) -> SessionRepository:
        ...

    @property
    def attendance(self) -> AttendanceRepository:
        ...

    @property
    def enrollment_query(self) -> EnrollmentQueryContract:
        ...

    async def __aenter__(self) -> "DeliveryUnitOfWork":
        """Start the transaction and initialize repositories."""
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        """Rollback if an exception occurred or if commit was not explicitly called."""
        ...

    async def commit(self) -> None:
        """Explicitly commit the transaction and persist outbox events."""
        ...

    def record(self, event: DomainEvent) -> None:
        """Record an event to be published when the transaction commits."""
        ...
