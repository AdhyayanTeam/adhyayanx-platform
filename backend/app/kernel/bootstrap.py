from __future__ import annotations

import logging

from app.kernel.config.loader import Settings
from app.kernel.container import Container
from app.kernel.discovery import discover_blueprints, discover_handlers
from app.kernel.lifecycle import Lifecycle

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
        self._wire_domains()
        self._wire_event_system()
        self._discover_extensions()

    def _wire_infrastructure(self) -> None:
        from app.infrastructure.postgres.database import Database

        db = Database(self.settings)
        self.container.register_instance(Database, db)

    def _wire_domains(self) -> None:
        from app.modules.platform.identity.auth_service import AuthService
        from app.modules.platform.identity.navigation_service import NavigationService
        from app.modules.platform.identity.password_policy import PasswordPolicy
        from app.modules.platform.identity.service import IdentityService
        from app.modules.platform.identity.token_service import TokenService
        from app.modules.platform.organizations.service import OrganizationService

        self.container.register(IdentityService, IdentityService)
        self.container.register(OrganizationService, OrganizationService)
        self.container.register(AuthService, AuthService)
        self.container.register(TokenService, TokenService)
        self.container.register(NavigationService, NavigationService)
        self.container.register(PasswordPolicy, PasswordPolicy)

    def _wire_event_system(self) -> None:
        from app.modules.platform.events.bus import EventBus
        from app.modules.platform.events.ports.event_bus import EventBus as EventBusInterface
        from app.modules.platform.events.publisher import Publisher

        event_bus = EventBus()
        publisher = Publisher()

        self.container.register_instance(EventBusInterface, event_bus)  # type: ignore[type-abstract]
        self.container.register_instance(Publisher, publisher)

    def _discover_extensions(self) -> None:
        blueprints = discover_blueprints(self.container)
        if blueprints:
            logger.info("Discovered blueprints: %s", ", ".join(blueprints))
        handlers = discover_handlers(self.container)
        logger.info("Discovered %d event handler groups", len(handlers))
