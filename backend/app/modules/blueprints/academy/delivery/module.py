from __future__ import annotations
from typing import TYPE_CHECKING, Any

from app.modules.platform.contracts.module import PlatformModule

if TYPE_CHECKING:
    from app.kernel.container import Container

class AcademyDeliveryModule(PlatformModule):
    name = "academy.delivery"

    def configure(self, container: Container) -> None:
        from app.modules.blueprints.academy.delivery.application.service import (
            BatchRepositoryFactory,
            BatchService,
            SessionRepositoryFactory,
            AttendanceRepositoryFactory,
            DeliveryService,
        )
        from app.modules.blueprints.academy.delivery.contracts.batch_query import BatchQueryContract
        from app.modules.blueprints.academy.delivery.application.query_service import PostgresBatchQueryService

        def _repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.delivery.infrastructure.postgres_repository import (
                PostgresBatchRepository,
            )
            return PostgresBatchRepository(session)

        def _session_repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.delivery.infrastructure.postgres_repository import (
                PostgresSessionRepository,
            )
            return PostgresSessionRepository(session)

        def _attendance_repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.delivery.infrastructure.postgres_repository import (
                PostgresAttendanceRepository,
            )
            return PostgresAttendanceRepository(session)

        container.register_instance(BatchRepositoryFactory, _repo_factory)
        container.register_instance(SessionRepositoryFactory, _session_repo_factory)
        container.register_instance(AttendanceRepositoryFactory, _attendance_repo_factory)
        container.register(BatchService, BatchService)
        container.register(DeliveryService, DeliveryService)
        container.register(BatchQueryContract, PostgresBatchQueryService)

    def register_handlers(self, subscribe: Any) -> None:
        pass
