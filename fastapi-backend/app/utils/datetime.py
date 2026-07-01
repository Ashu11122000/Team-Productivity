from datetime import UTC, datetime, timedelta


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

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    return dt.astimezone(UTC).isoformat()


def is_expired(expires_at: datetime) -> bool:
    """
    Check whether a datetime has already passed.
    """
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)

    return expires_at <= utc_now()

def add_timedelta(
    *,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
) -> datetime:
    """
    Return a UTC datetime after adding the specified duration.
    """

    return utc_now() + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )
    
def seconds_until(dt: datetime) -> int:
    """
    Return the number of whole seconds until a datetime.
    Returns 0 if the datetime has already passed.
    """

    remaining = int((dt.astimezone(UTC) - utc_now()).total_seconds())
    return max(remaining, 0)

__all__ = [
    "utc_now",
    "utc_iso",
    "to_iso",
    "is_expired",
    "add_timedelta",
    "seconds_until",
]