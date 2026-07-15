from __future__ import annotations

from app.modules.platform.events.ports.event_bus import EventHandler


class SubscriberRegistry:
    """Manages event-type to handler mappings."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def register(self, event_type: str, handler: EventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def get_handlers(self, event_type: str) -> list[EventHandler]:
        return self._handlers.get(event_type, [])

    def all_registrations(self) -> dict[str, list[EventHandler]]:
        return dict(self._handlers)
