"""Persistence interface for email verification and password reset tokens.

Purpose:
    Stores one-time tokens used for email verification and password reset.
    Tokens are hashed before storage; only the raw token is sent to the user.

Does NOT do:
    - Generate tokens (TokenService handles that)
    - Send emails (EmailService handles that)

Who depends on this:
    AuthService creates tokens during signup/forgot-password,
    loads and marks them used during verify-email/reset-password.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class VerificationTokenRepository(ABC):
    @abstractmethod
    async def create(self, token: dict[str, Any]) -> None: ...

    @abstractmethod
    async def load_by_token_hash(self, token_hash: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def mark_used(self, id: UUID) -> None: ...
