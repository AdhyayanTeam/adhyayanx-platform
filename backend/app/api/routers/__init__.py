from fastapi import FastAPI

from app.kernel.config.loader import Settings


def register_routers(app: FastAPI, settings: Settings) -> None:
    from app.modules.platform.identity.router import router as identity_router
    from app.modules.platform.organizations.router import router as organizations_router

    app.include_router(organizations_router, prefix=settings.api_prefix)
    app.include_router(identity_router, prefix=settings.api_prefix)
