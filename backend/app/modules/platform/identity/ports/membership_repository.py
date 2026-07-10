from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class MembershipRepository(ABC):
    @abstractmethod
    async def create(self, membership: dict[str, Any]) -> None: ...

    @abstractmethod
    async def load_by_user_and_org(
        self, user_id: UUID, organization_id: UUID
    ) -> dict[str, Any] | None: ...

    @abstractmethod
    async def list_for_user(self, user_id: UUID) -> list[dict[str, Any]]: ...
