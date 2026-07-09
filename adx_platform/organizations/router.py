from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from adx_platform.organizations.commands import (
    CreateOrganizationCommand,
    DeleteOrganizationCommand,
    UpdateOrganizationCommand,
)
from adx_platform.organizations.schemas import (
    OrganizationCreateRequest,
    OrganizationListResponse,
    OrganizationResponse,
    OrganizationUpdateRequest,
)
from adx_platform.organizations.service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organizations"])


def get_service(request: Request) -> OrganizationService:
    return request.app.state.container.resolve(OrganizationService)


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    body: OrganizationCreateRequest,
    service: OrganizationService = Depends(get_service),
) -> dict:
    command = CreateOrganizationCommand(
        name=body.name,
        slug=body.slug,
        metadata={"source": "api"},
    )
    return await service.create(command)


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_service),
) -> dict:
    return await service.get(organization_id)


@router.patch("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: UUID,
    body: OrganizationUpdateRequest,
    service: OrganizationService = Depends(get_service),
) -> dict:
    command = UpdateOrganizationCommand(
        organization_id=organization_id,
        name=body.name,
        slug=body.slug,
        metadata={"source": "api"},
    )
    return await service.update(command)


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_service),
) -> None:
    command = DeleteOrganizationCommand(
        organization_id=organization_id,
        metadata={"source": "api"},
    )
    await service.delete(command)


@router.get("", response_model=OrganizationListResponse)
async def list_organizations(
    skip: int = 0,
    limit: int = 100,
    service: OrganizationService = Depends(get_service),
) -> dict:
    items = await service.list(skip=skip, limit=limit)
    return {"items": items, "total": len(items)}
