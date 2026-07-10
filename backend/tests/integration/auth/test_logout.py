"""Integration test: logout flow."""

from __future__ import annotations

from typing import Any

import httpx

from tests.integration.auth.conftest import PREFIX


class TestLogout:
    async def _setup_logged_in_user(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Logout Co",
            "blueprint_code": "gym",
            "owner_name": "Logout User",
            "email": "logout-user@test.com",
            "password": "SecurePass1",
        })

        token_repo = repos["token"]
        token = list(token_repo._store.values())[0]
        user_repo = repos["user"]
        user = await user_repo.load_by_email("logout-user@test.com")
        assert user is not None
        await user_repo.set_verified(user["id"])
        await token_repo.mark_used(token["id"])

        login = await client.post(f"{PREFIX}/auth/login", json={
            "email": "logout-user@test.com",
            "password": "SecurePass1",
        })
        assert login.status_code == 200
        for cookie_key, cookie_value in login.cookies.items():
            client.cookies.set(cookie_key, cookie_value)

    async def test_logout_clears_cookie(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await self._setup_logged_in_user(client, repos)

        session_repo = repos["session"]
        assert len(session_repo._store) == 1
        sess = list(session_repo._store.values())[0]
        assert sess["revoked_at"] is None

        resp = await client.post(f"{PREFIX}/auth/logout")
        assert resp.status_code == 204

        assert sess["revoked_at"] is not None

    async def test_logout_revokes_session(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await self._setup_logged_in_user(client, repos)

        session_repo = repos["session"]
        sess = list(session_repo._store.values())[0]
        assert sess["revoked_at"] is None

        await client.post(f"{PREFIX}/auth/logout")
        assert sess["revoked_at"] is not None
