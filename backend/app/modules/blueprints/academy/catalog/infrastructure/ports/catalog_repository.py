from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class CatalogRepository(ABC):
    @abstractmethod
    async def save(self, course: dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def load(self, id: UUID, organization_id: UUID) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def list(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        pass
