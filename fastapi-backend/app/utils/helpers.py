import secrets
import string
import uuid


def generate_uuid() -> str:
    """
    Generate a UUID4 string.
    """
    return str(uuid.uuid4())


def generate_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure URL-safe token.
    """
    return secrets.token_urlsafe(length)


def random_string(length: int = 12) -> str:
    """
    Generate a secure random alphanumeric string.
    """
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

    return text[:length] + "..."