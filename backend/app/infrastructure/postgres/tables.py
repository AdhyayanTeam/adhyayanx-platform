"""SQLAlchemy table definitions for the ADX adx_platform."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class OrganizationTable(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    timezone = Column(String(50), nullable=False, default="UTC")
    lifecycle_state = Column(String(50), nullable=False, default="active")
    version = Column(Integer, nullable=False, default=1)
    extra = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class UserTable(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    lifecycle_state = Column(String(50), nullable=False, default="active")
    auth_provider = Column(String(50), nullable=False, default="email")
    auth_provider_id = Column(String(255), nullable=True)
    version = Column(Integer, nullable=False, default=1)
    extra = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class OrganizationRoleTable(Base):
    __tablename__ = "organization_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    name = Column(String(100), nullable=False)
    permissions = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))


class MembershipTable(Base):
    __tablename__ = "memberships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    role_id = Column(UUID(as_uuid=True), ForeignKey("organization_roles.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))


class SessionTable(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    refresh_token_hash = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_name = Column(String(255), nullable=True)
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    revoked_at = Column(DateTime(timezone=True), nullable=True)


class EmailVerificationTokenTable(Base):
    __tablename__ = "email_verification_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False)
    purpose = Column(String(50), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    used_at = Column(DateTime(timezone=True), nullable=True)


class OrganizationSubscriptionTable(Base):
    __tablename__ = "organization_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    blueprint_code = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="active")
    starts_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    ends_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))


class OutboxTable(Base):
    __tablename__ = "event_outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_type = Column(String(255), nullable=False)
    aggregate_type = Column(String(255), nullable=False)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False)
    data = Column(JSON, nullable=False)
    extra = Column(JSON, nullable=False)
    status = Column(String(20), nullable=False, default="pending", index=True)
    retry_count = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=5)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    processed_at = Column(DateTime(timezone=True), nullable=True)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)


class ProcessedEventTable(Base):
    __tablename__ = "processed_events"

    event_id = Column(UUID(as_uuid=True), primary_key=True)
    processed_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
