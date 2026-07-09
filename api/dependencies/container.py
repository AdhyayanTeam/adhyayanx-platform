from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from fastapi import Request

from kernel.container import Container

T = TypeVar("T")


def get_container(request: Request) -> Container:
    container: Container = request.app.state.container
    return container


def resolve(interface: type[T]) -> Callable[[Request], T]:
    """FastAPI dependency that resolves T from the DI container."""

    def _resolve(request: Request) -> T:
        return get_container(request).resolve(interface)

    return _resolve
