from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class OutboxEntry:
    id: UUID
    event_type: str
    aggregate_type: str
    aggregate_id: UUID
    data: dict[str, Any]
    metadata: dict[str, Any]
    status: str  # pending | processed | failed
    retry_count: int = 0
    max_retries: int = 5
    last_error: str | None = None
    created_at: datetime | None = None
    processed_at: datetime | None = None
    next_retry_at: datetime | None = None


class OutboxRepository(ABC):
    @abstractmethod
    async def append(self, entry: OutboxEntry) -> None: ...

    @abstractmethod
    async def fetch_next_batch(self, limit: int = 50) -> list[OutboxEntry]: ...

    @abstractmethod
    async def mark_processed(self, entry_id: UUID) -> None: ...

    @abstractmethod
    async def increment_retry(
        self, entry_id: UUID, error: str, next_retry_at: datetime
    ) -> None: ...

    @abstractmethod
    async def dead_letter(self, entry_id: UUID, error: str) -> None: ...
