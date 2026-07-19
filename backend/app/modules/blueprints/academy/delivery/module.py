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
            DeliveryService,
        )
        from app.modules.blueprints.academy.delivery.contracts.batch_query import BatchQueryContract
        from app.modules.blueprints.academy.delivery.application.query_service import PostgresBatchQueryService

        def _repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.delivery.infrastructure.postgres_repository import (
                PostgresBatchRepository,
            )
            return PostgresBatchRepository(session)

        def _enrollment_query_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.enrollment.infrastructure.postgres_enrollment_query import PostgresEnrollmentQueryService
            return PostgresEnrollmentQueryService(session)

        from app.modules.blueprints.academy.delivery.application.uow import DeliveryUnitOfWork, EnrollmentQueryFactory
        from app.modules.blueprints.academy.delivery.infrastructure.postgres_uow import PostgresDeliveryUnitOfWork

        from app.modules.blueprints.academy.delivery.application.queries import BatchOperationsQuery
        from app.modules.blueprints.academy.delivery.infrastructure.postgres_queries import PostgresBatchOperationsQuery

        container.register_instance(BatchRepositoryFactory, _repo_factory)
        container.register_instance(EnrollmentQueryFactory, _enrollment_query_factory)
        container.register(DeliveryUnitOfWork, PostgresDeliveryUnitOfWork)
        container.register(BatchService, BatchService)
        container.register(DeliveryService, DeliveryService)
        container.register(BatchQueryContract, PostgresBatchQueryService)
        container.register(BatchOperationsQuery, PostgresBatchOperationsQuery)

    def register_handlers(self, subscribe: Any) -> None:
        pass
