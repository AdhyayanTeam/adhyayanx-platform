from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class PolicyResult(BaseModel):
    allowed: bool
    reason: str | None = None


class Policy(ABC):
    name: str

    @abstractmethod
    async def evaluate(self, context: dict[str, Any]) -> PolicyResult: ...
