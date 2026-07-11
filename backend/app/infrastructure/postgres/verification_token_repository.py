from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.postgres.tables import EmailVerificationTokenTable
from app.modules.platform.identity.ports.verification_token_repository import (
    VerificationTokenRepository,
)


class PostgresVerificationTokenRepository(VerificationTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, token: dict[str, Any]) -> None:
        row = EmailVerificationTokenTable(
            id=token["id"],
            user_id=token["user_id"],
            token_hash=token["token_hash"],
            purpose=token["purpose"],
            expires_at=token["expires_at"],
            created_at=token.get("created_at", datetime.now(UTC)),
        )
        self._session.add(row)

    async def load_by_token_hash(self, token_hash: str) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(EmailVerificationTokenTable).where(
                EmailVerificationTokenTable.token_hash == token_hash
            )
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def mark_used(self, id: Any) -> None:
        await self._session.execute(
            update(EmailVerificationTokenTable)
            .where(EmailVerificationTokenTable.id == id)
            .values(used_at=datetime.now(UTC))
        )

    def _to_dict(self, row: EmailVerificationTokenTable) -> dict[str, Any]:
        return {
            "id": row.id,
            "user_id": row.user_id,
            "token_hash": row.token_hash,
            "purpose": row.purpose,
            "expires_at": row.expires_at,
            "created_at": row.created_at,
            "used_at": row.used_at,
        }
