"""Event handlers for organization events."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.modules.platform.contracts.event import DomainEvent

logger = logging.getLogger("app.modules.platform.organizations.handlers")


async def on_organization_created(event: DomainEvent) -> None:
    logger.info("Organization created handler: %s", event.aggregate_id)
    # Future: provision default workspace, create default roles, notify DHARA


async def on_organization_updated(event: DomainEvent) -> None:
    logger.debug("Organization updated: %s", event.aggregate_id)


async def on_organization_deleted(event: DomainEvent) -> None:
    logger.info("Organization deleted: %s", event.aggregate_id)
    # Future: clean up associated resources


def register_handlers(registry: dict[str, list[Any]]) -> None:
    registry["organization.created.v1"] = [on_organization_created]
    registry["organization.updated.v1"] = [on_organization_updated]
    registry["organization.deleted.v1"] = [on_organization_deleted]
