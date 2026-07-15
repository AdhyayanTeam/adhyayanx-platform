from __future__ import annotations

import hashlib
import logging
import secrets
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from uuid import UUID

import jwt

from app.shared.auth import REFRESH_TOKEN_BYTE_LENGTH

if TYPE_CHECKING:
    from app.kernel.config.loader import Settings

logger = logging.getLogger("app.modules.platform.identity.token_service")


class TokenService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        with open(settings.jwt_private_key_path) as f:
            self._private_key = f.read()
        with open(settings.jwt_public_key_path) as f:
            self._public_key = f.read()

    def create_access_token(
        self,
        user_id: UUID,
        org_id: UUID,
        roles: list[str] | None = None,
    ) -> str:
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": str(user_id),
            "org": str(org_id),
            "roles": roles or [],
            "iat": now,
            "exp": now + timedelta(minutes=self._settings.jwt_access_token_expire_minutes),
            "type": "access",
        }
        return jwt.encode(payload, self._private_key, algorithm=self._settings.jwt_algorithm)

    def create_refresh_token_pair(self) -> tuple[str, str]:
        raw = secrets.token_urlsafe(REFRESH_TOKEN_BYTE_LENGTH)
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        return raw, hashed

    def decode_access_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(
            token,
            self._public_key,
            algorithms=[self._settings.jwt_algorithm],
            options={"require": ["sub", "org", "exp", "iat", "type"]},
        )

    def hash_refresh_token(self, raw: str) -> str:
        return hashlib.sha256(raw.encode()).hexdigest()
