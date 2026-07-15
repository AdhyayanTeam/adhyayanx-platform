"""Outbox dispatcher for reliable event publishing.

Purpose:
    Polls the outbox table for pending events and dispatches them
    to the event bus. Handles retry logic and dead-lettering.

Responsibilities:
    - Poll pending events on an interval
    - Deserialize and dispatch events to handlers
    - Mark events as processed on success
    - Increment retry count on failure
    - Dead-letter events after max retries

Does NOT do:
    - Write events to the outbox (Publisher handles that)
    - Guarantee exactly-once delivery (at-least-once via outbox pattern)
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from datetime import UTC, datetime
from typing import Any

from app.foundation.constants.outbox import OUTBOX_POLL_INTERVAL_SECONDS
from app.modules.platform.events.ports.event_bus import EventBus
from app.modules.platform.events.ports.outbox_repository import OutboxRepository

logger = logging.getLogger("app.modules.platform.events.outbox")


class OutboxDispatcher:
    """Polls outbox table and dispatches events to handlers."""

    POLL_INTERVAL = OUTBOX_POLL_INTERVAL_SECONDS

    def __init__(
        self,
        outbox_repository: OutboxRepository,
        event_bus: EventBus,
    ) -> None:
        self._outbox = outbox_repository
        self._event_bus = event_bus
        self._running = False
        self._task: asyncio.Task[Any] | None = None

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
        entries = await self._outbox.fetch_next_batch()
        for entry in entries:
            await self._dispatch_one(entry)

    async def _dispatch_one(self, entry: Any) -> None:
        try:
            from app.modules.platform.contracts.event import DomainEvent

            event = DomainEvent(**entry.data)
            await self._event_bus.publish(event)
            await self._outbox.mark_processed(entry.id)
        except Exception as exc:
            await self._handle_failure(entry, exc)

    async def _handle_failure(self, entry: Any, exc: Exception) -> None:
        error_msg = str(exc)
        if entry.retry_count + 1 >= entry.max_retries:
            await self._outbox.dead_letter(entry.id, error_msg)
            logger.error(
                "Event dead-lettered after %d retries: %s [%s]",
                entry.retry_count,
                entry.event_type,
                entry.id,
            )
        else:
            import secrets

            backoff = min(2 ** entry.retry_count + secrets.randbelow(100) / 100, 60)
            next_retry = datetime.now(UTC).timestamp() + backoff
            next_retry_dt = datetime.fromtimestamp(next_retry, tz=UTC)
            await self._outbox.increment_retry(entry.id, error_msg, next_retry_dt)
            logger.warning(
                "Event dispatch failed (retry %d/%d): %s [%s]",
                entry.retry_count + 1,
                entry.max_retries,
                entry.event_type,
                entry.id,
            )
