"""
Security utilities for authentication and JWT management.

Responsibilities:
- Password hashing & verification
- Access token creation
- Access token validation
- Refresh token creation
- Refresh token validation
- Refresh token hashing
- Secure random token generation

Architecture:

API Routes
     │
     ▼
AuthService
     │
     ▼
Security Utilities
     │
     ▼
JWT / Argon2 / SHA256
"""

from __future__ import annotations

import hashlib
import secrets
import uuid
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.constants import (ACCESS_TOKEN, REFRESH_TOKEN)
from app.core.exceptions import InvalidTokenException

from fastapi import status
from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings

# ==========================================================
# Password Hasher
# ==========================================================

password_hasher = PasswordHash.recommended()

# ==========================================================
# Password Utilities
# ==========================================================


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.
    """
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a password against its stored hash.
    """
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# JWT Payload Helpers
# ==========================================================


def _base_payload(
    *,
    user_id: int | str,
    email: str,
    role: str,
    token_type: str,
    expires_delta: timedelta,
) -> dict[str, Any]:
    """
    Build the common JWT payload.
    """

    now = datetime.now(timezone.utc)

    return {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "type": token_type,
        "jti": str(uuid.uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + expires_delta, 
    }


# ==========================================================
# Access Tokens
# ==========================================================


def create_access_token(
    *,
    user_id: int | str,
    email: str,
    role: str,
) -> str:
    """
    Create a signed JWT access token.
    """

    payload = _base_payload(
        user_id=user_id,
        email=email,
        role=role,
        token_type=ACCESS_TOKEN,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and validate an access token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
        )

        if payload.get("type") != ACCESS_TOKEN:
            raise InvalidTokenException()

        return payload

    except JWTError as exc:
        raise InvalidTokenException() from exc


# ==========================================================
# Refresh Tokens (JWT)
# ==========================================================


def create_refresh_token(
    *,
    user_id: int | str,
    email: str,
    role: str,
) -> str:
    """
    Create a signed JWT refresh token.

    Used for:

    - Session renewal
    - Token rotation
    - Multi-device authentication
    """

    payload = _base_payload(
        user_id=user_id,
        email=email,
        role=role,
        token_type=REFRESH_TOKEN,
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        ),
    )

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    
    # ==========================================================
# Refresh Token Validation
# ==========================================================


def decode_refresh_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT refresh token.

    Raises:
        HTTPException:
            If the token is invalid, expired,
            or not a refresh token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
        )

        if payload.get("type") != REFRESH_TOKEN:
            raise InvalidTokenException()

        return payload

    except JWTError as exc:
        raise InvalidTokenException() from exc


# ==========================================================
# Secure Token Utilities
# ==========================================================


def generate_secure_token(
    length: int = 64,
) -> str:
    """
    Generate a cryptographically secure random token.

    Useful for:

    - Email verification
    - Password reset
    - API keys
    - Session identifiers
    """

    return secrets.token_urlsafe(length)


# ==========================================================
# Refresh Token Hashing
# ==========================================================


def hash_refresh_token(
    refresh_token: str,
) -> str:
    """
    Hash a refresh token before storing it.

    Raw refresh tokens should never be persisted.
    """

    return hashlib.sha256(
        refresh_token.encode("utf-8"),
    ).hexdigest()


def verify_refresh_token_hash(
    refresh_token: str,
    stored_hash: str,
) -> bool:
    """
    Verify a refresh token against its stored hash.
    """

    return hmac.compare_digest(
        hash_refresh_token(refresh_token),
        stored_hash,
    )


# ==========================================================
# JWT Helper Utilities
# ==========================================================


def get_token_expiration(
    payload: dict[str, Any],
) -> datetime:
    """
    Extract the expiration timestamp from
    a decoded JWT payload.
    """

    exp = payload.get("exp")

    if exp is None:
        raise InvalidTokenException()

    if isinstance(exp, datetime):
        return exp.astimezone(timezone.utc)

    return datetime.fromtimestamp(
        exp,
        tz=timezone.utc,
    )


def is_token_expired(
    payload: dict[str, Any],
) -> bool:
    """
    Determine whether a decoded JWT payload
    has expired.
    """

    return (
        get_token_expiration(payload)
        <= datetime.now(timezone.utc)
    )


def get_current_utc_time() -> datetime:
    """
    Return the current UTC timestamp.
    """

    return datetime.now(timezone.utc)


# ==========================================================
# Module Exports
# ==========================================================

__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "create_refresh_token",
    "decode_refresh_token",
    "generate_secure_token",
    "hash_refresh_token",
    "verify_refresh_token_hash",
    "get_token_expiration",
    "is_token_expired",
    "get_current_utc_time",
]