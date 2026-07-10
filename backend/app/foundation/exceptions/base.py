class ADXError(Exception):
    """Base exception for all ADX platform errors."""


class DomainError(ADXError):
    """Error raised when a domain rule is violated."""


class ValidationError(DomainError):
    """Error raised when command validation fails."""


class AuthenticationError(DomainError):
    """Error raised when authentication fails."""


class AuthorizationError(DomainError):
    """Error raised when the actor lacks permission."""


class AggregateNotFoundError(DomainError):
    """Error raised when an aggregate cannot be found."""


class ConcurrentModificationError(DomainError):
    """Error raised when optimistic lock check fails."""


class InfrastructureError(ADXError):
    """Error raised by infrastructure components."""


class DatabaseError(InfrastructureError):
    """Error raised by database operations."""


class QueueError(InfrastructureError):
    """Error raised by queue operations."""


class ThirdPartyError(InfrastructureError):
    """Error raised by external service calls."""


class ApplicationError(ADXError):
    """Error raised by application-level concerns."""
