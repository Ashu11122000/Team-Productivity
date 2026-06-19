# datetime and timezone handling, JWT encoding/decoding, password hashing
# timedelta for token expiration, HTTP exceptions for auth errors
from datetime import datetime, timedelta, timezone

# Any for JWT payload typing
from typing import Any

# HTTPException and status are used when raise authentication errors
from fastapi import HTTPException, status

# JWTError and jwt from python-jose for handling jwt tokens
from jose import JWTError, jwt

# PasswordHash from pwdlib for secure password hashing
from pwdlib import PasswordHash

from app.core.config import settings

# Password Hashing (Argon2) - recommended for secure password storage
password_hash = PasswordHash.recommended()

# Security utilities for password hashing and JWT token management
def hash_password(password: str) -> str:
    return password_hash.hash(password)

# Verify password against stored hash
def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify password against stored hash.
    """
    return password_hash.verify(
        plain_password,
        hashed_password,
    )

# Create JWT access token with user information and expiration
def create_access_token(
    user_id: str,
    email: str,
    role: str,
) -> str:
    """
    Create JWT access token.
    """

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": email,
        "user_id": user_id,
        "role": role,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

# Decode and validate JWT token, ensuring compatibility with NestJS JWT configuration
def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and validate JWT token.
    Compatible with NestJS JWT configuration.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )