from abc import ABC, abstractmethod
from uuid import UUID


class IdentityRepository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> dict | None:
        ...

    @abstractmethod
    async def load_by_email(self, email: str) -> dict | None:
        ...

    @abstractmethod
    async def save(self, user: dict) -> None:
        ...

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        ...

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        ...

    @abstractmethod
    async def list(self, organization_id: UUID, skip: int = 0, limit: int = 100) -> list[dict]:
        ...
