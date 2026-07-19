from __future__ import annotations
from typing import TYPE_CHECKING
from app.modules.platform.contracts.module import ApiModule

if TYPE_CHECKING:
    from fastapi import FastAPI

class AcademyAdmissionsApi(ApiModule):
    def register_routes(self, app: FastAPI, prefix: str) -> None:
        from app.modules.blueprints.academy.admissions.api.router import router
        app.include_router(router, prefix=f"{prefix}/academy")
