"""Event handlers for identity events."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from adx_platform.contracts.event import DomainEvent

logger = logging.getLogger("adx_platform.identity.handlers")


async def on_user_created(event: DomainEvent) -> None:
    logger.info("User created handler: %s", event.aggregate_id)


async def on_user_deactivated(event: DomainEvent) -> None:
    logger.info("User deactivated: %s", event.aggregate_id)


async def on_user_reactivated(event: DomainEvent) -> None:
    logger.info("User reactivated: %s", event.aggregate_id)


def register_handlers(registry: dict[str, list]) -> None:
    registry["user.created.v1"] = [on_user_created]
    registry["user.deactivated.v1"] = [on_user_deactivated]
    registry["user.reactivated.v1"] = [on_user_reactivated]
