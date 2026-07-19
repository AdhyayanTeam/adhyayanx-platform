from typing import Any
from app.modules.platform.contracts.module import PlatformModule
from app.kernel.container import Container

class AcademyAdmissionsModule(PlatformModule):
    name = "academy.admissions"

    def configure(self, container: Container) -> None:
        from app.modules.blueprints.academy.admissions.application.service import AdmissionsService
        from app.modules.blueprints.academy.admissions.application.queries import AdmissionsQueryService
        from app.modules.blueprints.academy.admissions.infrastructure.postgres_queries import PostgresAdmissionsQueryService
        from app.modules.blueprints.academy.admissions.infrastructure.unit_of_work import AdmissionsUnitOfWork
        from app.modules.blueprints.academy.admissions.infrastructure.postgres_uow import PostgresAdmissionsUnitOfWork

        container.register(AdmissionsUnitOfWork, PostgresAdmissionsUnitOfWork)
        container.register(AdmissionsService, AdmissionsService)
        container.register(AdmissionsQueryService, PostgresAdmissionsQueryService)

    def register_handlers(self, subscribe: Any) -> None:
        pass
