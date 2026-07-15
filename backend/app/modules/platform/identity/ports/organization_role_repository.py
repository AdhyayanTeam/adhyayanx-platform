"""Persistence interface for organization roles.

Purpose:
    Stores the roles defined within an organization (admin, member, viewer, etc.).
    Each role maps to a set of permissions.

Does NOT do:
    - Assign roles to users (MembershipRepository handles that)

Who depends on this:
    AuthService assigns the default 'owner' role during signup.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class OrganizationRoleRepository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> dict[str, Any] | None: ...

    @abstractmethod
    async def create(self, role: dict[str, Any]) -> None: ...

    @abstractmethod
    async def load_by_name_and_org(
        self, name: str, organization_id: UUID
    ) -> dict[str, Any] | None: ...

    @abstractmethod
    async def list_for_org(self, organization_id: UUID) -> list[dict[str, Any]]: ...
