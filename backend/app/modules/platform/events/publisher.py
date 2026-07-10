from __future__ import annotations

import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.tables import OutboxTable
from app.modules.platform.contracts.event import DomainEvent

logger = logging.getLogger("app.modules.platform.events.publisher")


class Publisher:
    """Writes domain events to the outbox within a database session."""

    async def publish(self, event: DomainEvent, session: AsyncSession) -> None:
        row = OutboxTable(
            id=event.event_id,
            event_type=event.event_type,
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            data=event.data | event.model_dump(),
            extra=event.metadata,
            status="pending",
            created_at=datetime.now(UTC),
        )
        session.add(row)
        logger.debug("Outbox entry queued: %s [%s]", event.event_type, event.event_id)
