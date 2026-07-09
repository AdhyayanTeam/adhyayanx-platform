from __future__ import annotations

from typing import TypeVar

from fastapi import Request

from kernel.container import Container

T = TypeVar("T")


def get_container(request: Request) -> Container:
    return request.app.state.container


def resolve(interface: type[T]) -> T:
    """FastAPI dependency that resolves T from the DI container."""

    def _resolve(request: Request) -> T:
        return get_container(request).resolve(interface)

    return _resolve
