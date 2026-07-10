from uuid import UUID

from app.modules.platform.contracts.command import Command


class CreateUserCommand(Command):
    command_type: str = "adx_platform.identity.create_user.v1"

    organization_id: UUID
    email: str
    name: str
    auth_provider: str = "email"
    auth_provider_id: str | None = None


class DeactivateUserCommand(Command):
    command_type: str = "adx_platform.identity.deactivate_user.v1"

    organization_id: UUID
    user_id: UUID


class ReactivateUserCommand(Command):
    command_type: str = "adx_platform.identity.reactivate_user.v1"

    organization_id: UUID
    user_id: UUID


class SignupCommand(Command):
    command_type: str = "adx_platform.identity.signup.v1"

    organization_name: str
    blueprint_code: str
    owner_name: str
    email: str
    password: str


class LoginCommand(Command):
    command_type: str = "adx_platform.identity.login.v1"

    email: str
    password: str
    ip_address: str = ""
    user_agent: str = ""
    device_name: str | None = None


class VerifyEmailCommand(Command):
    command_type: str = "adx_platform.identity.verify_email.v1"

    token: str


class ForgotPasswordCommand(Command):
    command_type: str = "adx_platform.identity.forgot_password.v1"

    email: str


class ResetPasswordCommand(Command):
    command_type: str = "adx_platform.identity.reset_password.v1"

    token: str
    new_password: str


class RefreshTokenCommand(Command):
    command_type: str = "adx_platform.identity.refresh_token.v1"

    refresh_token: str


class LogoutCommand(Command):
    command_type: str = "adx_platform.identity.logout.v1"

    refresh_token: str
