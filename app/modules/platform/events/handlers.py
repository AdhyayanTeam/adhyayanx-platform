"""Core event handlers for the platform event bus."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.platform.contracts.event import DomainEvent


async def log_all_events(event: DomainEvent) -> None:
    """Generic handler that logs every event. Useful for debugging."""
    import logging

    logger = logging.getLogger("app.modules.platform.events")
    logger.debug(
        "Event: %s [%s]",
        event.event_type,
        event.aggregate_id,
    )
