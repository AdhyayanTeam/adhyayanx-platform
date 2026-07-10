from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

from app.kernel.container import Container

logger = logging.getLogger("app.kernel")


class Lifecycle:
    """Manages application startup and shutdown hooks."""

    def __init__(self, container: Container) -> None:
        self.container = container
        self._startup_hooks: list[Callable[[], Awaitable[None]]] = []
        self._shutdown_hooks: list[Callable[[], Awaitable[None]]] = []
        self._tasks: list[asyncio.Task[Any]] = []

    def on_startup(self, hook: Callable[[], Awaitable[None]]) -> None:
        self._startup_hooks.append(hook)

    def on_shutdown(self, hook: Callable[[], Awaitable[None]]) -> None:
        self._shutdown_hooks.append(hook)

    def create_task(self, coro: Awaitable[Any]) -> None:
        task: asyncio.Task[Any] = asyncio.create_task(coro)  # type: ignore[arg-type]
        self._tasks.append(task)

    async def startup(self) -> None:
        logger.info("Starting ADX adx_platform...")
        for hook in self._startup_hooks:
            await hook()

    async def shutdown(self) -> None:
        logger.info("Shutting down ADX adx_platform...")
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        for hook in self._shutdown_hooks:
            await hook()

    @asynccontextmanager
    async def lifespan(self) -> AsyncIterator[None]:
        try:
            await self.startup()
            yield
        finally:
            await self.shutdown()
