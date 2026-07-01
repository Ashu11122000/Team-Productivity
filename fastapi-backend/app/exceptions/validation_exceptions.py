"""
Validation domain exceptions.

Raised whenever application-level validation or business
validation rules are violated.

These exceptions are independent of FastAPI and Pydantic
validation errors.
"""


class ValidationException(Exception):
    """Base exception for all validation-related errors."""

    default_message = "Validation failed."

    def __init__(self, message: str |None = None) -> None:
        super().__init__(message or self.default_message)


class RequiredFieldException(ValidationException):
    """Raised when a required field is missing."""

    default_message = "Required field is missing."


class InvalidFieldException(ValidationException):
    """Raised when a field contains an invalid value."""

    default_message = "Invalid field value."


class InvalidInputException(ValidationException):
    """Raised when user input is invalid."""

    default_message = "Invalid input provided."


class InvalidEmailException(ValidationException):
    """Raised when an email address is invalid."""

    default_message = "Invalid email address."


class InvalidPasswordException(ValidationException):
    """Raised when a password does not meet security requirements."""

    default_message = "Invalid password."


class InvalidUsernameException(ValidationException):
    """Raised when a username is invalid."""

    default_message = "Invalid username."


class InvalidUUIDException(ValidationException):
    """Raised when an invalid UUID is provided."""

    default_message = "Invalid UUID."


class InvalidDateException(ValidationException):
    """Raised when an invalid date or datetime is provided."""

    default_message = "Invalid date."


class InvalidFileExtensionException(ValidationException):
    """Raised when an uploaded file extension is not allowed."""

    default_message = "Invalid file extension."


class InvalidPaginationException(ValidationException):
    """Raised when pagination parameters are invalid."""

    default_message = "Invalid pagination parameters."


class InvalidSortFieldException(ValidationException):
    """Raised when an unsupported sort field is requested."""

    default_message = "Invalid sort field."


class InvalidFilterException(ValidationException):
    """Raised when an invalid filter is supplied."""

    default_message = "Invalid filter."


class InvalidOperationException(ValidationException):
    """Raised when an invalid operation is attempted."""

    default_message = "Invalid operation."


__all__ = [
    "ValidationException",
    "RequiredFieldException",
    "InvalidFieldException",
    "InvalidInputException",
    "InvalidEmailException",
    "InvalidPasswordException",
    "InvalidUsernameException",
    "InvalidUUIDException",
    "InvalidDateException",
    "InvalidFileExtensionException",
    "InvalidPaginationException",
    "InvalidSortFieldException",
    "InvalidFilterException",
    "InvalidOperationException",
]