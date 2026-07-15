"""Domain-level base for all aggregates in the platform.

Purpose:
    Provides every aggregate with identity, lifecycle tracking,
    optimistic versioning, and an event-sourcing hook (apply).

Responsibilities:
    - Assign a UUID identity on creation
    - Track lifecycle state (active/inactive) and version for concurrency
    - Stamp created_at / updated_at automatically
    - Increment version and timestamp on apply()

Does NOT do:
    - Persist itself (repositories handle that)
    - Enforce business rules (subclasses override validate_invariants)
    - Publish events (that happens in services after apply)

Who depends on this:
    IdentityService, OrganizationService, and every future aggregate
    that needs versioning and lifecycle state.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.foundation.types import LifecycleState


class BusinessObject(BaseModel, ABC):
    id: UUID = Field(default_factory=uuid4)
    organization_id: UUID
    workspace_id: UUID
    tenant_id: UUID
    lifecycle_state: str = LifecycleState.ACTIVE
    version: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def apply(self) -> None:
        self.version += 1
        self.updated_at = datetime.now(UTC)

    @abstractmethod
    def validate_invariants(self) -> bool: ...
