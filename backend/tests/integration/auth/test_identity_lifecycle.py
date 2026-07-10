"""Integration test: full identity lifecycle."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import httpx

from tests.integration.auth.conftest import PREFIX


class TestIdentityLifecycle:

    async def test_full_lifecycle(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        # 1. Signup
        signup = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Lifecycle Co",
            "blueprint_code": "academy",
            "owner_name": "Cycle User",
            "email": "cycle@test.com",
            "password": "SecurePass1",
        })
        assert signup.status_code == 201
        user_id = UUID(signup.json()["user"]["id"])
        org_id = UUID(signup.json()["organization"]["id"])

        # 2. Verify email
        raw_verify_token = str(uuid4())
        import hashlib
        verify_hash = hashlib.sha256(raw_verify_token.encode()).hexdigest()
        token_repo = repos["token"]
        await token_repo.create({
            "id": uuid4(),
            "user_id": user_id,
            "token_hash": verify_hash,
            "purpose": "VERIFY_EMAIL",
            "expires_at": datetime.now(UTC) + timedelta(hours=24),
            "created_at": datetime.now(UTC),
        })
        verify_resp = await client.post(f"{PREFIX}/auth/verify-email", json={
            "token": raw_verify_token,
        })
        assert verify_resp.status_code == 200
        assert verify_resp.json()["verified"] is True

        # 3. Login
        login = await client.post(f"{PREFIX}/auth/login", json={
            "email": "cycle@test.com",
            "password": "SecurePass1",
        })
        assert login.status_code == 200
        access_token = login.json()["access_token"]
        for cookie_key, cookie_value in login.cookies.items():
            client.cookies.set(cookie_key, cookie_value)

        # 4. GET /me
        me = await client.get(
            f"{PREFIX}/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me.status_code == 200
        me_body = me.json()
        assert me_body["user"]["email"] == "cycle@test.com"
        assert UUID(me_body["organization"]["id"]) == org_id
        assert "owner" in me_body["roles"]
        assert len(me_body["subscriptions"]) == 1
        assert me_body["subscriptions"][0]["blueprint_code"] == "academy"

        # 5. Refresh
        refresh = await client.post(f"{PREFIX}/auth/refresh")
        assert refresh.status_code == 200
        assert "access_token" in refresh.json()

        # 6. Logout
        logout = await client.post(f"{PREFIX}/auth/logout")
        assert logout.status_code == 204

        # 7. Old refresh token no longer works
        stale = await client.post(f"{PREFIX}/auth/refresh")
        assert stale.status_code in (401, 422)
