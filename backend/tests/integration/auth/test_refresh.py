"""Integration test: token refresh flow."""

from __future__ import annotations

from typing import Any

import httpx

from tests.integration.auth.conftest import PREFIX


class TestRefresh:
    async def _setup_logged_in_user(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Refresh Co",
            "blueprint_code": "clinic",
            "owner_name": "Refresh User",
            "email": "refresh-user@test.com",
            "password": "SecurePass1",
        })

        token_repo = repos["token"]
        token = list(token_repo._store.values())[0]
        user_repo = repos["user"]
        user = await user_repo.load_by_email("refresh-user@test.com")
        assert user is not None
        await user_repo.set_verified(user["id"])
        await token_repo.mark_used(token["id"])

        login = await client.post(f"{PREFIX}/auth/login", json={
            "email": "refresh-user@test.com",
            "password": "SecurePass1",
        })
        assert login.status_code == 200
        for cookie_key, cookie_value in login.cookies.items():
            client.cookies.set(cookie_key, cookie_value)

    async def test_refresh_returns_new_access_token(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await self._setup_logged_in_user(client, repos)

        resp = await client.post(f"{PREFIX}/auth/refresh")
        assert resp.status_code == 200, resp.text
        body = resp.json()

        assert "access_token" in body
        assert body["token_type"] == "bearer"

    async def test_refresh_fails_without_cookie(
        self, client: httpx.AsyncClient,
    ) -> None:
        resp = await client.post(f"{PREFIX}/auth/refresh")
        assert resp.status_code == 401
