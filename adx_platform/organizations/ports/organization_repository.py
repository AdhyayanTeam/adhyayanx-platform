from abc import ABC, abstractmethod
from uuid import UUID


class OrganizationRepository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> dict | None:
        ...

    @abstractmethod
    async def load_by_slug(self, slug: str) -> dict | None:
        ...

    @abstractmethod
    async def save(self, organization: dict) -> None:
        ...

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        ...

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        ...

    @abstractmethod
    async def exists_by_slug(self, slug: str) -> bool:
        ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[dict]:
        ...
