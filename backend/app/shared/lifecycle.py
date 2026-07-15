"""Lifecycle state enumeration for domain entities."""

from enum import StrEnum


class LifecycleState(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
