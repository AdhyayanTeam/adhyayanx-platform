"""Module manifest interfaces for ADX platform modules.

A platform module encapsulates domain logic and event handlers.
An API module encapsulates HTTP transport concerns.

Separation ensures modules remain transport-agnostic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastapi import FastAPI

    from app.kernel.container import Container


class PlatformModule(ABC):
    """Domain module interface.

    Responsible for:
    - Configuring services in the DI container
    - Registering event handlers on the event bus
    """

    name: str

    @abstractmethod
    def configure(self, container: Container) -> None:
        """Register services in the DI container."""
        ...

    @abstractmethod
    def register_handlers(self, subscribe: Callable[[str, Any], None]) -> None:
        """Subscribe event handlers to the event bus.

        Args:
            subscribe: Callable with signature (event_type: str, handler: EventHandler)
        """
        ...


class ApiModule(ABC):
    """HTTP transport interface.

    Responsible for:
    - Registering FastAPI routers

    Separated from PlatformModule so modules remain transport-agnostic.
    """

    @abstractmethod
    def register_routes(self, app: FastAPI, prefix: str) -> None:
        """Register FastAPI routers on the application."""
        ...
