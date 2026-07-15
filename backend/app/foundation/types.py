from datetime import datetime
from enum import StrEnum
from typing import TypeVar
from uuid import UUID

EntityId = UUID
Timestamp = datetime
Version = int

T = TypeVar("T")


class LifecycleState(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
