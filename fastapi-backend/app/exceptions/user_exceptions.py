"""
User domain exceptions.

Raised by the user service whenever user-related
business rules are violated.
"""


class UserException(Exception):
    """Base exception for all user-related errors."""

    default_message = "User operation failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)

class UserNotFoundException(UserException):
    """Raised when a user cannot be found."""
    default_message = "User not found."

class UserAlreadyExistsException(UserException):
    """Raised when attempting to register an existing user."""

    default_message = "User already exists."


class UserAlreadyActiveException(UserException):
    """Raised when activating an already active account."""


class UserAlreadyInactiveException(UserException):
    """Raised when deactivating an already inactive account."""


class UserProfileException(UserException):
    """Raised when profile operations fail."""


class InvalidUserOperationException(UserException):
    """Raised when an invalid user operation is attempted."""


class DuplicateEmailException(UserException):
    """Raised when an email address is already in use."""

    default_message = "Email address is already in use."


class DuplicateUsernameException(UserException):
    """Raised when a username is already in use."""

    default_message = "Username is already in use."
    
__all__ = [
    "UserException",
    "UserNotFoundException",
    "UserAlreadyExistsException",
    "UserAlreadyActiveException",
    "UserAlreadyInactiveException",
    "UserProfileException",
    "InvalidUserOperationException",
    "DuplicateEmailException",
    "DuplicateUsernameException",
]