from typing import Protocol
from uuid import UUID

from app.modules.blueprints.academy.delivery.domain.models import Session

class SessionRepository(Protocol):
    async def save(self, session_entity: Session) -> None:
        ...
    async def get(self, organization_id: UUID, session_id: UUID) -> Session | None:
        ...
    async def get_by_id(self, session_id: UUID) -> Session | None:
        ...
