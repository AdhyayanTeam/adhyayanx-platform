from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from app.modules.platform.contracts.repository import Repository
    from app.modules.platform.events.ports.outbox_repository import OutboxEntry


class PostgresUnitOfWork:
    """Unit of Work implementation for PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._repositories: dict[type, Repository] = {}
        self._outbox_entries: list[OutboxEntry] = []

    def register_repository(self, repo_type: type, repository: Repository) -> None:
        self._repositories[repo_type] = repository

    def repository(self, repo_type: type) -> Repository:
        return self._repositories[repo_type]

    def add_outbox_entry(self, entry: OutboxEntry) -> None:
        self._outbox_entries.append(entry)

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def rollback(self) -> None:
        await self.session.rollback()
        self._outbox_entries.clear()
