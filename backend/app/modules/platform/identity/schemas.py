from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: UUID
    organization_id: UUID
    email: str
    name: str
    is_verified: bool = False
    lifecycle_state: str
    auth_provider: str
    version: int
    created_at: datetime
    updated_at: datetime


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    lifecycle_state: str
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


# Auth schemas


class SignupRequest(BaseModel):
    organization_name: str = Field(..., min_length=1, max_length=255)
    blueprint_code: str = Field(..., min_length=1, max_length=50)
    owner_name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8, max_length=128)


class SignupResponse(BaseModel):
    organization: OrganizationResponse
    user: UserResponse
    verification_email_sent: bool
    message: str


class LoginRequest(BaseModel):
    email: str
    password: str
    device_name: str | None = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    organization: OrganizationResponse
    landing_url: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str | None = None


class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class VerifyEmailRequest(BaseModel):
    token: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class MeResponse(BaseModel):
    user: UserResponse
    organization: OrganizationResponse
    subscriptions: list[dict[str, Any]]
    roles: list[str]


class ErrorResponse(BaseModel):
    detail: str
