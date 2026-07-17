from __future__ import annotations

from app.modules.platform.contracts.event import DomainEvent


class CourseCreated(DomainEvent):
    event_type: str = "academy.course.created"
    course_id: str
    organization_id: str
    title: str


class CoursePublished(DomainEvent):
    event_type: str = "academy.course.published"
    course_id: str
    organization_id: str


class CourseArchived(DomainEvent):
    event_type: str = "academy.course.archived"
    course_id: str
    organization_id: str
