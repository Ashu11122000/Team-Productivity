import re
from typing import Final

EMAIL_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

MIN_PASSWORD_LENGTH: Final[int] = 8

UPPERCASE_PATTERN: Final[re.Pattern[str]] = re.compile(r"[A-Z]")
LOWERCASE_PATTERN: Final[re.Pattern[str]] = re.compile(r"[a-z]")
DIGIT_PATTERN: Final[re.Pattern[str]] = re.compile(r"\d")
SPECIAL_CHARACTER_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"[!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/~`]"
)


def is_valid_email(email: str) -> bool:
    """
    Validate an email address.
    """
    if is_blank(email):
        return False

    return bool(EMAIL_PATTERN.fullmatch(email.strip()))


def is_strong_password(password: str) -> bool:
    """
    Validate password strength.

    Requirements:
        - At least 8 characters
        - One uppercase letter
        - One lowercase letter
        - One digit
        - One special character
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        return False

    if not UPPERCASE_PATTERN.search(password):
        return False

    if not LOWERCASE_PATTERN.search(password):
        return False

    if not DIGIT_PATTERN.search(password):
        return False

    if not SPECIAL_CHARACTER_PATTERN.search(password):
        return False

    return True


def is_blank(value: str | None) -> bool:
    """
    Check whether a string is empty or contains only whitespace.
    """
    return value is None or not value.strip()

def normalize_email(email: str) -> str:
    """
    Normalize an email address for storage and comparison.
    """

    return email.strip().lower()

__all__ = [
    "is_valid_email",
    "is_strong_password",
    "is_blank",
    "normalize_email",
]