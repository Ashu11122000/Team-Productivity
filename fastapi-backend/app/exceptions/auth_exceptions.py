"""
Authentication domain exceptions.

These exceptions are raised by the authentication service and
converted into HTTP responses by the global exception handlers.
"""


class AuthenticationException(Exception):
    """Base exception for all authentication errors."""


class InvalidCredentialsException(AuthenticationException):
    """Raised when email or password is incorrect."""


class InvalidTokenException(AuthenticationException):
    """Raised when a JWT is invalid."""


class ExpiredTokenException(AuthenticationException):
    """Raised when a JWT has expired."""


class RefreshTokenException(AuthenticationException):
    """Raised when a refresh token is invalid."""


class UnauthorizedException(AuthenticationException):
    """Raised when authentication is required."""


class ForbiddenException(AuthenticationException):
    """Raised when the authenticated user lacks permission."""


class InactiveUserException(AuthenticationException):
    """Raised when an inactive user attempts to authenticate."""


class EmailAlreadyVerifiedException(AuthenticationException):
    """Raised when verifying an already verified email."""


class EmailVerificationException(AuthenticationException):
    """Raised when email verification fails."""


class PasswordResetException(AuthenticationException):
    """Raised when password reset fails."""