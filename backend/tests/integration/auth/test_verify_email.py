"""Integration test: email verification flow."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import httpx

from tests.integration.auth.conftest import PREFIX


class TestVerifyEmail:

    async def test_verify_email_with_valid_token(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        signup = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Verify Co",
            "blueprint_code": "salon",
            "owner_name": "Verify User",
            "email": "verify@test.com",
            "password": "SecurePass1",
        })
        assert signup.status_code == 201
        body = signup.json()
        user_id = UUID(body["user"]["id"])

        user_repo = repos["user"]
        stored = await user_repo.load(user_id)
        assert stored is not None
        assert stored["is_verified"] is False

        raw_token = str(uuid4())
        import hashlib
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        token_repo = repos["token"]
        await token_repo.create({
            "id": uuid4(),
            "user_id": user_id,
            "token_hash": token_hash,
            "purpose": "VERIFY_EMAIL",
            "expires_at": datetime.now(UTC) + timedelta(hours=24),
            "created_at": datetime.now(UTC),
        })

        resp = await client.post(f"{PREFIX}/auth/verify-email", json={
            "token": raw_token,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["verified"] is True
        assert "successfully" in data["message"].lower()

        stored2 = await user_repo.load(user_id)
        assert stored2 is not None
        assert stored2["is_verified"] is True

        token = await token_repo.load_by_token_hash(token_hash)
        assert token is not None
        assert token["used_at"] is not None

    async def test_verify_email_rejects_invalid_token(
        self, client: httpx.AsyncClient,
    ) -> None:
        resp = await client.post(f"{PREFIX}/auth/verify-email", json={
            "token": "bogus-token",
        })
        assert resp.status_code == 422

    async def test_verify_email_expired_token(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        signup = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Expired Token Co",
            "blueprint_code": "clinic",
            "owner_name": "Expired User",
            "email": "expired@test.com",
            "password": "SecurePass1",
        })
        assert signup.status_code == 201
        user_id = UUID(signup.json()["user"]["id"])
        raw_token = str(uuid4())

        import hashlib
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        token_repo = repos["token"]
        await token_repo.create({
            "id": uuid4(),
            "user_id": user_id,
            "token_hash": token_hash,
            "purpose": "VERIFY_EMAIL",
            "expires_at": datetime.now(UTC) - timedelta(hours=1),
            "created_at": datetime.now(UTC) - timedelta(hours=2),
        })

        resp = await client.post(f"{PREFIX}/auth/verify-email", json={
            "token": raw_token,
        })
        assert resp.status_code == 422

    async def test_verify_email_used_token(
        self, client: httpx.AsyncClient, repos: dict[str, Any],
    ) -> None:
        signup = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Used Token Co",
            "blueprint_code": "salon",
            "owner_name": "Used User",
            "email": "used@test.com",
            "password": "SecurePass1",
        })
        assert signup.status_code == 201
        user_id = UUID(signup.json()["user"]["id"])
        raw_token = str(uuid4())

        import hashlib
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        token_repo = repos["token"]
        token_id = uuid4()
        await token_repo.create({
            "id": token_id,
            "user_id": user_id,
            "token_hash": token_hash,
            "purpose": "VERIFY_EMAIL",
            "expires_at": datetime.now(UTC) + timedelta(hours=24),
            "created_at": datetime.now(UTC),
        })
        await token_repo.mark_used(token_id)

        resp = await client.post(f"{PREFIX}/auth/verify-email", json={
            "token": raw_token,
        })
        assert resp.status_code == 422
