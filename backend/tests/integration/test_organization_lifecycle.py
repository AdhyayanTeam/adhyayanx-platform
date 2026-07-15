"""Integration test: full organization lifecycle through the platform stack.

Tests the chain:
  POST /organizations → OrganizationService → Repository → Publisher
  → EventBus → OrganizationCreated handler → Assertion
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any
from uuid import UUID, uuid4

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.foundation.constants.pagination import DEFAULT_PAGE_LIMIT
from app.kernel.config.loader import Settings
from app.modules.platform.contracts.event import DomainEvent
from app.modules.platform.events.bus import EventBus
from app.modules.platform.events.publisher import Publisher
from app.modules.platform.organizations.ports.organization_repository import OrganizationRepository

# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


class DictOrganizationRepository(OrganizationRepository):
    """In-memory repository backed by a dict."""

    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def load(self, id: UUID) -> dict[str, Any] | None:
        return self._store.get(id)

    async def load_by_slug(self, slug: str) -> dict[str, Any] | None:
        for org in self._store.values():
            if org["slug"] == slug:
                return org
        return None

    async def create(self, organization: dict[str, Any]) -> None:
        self._store[organization["id"]] = dict(organization)

    async def save(self, organization: dict[str, Any]) -> None:
        org_id = organization["id"]
        if org_id in self._store:
            self._store[org_id].update(organization)
        else:
            self._store[org_id] = dict(organization)

    async def delete(self, id: UUID) -> None:
        self._store.pop(id, None)

    async def exists(self, id: UUID) -> bool:
        return id in self._store

    async def exists_by_slug(self, slug: str) -> bool:
        return any(org["slug"] == slug for org in self._store.values())

    async def list(self, skip: int = 0, limit: int = DEFAULT_PAGE_LIMIT) -> list[dict[str, Any]]:
        return list(self._store.values())[skip : skip + limit]


class MockAsyncSession:
    """Minimal AsyncSession stub — no real DB needed for this test."""

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def flush(self) -> None:
        pass

    def add(self, instance: Any) -> None:
        pass


class MockDatabase:
    """Database replacement that yields a MockAsyncSession."""

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        yield MockAsyncSession()  # type: ignore[misc]


class RecordingPublisher:
    """Test double: captures events and forwards to EventBus, bypassing outbox."""

    def __init__(self, bus: EventBus) -> None:
        self.published: list[DomainEvent] = []
        self._bus = bus

    async def publish(self, event: DomainEvent, _session: Any) -> None:
        self.published.append(event)
        await self._bus.publish(event)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def test_app() -> FastAPI:
    """Build a FastAPI app wired with test doubles."""
    from app.api.main import create_app
    from app.infrastructure.postgres.database import Database
    from app.modules.platform.organizations.service import OrganizationService

    app = create_app(Settings())
    container = app.state.container

    event_bus = EventBus()
    repo = DictOrganizationRepository()
    publisher = RecordingPublisher(event_bus)

    db = MockDatabase()
    container._instances[Database] = db
    container.register_instance(Publisher, publisher)
    container.register_instance(EventBus, event_bus)

    container._instances.pop(OrganizationService, None)
    container._registry.pop(OrganizationService, None)
    org_service = OrganizationService(db, publisher, lambda _: repo)  # type: ignore[arg-type]
    container.register_instance(OrganizationService, org_service)

    received: list[DomainEvent] = []

    async def spy(event: DomainEvent) -> None:
        received.append(event)

    event_bus.subscribe("organization.created.v1", spy)
    event_bus.subscribe("organization.updated.v1", spy)
    event_bus.subscribe("organization.deleted.v1", spy)

    app.state.received_events = received
    app.state.repo = repo
    app.state.publisher = publisher

    return app


@pytest.fixture
async def client(test_app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


PREFIX = "/api/v1"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestOrganizationLifecycle:
    """One integration test covering the full platform stack."""

    async def test_full_lifecycle(
        self,
        client: httpx.AsyncClient,
        test_app: FastAPI,
    ) -> None:
        slug = f"acme-{uuid4().hex[:8]}"

        # Phase 1: Create
        resp = await client.post(
            f"{PREFIX}/organizations",
            json={"name": "Acme Corp", "slug": slug},
        )
        assert resp.status_code == 201
        body = resp.json()
        org_id = body["id"]
        assert body["name"] == "Acme Corp"
        assert body["slug"] == slug
        assert body["lifecycle_state"] == "active"

        repo: DictOrganizationRepository = test_app.state.repo
        stored = await repo.load(UUID(org_id))
        assert stored is not None
        assert stored["name"] == "Acme Corp"

        # Phase 2: Get
        resp = await client.get(f"{PREFIX}/organizations/{org_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Acme Corp"

        # Phase 3: Update
        resp = await client.patch(
            f"{PREFIX}/organizations/{org_id}",
            json={"name": "Acme International"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Acme International"

        stored = await repo.load(UUID(org_id))
        assert stored is not None
        assert stored["name"] == "Acme International"

        # Phase 4: List
        resp = await client.get(f"{PREFIX}/organizations")
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] >= 1
        assert any(item["id"] == org_id for item in body["items"])

        # Phase 5: Delete
        resp = await client.delete(f"{PREFIX}/organizations/{org_id}")
        assert resp.status_code == 204

        stored = await repo.load(UUID(org_id))
        assert stored is None

        # Phase 6: Verify events
        await asyncio.sleep(0)

        received = test_app.state.received_events
        event_types = [e.event_type for e in received]
        assert "organization.created.v1" in event_types
        assert "organization.updated.v1" in event_types
        assert "organization.deleted.v1" in event_types

        publisher: RecordingPublisher = test_app.state.publisher
        assert len(publisher.published) >= 3
