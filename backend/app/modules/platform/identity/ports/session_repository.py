"""Persistence interface for refresh token sessions.

Purpose:
    Tracks active user sessions for refresh token rotation and revocation.
    Each session stores a hashed refresh token, device info, and last-seen time.

Does NOT do:
    - Create access tokens (TokenService handles that)

Who depends on this:
    AuthService creates sessions on login, revokes on logout,
    and rotates on refresh.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class SessionRepository(ABC):
    @abstractmethod
    async def create(self, session: dict[str, Any]) -> None: ...

    @abstractmethod
    async def load_by_refresh_hash(self, token_hash: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def revoke(self, id: UUID) -> None: ...

    @abstractmethod
    async def revoke_all_for_user(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def update_last_seen(self, id: UUID) -> None: ...
