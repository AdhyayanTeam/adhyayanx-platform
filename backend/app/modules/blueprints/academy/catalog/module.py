from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.modules.platform.contracts.module import PlatformModule

if TYPE_CHECKING:
    from app.kernel.container import Container


class AcademyCatalogModule(PlatformModule):
    name = "academy.catalog"

    def configure(self, container: Container) -> None:
        from app.modules.blueprints.academy.catalog.application.service import (
            CatalogRepositoryFactory,
            CatalogService,
        )

        def _repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.catalog.infrastructure.postgres_repository import (
                PostgresCatalogRepository,
            )

            return PostgresCatalogRepository(session)

        container.register_instance(CatalogRepositoryFactory, _repo_factory)
        container.register(CatalogService, CatalogService)

    def register_handlers(self, subscribe: Any) -> None:
        # Register handlers here if needed later.
        pass
