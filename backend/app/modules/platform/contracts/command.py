"""Immutable intent to change system state.

Purpose:
    Encodes what the caller wants to happen. Every command targets
    exactly one aggregate and is processed by exactly one handler.

Responsibilities:
    - Carry a unique command_id for idempotency
    - Declare command_type for routing and audit
    - Carry the data needed to execute the change

Does NOT do:
    - Validate business rules (handlers do that)
    - Persist changes (repositories do that)
    - Produce side effects (services coordinate that)

Who depends on this:
    Every service method accepts a Command subclass as input.
    Routers create commands from HTTP requests.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Command(BaseModel):
    command_id: UUID = Field(default_factory=uuid4)
    command_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    data: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    version: int = 1
