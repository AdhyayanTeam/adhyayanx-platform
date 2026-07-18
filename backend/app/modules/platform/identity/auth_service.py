"""Authentication and registration orchestration.

Purpose:
    Coordinates the full signup → verify → login → refresh → logout lifecycle.
    This is the only service that touches users, orgs, subscriptions,
    memberships, roles, sessions, and verification tokens in one transaction.

Does NOT do:
    - Validate passwords (PasswordPolicy handles that)
    - Issue JWT tokens (TokenService handles that)
    - Send emails (EmailService handles that, called here as a side effect)
    - Store data (repositories handle that)

Who depends on this:
    AuthService is resolved by the auth router and injected into endpoints.
    IdentityService delegates user creation to AuthService during signup.
"""

from __future__ import annotations

import logging
import re
import secrets
from datetime import UTC, datetime, timedelta
from time import perf_counter
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError

from app.foundation.constants.auth import (
    EMAIL_VERIFICATION_EXPIRY_HOURS,
    PASSWORD_RESET_EXPIRY_HOURS,
    SLUG_RETRY_ATTEMPTS,
    TOKEN_BYTE_LENGTH,
    TOKEN_HASH_SUFFIX_LENGTH,
)
from app.foundation.exceptions.base import ConflictError, ValidationError
from app.foundation.types import LifecycleState
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
    OrganizationSubscriptionCreated,
    PasswordReset,
    SessionRefreshed,
    UserCreated,
    UserLoggedIn,
    UserLoggedOut,
)
from app.modules.platform.identity.password_policy import PasswordPolicy
from app.modules.platform.notifications.email_service import EmailMessage
from app.modules.platform.organizations.events import OrganizationCreated

if TYPE_CHECKING:
    from app.infrastructure.postgres.database import Database
    from app.kernel.config.loader import Settings
    from app.modules.platform.events.publisher import Publisher
    from app.modules.platform.identity.navigation_service import NavigationService
    from app.modules.platform.identity.token_service import TokenService
    from app.modules.platform.notifications.email_service import EmailService

logger = logging.getLogger("app.modules.platform.identity.auth_service")


class RepositoryFactory:
    """Marker type for the repository factory callable.

    The composition root registers an instance of this type (a callable
    that takes a session and returns a dict of repositories). AuthService
    resolves it from the container.
    """

    def __call__(self, session: Any) -> dict[str, Any]:
        raise NotImplementedError


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
        repo_factory: RepositoryFactory | None = None,
    ) -> None:
        self._db = database
        self._publisher = publisher
        self._token_service = token_service
        self._navigation_service = navigation_service
        self._password_policy = password_policy
        self._settings = settings
        self._email_service = email_service
        self._repo_factory = repo_factory

    def _make_repos(self, session: Any) -> dict[str, Any]:
        if self._repo_factory is None:
            raise RuntimeError("AuthService requires repo_factory to be provided")
        return self._repo_factory(session)

    def set_email_service(self, service: Any) -> None:
        self._email_service = service

    @staticmethod
    def _ms(start: float) -> str:
        return f"{(perf_counter() - start) * 1000:.1f}ms"

    async def signup(self, command: SignupCommand) -> dict[str, Any]:
        """Create org + owner + subscription in one transaction.

        Why this exists: A new institute owner needs an organization,
        a user account, a role, a membership, a subscription, and a
        verification email — all atomically. If any step fails,
        nothing is persisted.
        """
        self._password_policy.validate(command.password, context=command.email)

        base_slug = _slugify(command.organization_name)
        for attempt in range(SLUG_RETRY_ATTEMPTS):
            slug = base_slug if attempt == 0 else f"{base_slug}-{secrets.token_hex(TOKEN_HASH_SUFFIX_LENGTH)}"
            try:
                return await self._attempt_signup(command, slug)
            except IntegrityError as e:
                err_str = str(e)
                if "users_email" in err_str:
                    raise ConflictError(
                        f"User with email '{command.email}' already exists"
                    ) from e
                if "organizations_slug" in err_str:
                    logger.info("Slug collision '%s', attempt %d, retrying", slug, attempt + 1)
                    continue
                raise

        raise ConflictError(
            f"Could not create unique organization slug after {SLUG_RETRY_ATTEMPTS} attempts"
        )

    async def _attempt_signup(
        self, command: SignupCommand, slug: str
    ) -> dict[str, Any]:
        timings: list[str] = []
        t_total = perf_counter()

        async with self._db.session() as session:
            repos = self._make_repos(session)
            org_repo = repos["org"]
            role_repo = repos["role"]
            user_repo = repos["user"]
            membership_repo = repos["membership"]
            sub_repo = repos["sub"]
            token_repo = repos["token"]

            t0 = perf_counter()
            org_id = uuid4()
            org = {
                "id": org_id,
                "name": command.organization_name,
                "slug": slug,
                "lifecycle_state": LifecycleState.ACTIVE,
                "version": 1,
                "metadata": {},
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }
            await org_repo.create(org)
            timings.append(f"create_org={self._ms(t0)}")

            t0 = perf_counter()
            await session.flush()
            timings.append(f"flush_org={self._ms(t0)}")

            t0 = perf_counter()
            owner_role_id = uuid4()
            await role_repo.create(
                {
                    "id": owner_role_id,
                    "organization_id": org_id,
                    "name": "owner",
                    "permissions": {"*": True},
                    "created_at": datetime.now(UTC),
                }
            )
            timings.append(f"create_role={self._ms(t0)}")

            t0 = perf_counter()
            user_id = uuid4()
            password_hash = self._password_policy.hash_password(command.password)
            timings.append(f"hash_password={self._ms(t0)}")

            t0 = perf_counter()
            user = {
                "id": user_id,
                "organization_id": org_id,
                "email": command.email,
                "name": command.owner_name,
                "password_hash": password_hash,
                "is_verified": False,
                "lifecycle_state": LifecycleState.ACTIVE,
                "auth_provider": "email",
                "auth_provider_id": None,
                "version": 1,
                "metadata": {},
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }
            await user_repo.create(user)
            timings.append(f"create_user={self._ms(t0)}")

            t0 = perf_counter()
            await session.flush()
            timings.append(f"flush={self._ms(t0)}")

            t0 = perf_counter()
            membership_id = uuid4()
            await membership_repo.create(
                {
                    "id": membership_id,
                    "user_id": user_id,
                    "organization_id": org_id,
                    "role_id": owner_role_id,
                    "created_at": datetime.now(UTC),
                }
            )
            timings.append(f"create_membership={self._ms(t0)}")

            t0 = perf_counter()
            sub_id = uuid4()
            await sub_repo.create(
                {
                    "id": sub_id,
                    "organization_id": org_id,
                    "blueprint_code": command.blueprint_code,
                    "status": "active",
                    "starts_at": datetime.now(UTC),
                    "ends_at": None,
                    "created_at": datetime.now(UTC),
                }
            )
            timings.append(f"create_subscription={self._ms(t0)}")

            t0 = perf_counter()
            verification_raw = secrets.token_urlsafe(TOKEN_BYTE_LENGTH)
            verification_hash = self._token_service.hash_refresh_token(verification_raw)
            token_row_id = uuid4()
            await token_repo.create(
                {
                    "id": token_row_id,
                    "user_id": user_id,
                    "token_hash": verification_hash,
                    "purpose": "VERIFY_EMAIL",
                    "expires_at": datetime.now(UTC) + timedelta(hours=EMAIL_VERIFICATION_EXPIRY_HOURS),
                    "created_at": datetime.now(UTC),
                }
            )
            timings.append(f"create_token={self._ms(t0)}")

            t0 = perf_counter()
            await self._publisher.publish(
                OrganizationCreated(
                    aggregate_id=org_id,
                    data={"name": command.organization_name, "slug": slug},
                ),
                session,
            )
            await self._publisher.publish(
                UserCreated(
                    aggregate_id=user_id,
                    data={
                        "email": command.email,
                        "name": command.owner_name,
                        "organization_id": str(org_id),
                    },
                ),
                session,
            )
            await self._publisher.publish(
                MembershipCreated(
                    aggregate_id=membership_id,
                    data={
                        "user_id": str(user_id),
                        "organization_id": str(org_id),
                        "role": "owner",
                    },
                ),
                session,
            )
            await self._publisher.publish(
                OrganizationSubscriptionCreated(
                    aggregate_id=sub_id,
                    data={
                        "organization_id": str(org_id),
                        "blueprint_code": command.blueprint_code,
                    },
                ),
                session,
            )
            await self._publisher.publish(
                EmailVerificationTokenCreated(
                    aggregate_id=token_row_id,
                    data={"user_id": str(user_id), "purpose": "VERIFY_EMAIL"},
                ),
                session,
            )
            timings.append(f"publish_events={self._ms(t0)}")

            t0 = perf_counter()
        timings.append(f"commit={self._ms(t0)}")

        t0 = perf_counter()
        email_sent = True
        if self._email_service is not None:
            try:
                await self._email_service.send(
                    EmailMessage(
                        template="verify-email",
                        to=command.email,
                        subject="Verify your email",
                        context={
                            "name": command.owner_name,
                            "organization": command.organization_name,
                            "verification_url": f"{self._settings.frontend_url}/verify-email?token={verification_raw}",
                        },
                    )
                )
            except Exception:
                logger.exception("Failed to send verification email to %s", command.email)
                email_sent = False
        timings.append(f"send_email={self._ms(t0)}")

        total_ms = self._ms(t_total)
        logger.info(
            "signup.profile %s TOTAL=%s",
            " ".join(timings),
            total_ms,
        )

        return {
            "organization": org,
            "user": user,
            "verification_url": f"{self._settings.frontend_url}/verify-email?token={verification_raw}",
            "verification_email_sent": email_sent,
            "message": "Organization created. Please verify your email.",
        }

    async def verify_email(self, command: VerifyEmailCommand) -> dict[str, Any]:
        """Mark user's email as verified using a one-time token.

        Why this exists: Email verification proves the user owns the
        email address. Until verified, the user cannot log in.
        """
        timings: list[str] = []
        t_total = perf_counter()

        t0 = perf_counter()
        token_hash = self._token_service.hash_refresh_token(command.token)
        timings.append(f"hash_token={self._ms(t0)}")

        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            token_repo = repos["token"]

            t0 = perf_counter()
            token = await token_repo.load_by_token_hash(token_hash)
            if token is None:
                raise ValidationError("Invalid verification token")
            if token["used_at"] is not None:
                raise ValidationError("Verification token has already been used")
            if token["expires_at"] < datetime.now(UTC):
                raise ValidationError("Verification token has expired")
            if token["purpose"] != "VERIFY_EMAIL":
                raise ValidationError("Invalid token purpose")
            timings.append(f"load_token={self._ms(t0)}")

            t0 = perf_counter()
            await token_repo.mark_used(token["id"])
            await user_repo.set_verified(token["user_id"])
            timings.append(f"mark_verified={self._ms(t0)}")

            t0 = perf_counter()
            await self._publisher.publish(
                EmailVerified(
                    aggregate_id=token["user_id"],
                    data={"purpose": "VERIFY_EMAIL"},
                ),
                session,
            )
            timings.append(f"publish_events={self._ms(t0)}")

            t0 = perf_counter()
        timings.append(f"commit={self._ms(t0)}")

        total_ms = self._ms(t_total)
        logger.info(
            "verify_email.profile %s TOTAL=%s",
            " ".join(timings),
            total_ms,
        )
        return {"verified": True, "message": "Email verified successfully"}

    async def login(self, command: LoginCommand) -> dict[str, Any]:
        """Validate credentials, rotate tokens, record session.

        Why this exists: Login is more than checking a password — it
        creates a refresh session, determines the landing URL based on
        the user's subscriptions, and records device info for revocation.
        """
        timings: list[str] = []
        t_total = perf_counter()

        t0 = perf_counter()
        async with self._db.session() as session:
            repos = self._make_repos(session)
            user_repo = repos["user"]
            org_repo = repos["org"]
            membership_repo = repos["membership"]
            role_repo = repos["role"]
            sub_repo = repos["sub"]
            session_repo = repos["session"]
            timings.append(f"setup={self._ms(t0)}")

            t0 = perf_counter()
            user = await user_repo.load_by_email(command.email)
            if user is None:
                raise ValidationError("Invalid email or password")
            if user["password_hash"] is None:
                raise ValidationError("This account uses a different authentication method")
            timings.append(f"load_user={self._ms(t0)}")

            t0 = perf_counter()
            if not self._password_policy.verify_password(user["password_hash"], command.password):
                raise ValidationError("Invalid email or password")
            timings.append(f"verify_password={self._ms(t0)}")

            if not user["is_verified"]:
                raise ValidationError("Email not verified. Please check your inbox.")
            if user["lifecycle_state"] != LifecycleState.ACTIVE:
                raise ValidationError("Account is inactive")

            t0 = perf_counter()
            org = await org_repo.load(user["organization_id"])
            if org is None:
                raise ValidationError("Organization not found")
            timings.append(f"load_org={self._ms(t0)}")

            t0 = perf_counter()
            memberships = await membership_repo.list_for_user(user["id"])
            roles: list[str] = []
            for ms in memberships:
                role = await role_repo.load(ms["role_id"])
                if role:
                    roles.append(role["name"])
            timings.append(f"load_roles={self._ms(t0)}")

            t0 = perf_counter()
            subscriptions = await sub_repo.load_active_by_org(org["id"])
            blueprint_codes = [s["blueprint_code"] for s in subscriptions]
            landing_url = self._navigation_service.resolve_landing(blueprint_codes)
            timings.append(f"resolve_landing={self._ms(t0)}")

            t0 = perf_counter()
            refresh_raw, refresh_hash = self._token_service.create_refresh_token_pair()
            session_id = uuid4()
            await session_repo.create(
                {
                    "id": session_id,
                    "user_id": user["id"],
                    "refresh_token_hash": refresh_hash,
                    "ip_address": command.ip_address,
                    "user_agent": command.user_agent,
                    "device_name": command.device_name,
                    "last_seen_at": datetime.now(UTC),
                    "expires_at": datetime.now(UTC)
                    + timedelta(
                        days=self._settings.jwt_refresh_token_expire_days,
                    ),
                    "created_at": datetime.now(UTC),
                }
            )
            timings.append(f"create_session={self._ms(t0)}")

            t0 = perf_counter()
            access_token = self._token_service.create_access_token(
                user["id"],
                org["id"],
                roles=roles,
            )
            timings.append(f"create_access_token={self._ms(t0)}")

            t0 = perf_counter()
            await self._publisher.publish(
                UserLoggedIn(
                    aggregate_id=user["id"],
                    data={
                        "organization_id": str(org["id"]),
                        "ip_address": command.ip_address,
                    },
                ),
                session,
            )
            timings.append(f"publish_events={self._ms(t0)}")

            t0 = perf_counter()
        timings.append(f"commit={self._ms(t0)}")

        total_ms = self._ms(t_total)
        logger.info(
            "login.profile %s TOTAL=%s",
            " ".join(timings),
            total_ms,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_raw,
            "token_type": "bearer",
            "user": user,
            "organization": org,
            "landing_url": landing_url,
        }

    async def refresh(self, refresh_token: str) -> dict[str, Any]:
        timings: list[str] = []
        t_total = perf_counter()

        t0 = perf_counter()
        token_hash = self._token_service.hash_refresh_token(refresh_token)
        timings.append(f"hash_token={self._ms(t0)}")

        async with self._db.session() as session:
            repos = self._make_repos(session)
            session_repo = repos["session"]
            user_repo = repos["user"]

            t0 = perf_counter()
            sess = await session_repo.load_by_refresh_hash(token_hash)
            if sess is None:
                raise ValidationError("Invalid refresh token")
            if sess["revoked_at"] is not None:
                raise ValidationError("Refresh token has been revoked")
            if sess["expires_at"] < datetime.now(UTC):
                raise ValidationError("Refresh token has expired")
            timings.append(f"load_session={self._ms(t0)}")

            t0 = perf_counter()
            user = await user_repo.load(sess["user_id"])
            if user is None:
                raise ValidationError("User not found")
            timings.append(f"load_user={self._ms(t0)}")

            t0 = perf_counter()
            await session_repo.update_last_seen(sess["id"])
            timings.append(f"update_last_seen={self._ms(t0)}")

            t0 = perf_counter()
            access_token = self._token_service.create_access_token(
                user["id"],
                user["organization_id"],
            )
            timings.append(f"create_access_token={self._ms(t0)}")

            t0 = perf_counter()
            await self._publisher.publish(
                SessionRefreshed(
                    aggregate_id=sess["id"],
                    data={"user_id": str(user["id"])},
                ),
                session,
            )
            timings.append(f"publish_events={self._ms(t0)}")

            t0 = perf_counter()
        timings.append(f"commit={self._ms(t0)}")

        total_ms = self._ms(t_total)
        logger.info(
            "refresh.profile %s TOTAL=%s",
            " ".join(timings),
            total_ms,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def logout(self, refresh_token: str) -> None:
        async with self._db.session() as session:
            repos = self._make_repos(session)
            session_repo = repos["session"]

            token_hash = self._token_service.hash_refresh_token(refresh_token)
            sess = await session_repo.load_by_refresh_hash(token_hash)
            if sess is not None and sess["revoked_at"] is None:
                await session_repo.revoke(sess["id"])

                await self._publisher.publish(
                    UserLoggedOut(
                        aggregate_id=sess["user_id"],
                        data={"session_id": str(sess["id"])},
                    ),
                    session,
                )

                logger.info("Logout: user=%s session=%s", sess["user_id"], sess["id"])

    async def forgot_password(self, email: str) -> dict[str, Any]:
        """Generate a password reset token and send it via email.

        Why this exists: Password recovery requires a one-time token
        sent to the user's email. The response is deliberately identical
        whether the email exists or not — to prevent email enumeration.
        """
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

            reset_raw = secrets.token_urlsafe(TOKEN_BYTE_LENGTH)
            reset_hash = self._token_service.hash_refresh_token(reset_raw)
            await token_repo.create(
                {
                    "id": uuid4(),
                    "user_id": user["id"],
                    "token_hash": reset_hash,
                    "purpose": "RESET_PASSWORD",
                    "expires_at": datetime.now(UTC) + timedelta(hours=PASSWORD_RESET_EXPIRY_HOURS),
                    "created_at": datetime.now(UTC),
                }
            )

            user_id = user["id"]
            user_email = user["email"]
            logger.info(
                "Password reset requested: user=%s reset_url=%s/reset-password?token=%s",
                user["id"],
                self._settings.frontend_url,
                reset_raw,
            )

        if reset_raw is not None and self._email_service is not None and user_id is not None:
            try:
                await self._email_service.send(
                    EmailMessage(
                        template="reset-password",
                        to=user_email,
                        subject="Reset your password",
                        context={
                            "reset_url": f"{self._settings.frontend_url}/reset-password?token={reset_raw}",
                        },
                    )
                )
            except Exception:
                logger.exception("Failed to send password reset email to %s", user_email)

        return {"email_sent": True, "message": "If the email exists, a reset link was sent"}

    async def reset_password(self, command: ResetPasswordCommand) -> dict[str, Any]:
        """Replace password using a valid reset token and revoke all sessions.

        Why this exists: After a password reset, all existing sessions
        must be revoked to force re-authentication on all devices.
        """
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

            await self._publisher.publish(
                PasswordReset(
                    aggregate_id=token["user_id"],
                    data={"purpose": "RESET_PASSWORD"},
                ),
                session,
            )

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
