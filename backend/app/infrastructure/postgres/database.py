from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from contextvars import ContextVar
from datetime import datetime
from uuid import UUID

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.kernel.config.loader import Settings

logger = logging.getLogger("app.infrastructure.postgres.database")

_sql_count: ContextVar[int] = ContextVar("sql_count", default=0)


def get_sql_count() -> int:
    return _sql_count.get()


def _json_default(obj: object) -> str:
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


class Database:
    """Manages the async SQLAlchemy engine and session factory."""

    def __init__(self, settings: Settings) -> None:
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=1800,
            json_serializer=lambda v: json.dumps(v, default=_json_default),
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self._install_statement_counter()

    def _install_statement_counter(self) -> None:
        sync_engine = self.engine.sync_engine
        event.listen(sync_engine, "before_cursor_execute", self._on_before_execute)
        event.listen(sync_engine, "after_cursor_execute", self._on_after_execute)

    @staticmethod
    def _on_before_execute(_conn, _cursor, _statement, _parameters, _context, _executemany):
        pass

    @staticmethod
    def _on_after_execute(_conn, _cursor, _statement, _parameters, _context, _executemany):
        _sql_count.set(_sql_count.get() + 1)

    async def close(self) -> None:
        sync_engine = self.engine.sync_engine
        event.remove(sync_engine, "before_cursor_execute", self._on_before_execute)
        event.remove(sync_engine, "after_cursor_execute", self._on_after_execute)
        await self.engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        _sql_count.set(0)
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
