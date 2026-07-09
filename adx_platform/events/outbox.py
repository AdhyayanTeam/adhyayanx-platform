from __future__ import annotations

import asyncio
import contextlib
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

logger = logging.getLogger("adx_platform.outbox")


@dataclass
class OutboxEntry:
    id: UUID = field(default_factory=uuid4)
    event_type: str = ""
    aggregate_type: str = ""
    aggregate_id: UUID | None = None
    data: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    status: str = "pending"
    retry_count: int = 0
    max_retries: int = 5
    last_error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    processed_at: datetime | None = None
    next_retry_at: datetime | None = None


class OutboxDispatcher:
    """Polls outbox table and dispatches events to handlers."""

    POLL_INTERVAL = 0.1

    def __init__(self) -> None:
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._poll_loop())
        logger.info("Outbox dispatcher started")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
        logger.info("Outbox dispatcher stopped")

    async def _poll_loop(self) -> None:
        while self._running:
            try:
                await self._dispatch_batch()
            except Exception:
                logger.exception("Outbox dispatch error")
            await asyncio.sleep(self.POLL_INTERVAL)

    async def _dispatch_batch(self) -> None:
        """Override in subclass with actual outbox repository integration."""
        # To be wired with OutboxRepository.fetch_next_batch
        pass
