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
        from app.modules.platform.identity.auth_service import AuthService
        from app.modules.platform.identity.navigation_service import NavigationService
        from app.modules.platform.identity.password_policy import PasswordPolicy
        from app.modules.platform.identity.service import IdentityService
        from app.modules.platform.identity.token_service import TokenService

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
