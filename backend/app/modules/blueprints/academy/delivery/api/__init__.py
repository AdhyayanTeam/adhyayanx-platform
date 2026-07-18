from __future__ import annotations

from typing import TYPE_CHECKING

from app.modules.platform.contracts.module import ApiModule

if TYPE_CHECKING:
    from fastapi import FastAPI

class AcademyDeliveryApi(ApiModule):
    def register_routes(self, app: FastAPI, prefix: str) -> None:
        from app.modules.blueprints.academy.delivery.api.router import router, sessions_router
        app.include_router(router, prefix=f"{prefix}/academy")
        app.include_router(sessions_router, prefix=f"{prefix}/academy")
