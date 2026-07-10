"""Integration test: login flow."""

from __future__ import annotations

from typing import Any

import httpx

from tests.integration.auth.conftest import PREFIX


class TestLogin:
    async def _signup_and_verify(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> str:
        signup = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Login Co",
            "blueprint_code": "academy",
            "owner_name": "Login User",
            "email": "login-user@test.com",
            "password": "SecurePass1",
        })
        assert signup.status_code == 201

        token_repo = repos["token"]
        token = list(token_repo._store.values())[0]

        user_repo = repos["user"]
        user = await user_repo.load_by_email("login-user@test.com")
        assert user is not None
        await user_repo.set_verified(user["id"])
        await token_repo.mark_used(token["id"])

        return str(user["id"])

    async def test_login_success(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await self._signup_and_verify(client, repos)

        resp = await client.post(f"{PREFIX}/auth/login", json={
            "email": "login-user@test.com",
            "password": "SecurePass1",
        })
        assert resp.status_code == 200, resp.text
        body = resp.json()

        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert body["user"]["email"] == "login-user@test.com"
        assert body["user"]["is_verified"] is True
        assert "landing_url" in body
        assert "academy" in body["landing_url"]

        assert "refresh_token" in resp.cookies
        cookie = resp.cookies["refresh_token"]
        assert len(cookie) > 0

    async def test_login_fails_without_verification(
        self, client: httpx.AsyncClient,
    ) -> None:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Unverified Co",
            "blueprint_code": "clinic",
            "owner_name": "Unverified",
            "email": "unverified@test.com",
            "password": "SecurePass1",
        })

        resp = await client.post(f"{PREFIX}/auth/login", json={
            "email": "unverified@test.com",
            "password": "SecurePass1",
        })
        assert resp.status_code == 422

    async def test_login_fails_with_wrong_password(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await self._signup_and_verify(client, repos)

        resp = await client.post(f"{PREFIX}/auth/login", json={
            "email": "login-user@test.com",
            "password": "WrongPassword1",
        })
        assert resp.status_code == 422
