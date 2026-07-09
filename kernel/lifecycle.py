from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from kernel.container import Container

logger = logging.getLogger("adx.kernel")


class Lifecycle:
    """Manages application startup and shutdown hooks."""

    def __init__(self, container: Container) -> None:
        self.container = container
        self._startup_hooks: list[Callable] = []
        self._shutdown_hooks: list[Callable] = []
        self._tasks: list[asyncio.Task] = []

    def on_startup(self, hook: Callable) -> None:
        self._startup_hooks.append(hook)

    def on_shutdown(self, hook: Callable) -> None:
        self._shutdown_hooks.append(hook)

    def create_task(self, coro) -> None:
        task = asyncio.create_task(coro)
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
