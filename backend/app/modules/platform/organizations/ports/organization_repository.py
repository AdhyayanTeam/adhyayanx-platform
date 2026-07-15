from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from app.foundation.constants.pagination import DEFAULT_PAGE_LIMIT


class OrganizationRepository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> dict[str, Any] | None: ...

    @abstractmethod
    async def load_by_slug(self, slug: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def create(self, organization: dict[str, Any]) -> None: ...

    @abstractmethod
    async def save(self, organization: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...

    @abstractmethod
    async def exists(self, id: UUID) -> bool: ...

    @abstractmethod
    async def exists_by_slug(self, slug: str) -> bool: ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = DEFAULT_PAGE_LIMIT) -> list[dict[str, Any]]: ...
