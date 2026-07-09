from __future__ import annotations

import logging

from kernel.config.loader import Settings
from kernel.container import Container
from kernel.discovery import discover_blueprints, discover_handlers
from kernel.lifecycle import Lifecycle

logger = logging.getLogger("adx.kernel")


class Bootstrap:
    """Orchestrates application startup."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.container = Container()
        self.lifecycle = Lifecycle(self.container)

    def configure(self) -> None:
        self.container.register_instance(Settings, self.settings)
        self._wire_infrastructure()
        self._wire_domains()
        self._wire_event_system()
        self._discover_extensions()

    def _wire_infrastructure(self) -> None:
        from infrastructure.postgres.database import Database
        db = Database(self.settings)
        self.container.register_instance(Database, db)

    def _wire_domains(self) -> None:
        from adx_platform.identity.service import IdentityService
        from adx_platform.organizations.service import OrganizationService

        self.container.register(OrganizationService, OrganizationService)
        self.container.register(IdentityService, IdentityService)

    def _wire_event_system(self) -> None:
        from adx_platform.events.bus import EventBus
        from adx_platform.events.ports.event_bus import EventBus as EventBusInterface
        from adx_platform.events.publisher import Publisher

        event_bus = EventBus()
        publisher = Publisher()

        self.container.register_instance(EventBusInterface, event_bus)
        self.container.register_instance(Publisher, publisher)

    def _discover_extensions(self) -> None:
        blueprints = discover_blueprints(self.container)
        if blueprints:
            logger.info("Discovered blueprints: %s", ", ".join(blueprints))
        handlers = discover_handlers(self.container)
        logger.info("Discovered %d event handler groups", len(handlers))
