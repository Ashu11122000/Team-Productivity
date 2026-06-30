"""
Authentication-related Pydantic schemas.

This module provides authentication-specific request and
response schemas.

To avoid duplication, request schemas defined in user.py are
re-exported here.

Used by:

- Login
- Registration
- Refresh Tokens
- Logout
- Password Reset
- Email Verification
- Session Management

Architecture:

API Routes
      │
      ▼
Authentication Service
      │
      ▼
Repositories
      │
      ▼
JWT / Refresh Tokens
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

# ==========================================================
# Re-export User Authentication Schemas
# ==========================================================

from app.schemas.user import (
    ForgotPasswordRequest,
    LogoutRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    ResendVerificationRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    VerifyEmailRequest,
)


# ==========================================================
# Login Response
# ==========================================================


class LoginResponse(TokenResponse):
    """
    Response returned after successful authentication.

    Extends TokenResponse and adds basic user information.
    """

    user_id: int = Field(
        ...,
        description="Authenticated user identifier.",
        examples=[1],
    )

    message: str = Field(
        default="Login successful.",
        description="Authentication result message.",
    )


# ==========================================================
# Token Verification Response
# ==========================================================


class TokenVerificationResponse(BaseModel):
    """
    Response returned after verifying
    an access token.
    """

    valid: bool = Field(
        ...,
        description="Whether the token is valid.",
        examples=[True],
    )

    expired: bool = Field(
        default=False,
        description="Whether the token has expired.",
    )

    user_id: int | None = Field(
        default=None,
        description="Authenticated user identifier.",
    )


# ==========================================================
# Authentication Status
# ==========================================================


class AuthenticationStatusResponse(BaseModel):
    """
    Response indicating whether a user
    is currently authenticated.
    """

    authenticated: bool = Field(
        ...,
        description="Authentication status.",
        examples=[True],
    )

    user_id: int | None = Field(
        default=None,
        description="Authenticated user identifier.",
    )

    expires_at: datetime | None = Field(
        default=None,
        description="Access token expiration time.",
    )
    
    # ==========================================================
# Authenticated User Response
# ==========================================================


class AuthenticatedResponse(BaseModel):
    """
    Response returned after successfully
    authenticating a user.

    Useful for:

    - /auth/me
    - Session validation
    - Frontend bootstrap
    """

    authenticated: bool = Field(
        default=True,
        description="Whether the request is authenticated.",
    )

    user_id: int = Field(
        ...,
        description="Authenticated user identifier.",
        examples=[1],
    )

    email: str = Field(
        ...,
        description="Authenticated user email.",
        examples=["john.doe@example.com"],
    )

    role: str = Field(
        ...,
        description="Authenticated user role.",
        examples=["MEMBER"],
    )


# ==========================================================
# Session Response
# ==========================================================


class SessionResponse(BaseModel):
    """
    Represents an active login session.

    Future use:

    - Multi-device login
    - Security dashboard
    - Session management
    """

    session_id: str = Field(
        ...,
        description="Unique session identifier.",
    )

    device: str | None = Field(
        default=None,
        description="Device information.",
        examples=["Windows Desktop"],
    )

    browser: str | None = Field(
        default=None,
        description="Browser name.",
        examples=["Chrome"],
    )

    operating_system: str | None = Field(
        default=None,
        description="Operating system.",
        examples=["Windows 11"],
    )

    ip_address: str | None = Field(
        default=None,
        description="Client IP address.",
        examples=["192.168.1.100"],
    )

    location: str | None = Field(
        default=None,
        description="Approximate login location.",
        examples=["Patna, Bihar"],
    )

    current: bool = Field(
        default=False,
        description="Whether this is the current session.",
    )

    created_at: datetime = Field(
        ...,
        description="Session creation timestamp.",
    )

    last_activity: datetime = Field(
        ...,
        description="Last activity timestamp.",
    )


# ==========================================================
# Revoke Session
# ==========================================================


class RevokeSessionRequest(BaseModel):
    """
    Request schema for revoking
    an active session.
    """

    session_id: str = Field(
        ...,
        description="Session identifier.",
    )


# ==========================================================
# Session List Response
# ==========================================================


class SessionListResponse(BaseModel):
    """
    Response returned when listing
    active sessions.
    """

    total: int = Field(
        ...,
        description="Total active sessions.",
        examples=[3],
    )

    sessions: list[SessionResponse] = Field(
        ...,
        description="List of active sessions.",
    )


# ==========================================================
# Logout Response
# ==========================================================


class LogoutResponse(BaseModel):
    """
    Response returned after logout.
    """

    success: bool = Field(
        default=True,
        description="Whether logout succeeded.",
    )

    message: str = Field(
        default="Logout successful.",
        description="Logout result message.",
    )


# ==========================================================
# Password Reset Response
# ==========================================================


class PasswordResetResponse(BaseModel):
    """
    Response returned after
    successfully resetting a password.
    """

    success: bool = Field(
        default=True,
        description="Whether the password reset succeeded.",
    )

    message: str = Field(
        default="Password reset successful.",
        description="Operation result message.",
    )


# ==========================================================
# Email Verification Response
# ==========================================================


class EmailVerificationResponse(BaseModel):
    """
    Response returned after
    successful email verification.
    """

    success: bool = Field(
        default=True,
        description="Whether email verification succeeded.",
    )

    verified: bool = Field(
        default=True,
        description="Email verification status.",
    )

    message: str = Field(
        default="Email verified successfully.",
        description="Operation result message.",
    )