from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    lifecycle_state: str
    version: int
    created_at: datetime
    updated_at: datetime


class OrganizationCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")


class OrganizationUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")


class OrganizationListResponse(BaseModel):
    items: list[OrganizationResponse]
    total: int
