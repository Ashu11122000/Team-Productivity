import re

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def is_valid_email(email: str) -> bool:
    """
    Validate an email address.
    """
    return bool(EMAIL_PATTERN.fullmatch(email))


def is_strong_password(password: str) -> bool:
    """
    Validate password strength.

    Requirements:
    - At least 8 characters
    - One uppercase letter
    - One lowercase letter
    - One digit
    """

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True


def is_blank(value: str | None) -> bool:
    """
    Check whether a string is empty or contains only whitespace.
    """
    return value is None or value.strip() == ""