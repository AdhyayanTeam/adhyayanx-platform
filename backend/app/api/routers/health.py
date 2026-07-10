from __future__ import annotations

from fastapi import APIRouter, Request
from sqlalchemy import text

from app.infrastructure.postgres.database import Database
from app.kernel.config.loader import Settings

router = APIRouter(tags=["health"])


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(request: Request) -> dict[str, str]:
    container = request.app.state.container
    settings = container.resolve(Settings)
    db = Database(settings)
    try:
        async with db.session() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "error", "database": "disconnected"}
