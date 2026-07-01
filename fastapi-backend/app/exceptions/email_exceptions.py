"""
Email domain exceptions.

Raised whenever email-related operations fail.
"""


class EmailException(Exception):
    """Base exception for all email-related errors."""

    default_message = "Email operation failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class EmailSendException(EmailException):
    """Raised when sending an email fails."""

    default_message = "Unable to send email."


class EmailTemplateException(EmailException):
    """Raised when an email template cannot be rendered."""

    default_message = "Email template rendering failed."


class InvalidEmailRecipientException(EmailException):
    """Raised when the recipient email address is invalid."""

    default_message = "Invalid email recipient."


class EmailConfigurationException(EmailException):
    """Raised when email configuration is invalid."""

    default_message = "Email service is not configured correctly."


class EmailDeliveryException(EmailException):
    """Raised when email delivery fails."""

    default_message = "Email delivery failed."


class EmailVerificationSendException(EmailException):
    """Raised when verification email sending fails."""

    default_message = "Unable to send email verification."


class PasswordResetEmailException(EmailException):
    """Raised when password reset email sending fails."""

    default_message = "Unable to send password reset email."


__all__ = [
    "EmailException",
    "EmailSendException",
    "EmailTemplateException",
    "InvalidEmailRecipientException",
    "EmailConfigurationException",
    "EmailDeliveryException",
    "EmailVerificationSendException",
    "PasswordResetEmailException",
]