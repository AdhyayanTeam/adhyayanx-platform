"""SQLAlchemy table definitions for the Academy blueprint."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.postgres.tables import Base


class CourseTable(Base):
    __tablename__ = "academy_courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    lifecycle_state = Column(String(50), nullable=False, default="draft")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
