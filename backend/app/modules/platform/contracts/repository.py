"""Persistence abstraction for aggregates.

Purpose:
    Each aggregate type gets its own repository. The repository
    interface is defined in the domain layer; infrastructure
    implements it with a specific database.

Responsibilities:
    - Load an aggregate by ID
    - Save (create or update) an aggregate
    - Delete an aggregate
    - Check if an aggregate exists

Does NOT do:
    - Enforce business rules (that's the aggregate's job)
    - Coordinate transactions (unit of work handles that)

Who depends on this:
    Services call repository methods to load and persist aggregates.
    The concrete implementation (Postgres, in-memory for tests) is
    injected via the dependency container.
"""

from abc import ABC, abstractmethod
from typing import TypeVar
from uuid import UUID

from app.modules.platform.contracts.business_object import BusinessObject

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
