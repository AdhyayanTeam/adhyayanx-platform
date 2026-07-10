from uuid import UUID

from app.modules.platform.contracts.command import Command


class CreateOrganizationCommand(Command):
    command_type: str = "adx_platform.organization.create.v1"

    name: str
    slug: str


class UpdateOrganizationCommand(Command):
    command_type: str = "adx_platform.organization.update.v1"

    organization_id: UUID
    name: str | None = None
    slug: str | None = None


class DeleteOrganizationCommand(Command):
    command_type: str = "adx_platform.organization.delete.v1"

    organization_id: UUID
