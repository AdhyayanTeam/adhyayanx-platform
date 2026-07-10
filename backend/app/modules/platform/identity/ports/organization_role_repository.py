from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class OrganizationRoleRepository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> dict[str, Any] | None: ...

    @abstractmethod
    async def create(self, role: dict[str, Any]) -> None: ...

    @abstractmethod
    async def load_by_name_and_org(
        self, name: str, organization_id: UUID
    ) -> dict[str, Any] | None: ...

    @abstractmethod
    async def list_for_org(self, organization_id: UUID) -> list[dict[str, Any]]: ...
