from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.api.dependencies import get_current_user
from app.modules.blueprints.academy.catalog.application.commands import (
    ArchiveCourseCommand,
    CreateCourseCommand,
    PublishCourseCommand,
)
from app.modules.blueprints.academy.catalog.application.service import CatalogService

router = APIRouter(prefix="/catalog", tags=["academy-catalog"])


def get_catalog_service(request: Request) -> CatalogService:
    container = request.app.state.container
    return container.resolve(CatalogService)


class CreateCourseRequest(BaseModel):
    title: str
    description: str | None = None


class CourseResponse(BaseModel):
    id: UUID
    organization_id: UUID
    title: str
    description: str | None
    lifecycle_state: str


@router.post("/courses", response_model=CourseResponse)
async def create_course(
    request: CreateCourseRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> Any:
    return await service.create_course(
        command=CreateCourseCommand(title=request.title, description=request.description),
        organization_id=current_user["organization"]["id"],
        roles=current_user.get("roles", []),
    )


@router.get("/courses", response_model=list[CourseResponse])
async def list_courses(
    current_user: dict[str, Any] = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> Any:
    return await service.list_courses(
        organization_id=current_user["organization"]["id"],
    )


@router.post("/courses/{course_id}/publish", response_model=CourseResponse)
async def publish_course(
    course_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> Any:
    return await service.publish_course(
        command=PublishCourseCommand(course_id=course_id),
        organization_id=current_user["organization"]["id"],
        roles=current_user.get("roles", []),
    )


@router.post("/courses/{course_id}/archive", response_model=CourseResponse)
async def archive_course(
    course_id: UUID,
    current_user: dict[str, Any] = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> Any:
    return await service.archive_course(
        command=ArchiveCourseCommand(course_id=course_id),
        organization_id=current_user["organization"]["id"],
        roles=current_user.get("roles", []),
    )
