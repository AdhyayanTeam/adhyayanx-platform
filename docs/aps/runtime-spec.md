# ADX Platform Runtime Specification

> Version 1.0
> Status: Draft
> Applies to: Backend Platform Runtime

---

## 1. Command Lifecycle

A command is the atomic unit of state change in ADX. Every mutation flows through this lifecycle.

### 1.1 Lifecycle Stages

```
┌──────────┐
│  Receive │  HTTP request → Router → Deserialize → Validate schema
└────┬─────┘
     ▼
┌──────────┐
│  Authorize │  Permission check against identity + capability
└────┬─────┘
     ▼
┌───────────┐
│  Validate  │  Business rule validation (policies, invariants)
└────┬─────┘
     ▼
┌───────────┐
│  Execute   │  Unit of Work (see §2)
│  + Outbox  │    - Load aggregate
│            │    - Apply command
│            │    - Raise domain events
│            │    - Persist aggregate
│            │    - Persist outbox entries
└────┬─────┘
     ▼
┌──────────┐
│  Commit   │  Transaction commits. Events are now durable.
└────┬─────┘
     ▼
┌────────────┐
│  Dispatch   │  Outbox dispatcher reads + publishes events (async)
└────────────┘
```

### 1.2 Command Contract

Every command MUST be a Pydantic model extending `adx_platform.contracts.command.Command`:

```python
class Command(BaseModel):
    command_id: UUID
    command_type: str        # Fully qualified: "adx_platform.organization.create.v1"
    timestamp: datetime
    data: dict               # Domain-specific payload
    metadata: dict           # correlation_id, causation_id, tenant_id, actor_id
    version: int = 1         # Schema version
```

### 1.3 Rules

| Rule | Enforcement |
|---|---|
| Commands are immutable | No mutation after construction |
| Commands carry correlation_id | Every command + event chain shares one correlation_id |
| Commands are validated before UoW | Schema validation → authorization → business rules |
| Commands never access infrastructure | DI of repositories only through ports |
| Commands are synchronous | Awaited by caller. Side effects are async through events. |

---

## 2. Unit of Work

The Unit of Work (UoW) ensures that aggregate changes and event outbox entries are persisted atomically.

### 2.1 Scope

```
async with unit_of_work() as uow:
    aggregate = await uow.repository.load(aggregate_id)
    aggregate.apply(command)
    await uow.repository.save(aggregate)
    await uow.outbox.append(aggregate.events)
    await uow.commit()
```

### 2.2 UoW Implementation Rules

| Concern | Rule |
|---|---|
| Transaction | PostgreSQL transaction. One UoW = one transaction. |
| Aggregate loading | Repository returns aggregate with version for optimistic locking. |
| Auto-flush on save | `repository.save()` stages changes. `uow.commit()` flushes all. |
| Outbox append | Events appended to outbox table within same transaction. |
| Rollback | Any exception within `uow` context → full rollback. |
| Nested UoW | Forbidden. One UoW per command. |

### 2.3 Concurrency

```python
# Optimistic locking via version field
class BusinessObject:
    id: UUID
    version: int  # Incremented on every save

    def apply(self, command: Command):
        # Mutate state
        self.version += 1

# SQL:
# UPDATE aggregates SET ... WHERE id = $1 AND version = $2
# If affected_rows == 0 → raise ConcurrentModificationError
```

---

## 3. Aggregate Rules

### 3.1 Definition

An aggregate is a cluster of domain objects treated as a single unit. Example: Organization aggregate contains Organization + Settings + BillingPlan.

### 3.2 Rules

| Rule | Rationale |
|---|---|
| One aggregate per transaction | Prevents distributed locking across aggregates |
| Aggregate boundary = consistency boundary | Within aggregate: strong consistency. Across: eventual. |
| Aggregate root is the only entry point | External access only through the root entity |
| Aggregate publishes events | Events raised by aggregate root method calls |
| Aggregate is versioned | Optimistic lock key. Incremented on every command. |

### 3.3 Loading

```python
class OrganizationRepository(ABC):
    @abstractmethod
    async def load(self, id: UUID) -> Organization: ...
    @abstractmethod
    async def save(self, organization: Organization) -> None: ...
```

Aggregates are loaded eagerly within the UoW. Lazy loading is forbidden — all required state is loaded at the UoW boundary.

---

## 4. Event Publication

### 4.1 Event Contract

```python
class DomainEvent(BaseModel):
    event_id: UUID
    event_type: str           # "organization.created.v1"
    aggregate_id: UUID
    aggregate_type: str       # "organization"
    timestamp: datetime
    data: dict
    metadata: dict            # correlation_id, causation_id, tenant_id, actor_id
    version: int = 1
```

### 4.2 Publication Flow

```
Aggregate.apply(command)
  → aggregate.raise_event(DomainEvent(...))
    → event appended to aggregate._events list

repository.save(aggregate)
  → aggregate._events extracted and cleared

uow.outbox.append(events)
  → outbox rows inserted in same transaction
```

### 4.3 Event Naming Convention

```
{dot.notation.event.type}.v{major_version}

Examples:
  organization.created.v1
  workspace.provisioned.v1
  student.enrolled.v1
```

Breaking changes increment the major version. Non-breaking additions only add fields with defaults.

---

## 5. Transaction Boundaries

### 5.1 Rules

| Context | Boundary |
|---|---|
| Single command | Wrapped in UoW. One aggregate. |
| Query | No transaction. Read-only. |
| Use case (cross-domain) | No transaction spanning multiple UoWs. Each command within the use case has its own UoW. |
| Event handler | Runs in its own UoW if it needs to write. Never shares a transaction with the publisher. |
| Outbox dispatcher | Reads outbox. Each event is processed independently. |

### 5.2 Example: Use Case Transaction Boundaries

```python
# usecases/create_workspace.py
class CreateWorkspaceUseCase:
    def __init__(self, org_repo, ws_repo, storage_repo, event_bus):
        ...

    async def execute(self, command: CreateWorkspaceCommand) -> WorkspaceResponse:
        # UoW 1: Create organization
        async with unit_of_work() as uow:
            org = Organization.create(command)
            await uow.org_repo.save(org)
            await uow.outbox.append(org.events)
            await uow.commit()

        # UoW 2: Provision workspace
        async with unit_of_work() as uow:
            ws = Workspace.create(command, org.id)
            await uow.ws_repo.save(ws)
            await uow.outbox.append(ws.events)
            await uow.commit()

        # UoW 3: Provision storage
        async with unit_of_work() as uow:
            storage = StorageProvisioning.create(ws.id)
            await uow.storage_repo.save(storage)
            await uow.outbox.append(storage.events)
            await uow.commit()

        return WorkspaceResponse(org_id=org.id, workspace_id=ws.id)
```

Each UoW commits independently. If UoW 3 fails, UoW 1 and 2 are NOT rolled back. Compensation events would be needed for multi-aggregate sagas.

---

## 6. Outbox Pattern

### 6.1 Outbox Table Schema

```sql
CREATE TABLE event_outbox (
    id              UUID PRIMARY KEY,
    event_type      VARCHAR(255) NOT NULL,
    aggregate_type  VARCHAR(255) NOT NULL,
    aggregate_id    UUID NOT NULL,
    data            JSONB NOT NULL,
    metadata        JSONB NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    retry_count     INT NOT NULL DEFAULT 0,
    max_retries     INT NOT NULL DEFAULT 5,
    last_error      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at    TIMESTAMPTZ,
    next_retry_at   TIMESTAMPTZ
);

CREATE INDEX idx_outbox_pending ON event_outbox (created_at)
    WHERE status = 'pending' AND next_retry_at IS NULL;

CREATE INDEX idx_outbox_retry ON event_outbox (next_retry_at)
    WHERE status = 'pending' AND next_retry_at IS NOT NULL
    ORDER BY next_retry_at;
```

### 6.2 Dispatcher

```python
# platform/events/ports/outbox_repository.py
class OutboxRepository(ABC):
    @abstractmethod
    async def fetch_next_batch(self, limit: int = 50) -> list[OutboxEntry]: ...
    @abstractmethod
    async def mark_processed(self, entry_id: UUID) -> None: ...
    @abstractmethod
    async def increment_retry(self, entry_id: UUID, error: str) -> None: ...
    @abstractmethod
    async def dead_letter(self, entry_id: UUID, error: str) -> None: ...

# infrastructure/postgres/outbox_dispatcher.py
class PostgresOutboxDispatcher:
    """
    Polls outbox table using FOR UPDATE SKIP LOCKED.
    Runs in its own background task in the API process.
    """
    POLL_INTERVAL = 0.1  # seconds

    async def start(self):
        while self._running:
            batch = await self.outbox_repo.fetch_next_batch(50)
            for entry in batch:
                asyncio.create_task(self.process(entry))
            await asyncio.sleep(self.POLL_INTERVAL)

    async def process(self, entry: OutboxEntry):
        try:
            handlers = self.registry.get(entry.event_type)
            await self.event_bus.publish(entry, handlers)
            await self.outbox_repo.mark_processed(entry.id)
        except Exception as e:
            await self.outbox_repo.increment_retry(entry.id, str(e))
            if entry.retry_count >= entry.max_retries:
                await self.outbox_repo.dead_letter(entry.id, str(e))
```

### 6.3 Concurrent Dispatchers

Multiple dispatchers can run safely using `FOR UPDATE SKIP LOCKED`. Each entry is locked by one dispatcher. This enables horizontal scaling of the dispatcher.

---

## 7. Retry Semantics

### 7.1 Outbox Delivery Retry

| Parameter | Value |
|---|---|
| Max retries | 5 |
| Backoff | Exponential: 1s, 2s, 4s, 8s, 16s |
| After max | Moved to dead letter queue (status = `dead_letter`) |
| Dead letter action | Logged with full event payload. Manual or automated replay. |

### 7.2 Subscriber Retry

| Scenario | Behavior |
|---|---|
| Transient error (DB timeout, network) | Retry within handler. Max 3 immediate retries with 100ms backoff. |
| Permanent error (invalid data, schema mismatch) | Log error. Do not retry. Notify dead letter. |
| Unhandled exception (bug) | Retry via outbox. If persistent, dead letter after 5 outbox retries. |

### 7.3 Idempotent Subscribers

Every subscriber MUST handle duplicate delivery. The outbox dispatcher delivers at-least-once — subscribers are responsible for deduplication.

```python
class ProcessedEventStore(ABC):
    @abstractmethod
    async def exists(self, event_id: UUID) -> bool: ...
    @abstractmethod
    async def record(self, event_id: UUID) -> None: ...

class OrganizationCreatedSubscriber:
    def __init__(self, processed_events: ProcessedEventStore):
        self.processed_events = processed_events

    async def handle(self, event: OrganizationCreated) -> None:
        if await self.processed_events.exists(event.event_id):
            return  # Already processed — idempotent
        # Business logic
        await self.processed_events.record(event.event_id)
```

---

## 8. Workflow Execution

### 8.1 Workflow Model

A workflow is a state machine with defined transitions and steps.

```python
class WorkflowDefinition(BaseModel):
    id: UUID
    name: str
    version: str
    initial_state: str
    states: dict[str, StateDefinition]
    transitions: dict[str, list[str]]  # "current_state" → ["next_state", ...]

class WorkflowInstance(BaseModel):
    id: UUID
    definition_id: UUID
    aggregate_id: UUID
    current_state: str
    data: dict
    events: list[DomainEvent]  # Raised by step execution
```

### 8.2 Execution Flow

```
Event received → Workflow engine loads instance
  → Validates transition (source state → target state)
  → Executes step (state-specific handler)
  → Step succeeds → state advances → events raised → outbox appended
  → Step fails → state rolls back → error event raised
```

### 8.3 Workflow Steps

```python
class WorkflowStep(ABC):
    step_name: str

    @abstractmethod
    async def execute(self, context: WorkflowContext) -> StepResult:
        """
        Execute the step. Return success or failure.
        Side effects (notifications, DHARA jobs) are raised as events,
        not called directly.
        """
        ...

    @abstractmethod
    async def compensate(self, context: WorkflowContext) -> None:
        """
        Undo the step. Called when a later step fails
        and the workflow needs to roll back.
        """
        ...
```

### 8.4 Saga / Compensation

Workflows that span multiple aggregates use the Saga pattern (compensating actions for each completed step on failure). This is reserved for workflows where eventual consistency and compensation are acceptable.

---

## 9. Idempotency

### 9.1 Command Idempotency

Commands are NOT inherently idempotent. The caller is responsible for deduplication. However, command handlers SHOULD check for duplicate command_ids:

```python
class CommandDeduplicationStore(ABC):
    @abstractmethod
    async def is_duplicate(self, command_id: UUID) -> bool: ...
    @abstractmethod
    async def mark_executed(self, command_id: UUID) -> None: ...
```

### 9.2 Event Handler Idempotency

ALL event handlers MUST be idempotent. The standard implementation uses `ProcessedEventStore`:

```python
# platform/events/ports/processed_event_store.py
class ProcessedEventStore(ABC):
    @abstractmethod
    async def exists(self, event_id: UUID) -> bool: ...
    @abstractmethod
    async def record(self, event_id: UUID, ttl: timedelta | None = None) -> None: ...
```

SQL implementation:

```sql
CREATE TABLE processed_events (
    event_id UUID PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- INSERT ... ON CONFLICT DO NOTHING;
-- If affected_rows == 0 → already processed
```

### 9.3 Outbox Entry Idempotency

Outbox entries are idempotent by virtue of their unique `id`. The `FOR UPDATE SKIP LOCKED` query guarantees no outbox entry is processed by more than one dispatcher simultaneously.

---

## 10. Concurrency Control

### 10.1 Optimistic Locking

Every aggregate type uses a `version` integer for optimistic locking.

| Operation | SQL |
|---|---|
| Load | `SELECT *, version FROM aggregates WHERE id = $1` |
| Save | `UPDATE aggregates SET ..., version = version + 1 WHERE id = $1 AND version = $2` |
| Conflict | If affected rows = 0: raise `ConcurrentModificationError` |

### 10.2 ConcurrentModificationError Handling

```python
class ConcurrentModificationError(Exception):
    """Raised when optimistic lock check fails."""
    ...

# Handler in service layer:
try:
    async with unit_of_work() as uow:
        aggregate = await uow.repository.load(id)
        aggregate.apply(command)
        await uow.repository.save(aggregate)
        await uow.outbox.append(aggregate.events)
        await uow.commit()
except ConcurrentModificationError:
    # Retry: reload aggregate and re-apply command
    # Max 3 retries, then fail
    ...
```

### 10.3 Read vs Write Concurrency

| Operation | Isolation | Notes |
|---|---|---|
| Query (read) | READ COMMITTED | No lock. May read stale data. |
| Command (write) | REPEATABLE READ (or SERIALIZABLE for financial) | Prevents phantom reads within UoW. |
| Outbox poller | READ COMMITTED + FOR UPDATE SKIP LOCKED | Each dispatcher locks its batch. |

---

## 11. Error Handling

### 11.1 Exception Hierarchy

```
ADXError (foundation/exceptions/base.py)
├── DomainError
│   ├── ValidationError
│   ├── AuthorizationError
│   ├── AggregateNotFoundError
│   └── ConcurrentModificationError
├── InfrastructureError
│   ├── DatabaseError
│   ├── QueueError
│   └── ThirdPartyError
└── ApplicationError
    └── ConfigurationError
```

### 11.2 HTTP Error Mapping

```python
ERROR_MAP = {
    ValidationError:             (422, "UNPROCESSABLE_ENTITY"),
    AuthorizationError:          (403, "FORBIDDEN"),
    AggregateNotFoundError:      (404, "NOT_FOUND"),
    ConcurrentModificationError: (409, "CONFLICT"),
    DatabaseError:               (500, "INTERNAL_ERROR"),
    ADXError:                    (500, "INTERNAL_ERROR"),
}
```

Exceptions are caught at the router middleware layer (FastAPI exception handler), not in service code.

### 11.3 Event Handler Errors

| Error type | Dispatcher action |
|---|---|
| `DomainError` | Retry via outbox |
| `InfrastructureError` | Retry via outbox |
| Any unhandled exception | Retry via outbox |

No event handler should catch exceptions silently. All errors propagate to the outbox dispatcher, which handles retry and dead letter routing.

---

## 12. Observability

### 12.1 Metrics

Every command and event handler MUST emit:

| Metric | Type | Tags |
|---|---|---|
| `command.executed` | Counter | `type`, `status` (success/failure) |
| `command.duration` | Histogram | `type` |
| `event.published` | Counter | `type` |
| `event.processed` | Counter | `type`, `handler`, `status` |
| `outbox.lag` | Gauge | `aggregate_type` |
| `outbox.dead_letter` | Counter | `type` |

### 12.2 Tracing

Every command and event carries:

| Trace field | Source | Purpose |
|---|---|---|
| `trace_id` | Generated at HTTP request boundary | Spans all downstream operations |
| `span_id` | Generated per operation | Links individual operations |
| `correlation_id` | Generated per command | Links command → all events it triggers |
| `causation_id` | Event metadata | Links event → parent event that caused it |

### 12.3 Logging

| Context | Logger | Fields |
|---|---|---|
| Command execution | `adx_platform.commands` | command_id, command_type, correlation_id, aggregate_id, duration |
| Event dispatch | `adx_platform.events` | event_id, event_type, correlation_id, causation_id |
| Outbox poll | `adx_platform.outbox` | batch_size, processed_count, failed_count, lag_ms |
| Workflow execution | `adx_platform.workflows` | instance_id, definition_id, current_state, transition, step |

---

## Appendix A: State Transitions Summary

```
                          Command
                            │
                            ▼
                    ┌────────────────┐
                    │   Validating    │
                    └───────┬────────┘
                            │ validated
                            ▼
                    ┌────────────────┐
                    │   Authorizing   │
                    └───────┬────────┘
                            │ authorized
                            ▼
                    ┌────────────────┐
                    │  Executing(UoW) │
                    └───────┬────────┘
                            │ committed
                            ▼
                    ┌────────────────┐
                    │  Dispatched     │ Event published → subscribers
                    └────────────────┘

                      Subscriber
                         │
                         ▼
                    ┌───────────┐
                    │  Receive   │
                    └─────┬─────┘
                          │
                    ┌─────▼──────┐
                    │  Deduplicate │ → If duplicate, return
                    └─────┬──────┘
                          │ new event
                    ┌─────▼──────┐
                    │   Handle    │ → Business logic
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │   Record    │ → processed_events table
                    └────────────┘
```

---

## Appendix B: Key Decisions Log

| Decision | Date | Rationale |
|---|---|---|
| Transactional Outbox | 2026-07-09 | At-least-once delivery without event loss. Atomic with aggregate persistence. |
| One aggregate per UoW | 2026-07-09 | Avoids distributed locking. Clear consistency boundaries. |
| Optimistic concurrency | 2026-07-09 | No locks held across HTTP waits. Version field is simple and reliable. |
| Event type includes version | 2026-07-09 | Enables schema evolution without breaking subscribers. |
| Subscriber idempotency via processed_events | 2026-07-09 | Simple, durable deduplication. Works with at-least-once delivery. |
| In-process outbox dispatcher | 2026-07-09 | No additional infrastructure. Single process until scaling demands separation. |
| FOR UPDATE SKIP LOCKED | 2026-07-09 | Safe concurrent dispatching. Available in PostgreSQL 9.5+. |

---

*This specification is the architectural constitution of the ADX backend. All runtime behavior must conform to these rules. Exceptions require a documented architectural decision record (ADR) approved by the platform team lead.*
