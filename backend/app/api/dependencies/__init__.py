from typing import Any, cast

from fastapi import Header, HTTPException, Request, status

from app.foundation.exceptions.base import ValidationError


async def get_current_user(
    _request: Request,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]

    container = _request.app.state.container

    # We must lazily resolve AuthService to avoid circular dependencies during setup
    from app.modules.platform.identity.auth_service import AuthService

    auth_service = container.resolve(AuthService)

    try:
        current_user = await auth_service.get_current_user(token)
        return cast(dict[str, Any], current_user)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
