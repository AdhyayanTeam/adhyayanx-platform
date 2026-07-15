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


class MembershipCreated(DomainEvent):
    event_type: str = "membership.created.v1"
    aggregate_type: str = "membership"


class OrganizationSubscriptionCreated(DomainEvent):
    event_type: str = "organization_subscription.created.v1"
    aggregate_type: str = "organization_subscription"


class EmailVerificationTokenCreated(DomainEvent):
    event_type: str = "email_verification_token.created.v1"
    aggregate_type: str = "email_verification_token"


class EmailVerified(DomainEvent):
    event_type: str = "email.verified.v1"
    aggregate_type: str = "user"


class PasswordReset(DomainEvent):
    event_type: str = "password.reset.v1"
    aggregate_type: str = "user"


class UserLoggedIn(DomainEvent):
    event_type: str = "user.logged_in.v1"
    aggregate_type: str = "user"


class UserLoggedOut(DomainEvent):
    event_type: str = "user.logged_out.v1"
    aggregate_type: str = "user"


class SessionRefreshed(DomainEvent):
    event_type: str = "session.refreshed.v1"
    aggregate_type: str = "session"
