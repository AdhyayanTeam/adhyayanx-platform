from __future__ import annotations

from typing import TYPE_CHECKING

from app.modules.platform.contracts.module import ApiModule

if TYPE_CHECKING:
    from fastapi import FastAPI

class AcademyEnrollmentApi(ApiModule):
    def register_routes(self, app: FastAPI, prefix: str) -> None:
        from app.modules.blueprints.academy.enrollment.api.router import router, students_router
        app.include_router(router, prefix=f"{prefix}/academy")
        app.include_router(students_router, prefix=f"{prefix}/academy")
