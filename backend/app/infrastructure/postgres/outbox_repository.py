from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.tables import OutboxTable
from app.modules.platform.events.ports.outbox_repository import OutboxEntry, OutboxRepository


class PostgresOutboxRepository(OutboxRepository):
    """PostgreSQL implementation of the outbox repository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def append(self, entry: OutboxEntry) -> None:
        row = OutboxTable(
            id=entry.id,
            event_type=entry.event_type,
            aggregate_type=entry.aggregate_type,
            aggregate_id=entry.aggregate_id,
            data=entry.data,
            extra=entry.metadata,
            status=entry.status,
            retry_count=entry.retry_count,
            max_retries=entry.max_retries,
            created_at=entry.created_at or datetime.now(UTC),
        )
        self.session.add(row)

    async def fetch_next_batch(self, limit: int = 50) -> list[OutboxEntry]:
        from sqlalchemy import text

        rows = await self.session.execute(
            text("""
                SELECT * FROM event_outbox
                WHERE status = 'pending'
                    AND (next_retry_at IS NULL OR next_retry_at <= NOW())
                ORDER BY created_at
                LIMIT :limit
                FOR UPDATE SKIP LOCKED
            """),
            {"limit": limit},
        )
        entries = []
        for row in rows.mappings():
            entries.append(
                OutboxEntry(
                    id=row["id"],
                    event_type=row["event_type"],
                    aggregate_type=row["aggregate_type"],
                    aggregate_id=row["aggregate_id"],
                    data=row["data"],
                    metadata=row["extra"],
                    status=row["status"],
                    retry_count=row["retry_count"],
                    max_retries=row["max_retries"],
                    last_error=row.get("last_error"),
                    created_at=row["created_at"],
                    processed_at=row.get("processed_at"),
                    next_retry_at=row.get("next_retry_at"),
                )
            )
        return entries

    async def mark_processed(self, entry_id: UUID) -> None:
        await self.session.execute(
            update(OutboxTable)
            .where(OutboxTable.id == entry_id)
            .values(
                status="processed",
                processed_at=datetime.now(UTC),
            )
        )

    async def increment_retry(self, entry_id: UUID, error: str, next_retry_at: datetime) -> None:
        await self.session.execute(
            update(OutboxTable)
            .where(OutboxTable.id == entry_id)
            .values(
                retry_count=OutboxTable.retry_count + 1,
                last_error=error,
                next_retry_at=next_retry_at,
            )
        )

    async def dead_letter(self, entry_id: UUID, error: str) -> None:
        await self.session.execute(
            update(OutboxTable)
            .where(OutboxTable.id == entry_id)
            .values(
                status="dead_letter",
                last_error=error,
                processed_at=datetime.now(UTC),
            )
        )
