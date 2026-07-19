from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.foundation.exceptions.base import (
    ADXError,
    AggregateNotFoundError,
    AuthorizationError,
    ConcurrentModificationError,
    ConflictError,
    ValidationError,
)

logger = logging.getLogger("app.api")


ERROR_MAP: dict[type[ADXError], tuple[int, str]] = {
    ValidationError: (422, "UNPROCESSABLE_ENTITY"),
    AuthorizationError: (403, "FORBIDDEN"),
    AggregateNotFoundError: (404, "NOT_FOUND"),
    ConflictError: (409, "CONFLICT"),
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

    from fastapi.exceptions import RequestValidationError
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        with open("/home/mrigesh/Desktop/Khazana/ADX/adhyayanx-platform/backend/error.log", "a") as f:
            f.write(f"422 Error at {request.url}:\n")
            f.write(str(exc.errors()) + "\n")
            f.write(f"Body: {exc.body}\n")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        import traceback
        with open("/home/mrigesh/Desktop/Khazana/ADX/adhyayanx-platform/backend/error.log", "a") as f:
            f.write(traceback.format_exc())
            f.write("\n")
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
            },
        )
