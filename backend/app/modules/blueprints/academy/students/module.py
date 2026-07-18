from __future__ import annotations
from typing import TYPE_CHECKING, Any

from app.modules.platform.contracts.module import PlatformModule

if TYPE_CHECKING:
    from app.kernel.container import Container

class AcademyStudentsModule(PlatformModule):
    name = "academy.students"

    def configure(self, container: Container) -> None:
        from app.modules.blueprints.academy.students.application.service import (
            StudentRepositoryFactory,
            StudentService,
        )
        from app.modules.blueprints.academy.students.contracts.student_query import StudentQueryContract
        from app.modules.blueprints.academy.students.application.query_service import PostgresStudentQueryService

        def _repo_factory(session: Any) -> Any:
            from app.modules.blueprints.academy.students.infrastructure.postgres_repository import (
                PostgresStudentRepository,
            )
            return PostgresStudentRepository(session)

        container.register_instance(StudentRepositoryFactory, _repo_factory)
        container.register(StudentService, StudentService)
        container.register(StudentQueryContract, PostgresStudentQueryService)

    def register_handlers(self, subscribe: Any) -> None:
        pass
