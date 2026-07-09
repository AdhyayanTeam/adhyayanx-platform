from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    aggregate_id: UUID
    aggregate_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    data: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
    version: int = 1
