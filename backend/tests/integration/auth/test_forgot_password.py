"""Integration test: forgot password flow."""

from __future__ import annotations

from typing import Any

import httpx

from tests.integration.auth.conftest import PREFIX


class TestForgotPassword:

    async def test_forgot_password_creates_reset_token(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Forgot Co",
            "blueprint_code": "clinic",
            "owner_name": "Forgot User",
            "email": "forgot@test.com",
            "password": "SecurePass1",
        })

        resp = await client.post(f"{PREFIX}/auth/forgot-password", json={
            "email": "forgot@test.com",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("email_sent") is True

        token_repo = repos["token"]
        reset_tokens = [
            t for t in token_repo._store.values()
            if t["purpose"] == "RESET_PASSWORD"
        ]
        assert len(reset_tokens) == 1
        assert reset_tokens[0]["user_id"] is not None

    async def test_forgot_password_no_email_enumeration(
        self, client: httpx.AsyncClient,
    ) -> None:
        resp = await client.post(f"{PREFIX}/auth/forgot-password", json={
            "email": "nonexistent@test.com",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("email_sent") is True
