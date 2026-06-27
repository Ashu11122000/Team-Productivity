"""
User domain exceptions.

Raised by the user service whenever user-related
business rules are violated.
"""


class UserException(Exception):
    """Base exception for user-related errors."""


class UserNotFoundException(UserException):
    """Raised when a user cannot be found."""


class UserAlreadyExistsException(UserException):
    """Raised when attempting to register an existing user."""


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


class DuplicateUsernameException(UserException):
    """Raised when a username is already in use."""