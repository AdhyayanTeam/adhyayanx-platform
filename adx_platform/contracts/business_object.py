from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BusinessObject(BaseModel, ABC):
    id: UUID = Field(default_factory=uuid4)
    organization_id: UUID
    workspace_id: UUID
    tenant_id: UUID
    lifecycle_state: str = "active"
    version: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def apply(self) -> None:
        self.version += 1
        self.updated_at = datetime.now(UTC)

    @abstractmethod
    def validate_invariants(self) -> bool: ...
