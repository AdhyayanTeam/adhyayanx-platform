from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from app.foundation.exceptions.base import ValidationError


class CourseLifecycleState(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Course:
    id: UUID
    organization_id: UUID
    title: str
    description: str | None
    lifecycle_state: CourseLifecycleState

    def publish(self) -> None:
        if self.lifecycle_state != CourseLifecycleState.DRAFT:
            raise ValidationError("Only draft courses can be published.")
        self.lifecycle_state = CourseLifecycleState.PUBLISHED

    def archive(self) -> None:
        if self.lifecycle_state == CourseLifecycleState.ARCHIVED:
            raise ValidationError("Course is already archived.")
        self.lifecycle_state = CourseLifecycleState.ARCHIVED
