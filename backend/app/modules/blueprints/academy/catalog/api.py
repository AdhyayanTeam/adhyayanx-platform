from __future__ import annotations

from typing import TYPE_CHECKING

from app.modules.platform.contracts.module import ApiModule

if TYPE_CHECKING:
    from fastapi import FastAPI


class AcademyCatalogApi(ApiModule):
    def register_routes(self, app: FastAPI, prefix: str) -> None:
        from app.modules.blueprints.academy.catalog.api.router import router as catalog_router

        # Typically blueprints have a blueprint prefix like /academy, so we prepend it.
        app.include_router(catalog_router, prefix=f"{prefix}/academy")
