from abc import ABC, abstractmethod
from collections.abc import Callable

from adx_platform.contracts.event import DomainEvent

EventHandler = Callable[[DomainEvent], None]


class EventBus(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        ...

    @abstractmethod
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        ...

    @abstractmethod
    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        ...
