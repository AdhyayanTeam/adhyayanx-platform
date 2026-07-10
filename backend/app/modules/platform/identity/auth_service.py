from __future__ import annotations

import logging
import re
import secrets
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from app.foundation.exceptions.base import ValidationError
from app.modules.platform.identity.commands import (
    LoginCommand,
    ResetPasswordCommand,
    SignupCommand,
    VerifyEmailCommand,
)
from app.modules.platform.identity.events import (
    EmailVerificationTokenCreated,
    EmailVerified,
    MembershipCreated,
    OrganizationCreated,
    OrganizationSubscriptionCreated,
    PasswordReset,
    SessionRefreshed,
    UserCreated,
    UserLoggedIn,
    UserLoggedOut,
)
from app.modules.platform.identity.password_policy import PasswordPolicy
from app.modules.platform.notifications.email_service import EmailMessage

if TYPE_CHECKING:
    from app.infrastructure.postgres.database import Database
    from app.kernel.config.loader import Settings
    from app.modules.platform.events.publisher import Publisher
    from app.modules.platform.identity.navigation_service import NavigationService
    from app.modules.platform.identity.token_service import TokenService
    from app.modules.platform.notifications.email_service import EmailService

logger = logging.getLogger("app.modules.platform.identity.auth_service")


def _default_repo_factory(session: Any) -> dict[str, Any]:
    from app.infrastructure.postgres.identity_repository import PostgresIdentityRepository
    from app.infrastructure.postgres.membership_repository import (
        PostgresMembershipRepository,
    )
    from app.infrastructure.postgres.organization_repository import (
        PostgresOrganizationRepository,
    )
    from app.infrastructure.postgres.organization_role_repository import (
        PostgresOrganizationRoleRepository,
    )
    from app.infrastructure.postgres.organization_subscription_repository import (
        PostgresOrganizationSubscriptionRepository,
    )
    from app.infrastructure.postgres.session_repository import PostgresSessionRepository
    from app.infrastructure.postgres.verification_token_repository import (
        PostgresVerificationTokenRepository,
    )

    return {
        "user": PostgresIdentityRepository(session),
        "org": PostgresOrganizationRepository(session),
        "role": PostgresOrganizationRoleRepository(session),
        "membership": PostgresMembershipRepository(session),
        "sub": PostgresOrganizationSubscriptionRepository(session),
        "session": PostgresSessionRepository(session),
        "token": PostgresVerificationTokenRepository(session),
    }


class AuthService:

    def __init__(
        self,
        database: Database,
        publisher: Publisher,
        token_service: TokenService,
        navigation_service: NavigationService,
        password_policy: PasswordPolicy,
        settings: Settings,
        email_service: EmailService | None = None,
        repo_factory: Callable[[Any], dict[str, Any]] | None = None,
    ) -> None:
        self._db = database
        self._publisher = publisher
        self._token_service = token_service
        self._navigation_service = navigation_service
        self._password_policy = password_policy
        self._settings = settings
        self._email_service = email_service
        self._repo_factory = repo_factory or _default_repo_factory

    def _make_repos(self, session: Any) -> dict[str, Any]:
        return self._repo_factory(session)

    def set_email_service(self, service: Any) -> None:
        self._email_service = service

    async def signup(self, command: SignupCommand) -> dict[str, Any]:
        self._password_policy.validate(command.password, context=command.email)

        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            org_repo = repos["org"]
            role_repo = repos["role"]
            membership_repo = repos["membership"]
            sub_repo = repos["sub"]
            token_repo = repos["token"]

            existing_user = await user_repo.load_by_email(command.email)
            if existing_user is not None:
                raise ValidationError(f"User with email '{command.email}' already exists")

            slug = _slugify(command.organization_name)
            if await org_repo.exists_by_slug(slug):
                raise ValidationError(f"Organization with slug '{slug}' already exists")

            org_id = uuid4()
            org = {
                "id": org_id,
                "name": command.organization_name,
                "slug": slug,
                "lifecycle_state": "active",
                "version": 1,
                "metadata": {},
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }
            await org_repo.save(org)

            owner_role_id = uuid4()
            await role_repo.create({
                "id": owner_role_id,
                "organization_id": org_id,
                "name": "owner",
                "permissions": {"*": True},
                "created_at": datetime.now(UTC),
            })

            user_id = uuid4()
            password_hash = self._password_policy.hash_password(command.password)
            user = {
                "id": user_id,
                "organization_id": org_id,
                "email": command.email,
                "name": command.owner_name,
                "password_hash": password_hash,
                "is_verified": False,
                "lifecycle_state": "active",
                "auth_provider": "email",
                "auth_provider_id": None,
                "version": 1,
                "metadata": {},
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }
            await user_repo.save(user)

            membership_id = uuid4()
            await membership_repo.create({
                "id": membership_id,
                "user_id": user_id,
                "organization_id": org_id,
                "role_id": owner_role_id,
                "created_at": datetime.now(UTC),
            })

            sub_id = uuid4()
            await sub_repo.create({
                "id": sub_id,
                "organization_id": org_id,
                "blueprint_code": command.blueprint_code,
                "status": "active",
                "starts_at": datetime.now(UTC),
                "ends_at": None,
                "created_at": datetime.now(UTC),
            })

            verification_raw = secrets.token_urlsafe(32)
            verification_hash = self._token_service.hash_refresh_token(verification_raw)
            token_row_id = uuid4()
            await token_repo.create({
                "id": token_row_id,
                "user_id": user_id,
                "token_hash": verification_hash,
                "purpose": "VERIFY_EMAIL",
                "expires_at": datetime.now(UTC) + timedelta(hours=24),
                "created_at": datetime.now(UTC),
            })

            await self._publisher.publish(OrganizationCreated(
                aggregate_id=org_id,
                data={"name": command.organization_name, "slug": slug},
            ), session)
            await self._publisher.publish(UserCreated(
                aggregate_id=user_id,
                data={
                    "email": command.email,
                    "name": command.owner_name,
                    "organization_id": str(org_id),
                },
            ), session)
            await self._publisher.publish(MembershipCreated(
                aggregate_id=membership_id,
                data={
                    "user_id": str(user_id),
                    "organization_id": str(org_id),
                    "role": "owner",
                },
            ), session)
            await self._publisher.publish(OrganizationSubscriptionCreated(
                aggregate_id=sub_id,
                data={
                    "organization_id": str(org_id),
                    "blueprint_code": command.blueprint_code,
                },
            ), session)
            await self._publisher.publish(EmailVerificationTokenCreated(
                aggregate_id=token_row_id,
                data={"user_id": str(user_id), "purpose": "VERIFY_EMAIL"},
            ), session)

            logger.info("Signup complete: org=%s user=%s", org_id, user_id)

        email_sent = True
        if self._email_service is not None:
            try:
                await self._email_service.send(EmailMessage(
                    template="verify-email",
                    to=command.email,
                    subject="Verify your email",
                    context={
                        "name": command.owner_name,
                        "organization": command.organization_name,
                        "verification_url": f"/auth/verify-email?token={verification_raw}",
                    },
                ))
            except Exception:
                logger.exception("Failed to send verification email to %s", command.email)
                email_sent = False

        return {
            "organization": org,
            "user": user,
            "verification_url": f"/auth/verify-email?token={verification_raw}",
            "verification_email_sent": email_sent,
            "message": "Organization created. Please verify your email.",
        }

    async def verify_email(self, command: VerifyEmailCommand) -> dict[str, Any]:
        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            token_repo = repos["token"]

            token_hash = self._token_service.hash_refresh_token(command.token)
            token = await token_repo.load_by_token_hash(token_hash)
            if token is None:
                raise ValidationError("Invalid verification token")
            if token["used_at"] is not None:
                raise ValidationError("Verification token has already been used")
            if token["expires_at"] < datetime.now(UTC):
                raise ValidationError("Verification token has expired")
            if token["purpose"] != "VERIFY_EMAIL":
                raise ValidationError("Invalid token purpose")

            await token_repo.mark_used(token["id"])
            await user_repo.set_verified(token["user_id"])

            await self._publisher.publish(EmailVerified(
                aggregate_id=token["user_id"],
                data={"purpose": "VERIFY_EMAIL"},
            ), session)

            logger.info("Email verified: user=%s", token["user_id"])
            return {"verified": True, "message": "Email verified successfully"}

    async def login(self, command: LoginCommand) -> dict[str, Any]:
        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            org_repo = repos["org"]
            membership_repo = repos["membership"]
            role_repo = repos["role"]
            sub_repo = repos["sub"]
            session_repo = repos["session"]

            user = await user_repo.load_by_email(command.email)
            if user is None:
                raise ValidationError("Invalid email or password")
            if user["password_hash"] is None:
                raise ValidationError("This account uses a different authentication method")
            if not self._password_policy.verify_password(user["password_hash"], command.password):
                raise ValidationError("Invalid email or password")
            if not user["is_verified"]:
                raise ValidationError("Email not verified. Please check your inbox.")
            if user["lifecycle_state"] != "active":
                raise ValidationError("Account is inactive")

            org = await org_repo.load(user["organization_id"])
            if org is None:
                raise ValidationError("Organization not found")

            memberships = await membership_repo.list_for_user(user["id"])
            roles: list[str] = []
            for ms in memberships:
                role = await role_repo.load(ms["role_id"])
                if role:
                    roles.append(role["name"])

            subscriptions = await sub_repo.load_active_by_org(org["id"])
            blueprint_codes = [s["blueprint_code"] for s in subscriptions]
            landing_url = self._navigation_service.resolve_landing(blueprint_codes)

            refresh_raw, refresh_hash = self._token_service.create_refresh_token_pair()
            session_id = uuid4()
            await session_repo.create({
                "id": session_id,
                "user_id": user["id"],
                "refresh_token_hash": refresh_hash,
                "ip_address": command.ip_address,
                "user_agent": command.user_agent,
                "device_name": command.device_name,
                "last_seen_at": datetime.now(UTC),
                "expires_at": datetime.now(UTC) + timedelta(
                    days=self._settings.jwt_refresh_token_expire_days,
                ),
                "created_at": datetime.now(UTC),
            })

            access_token = self._token_service.create_access_token(
                user["id"], org["id"], roles=roles,
            )

            await self._publisher.publish(UserLoggedIn(
                aggregate_id=user["id"],
                data={
                    "organization_id": str(org["id"]),
                    "ip_address": command.ip_address,
                },
            ), session)

            logger.info("Login: user=%s org=%s", user["id"], org["id"])
            return {
                "access_token": access_token,
                "refresh_token": refresh_raw,
                "token_type": "bearer",
                "user": user,
                "organization": org,
                "landing_url": landing_url,
            }

    async def refresh(self, refresh_token: str) -> dict[str, Any]:
        async with self._db.session() as session:
            repos = self._make_repos(session)
            session_repo = repos["session"]
            user_repo = repos["user"]

            token_hash = self._token_service.hash_refresh_token(refresh_token)
            sess = await session_repo.load_by_refresh_hash(token_hash)
            if sess is None:
                raise ValidationError("Invalid refresh token")
            if sess["revoked_at"] is not None:
                raise ValidationError("Refresh token has been revoked")
            if sess["expires_at"] < datetime.now(UTC):
                raise ValidationError("Refresh token has expired")

            user = await user_repo.load(sess["user_id"])
            if user is None:
                raise ValidationError("User not found")

            await session_repo.update_last_seen(sess["id"])

            access_token = self._token_service.create_access_token(
                user["id"], user["organization_id"],
            )

            await self._publisher.publish(SessionRefreshed(
                aggregate_id=sess["id"],
                data={"user_id": str(user["id"])},
            ), session)

            logger.info("Token refresh: user=%s session=%s", user["id"], sess["id"])
            return {"access_token": access_token, "token_type": "bearer"}

    async def logout(self, refresh_token: str) -> None:
        async with self._db.session() as session:
            repos = self._make_repos(session)
            session_repo = repos["session"]

            token_hash = self._token_service.hash_refresh_token(refresh_token)
            sess = await session_repo.load_by_refresh_hash(token_hash)
            if sess is not None and sess["revoked_at"] is None:
                await session_repo.revoke(sess["id"])

                await self._publisher.publish(UserLoggedOut(
                    aggregate_id=sess["user_id"],
                    data={"session_id": str(sess["id"])},
                ), session)

                logger.info("Logout: user=%s session=%s", sess["user_id"], sess["id"])

    async def forgot_password(self, email: str) -> dict[str, Any]:
        reset_raw: str | None = None
        user_id: UUID | None = None
        user_email: str = email

        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            token_repo = repos["token"]

            user = await user_repo.load_by_email(email)
            if user is None:
                return {"email_sent": True, "message": "If the email exists, a reset link was sent"}

            reset_raw = secrets.token_urlsafe(32)
            reset_hash = self._token_service.hash_refresh_token(reset_raw)
            await token_repo.create({
                "id": uuid4(),
                "user_id": user["id"],
                "token_hash": reset_hash,
                "purpose": "RESET_PASSWORD",
                "expires_at": datetime.now(UTC) + timedelta(hours=1),
                "created_at": datetime.now(UTC),
            })

            user_id = user["id"]
            user_email = user["email"]
            logger.info(
                "Password reset requested: user=%s reset_url=/auth/reset-password?token=%s",
                user["id"], reset_raw,
            )

        if reset_raw is not None and self._email_service is not None and user_id is not None:
            try:
                await self._email_service.send(EmailMessage(
                    template="reset-password",
                    to=user_email,
                    subject="Reset your password",
                    context={
                        "reset_url": f"/auth/reset-password?token={reset_raw}",
                    },
                ))
            except Exception:
                logger.exception("Failed to send password reset email to %s", user_email)

        return {"email_sent": True, "message": "If the email exists, a reset link was sent"}

    async def reset_password(self, command: ResetPasswordCommand) -> dict[str, Any]:
        self._password_policy.validate(command.new_password)

        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            token_repo = repos["token"]
            session_repo = repos["session"]

            token_hash = self._token_service.hash_refresh_token(command.token)
            token = await token_repo.load_by_token_hash(token_hash)
            if token is None:
                raise ValidationError("Invalid reset token")
            if token["used_at"] is not None:
                raise ValidationError("Reset token has already been used")
            if token["expires_at"] < datetime.now(UTC):
                raise ValidationError("Reset token has expired")
            if token["purpose"] != "RESET_PASSWORD":
                raise ValidationError("Invalid token purpose")

            new_hash = self._password_policy.hash_password(command.new_password)
            await user_repo.update_password(token["user_id"], new_hash)
            await token_repo.mark_used(token["id"])
            await session_repo.revoke_all_for_user(token["user_id"])

            await self._publisher.publish(PasswordReset(
                aggregate_id=token["user_id"],
                data={"purpose": "RESET_PASSWORD"},
            ), session)

            logger.info("Password reset: user=%s", token["user_id"])
            return {"reset": True, "message": "Password reset successfully"}

    async def get_current_user(self, access_token: str) -> dict[str, Any]:
        payload = self._token_service.decode_access_token(access_token)
        user_id = UUID(payload["sub"])
        org_id = UUID(payload["org"])

        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            org_repo = repos["org"]
            membership_repo = repos["membership"]
            role_repo = repos["role"]
            sub_repo = repos["sub"]

            user = await user_repo.load(user_id)
            if user is None:
                raise ValidationError("User not found")

            org = await org_repo.load(org_id)
            if org is None:
                raise ValidationError("Organization not found")

            memberships = await membership_repo.list_for_user(user_id)
            roles: list[str] = []
            for ms in memberships:
                role = await role_repo.load(ms["role_id"])
                if role:
                    roles.append(role["name"])

            subscriptions = await sub_repo.load_active_by_org(org_id)
            subs_list = [
                {"id": str(s["id"]), "blueprint_code": s["blueprint_code"], "status": s["status"]}
                for s in subscriptions
            ]

            return {
                "user": user,
                "organization": org,
                "subscriptions": subs_list,
                "roles": roles,
            }


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", "-"))
    return slug[:80] or "org"
