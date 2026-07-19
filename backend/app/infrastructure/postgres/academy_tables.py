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


class StudentTable(Base):
    __tablename__ = "academy_students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    email = Column(String(320), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class BatchTable(Base):
    __tablename__ = "academy_batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_courses.id"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class EnrollmentTable(Base):
    __tablename__ = "academy_enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_students.id"),
        nullable=False,
        index=True,
    )
    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_courses.id"),
        nullable=False,
        index=True,
    )
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class BatchAssignmentTable(Base):
    __tablename__ = "academy_batch_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    enrollment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_enrollments.id"),
        nullable=False,
        index=True,
    )
    batch_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_batches.id"),
        nullable=False,
        index=True,
    )
    assigned_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    ended_at = Column(DateTime(timezone=True), nullable=True)


class SessionTable(Base):
    __tablename__ = "academy_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    batch_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_batches.id"),
        nullable=False,
        index=True,
    )
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False, default="scheduled")
    attendance_submitted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class AttendanceRecordTable(Base):
    __tablename__ = "academy_attendance_records"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_sessions.id"),
        primary_key=True,
    )
    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academy_students.id"),
        primary_key=True,
    )
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
