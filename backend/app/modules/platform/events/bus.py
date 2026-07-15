"""In-memory event bus for dispatching domain events to handlers.

Purpose:
    Routes published events to all registered handlers for that event type.
    This is the synchronous dispatch layer — handlers are awaited sequentially.

Does NOT do:
    - Persist events (the outbox handles that)
    - Guarantee delivery (fire-and-forget from the publisher)
    - Handle retries (failed handlers are logged and skipped)

Who depends on this:
    Publisher wraps this bus and adds outbox integration.
    Services publish events through Publisher, which delegates here.
"""

from __future__ import annotations

import logging

from app.modules.platform.contracts.event import DomainEvent
from app.modules.platform.events.ports.event_bus import EventBus as EventBusInterface
from app.modules.platform.events.ports.event_bus import EventHandler

logger = logging.getLogger("app.modules.platform.events")


class EventBus(EventBusInterface):
    """In-memory event bus. Dispatches to registered handlers."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = {}

    async def publish(self, event: DomainEvent) -> None:
        handlers = self._subscribers.get(event.event_type, [])
        if not handlers:
            logger.debug("No handlers registered for %s", event.event_type)
            return
        for handler in handlers:
            try:
                await handler(event)
            except Exception:
                logger.exception("Handler failed for %s", event.event_type)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info("Subscribed handler %s to %s", handler.__name__, event_type)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        handlers = self._subscribers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)
            logger.info("Unsubscribed handler %s from %s", handler.__name__, event_type)
