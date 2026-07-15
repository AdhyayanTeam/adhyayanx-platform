"""Event bus interface and handler type definition.

Purpose:
    Defines the contract that all event bus implementations must satisfy.
    The event bus is the central nervous system for cross-cutting side effects.

Responsibilities:
    - Publish events to all registered handlers
    - Allow subscribe/unsubscribe at runtime

Does NOT do:
    - Persist events (the outbox handles that)
    - Guarantee delivery (fire-and-forget from the publisher)

Who depends on this:
    AuthService and OrganizationService publish events through this.
    OutboxDispatcher dispatches buffered events through this.
"""

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

from app.modules.platform.contracts.event import DomainEvent

EventHandler = Callable[[DomainEvent], Awaitable[None]]


class EventBus(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None: ...

    @abstractmethod
    def subscribe(self, event_type: str, handler: EventHandler) -> None: ...

    @abstractmethod
    def unsubscribe(self, event_type: str, handler: EventHandler) -> None: ...
