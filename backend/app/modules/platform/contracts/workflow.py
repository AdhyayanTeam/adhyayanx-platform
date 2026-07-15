"""Multi-step process with compensation.

Purpose:
    Models long-running business processes that span multiple steps,
    where each step can be compensated (undone) if a later step fails.

Responsibilities:
    - Define states, transitions, and steps for a workflow
    - Execute steps in order, compensating on failure

Does NOT do:
    - Handle persistence (the workflow engine does that)
    - Route events (the event bus does that)

Who depends on this:
    Future: enrollment workflows, fee payment plans, batch transitions.
    Not actively used yet — placeholder for Sprint 3+.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class StateDefinition(BaseModel):
    name: str
    on_enter: list[str] | None = None
    on_exit: list[str] | None = None


class WorkflowDefinition(BaseModel):
    id: UUID
    name: str
    version: str
    initial_state: str
    states: dict[str, StateDefinition]
    transitions: dict[str, list[str]]


class WorkflowInstance(BaseModel):
    id: UUID
    definition_id: UUID
    aggregate_id: UUID
    current_state: str
    data: dict[str, Any]


class StepResult(BaseModel):
    success: bool
    data: dict[str, Any] = {}
    error: str | None = None


class WorkflowContext(BaseModel):
    instance: WorkflowInstance
    definition: WorkflowDefinition
    data: dict[str, Any]


class WorkflowStep(ABC):
    step_name: str

    @abstractmethod
    async def execute(self, context: WorkflowContext) -> StepResult: ...

    @abstractmethod
    async def compensate(self, context: WorkflowContext) -> None: ...
