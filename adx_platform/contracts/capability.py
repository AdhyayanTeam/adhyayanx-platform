from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from adx_platform.contracts.command import Command
    from adx_platform.contracts.event import DomainEvent
    from adx_platform.contracts.policy import Policy


class Capability(ABC):
    name: str
    version: str

    @property
    @abstractmethod
    def commands(self) -> list[type[Command]]: ...

    @property
    @abstractmethod
    def events(self) -> list[type[DomainEvent]]: ...

    @property
    @abstractmethod
    def policies(self) -> list[type[Policy]]: ...
