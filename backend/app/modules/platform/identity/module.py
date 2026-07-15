"""Identity module manifest.

Encapsulates user management, authentication, sessions, and verification.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.modules.platform.contracts.module import PlatformModule

if TYPE_CHECKING:
    from app.kernel.container import Container


class IdentityModule(PlatformModule):
    name = "identity"

    def configure(self, container: Container) -> None:
        from app.modules.platform.identity.auth_service import AuthService, RepositoryFactory
        from app.modules.platform.identity.navigation_service import NavigationService
        from app.modules.platform.identity.password_policy import PasswordPolicy
        from app.modules.platform.identity.service import IdentityService
        from app.modules.platform.identity.token_service import TokenService

        def _repo_factory(session: Any) -> dict[str, Any]:
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

        container.register_instance(RepositoryFactory, _repo_factory)
        container.register(IdentityService, IdentityService)
        container.register(AuthService, AuthService)
        container.register(TokenService, TokenService)
        container.register(NavigationService, NavigationService)
        container.register(PasswordPolicy, PasswordPolicy)

    def register_handlers(self, subscribe: Any) -> None:
        from app.modules.platform.identity.handlers import (
            on_user_created,
            on_user_deactivated,
            on_user_reactivated,
        )

        subscribe("user.created.v1", on_user_created)
        subscribe("user.deactivated.v1", on_user_deactivated)
        subscribe("user.reactivated.v1", on_user_reactivated)
