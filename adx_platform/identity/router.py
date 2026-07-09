from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from adx_platform.identity.commands import (
    CreateUserCommand,
    DeactivateUserCommand,
    ReactivateUserCommand,
)
from adx_platform.identity.schemas import (
    CreateUserRequest,
    UserListResponse,
    UserResponse,
)
from adx_platform.identity.service import IdentityService

router = APIRouter(prefix="/users", tags=["identity"])


def get_service(request: Request) -> IdentityService:
    return request.app.state.container.resolve(IdentityService)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserRequest,
    service: IdentityService = Depends(get_service),
) -> dict:
    command = CreateUserCommand(
        organization_id=body.organization_id,
        email=body.email,
        name=body.name,
        auth_provider=body.auth_provider,
        auth_provider_id=body.auth_provider_id,
        metadata={"source": "api"},
    )
    return await service.create_user(command)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    service: IdentityService = Depends(get_service),
) -> dict:
    return await service.get(user_id)


@router.get("/by-email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    service: IdentityService = Depends(get_service),
) -> dict:
    return await service.get_by_email(email)


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: UUID,
    service: IdentityService = Depends(get_service),
) -> dict:
    command = DeactivateUserCommand(
        organization_id=UUID(int=0),
        user_id=user_id,
        metadata={"source": "api"},
    )
    return await service.deactivate(command)


@router.post("/{user_id}/reactivate", response_model=UserResponse)
async def reactivate_user(
    user_id: UUID,
    service: IdentityService = Depends(get_service),
) -> dict:
    command = ReactivateUserCommand(
        organization_id=UUID(int=0),
        user_id=user_id,
        metadata={"source": "api"},
    )
    return await service.reactivate(command)


@router.get("", response_model=UserListResponse)
async def list_users(
    organization_id: UUID,
    skip: int = 0,
    limit: int = 100,
    service: IdentityService = Depends(get_service),
) -> dict:
    items = await service.list(organization_id, skip=skip, limit=limit)
    return {"items": items, "total": len(items)}
