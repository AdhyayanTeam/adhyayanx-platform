from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.foundation.exceptions.base import (
    ADXError,
    AggregateNotFoundError,
    AuthorizationError,
    ConcurrentModificationError,
    ValidationError,
)

logger = logging.getLogger("app.api")


ERROR_MAP: dict[type[ADXError], tuple[int, str]] = {
    ValidationError: (422, "UNPROCESSABLE_ENTITY"),
    AuthorizationError: (403, "FORBIDDEN"),
    AggregateNotFoundError: (404, "NOT_FOUND"),
    ConcurrentModificationError: (409, "CONFLICT"),
}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ADXError)
    async def adx_error_handler(request: Request, exc: ADXError) -> JSONResponse:
        status_code, code = ERROR_MAP.get(type(exc), (500, "INTERNAL_ERROR"))
        logger.warning("ADXError: %s - %s", code, str(exc))
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {"code": code, "message": str(exc)},
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
            },
        )
