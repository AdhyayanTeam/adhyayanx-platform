"""Integration test: GET /me."""

from __future__ import annotations

from typing import Any, cast

import httpx

from tests.integration.auth.conftest import PREFIX


class TestMe:
    async def _setup_logged_in_user(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> str:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Me Co",
            "blueprint_code": "salon",
            "owner_name": "Me User",
            "email": "me-user@test.com",
            "password": "SecurePass1",
        })

        token_repo = repos["token"]
        token = list(token_repo._store.values())[0]
        user_repo = repos["user"]
        user = await user_repo.load_by_email("me-user@test.com")
        assert user is not None
        await user_repo.set_verified(user["id"])
        await token_repo.mark_used(token["id"])

        login = await client.post(f"{PREFIX}/auth/login", json={
            "email": "me-user@test.com",
            "password": "SecurePass1",
        })
        assert login.status_code == 200
        return cast(str, login.json()["access_token"])

    async def test_get_me_returns_user_info(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        token = await self._setup_logged_in_user(client, repos)

        resp = await client.get(
            f"{PREFIX}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()

        assert body["user"]["email"] == "me-user@test.com"
        assert body["user"]["name"] == "Me User"
        assert body["organization"]["name"] == "Me Co"
        assert len(body["subscriptions"]) == 1
        assert body["subscriptions"][0]["blueprint_code"] == "salon"
        assert "owner" in body["roles"]

    async def test_get_me_requires_auth(
        self, client: httpx.AsyncClient,
    ) -> None:
        resp = await client.get(f"{PREFIX}/auth/me")
        assert resp.status_code == 401
