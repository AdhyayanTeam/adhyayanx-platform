"""ADX Platform API entry point."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware.error_handler import register_error_handlers
from app.api.middleware.logging import LoggingMiddleware
from app.api.routers import register_routers
from app.kernel.bootstrap import Bootstrap
from app.kernel.config.loader import Settings

if TYPE_CHECKING:
    from app.modules.platform.notifications.email_service import EmailService


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(format="%(message)s", level=getattr(logging, settings.log_level.upper()))

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url=f"{settings.api_prefix}/docs",
        openapi_url=f"{settings.api_prefix}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)

    register_error_handlers(app)
    register_routers(app, settings)

    bootstrap = Bootstrap(settings)
    bootstrap.configure()
    app.state.container = bootstrap.container

    email_service = _build_email_service(settings)
    from app.modules.platform.identity.auth_service import AuthService
    auth_service = bootstrap.container.resolve(AuthService)
    auth_service.set_email_service(email_service)

    return app


def _build_email_service(settings: Settings) -> EmailService:
    provider = settings.email_provider
    if provider == "resend":
        from app.modules.platform.notifications.resend_provider import (
            ResendEmailProvider,
        )
        return ResendEmailProvider(
            api_key=settings.resend_api_key,
            from_address=settings.email_from_address,
        )
    from app.modules.platform.notifications.console_provider import (
        ConsoleEmailProvider,
    )
    return ConsoleEmailProvider()


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
