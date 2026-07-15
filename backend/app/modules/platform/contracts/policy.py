"""Reactive rule: when X happens, ensure Y.

Purpose:
    Decouples side effects from command handlers. A policy watches
    for events and decides what to do next, without the original
    handler knowing about downstream consequences.

Responsibilities:
    - Evaluate whether an action should proceed
    - Return an allowed/denied result with a reason

Does NOT do:
    - Persist changes (handlers do that)
    - Route events (the event bus does that)

Who depends on this:
    Event handlers evaluate policies before executing side effects.
    For example: "when user signs up, check if org limit is reached."
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class PolicyResult(BaseModel):
    allowed: bool
    reason: str | None = None


class Policy(ABC):
    name: str

    @abstractmethod
    async def evaluate(self, context: dict[str, Any]) -> PolicyResult: ...
