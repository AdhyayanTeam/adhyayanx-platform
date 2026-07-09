from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: UUID
    organization_id: UUID
    email: str
    name: str
    lifecycle_state: str
    auth_provider: str
    version: int
    created_at: datetime
    updated_at: datetime


class CreateUserRequest(BaseModel):
    organization_id: UUID
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    name: str = Field(..., min_length=1, max_length=255)
    auth_provider: str = Field(default="email")
    auth_provider_id: str | None = None


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
