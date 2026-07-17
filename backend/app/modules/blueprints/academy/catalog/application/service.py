from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from app.foundation.exceptions.base import AuthorizationError, ValidationError
from app.modules.blueprints.academy.catalog.application.commands import (
    ArchiveCourseCommand,
    CreateCourseCommand,
    PublishCourseCommand,
)
from app.modules.blueprints.academy.catalog.domain.events import (
    CourseArchived,
    CourseCreated,
    CoursePublished,
)
from app.modules.blueprints.academy.catalog.domain.models import Course, CourseLifecycleState

if TYPE_CHECKING:
    from app.infrastructure.postgres.database import Database
    from app.modules.blueprints.academy.catalog.infrastructure.ports.catalog_repository import (
        CatalogRepository,
    )
    from app.modules.platform.events.publisher import Publisher

logger = logging.getLogger("app.modules.blueprints.academy.catalog.application.service")


class CatalogRepositoryFactory:
    def __call__(self, session: Any) -> CatalogRepository:
        raise NotImplementedError


class CatalogService:
    def __init__(
        self,
        database: Database,
        publisher: Publisher,
        repo_factory: CatalogRepositoryFactory | None = None,
    ) -> None:
        self._db = database
        self._publisher = publisher
        self._repo_factory = repo_factory

    def _make_repo(self, session: Any) -> CatalogRepository:
        if self._repo_factory is None:
            raise RuntimeError("CatalogService requires repo_factory")
        return self._repo_factory(session)

    def _require_admin(self, roles: list[str]) -> None:
        if "owner" not in roles and "admin" not in roles:
            raise AuthorizationError("Only owners and admins can manage courses.")

    async def create_course(
        self, command: CreateCourseCommand, organization_id: UUID, roles: list[str]
    ) -> dict[str, Any]:
        self._require_admin(roles)

        course = Course(
            id=uuid4(),
            organization_id=organization_id,
            title=command.title,
            description=command.description,
            lifecycle_state=CourseLifecycleState.DRAFT,
        )

        async with self._db.session() as session:
            repo = self._make_repo(session)

            course_dict = {
                "id": course.id,
                "organization_id": course.organization_id,
                "title": course.title,
                "description": course.description,
                "lifecycle_state": course.lifecycle_state.value,
            }
            await repo.save(course_dict)

            await self._publisher.publish(
                CourseCreated(
                    aggregate_type="academy.course",
                    aggregate_id=course.id,
                    course_id=str(course.id),
                    organization_id=str(course.organization_id),
                    title=course.title,
                ),
                session,
            )

        logger.info("Course created: %s in org %s", course.id, organization_id)
        return course_dict

    async def list_courses(self, organization_id: UUID) -> list[dict[str, Any]]:
        async with self._db.session() as session:
            repo = self._make_repo(session)
            return await repo.list(organization_id=organization_id)

    async def publish_course(
        self, command: PublishCourseCommand, organization_id: UUID, roles: list[str]
    ) -> dict[str, Any]:
        self._require_admin(roles)

        async with self._db.session() as session:
            repo = self._make_repo(session)
            course_data = await repo.load(command.course_id, organization_id)
            if not course_data:
                raise ValidationError("Course not found.")

            course = Course(
                id=course_data["id"],
                organization_id=course_data["organization_id"],
                title=course_data["title"],
                description=course_data["description"],
                lifecycle_state=CourseLifecycleState(course_data["lifecycle_state"]),
            )

            course.publish()
            course_data["lifecycle_state"] = course.lifecycle_state.value
            await repo.save(course_data)

            await self._publisher.publish(
                CoursePublished(
                    aggregate_type="academy.course",
                    aggregate_id=course.id,
                    course_id=str(course.id),
                    organization_id=str(course.organization_id),
                ),
                session,
            )

        logger.info("Course published: %s in org %s", course.id, organization_id)
        return course_data

    async def archive_course(
        self, command: ArchiveCourseCommand, organization_id: UUID, roles: list[str]
    ) -> dict[str, Any]:
        self._require_admin(roles)

        async with self._db.session() as session:
            repo = self._make_repo(session)
            course_data = await repo.load(command.course_id, organization_id)
            if not course_data:
                raise ValidationError("Course not found.")

            course = Course(
                id=course_data["id"],
                organization_id=course_data["organization_id"],
                title=course_data["title"],
                description=course_data["description"],
                lifecycle_state=CourseLifecycleState(course_data["lifecycle_state"]),
            )

            course.archive()
            course_data["lifecycle_state"] = course.lifecycle_state.value
            await repo.save(course_data)

            await self._publisher.publish(
                CourseArchived(
                    aggregate_type="academy.course",
                    aggregate_id=course.id,
                    course_id=str(course.id),
                    organization_id=str(course.organization_id),
                ),
                session,
            )

        logger.info("Course archived: %s in org %s", course.id, organization_id)
        return course_data
