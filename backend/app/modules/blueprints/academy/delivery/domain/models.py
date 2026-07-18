from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Batch:
    id: UUID
    organization_id: UUID
    course_id: UUID
    name: str
    start_date: datetime | None
    created_at: datetime
    updated_at: datetime
