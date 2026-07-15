"""Organizations module manifest.

Encapsulates organization (tenant) management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.modules.platform.contracts.module import PlatformModule

if TYPE_CHECKING:
    from app.kernel.container import Container


class OrganizationModule(PlatformModule):
    name = "organizations"

    def configure(self, container: Container) -> None:
        from app.modules.platform.organizations.service import OrganizationService

        container.register(OrganizationService, OrganizationService)

    def register_handlers(self, subscribe: Any) -> None:
        from app.modules.platform.organizations.handlers import (
            on_organization_created,
            on_organization_deleted,
            on_organization_updated,
        )

        subscribe("organization.created.v1", on_organization_created)
        subscribe("organization.updated.v1", on_organization_updated)
        subscribe("organization.deleted.v1", on_organization_deleted)
