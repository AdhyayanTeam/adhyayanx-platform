"""Event outbox constants."""

from enum import StrEnum

OUTBOX_MAX_RETRIES = 5
OUTBOX_POLL_INTERVAL_SECONDS = 0.1


class OutboxStatus(StrEnum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
    DEAD = "dead"
