from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Student:
    id: UUID
    organization_id: UUID
    name: str
    email: str
    phone: str | None
    created_at: datetime
    updated_at: datetime
