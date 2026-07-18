from dataclasses import dataclass
from typing import Protocol, Any
from uuid import UUID, uuid4
from datetime import datetime, UTC

from app.infrastructure.postgres.database import Database
from app.modules.blueprints.academy.delivery.domain.models import Batch

@dataclass(frozen=True)
class CreateBatchCommand:
    organization_id: UUID
    course_id: UUID
    name: str
    start_date: datetime | None = None

class BatchRepository(Protocol):
    async def save(self, batch: Batch) -> None:
        ...

    async def get(self, organization_id: UUID, batch_id: UUID) -> Batch | None:
        ...

class BatchRepositoryFactory(Protocol):
    def __call__(self, session: Any) -> BatchRepository:
        ...

class BatchService:
    def __init__(self, db: Database, repo_factory: BatchRepositoryFactory) -> None:
        self._db = db
        self._repo_factory = repo_factory

    async def create_batch(self, cmd: CreateBatchCommand) -> UUID:
        now = datetime.now(UTC)
        batch = Batch(
            id=uuid4(),
            organization_id=cmd.organization_id,
            course_id=cmd.course_id,
            name=cmd.name,
            start_date=cmd.start_date,
            created_at=now,
            updated_at=now,
        )
        async with self._db.session() as session:
            repo = self._repo_factory(session)
            await repo.save(batch)
        return batch.id
