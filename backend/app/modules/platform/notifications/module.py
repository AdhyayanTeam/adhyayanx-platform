"""Notifications module manifest.

Encapsulates email sending and notification delivery.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.modules.platform.contracts.module import PlatformModule

if TYPE_CHECKING:
    from app.kernel.container import Container


class NotificationsModule(PlatformModule):
    name = "notifications"

    def configure(self, container: Container) -> None:
        # EmailService is wired in api/main.py based on settings.email_provider
        pass

    def register_handlers(self, subscribe: Any) -> None:
        # Future: subscribe to events that trigger notifications
        pass
