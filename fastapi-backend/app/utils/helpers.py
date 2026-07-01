import secrets
import string
import uuid
from typing import Final

DEFAULT_TOKEN_LENGTH: Final[int] = 32
DEFAULT_RANDOM_STRING_LENGTH: Final[int] = 12
MIN_RANDOM_LENGTH: Final[int] = 1
MAX_RANDOM_LENGTH: Final[int] = 1024

def generate_uuid() -> str:
    """
    Generate a UUID4 string.
    """
    return str(uuid.uuid4())


def generate_token(length: int = DEFAULT_TOKEN_LENGTH) -> str:
    """
    Generate a cryptographically secure URL-safe token.
    """
    if not MIN_RANDOM_LENGTH <= length <= MAX_RANDOM_LENGTH:
        raise ValueError(
            f"Token length must be between {MIN_RANDOM_LENGTH} and {MAX_RANDOM_LENGTH}."
        )
    return secrets.token_urlsafe(length)


def random_string(length: int = DEFAULT_RANDOM_STRING_LENGTH) -> str:
    """
    Generate a secure random alphanumeric string.
    """
    if not MIN_RANDOM_LENGTH <= length <= MAX_RANDOM_LENGTH:
        raise ValueError(
            f"String length must be between {MIN_RANDOM_LENGTH} and {MAX_RANDOM_LENGTH}."
        )
    alphabet = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def truncate(text: str, length: int = 100) -> str:
    """
    Truncate text to a maximum length.
    """
    if len(text) <= length:
        return text

    if length < 3:
        raise ValueError("Length must be at least 3.")

    return text[: length - 3] + "..."

def generate_numeric_code(
    length: int = 6,
) -> str:
    """
    Generate a secure numeric verification code.
    """

    if not MIN_RANDOM_LENGTH <= length <= 12:
        raise ValueError("Code length must be between 1 and 12.")

    digits = string.digits

    return "".join(
        secrets.choice(digits)
        for _ in range(length)
    )
    
__all__ = [
    "generate_uuid",
    "generate_token",
    "random_string",
    "generate_numeric_code",
    "truncate",
]