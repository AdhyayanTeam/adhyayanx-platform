from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class VerificationTokenRepository(ABC):
    @abstractmethod
    async def create(self, token: dict[str, Any]) -> None: ...

    @abstractmethod
    async def load_by_token_hash(self, token_hash: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def mark_used(self, id: Any) -> None: ...
