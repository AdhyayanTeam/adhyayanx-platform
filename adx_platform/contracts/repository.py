from abc import ABC, abstractmethod
from typing import TypeVar
from uuid import UUID

from adx_platform.contracts.business_object import BusinessObject

T = TypeVar("T", bound=BusinessObject)


class Repository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> T: ...

    @abstractmethod
    async def save(self, aggregate: T) -> None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...

    @abstractmethod
    async def exists(self, id: UUID) -> bool: ...
