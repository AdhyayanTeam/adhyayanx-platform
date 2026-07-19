from __future__ import annotations
from typing import TYPE_CHECKING, Any

from app.modules.platform.contracts.module import PlatformModule

if TYPE_CHECKING:
    from app.kernel.container import Container

class AcademyEnrollmentModule(PlatformModule):
    name = "academy.enrollment"

    def configure(self, container: Container) -> None:
        from app.modules.blueprints.academy.enrollment.application.service import (
            EnrollmentRepositoryFactory,
            EnrollmentService,
        )
        # Import the contracts implemented in other modules to inject them
        from app.modules.blueprints.academy.catalog.contracts.course_query import CourseQueryContract
        from app.modules.blueprints.academy.students.contracts.student_query import StudentQueryContract
        from app.modules.blueprints.academy.delivery.contracts.batch_query import BatchQueryContract

        def _repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.enrollment.infrastructure.postgres_repository import (
                PostgresEnrollmentRepository,
            )
            return PostgresEnrollmentRepository(session)

        container.register_instance(EnrollmentRepositoryFactory, _repo_factory)
        container.register(EnrollmentService, EnrollmentService)

        from app.modules.blueprints.academy.enrollment.application.queries import EnrollmentQueryService
        from app.modules.blueprints.academy.enrollment.infrastructure.postgres_queries import PostgresEnrollmentQueryService
        container.register(EnrollmentQueryService, PostgresEnrollmentQueryService)

    def register_handlers(self, subscribe: Any) -> None:
        pass
