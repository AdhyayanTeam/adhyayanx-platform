"""Integration test: signup flow through AuthService."""

from __future__ import annotations

from typing import Any
from uuid import UUID

import httpx
from fastapi import FastAPI

from tests.integration.auth.conftest import (
    PREFIX,
    DictIdentityRepository,
    DictMembershipRepository,
    DictOrganizationRepository,
    DictOrganizationRoleRepository,
    DictOrganizationSubscriptionRepository,
    DictVerificationTokenRepository,
)


class TestSignup:
    async def test_signup_creates_org_user_role_membership_subscription(
        self, client: httpx.AsyncClient, test_app_and_repos: tuple[FastAPI, dict[str, Any]],
    ) -> None:
        app, repos = test_app_and_repos
        resp = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Test Clinic",
            "blueprint_code": "clinic",
            "owner_name": "Dr. Smith",
            "email": "dr.smith@test.com",
            "password": "SecurePass1",
        })
        assert resp.status_code == 201, resp.text
        body = resp.json()

        assert body["organization"]["name"] == "Test Clinic"
        org_id = UUID(body["organization"]["id"])

        assert body["user"]["email"] == "dr.smith@test.com"
        assert body["user"]["name"] == "Dr. Smith"
        assert body["user"]["is_verified"] is False
        user_id = UUID(body["user"]["id"])

        assert body["verification_email_sent"] is True
        assert "verify your email" in body["message"].lower()

        user_repo: DictIdentityRepository = repos["user"]
        stored_user = await user_repo.load(user_id)
        assert stored_user is not None
        assert stored_user["password_hash"] is not None

        org_repo: DictOrganizationRepository = repos["org"]
        stored_org = await org_repo.load(org_id)
        assert stored_org is not None

        role_repo: DictOrganizationRoleRepository = repos["role"]
        owner_role = await role_repo.load_by_name_and_org("owner", org_id)
        assert owner_role is not None

        membership_repo: DictMembershipRepository = repos["membership"]
        membership = await membership_repo.load_by_user_and_org(user_id, org_id)
        assert membership is not None
        assert membership["role_id"] == owner_role["id"]

        sub_repo: DictOrganizationSubscriptionRepository = repos["sub"]
        subs = await sub_repo.load_active_by_org(org_id)
        assert len(subs) == 1
        assert subs[0]["blueprint_code"] == "clinic"

        token_repo: DictVerificationTokenRepository = repos["token"]
        assert len(token_repo._store) == 1
        token = list(token_repo._store.values())[0]
        assert token["purpose"] == "VERIFY_EMAIL"

        publisher = app.state.publisher
        event_types = [e.event_type for e in publisher.published]
        assert "organization.created.v1" in event_types
        assert "user.created.v1" in event_types
        assert "membership.created.v1" in event_types
        assert "organization_subscription.created.v1" in event_types
        assert "email_verification_token.created.v1" in event_types

    async def test_signup_rejects_duplicate_email(
        self, client: httpx.AsyncClient,
    ) -> None:
        payload = {
            "organization_name": "First Org",
            "blueprint_code": "academy",
            "owner_name": "Alice",
            "email": "alice@test.com",
            "password": "SecurePass1",
        }
        resp1 = await client.post(f"{PREFIX}/auth/signup", json=payload)
        assert resp1.status_code == 201

        payload["organization_name"] = "Second Org"
        payload["owner_name"] = "Bob"
        resp2 = await client.post(f"{PREFIX}/auth/signup", json=payload)
        assert resp2.status_code == 409

    async def test_signup_generates_unique_slug(
        self, client: httpx.AsyncClient,
    ) -> None:
        resp1 = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Same Name Org",
            "blueprint_code": "clinic",
            "owner_name": "Alice",
            "email": "alice2@test.com",
            "password": "SecurePass1",
        })
        assert resp1.status_code == 201
        slug1 = resp1.json()["organization"]["slug"]

        resp2 = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Same Name Org",
            "blueprint_code": "clinic",
            "owner_name": "Bob",
            "email": "bob@test.com",
            "password": "SecurePass1",
        })
        assert resp2.status_code == 201
        slug2 = resp2.json()["organization"]["slug"]

        assert slug1 == "same-name-org"
        assert slug2 != slug1
        assert slug2.startswith("same-name-org-")

    async def test_signup_rejects_weak_password(
        self, client: httpx.AsyncClient,
    ) -> None:
        resp = await client.post(f"{PREFIX}/auth/signup", json={
            "organization_name": "Weak Org",
            "blueprint_code": "gym",
            "owner_name": "Weak",
            "email": "weak@test.com",
            "password": "password",
        })
        assert resp.status_code == 422
