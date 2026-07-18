"""Application bootstrap — the single composition root.

Wires infrastructure, event system, domain modules, and extensions.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.kernel.config.loader import Settings
from app.kernel.container import Container
from app.kernel.discovery import discover_blueprints, discover_handlers
from app.kernel.lifecycle import Lifecycle

if TYPE_CHECKING:
    from app.modules.platform.contracts.module import PlatformModule

logger = logging.getLogger("app.kernel")


class Bootstrap:
    """Orchestrates application startup."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.container = Container()
        self.lifecycle = Lifecycle(self.container)

    def configure(self) -> None:
        self.container.register_instance(Settings, self.settings)
        self._wire_infrastructure()
        self._wire_event_system()
        self._register_modules()
        self._discover_extensions()

    def _wire_infrastructure(self) -> None:
        from app.infrastructure.postgres.database import Database

        db = Database(self.settings)
        self.container.register_instance(Database, db)

    def _wire_event_system(self) -> None:
        from typing import Any

        from app.infrastructure.postgres.outbox_repository import PostgresOutboxRepository
        from app.modules.platform.events.bus import EventBus
        from app.modules.platform.events.ports.event_bus import EventBus as EventBusInterface
        from app.modules.platform.events.publisher import Publisher

        def _outbox_factory(session: Any) -> Any:
            return PostgresOutboxRepository(session)

        self._event_bus = EventBus()
        publisher = Publisher(outbox_factory=_outbox_factory)

        self.container.register_instance(EventBusInterface, self._event_bus)  # type: ignore[type-abstract]
        self.container.register_instance(Publisher, publisher)

    def _register_modules(self) -> None:
        """Configure domain modules and register their event handlers.

        Modules are instantiated explicitly here.
        No filesystem scanning or dynamic imports.
        """
        from app.modules.platform.identity.module import IdentityModule
        from app.modules.platform.notifications.module import NotificationsModule
        from app.modules.platform.organizations.module import OrganizationModule
        from app.modules.blueprints.academy.catalog.module import AcademyCatalogModule
        from app.modules.blueprints.academy.students.module import AcademyStudentsModule
        from app.modules.blueprints.academy.delivery.module import AcademyDeliveryModule
        from app.modules.blueprints.academy.enrollment.module import AcademyEnrollmentModule

        modules: list[PlatformModule] = [
            IdentityModule(),
            OrganizationModule(),
            NotificationsModule(),
            AcademyCatalogModule(),
            AcademyStudentsModule(),
            AcademyDeliveryModule(),
            AcademyEnrollmentModule(),
        ]

        for module in modules:
            module.configure(self.container)
            module.register_handlers(self._event_bus.subscribe)
            logger.info("Registered module: %s", module.name)

    def _discover_extensions(self) -> None:
        """Discover blueprints and event handler groups."""
        blueprints = discover_blueprints(self.container)
        if blueprints:
            logger.info("Discovered blueprints: %s", ", ".join(blueprints))
        handlers = discover_handlers(self.container)
        logger.info("Discovered %d event handler groups", len(handlers))

    async def shutdown(self) -> None:
        from app.infrastructure.postgres.database import Database

        logger.info("Shutting down application...")
        try:
            db = self.container.resolve(Database)
            await db.close()
        except KeyError:
            pass
        logger.info("Application shutdown complete")
