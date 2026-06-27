from datetime import UTC, datetime


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """
    return datetime.now(UTC)


def utc_iso() -> str:
    """
    Return the current UTC datetime in ISO 8601 format.
    """
    return utc_now().isoformat()


def to_iso(dt: datetime | None) -> str | None:
    """
    Convert a datetime object to an ISO 8601 string.
    """
    if dt is None:
        return None

    return dt.astimezone(UTC).isoformat()


def is_expired(expires_at: datetime) -> bool:
    """
    Check whether a datetime has already passed.
    """
    return expires_at <= utc_now()