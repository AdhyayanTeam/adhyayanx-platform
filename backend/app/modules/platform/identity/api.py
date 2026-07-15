"""Identity API module.

Registers HTTP routes for authentication and user management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.modules.platform.contracts.module import ApiModule

if TYPE_CHECKING:
    from fastapi import FastAPI


class IdentityApi(ApiModule):
    def register_routes(self, app: FastAPI, prefix: str) -> None:
        from app.modules.platform.identity.auth_router import router as auth_router
        from app.modules.platform.identity.router import router as identity_router

        app.include_router(auth_router, prefix=prefix)
        app.include_router(identity_router, prefix=prefix)
