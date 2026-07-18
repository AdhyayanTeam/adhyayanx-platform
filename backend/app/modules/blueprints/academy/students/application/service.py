from dataclasses import dataclass
from typing import Protocol, Any
from uuid import UUID, uuid4
from datetime import datetime, UTC

from app.infrastructure.postgres.database import Database
from app.modules.blueprints.academy.students.domain.models import Student

@dataclass(frozen=True)
class CreateStudentCommand:
    organization_id: UUID
    name: str
    email: str
    phone: str | None = None

class StudentRepository(Protocol):
    async def save(self, student: Student) -> None:
        ...

    async def get(self, organization_id: UUID, student_id: UUID) -> Student | None:
        ...

class StudentRepositoryFactory(Protocol):
    def __call__(self, session: Any) -> StudentRepository:
        ...

class StudentService:
    def __init__(self, db: Database, repo_factory: StudentRepositoryFactory) -> None:
        self._db = db
        self._repo_factory = repo_factory

    async def create_student(self, cmd: CreateStudentCommand) -> UUID:
        now = datetime.now(UTC)
        student = Student(
            id=uuid4(),
            organization_id=cmd.organization_id,
            name=cmd.name,
            email=cmd.email,
            phone=cmd.phone,
            created_at=now,
            updated_at=now,
        )
        async with self._db.session() as session:
            repo = self._repo_factory(session)
            await repo.save(student)
        return student.id
