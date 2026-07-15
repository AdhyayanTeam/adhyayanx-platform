"""Persistence interface for user identity data.

Purpose:
    Abstracts how user records are stored and retrieved.
    IdentityService depends on this, never on the concrete Postgres impl.

Does NOT do:
    - Enforce password rules (PasswordPolicy handles that)
    - Issue JWT tokens (TokenService handles that)

Who depends on this:
    IdentityService, AuthService, and test doubles (DictIdentityRepository).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from app.shared.pagination import DEFAULT_PAGE_LIMIT


class IdentityRepository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> dict[str, Any] | None: ...

    @abstractmethod
    async def load_by_email(self, email: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def create(self, user: dict[str, Any]) -> None: ...

    @abstractmethod
    async def save(self, user: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...

    @abstractmethod
    async def exists(self, id: UUID) -> bool: ...

    @abstractmethod
    async def list(
        self, organization_id: UUID, skip: int = 0, limit: int = DEFAULT_PAGE_LIMIT
    ) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def update_password(self, id: UUID, password_hash: str) -> None: ...

    @abstractmethod
    async def set_verified(self, id: UUID) -> None: ...
