"""Groups related commands, events, and policies into a business capability.

Purpose:
    Declares the public surface of a capability — what commands it accepts,
    what events it publishes, and what policies it enforces.

Responsibilities:
    - Declare command types this capability handles
    - Declare event types this capability publishes
    - Declare policy types this capability evaluates

Does NOT do:
    - Execute commands (services do that)
    - Route events (the event bus does that)
    - Enforce policies (handlers evaluate them)

Who depends on this:
    Capability registrations in kernel/bootstrap.py use this to wire
    command handlers, event handlers, and policies to the right modules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.platform.contracts.command import Command
    from app.modules.platform.contracts.event import DomainEvent
    from app.modules.platform.contracts.policy import Policy


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
