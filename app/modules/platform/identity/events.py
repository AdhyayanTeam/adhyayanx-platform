from app.modules.platform.contracts.event import DomainEvent


class UserCreated(DomainEvent):
    event_type: str = "user.created.v1"
    aggregate_type: str = "user"


class UserDeactivated(DomainEvent):
    event_type: str = "user.deactivated.v1"
    aggregate_type: str = "user"


class UserReactivated(DomainEvent):
    event_type: str = "user.reactivated.v1"
    aggregate_type: str = "user"
