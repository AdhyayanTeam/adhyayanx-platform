"""Organizations API module.

Registers HTTP routes for organization management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.modules.platform.contracts.module import ApiModule

if TYPE_CHECKING:
    from fastapi import FastAPI


class OrganizationApi(ApiModule):
    def register_routes(self, app: FastAPI, prefix: str) -> None:
        from app.modules.platform.organizations.router import (
            router as organizations_router,
        )

        app.include_router(organizations_router, prefix=prefix)
