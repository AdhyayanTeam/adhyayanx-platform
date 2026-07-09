from abc import ABC, abstractmethod

from pydantic import BaseModel


class PolicyResult(BaseModel):
    allowed: bool
    reason: str | None = None


class Policy(ABC):
    name: str

    @abstractmethod
    async def evaluate(self, context: dict) -> PolicyResult:
        ...
