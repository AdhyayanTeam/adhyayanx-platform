
from adx_platform.contracts.event import DomainEvent


class OrganizationCreated(DomainEvent):
    event_type: str = "organization.created.v1"
    aggregate_type: str = "organization"


class OrganizationUpdated(DomainEvent):
    event_type: str = "organization.updated.v1"
    aggregate_type: str = "organization"


class OrganizationDeleted(DomainEvent):
    event_type: str = "organization.deleted.v1"
    aggregate_type: str = "organization"
