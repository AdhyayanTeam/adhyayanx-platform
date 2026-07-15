"""Register API routes on the FastAPI application.

Uses ApiModule manifests for transport-level route registration.
"""

from fastapi import FastAPI

from app.kernel.config.loader import Settings


def register_routers(app: FastAPI, settings: Settings) -> None:
    from app.api.routers.health import router as health_router
    from app.modules.platform.identity.api import IdentityApi
    from app.modules.platform.organizations.api import OrganizationApi

    app.include_router(health_router)

    api_modules = [
        IdentityApi(),
        OrganizationApi(),
    ]
    for module in api_modules:
        module.register_routes(app, settings.api_prefix)
