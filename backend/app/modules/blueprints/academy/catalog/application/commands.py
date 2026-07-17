from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateCourseCommand:
    title: str
    description: str | None


@dataclass
class PublishCourseCommand:
    course_id: UUID


@dataclass
class ArchiveCourseCommand:
    course_id: UUID
