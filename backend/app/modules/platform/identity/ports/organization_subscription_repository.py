from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class OrganizationSubscriptionRepository(ABC):
    @abstractmethod
    async def create(self, subscription: dict[str, Any]) -> None: ...

    @abstractmethod
    async def load_active_by_org(self, organization_id: UUID) -> list[dict[str, Any]]: ...
