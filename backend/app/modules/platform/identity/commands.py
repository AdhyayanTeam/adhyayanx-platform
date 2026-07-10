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
