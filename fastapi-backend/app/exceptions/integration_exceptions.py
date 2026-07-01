"""
Integration domain exceptions.

Raised whenever communication with external services or
third-party integrations fails.

Examples:
- Open Library API
- Redis
- Email Provider
- Future AI Services
- Future Cloud Storage
"""


class IntegrationException(Exception):
    """Base exception for all integration-related errors."""

    default_message = "External integration failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class ExternalServiceUnavailableException(IntegrationException):
    """Raised when an external service is unavailable."""

    default_message = "External service is currently unavailable."


class ExternalServiceTimeoutException(IntegrationException):
    """Raised when an external service request times out."""

    default_message = "External service request timed out."


class InvalidExternalResponseException(IntegrationException):
    """Raised when an external service returns an invalid response."""

    default_message = "Received an invalid response from the external service."


class OpenLibraryException(IntegrationException):
    """Raised when Open Library operations fail."""

    default_message = "Open Library service is unavailable."


class RedisConnectionException(IntegrationException):
    """Raised when Redis cannot be reached."""

    default_message = "Unable to connect to Redis."


class StorageProviderException(IntegrationException):
    """Raised when storage provider operations fail."""

    default_message = "Storage provider operation failed."


class ThirdPartyAuthenticationException(IntegrationException):
    """Raised when third-party authentication fails."""

    default_message = "Third-party authentication failed."


__all__ = [
    "IntegrationException",
    "ExternalServiceUnavailableException",
    "ExternalServiceTimeoutException",
    "InvalidExternalResponseException",
    "OpenLibraryException",
    "RedisConnectionException",
    "StorageProviderException",
    "ThirdPartyAuthenticationException",
]