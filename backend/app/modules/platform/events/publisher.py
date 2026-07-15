"""Writes domain events to the outbox within a database session.

Purpose:
    Buffers domain events in the event outbox so they can be dispatched
    reliably after the transaction commits.

Invariants:
    Publisher is stateless. It must never cache repositories, sessions,
    or transactions. Every call operates entirely through the supplied
    outbox repository, constructed fresh from the factory.

Does NOT do:
    - Dispatch events (OutboxDispatcher handles that)
    - Manage sessions or transactions (the caller owns those)

Who depends on this:
    Services call publish() inside a session context to enqueue events.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from app.modules.platform.contracts.event import DomainEvent
from app.modules.platform.events.ports.outbox_repository import OutboxEntry, OutboxRepository

logger = logging.getLogger("app.modules.platform.events.publisher")


class Publisher:
    """Writes domain events to the outbox via OutboxRepository port.

    The outbox_factory is a callable that takes a session and returns
    an OutboxRepository bound to that session. This keeps Publisher
    free of infrastructure knowledge — the factory is injected by the
    composition root.
    """

    def __init__(self, outbox_factory: Callable[[Any], OutboxRepository]) -> None:
        self._outbox_factory = outbox_factory

    async def publish(self, event: DomainEvent, session: Any) -> None:
        outbox = self._outbox_factory(session)
        entry = OutboxEntry(
            id=event.event_id,
            event_type=event.event_type,
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            data=event.data | event.model_dump(),
            metadata=event.metadata,
        )
        await outbox.append(entry)
        logger.debug("Outbox entry queued: %s [%s]", event.event_type, event.event_id)
