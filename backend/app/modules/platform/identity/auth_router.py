"""Authentication endpoints — signup, login, refresh, logout, verify, reset.

Purpose:
    Translates HTTP requests into Commands and delegates to AuthService.
    This is the thinnest layer — no business logic, just request parsing.

Does NOT do:
    - Validate passwords (PasswordPolicy handles that)
    - Issue tokens (TokenService handles that)
    - Send emails (EmailService handles that)

Who depends on this:
    FastAPI mounts this router at /api/v1/auth.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status

from app.kernel.config.loader import Settings
from app.kernel.container import Container
from app.modules.platform.identity.commands import (
    LoginCommand,
    SignupCommand,
    VerifyEmailCommand,
)
from app.modules.platform.identity.schemas import (
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    MeResponse,
    ResetPasswordRequest,
    SignupRequest,
    SignupResponse,
    TokenRefreshResponse,
    VerifyEmailRequest,
)

if TYPE_CHECKING:
    from app.modules.platform.identity.auth_service import AuthService

_REFRESH_COOKIE = "refresh_token"


def _get_settings(request: Request) -> Settings:
    container: Container = request.app.state.container
    return container.resolve(Settings)


def _get_service(request: Request) -> AuthService:
    from app.modules.platform.identity.auth_service import AuthService

    container: Container = request.app.state.container
    return container.resolve(AuthService)


def _set_refresh_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        key=_REFRESH_COOKIE,
        value=token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.jwt_refresh_token_expire_days * 24 * 3600,
        path="/",
    )


def _clear_refresh_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=_REFRESH_COOKIE,
        path="/",
    )


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: SignupRequest,
    request: Request,
    service: AuthService = Depends(_get_service),
) -> dict[str, Any]:
    command = SignupCommand(
        organization_name=body.organization_name,
        blueprint_code=body.blueprint_code,
        owner_name=body.owner_name,
        email=body.email,
        password=body.password,
        metadata={"source": "api"},
    )
    result = await service.signup(command)
    return {
        "organization": result["organization"],
        "user": result["user"],
        "verification_email_sent": result["verification_email_sent"],
        "message": result["message"],
    }


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    service: AuthService = Depends(_get_service),
    settings: Settings = Depends(_get_settings),
) -> dict[str, Any]:
    command = LoginCommand(
        email=body.email,
        password=body.password,
        device_name=body.device_name,
        ip_address=request.client.host if request.client else "",
        user_agent=request.headers.get("user-agent", ""),
        metadata={"source": "api"},
    )
    result = await service.login(command)
    _set_refresh_cookie(response, result["refresh_token"], settings)
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user": result["user"],
        "organization": result["organization"],
        "landing_url": result["landing_url"],
    }


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=_REFRESH_COOKIE),
    service: AuthService = Depends(_get_service),
    settings: Settings = Depends(_get_settings),
) -> dict[str, Any]:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )
    result = await service.refresh(refresh_token)
    _set_refresh_cookie(response, refresh_token, settings)
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=_REFRESH_COOKIE),
    service: AuthService = Depends(_get_service),
    settings: Settings = Depends(_get_settings),
) -> None:
    if refresh_token:
        await service.logout(refresh_token)
    _clear_refresh_cookie(response, settings)


@router.post("/verify-email")
async def verify_email(
    body: VerifyEmailRequest,
    service: AuthService = Depends(_get_service),
) -> Any:
    command = VerifyEmailCommand(token=body.token)
    return await service.verify_email(command)


@router.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest,
    service: AuthService = Depends(_get_service),
) -> Any:
    return await service.forgot_password(body.email)


@router.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest,
    service: AuthService = Depends(_get_service),
) -> Any:
    from app.modules.platform.identity.commands import ResetPasswordCommand as RPCmd

    command = RPCmd(token=body.token, new_password=body.new_password)
    return await service.reset_password(command)


@router.get("/me", response_model=MeResponse)
async def get_me(
    request: Request,
    service: AuthService = Depends(_get_service),
) -> Any:
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )
    access_token = auth_header.removeprefix("Bearer ")
    return await service.get_current_user(access_token)
