from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.tables import SessionTable
from app.modules.platform.identity.ports.session_repository import SessionRepository


class PostgresSessionRepository(SessionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, session_data: dict[str, Any]) -> None:
        row = SessionTable(
            id=session_data["id"],
            user_id=session_data["user_id"],
            refresh_token_hash=session_data["refresh_token_hash"],
            ip_address=session_data.get("ip_address"),
            user_agent=session_data.get("user_agent"),
            device_name=session_data.get("device_name"),
            last_seen_at=session_data.get("last_seen_at"),
            expires_at=session_data["expires_at"],
            created_at=session_data.get("created_at", datetime.now(UTC)),
        )
        self._session.add(row)
        await self._session.flush()

    async def load_by_refresh_hash(self, token_hash: str) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(SessionTable).where(SessionTable.refresh_token_hash == token_hash)
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def revoke(self, id: UUID) -> None:
        await self._session.execute(
            update(SessionTable).where(SessionTable.id == id).values(revoked_at=datetime.now(UTC))
        )

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        await self._session.execute(
            update(SessionTable)
            .where(SessionTable.user_id == user_id, SessionTable.revoked_at.is_(None))
            .values(revoked_at=datetime.now(UTC))
        )

    async def update_last_seen(self, id: UUID) -> None:
        await self._session.execute(
            update(SessionTable).where(SessionTable.id == id).values(last_seen_at=datetime.now(UTC))
        )

    def _to_dict(self, row: SessionTable) -> dict[str, Any]:
        return {
            "id": row.id,
            "user_id": row.user_id,
            "refresh_token_hash": row.refresh_token_hash,
            "ip_address": row.ip_address,
            "user_agent": row.user_agent,
            "device_name": row.device_name,
            "last_seen_at": row.last_seen_at,
            "expires_at": row.expires_at,
            "created_at": row.created_at,
            "revoked_at": row.revoked_at,
        }
