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
        )
        from app.modules.blueprints.academy.delivery.contracts.batch_query import BatchQueryContract
        from app.modules.blueprints.academy.delivery.application.query_service import PostgresBatchQueryService

        def _repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.delivery.infrastructure.postgres_repository import (
                PostgresBatchRepository,
            )
            return PostgresBatchRepository(session)

        container.register_instance(BatchRepositoryFactory, _repo_factory)
        container.register(BatchService, BatchService)
        container.register(BatchQueryContract, PostgresBatchQueryService)

    def register_handlers(self, subscribe: Any) -> None:
        pass
