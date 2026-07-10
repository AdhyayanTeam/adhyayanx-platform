"""Shared fixtures for auth integration tests."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.kernel.config.loader import Settings
from app.modules.platform.contracts.event import DomainEvent
from app.modules.platform.events.bus import EventBus
from app.modules.platform.events.publisher import Publisher
from app.modules.platform.identity.auth_service import AuthService
from app.modules.platform.identity.navigation_service import NavigationService
from app.modules.platform.identity.password_policy import PasswordPolicy
from app.modules.platform.identity.ports.identity_repository import IdentityRepository
from app.modules.platform.identity.ports.membership_repository import MembershipRepository
from app.modules.platform.identity.ports.organization_role_repository import (
    OrganizationRoleRepository,
)
from app.modules.platform.identity.ports.organization_subscription_repository import (
    OrganizationSubscriptionRepository,
)
from app.modules.platform.identity.ports.session_repository import SessionRepository
from app.modules.platform.identity.ports.verification_token_repository import (
    VerificationTokenRepository,
)
from app.modules.platform.identity.token_service import TokenService

PREFIX = "/api/v1"


class DictIdentityRepository(IdentityRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def load(self, id: UUID) -> dict[str, Any] | None:
        return self._store.get(id)

    async def load_by_email(self, email: str) -> dict[str, Any] | None:
        for user in self._store.values():
            if user["email"] == email:
                return user
        return None

    async def save(self, user: dict[str, Any]) -> None:
        uid = user["id"]
        if uid in self._store:
            self._store[uid].update(user)
        else:
            self._store[uid] = dict(user)

    async def delete(self, id: UUID) -> None:
        self._store.pop(id, None)

    async def exists(self, id: UUID) -> bool:
        return id in self._store

    async def list(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        return [
            u for u in self._store.values()
            if u["organization_id"] == organization_id
        ][skip : skip + limit]

    async def update_password(self, id: UUID, password_hash: str) -> None:
        if id in self._store:
            self._store[id]["password_hash"] = password_hash

    async def set_verified(self, id: UUID) -> None:
        if id in self._store:
            self._store[id]["is_verified"] = True


class DictOrganizationRoleRepository(OrganizationRoleRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def load(self, id: UUID) -> dict[str, Any] | None:
        return self._store.get(id)

    async def create(self, role: dict[str, Any]) -> None:
        self._store[role["id"]] = dict(role)

    async def load_by_name_and_org(
        self, name: str, organization_id: UUID
    ) -> dict[str, Any] | None:
        for role in self._store.values():
            if role["name"] == name and role["organization_id"] == organization_id:
                return role
        return None

    async def list_for_org(self, organization_id: UUID) -> list[dict[str, Any]]:
        return [r for r in self._store.values() if r["organization_id"] == organization_id]


class DictMembershipRepository(MembershipRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def create(self, membership: dict[str, Any]) -> None:
        self._store[membership["id"]] = dict(membership)

    async def load_by_user_and_org(
        self, user_id: UUID, organization_id: UUID
    ) -> dict[str, Any] | None:
        for m in self._store.values():
            if m["user_id"] == user_id and m["organization_id"] == organization_id:
                return m
        return None

    async def list_for_user(self, user_id: UUID) -> list[dict[str, Any]]:
        return [m for m in self._store.values() if m["user_id"] == user_id]


class DictOrganizationSubscriptionRepository(OrganizationSubscriptionRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def create(self, subscription: dict[str, Any]) -> None:
        self._store[subscription["id"]] = dict(subscription)

    async def load_active_by_org(self, organization_id: UUID) -> list[dict[str, Any]]:
        return [
            s for s in self._store.values()
            if s["organization_id"] == organization_id and s.get("status") == "active"
        ]


class DictSessionRepository(SessionRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def create(self, session_data: dict[str, Any]) -> None:
        data = dict(session_data)
        data.setdefault("revoked_at", None)
        data.setdefault("last_seen_at", None)
        self._store[session_data["id"]] = data

    async def load_by_refresh_hash(self, token_hash: str) -> dict[str, Any] | None:
        for s in self._store.values():
            if s["refresh_token_hash"] == token_hash:
                return s
        return None

    async def revoke(self, id: UUID) -> None:
        if id in self._store:
            self._store[id]["revoked_at"] = datetime.now(UTC)

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        for s in self._store.values():
            if s["user_id"] == user_id:
                s["revoked_at"] = datetime.now(UTC)

    async def update_last_seen(self, id: UUID) -> None:
        if id in self._store:
            self._store[id]["last_seen_at"] = datetime.now(UTC)


class DictVerificationTokenRepository(VerificationTokenRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def create(self, token: dict[str, Any]) -> None:
        data = dict(token)
        data.setdefault("used_at", None)
        self._store[token["id"]] = data

    async def load_by_token_hash(self, token_hash: str) -> dict[str, Any] | None:
        for t in self._store.values():
            if t["token_hash"] == token_hash:
                return t
        return None

    async def mark_used(self, id: Any) -> None:
        if id in self._store:
            self._store[id]["used_at"] = datetime.now(UTC)


class DictOrganizationRepository:
    def __init__(self) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}

    async def load(self, id: UUID) -> dict[str, Any] | None:
        return self._store.get(id)

    async def load_by_slug(self, slug: str) -> dict[str, Any] | None:
        for org in self._store.values():
            if org["slug"] == slug:
                return org
        return None

    async def save(self, organization: dict[str, Any]) -> None:
        self._store[organization["id"]] = dict(organization)

    async def delete(self, id: UUID) -> None:
        self._store.pop(id, None)

    async def exists(self, id: UUID) -> bool:
        return id in self._store

    async def exists_by_slug(self, slug: str) -> bool:
        return any(org["slug"] == slug for org in self._store.values())

    async def list(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        return list(self._store.values())[skip : skip + limit]


class MockAsyncSession:
    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    async def close(self) -> None:
        pass

    def add(self, instance: Any) -> None:
        pass


class MockDatabase:
    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        yield MockAsyncSession()  # type: ignore[misc]


class RecordingPublisher(Publisher):
    def __init__(self, bus: EventBus) -> None:
        self.published: list[DomainEvent] = []
        self._bus = bus

    async def publish(self, event: DomainEvent, _session: AsyncSession) -> None:
        self.published.append(event)
        await self._bus.publish(event)


@pytest.fixture
def test_app_and_repos() -> tuple[FastAPI, dict[str, Any]]:
    from app.api.main import create_app
    from app.infrastructure.postgres.database import Database

    settings = Settings()
    app = create_app(settings)
    container = app.state.container

    event_bus = EventBus()
    publisher = RecordingPublisher(event_bus)

    user_repo = DictIdentityRepository()
    org_repo = DictOrganizationRepository()
    role_repo = DictOrganizationRoleRepository()
    membership_repo = DictMembershipRepository()
    sub_repo = DictOrganizationSubscriptionRepository()
    session_repo = DictSessionRepository()
    token_repo = DictVerificationTokenRepository()

    db = MockDatabase()
    token_service = TokenService(settings)
    nav_service = NavigationService()
    password_policy = PasswordPolicy(settings)

    container._instances[Database] = db
    container.register_instance(Publisher, publisher)
    container.register_instance(EventBus, event_bus)
    container.register_instance(TokenService, token_service)
    container.register_instance(NavigationService, nav_service)
    container.register_instance(PasswordPolicy, password_policy)

    container._instances.pop(AuthService, None)
    container._registry.pop(AuthService, None)

    def test_repo_factory(_session: Any) -> dict[str, Any]:
        return {
            "user": user_repo,
            "org": org_repo,
            "role": role_repo,
            "membership": membership_repo,
            "sub": sub_repo,
            "session": session_repo,
            "token": token_repo,
        }

    auth_service = AuthService(
        database=db,  # type: ignore[arg-type]
        publisher=publisher,
        token_service=token_service,
        navigation_service=nav_service,
        password_policy=password_policy,
        settings=settings,
        repo_factory=test_repo_factory,
    )
    container.register_instance(AuthService, auth_service)

    repos = {
        "user": user_repo,
        "org": org_repo,
        "role": role_repo,
        "membership": membership_repo,
        "sub": sub_repo,
        "session": session_repo,
        "token": token_repo,
    }
    app.state.repos = repos
    app.state.event_bus = event_bus
    app.state.publisher = publisher

    return app, repos


@pytest.fixture
async def client(
    test_app_and_repos: tuple[FastAPI, dict[str, Any]],
) -> AsyncIterator[httpx.AsyncClient]:
    app, _ = test_app_and_repos
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def repos(test_app_and_repos: tuple[FastAPI, dict[str, Any]]) -> dict[str, Any]:
    return test_app_and_repos[1]
