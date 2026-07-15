"""Something that happened in the domain.

Purpose:
    Records a fact that other parts of the system may react to.
    Events are published after state changes, never before.

Responsibilities:
    - Carry a unique event_id for deduplication
    - Declare event_type and aggregate_id for routing
    - Carry the data that downstream handlers need

Does NOT do:
    - Trigger its own processing (the event bus does that)
    - Roll back on failure (events are fire-and-forget from the publisher)

Who depends on this:
    Services publish events after successful state changes.
    Event handlers subscribe to event types to trigger side effects
    (send emails, update read models, notify external systems).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    aggregate_id: UUID
    aggregate_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    data: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    version: int = 1
