"""Integration test: reset password flow."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import httpx

from tests.integration.auth.conftest import PREFIX


class TestResetPassword:

    async def test_reset_password_happy_path(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Reset Co",
            "blueprint_code": "clinic",
            "owner_name": "Reset User",
            "email": "reset@test.com",
            "password": "SecurePass1",
        })
        token_repo = repos["token"]
        token = list(token_repo._store.values())[0]
        user_repo = repos["user"]
        user = await user_repo.load_by_email("reset@test.com")
        assert user is not None
        old_password_hash = user["password_hash"]
        await user_repo.set_verified(user["id"])
        await token_repo.mark_used(token["id"])

        raw_token = str(uuid4())
        import hashlib
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        await token_repo.create({
            "id": uuid4(),
            "user_id": user["id"],
            "token_hash": token_hash,
            "purpose": "RESET_PASSWORD",
            "expires_at": datetime.now(UTC) + timedelta(hours=1),
            "created_at": datetime.now(UTC),
        })

        resp = await client.post(f"{PREFIX}/auth/reset-password", json={
            "token": raw_token,
            "new_password": "NewStrongP@ss1",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("reset") is True

        updated = await user_repo.load_by_email("reset@test.com")
        assert updated is not None
        assert updated["password_hash"] != old_password_hash

        login = await client.post(f"{PREFIX}/auth/login", json={
            "email": "reset@test.com",
            "password": "NewStrongP@ss1",
        })
        assert login.status_code == 200

    async def test_reset_password_invalid_token(
        self, client: httpx.AsyncClient,
    ) -> None:
        resp = await client.post(f"{PREFIX}/auth/reset-password", json={
            "token": "bogus-token",
            "new_password": "NewStrongP@ss1",
        })
        assert resp.status_code == 422

    async def test_reset_password_expired_token(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Expired Reset Co",
            "blueprint_code": "clinic",
            "owner_name": "Exp Reset User",
            "email": "exp-reset@test.com",
            "password": "SecurePass1",
        })
        user_repo = repos["user"]
        user = await user_repo.load_by_email("exp-reset@test.com")
        assert user is not None
        token_repo = repos["token"]
        token = list(token_repo._store.values())[0]
        await user_repo.set_verified(user["id"])
        await token_repo.mark_used(token["id"])

        raw_token = str(uuid4())
        import hashlib
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        await token_repo.create({
            "id": uuid4(),
            "user_id": user["id"],
            "token_hash": token_hash,
            "purpose": "RESET_PASSWORD",
            "expires_at": datetime.now(UTC) - timedelta(hours=1),
            "created_at": datetime.now(UTC) - timedelta(hours=2),
        })

        resp = await client.post(f"{PREFIX}/auth/reset-password", json={
            "token": raw_token,
            "new_password": "NewStrongP@ss1",
        })
        assert resp.status_code == 422

    async def test_reset_password_revokes_all_sessions(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Revoke Sessions Co",
            "blueprint_code": "clinic",
            "owner_name": "Revoke User",
            "email": "revoke-sess@test.com",
            "password": "SecurePass1",
        })
        token_repo = repos["token"]
        token = list(token_repo._store.values())[0]
        user_repo = repos["user"]
        user = await user_repo.load_by_email("revoke-sess@test.com")
        assert user is not None
        await user_repo.set_verified(user["id"])
        await token_repo.mark_used(token["id"])

        login = await client.post(f"{PREFIX}/auth/login", json={
            "email": "revoke-sess@test.com",
            "password": "SecurePass1",
        })
        assert login.status_code == 200
        for cookie_key, cookie_value in login.cookies.items():
            client.cookies.set(cookie_key, cookie_value)

        session_repo = repos["session"]
        assert len(session_repo._store) == 1

        raw_token = str(uuid4())
        import hashlib
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        await token_repo.create({
            "id": uuid4(),
            "user_id": user["id"],
            "token_hash": token_hash,
            "purpose": "RESET_PASSWORD",
            "expires_at": datetime.now(UTC) + timedelta(hours=1),
            "created_at": datetime.now(UTC),
        })

        await client.post(f"{PREFIX}/auth/reset-password", json={
            "token": raw_token,
            "new_password": "NewStrongP@ss1",
        })

        for session in session_repo._store.values():
            assert session["revoked_at"] is not None
