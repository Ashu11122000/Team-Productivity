"""
User-related Pydantic schemas.

This module defines request and response schemas used by:

- Authentication
- User Management
- JWT Authentication
- Refresh Tokens
- Session Management
- Email Verification
- Password Reset
- RBAC
- User Analytics

Architecture:

API Routes
     │
     ▼
Services
     │
     ▼
Repositories
     │
     ▼
SQLAlchemy Models
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# Base User Schema
# ==========================================================


class UserBase(BaseModel):
    """
    Base schema shared by multiple user request models.
    """

    email: EmailStr = Field(
        ...,
        description="Unique user email address.",
        examples=["john.doe@example.com"],
    )


# ==========================================================
# User Registration
# ==========================================================


class UserCreate(UserBase):
    """
    Request schema for user registration.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password.",
        examples=["StrongPassword123!"],
    )


# ==========================================================
# User Login
# ==========================================================


class UserLogin(UserBase):
    """
    Request schema for authenticating a user.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password.",
    )

    remember_me: bool = Field(
        default=False,
        description="Whether to keep the user logged in.",
    )


# ==========================================================
# JWT Token Response
# ==========================================================


class TokenResponse(BaseModel):
    """
    JWT authentication response.

    Returned after:

    - Login
    - Refresh token rotation
    """

    access_token: str = Field(
        ...,
        description="JWT access token.",
    )

    refresh_token: str = Field(
        ...,
        description="Refresh token.",
    )

    token_type: str = Field(
        default="bearer",
        description="Authentication scheme.",
        examples=["bearer"],
    )

    expires_in: int = Field(
        ...,
        description="Access token expiration time (seconds).",
        examples=[3600],
    )


# ==========================================================
# Refresh Token Request
# ==========================================================


class RefreshTokenRequest(BaseModel):
    """
    Request schema for refreshing an access token.
    """

    refresh_token: str = Field(
        ...,
        description="Previously issued refresh token.",
    )


# ==========================================================
# Refresh Token Response
# ==========================================================


class RefreshTokenResponse(TokenResponse):
    """
    Response returned after successful refresh token
    rotation.

    Inherits every field from TokenResponse.
    """

    pass


# ==========================================================
# Logout Request
# ==========================================================


class LogoutRequest(BaseModel):
    """
    Logout request.

    Supports:

    - Current device logout
    - Logout from every device
    """

    refresh_token: str = Field(
        ...,
        description="Refresh token to revoke.",
    )

    logout_all_devices: bool = Field(
        default=False,
        description="Whether to revoke every active session.",
    )
    
    # ==========================================================
# User Profile Update
# ==========================================================


class UserUpdate(BaseModel):
    """
    Request schema for updating the authenticated user's profile.

    Only profile fields are editable by the user.
    Administrative fields are handled separately.
    """

    email: EmailStr | None = Field(
        default=None,
        description="Updated email address.",
        examples=["john.doe@example.com"],
    )


# ==========================================================
# User Role Update (Admin Only)
# ==========================================================


class UserRoleUpdate(BaseModel):
    """
    Request schema for updating a user's role.

    Accessible only to administrators.
    """

    role: Literal["ADMIN", "MEMBER"] = Field(
        ...,
        description="New role assigned to the user.",
        examples=["MEMBER"],
    )


# ==========================================================
# User Status Update (Admin Only)
# ==========================================================


class UserStatusUpdate(BaseModel):
    """
    Request schema for activating or deactivating
    a user account.

    Accessible only to administrators.
    """

    is_active: bool = Field(
        ...,
        description="Whether the account should remain active.",
        examples=[True],
    )


# ==========================================================
# User Response
# ==========================================================


class UserResponse(BaseModel):
    """
    Standard user response returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique user identifier.",
        examples=[1],
    )

    email: EmailStr = Field(
        ...,
        description="User email address.",
    )

    role: Literal["ADMIN", "MEMBER"] = Field(
        ...,
        description="User role.",
        examples=["MEMBER"],
    )

    is_active: bool = Field(
        ...,
        description="Whether the account is active.",
        examples=[True],
    )

    last_login: datetime | None = Field(
        default=None,
        description="Timestamp of the user's last successful login.",
    )

    created_at: datetime = Field(
        ...,
        description="Timestamp when the account was created.",
    )

    updated_at: datetime = Field(
        ...,
        description="Timestamp when the account was last updated.",
    )


# ==========================================================
# User Summary
# ==========================================================


class UserSummary(BaseModel):
    """
    Lightweight user representation.

    Useful inside nested API responses,
    activity logs and audit records.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique user identifier.",
        examples=[1],
    )

    email: EmailStr = Field(
        ...,
        description="User email address.",
    )

    role: Literal["ADMIN", "MEMBER"] = Field(
        ...,
        description="User role.",
    )


# ==========================================================
# Current Authenticated User
# ==========================================================


class CurrentUser(BaseModel):
    """
    User information extracted from the validated JWT.

    Used internally by:

    - Authentication dependencies
    - Authorization
    - RBAC
    - Ownership validation
    - Service layer
    """

    user_id: int = Field(
        ...,
        description="Authenticated user identifier.",
    )

    email: EmailStr = Field(
        ...,
        description="Authenticated user email.",
    )

    role: Literal["ADMIN", "MEMBER"] = Field(
        ...,
        description="Authenticated user role.",
    )

    is_active: bool = Field(
        ...,
        description="Whether the authenticated account is active.",
    )

    permissions: list[str] = Field(
        default_factory=list,
        description="Future RBAC permissions.",
        examples=[["notes:read", "notes:create"]],
    )


# ==========================================================
# User Status Response
# ==========================================================


class UserStatusResponse(BaseModel):
    """
    Response returned after changing
    a user's account status.
    """

    success: bool = Field(
        default=True,
        description="Whether the operation succeeded.",
    )

    user_id: int = Field(
        ...,
        description="Affected user identifier.",
    )

    is_active: bool = Field(
        ...,
        description="Current account status.",
    )

    message: str = Field(
        ...,
        description="Operation result message.",
        examples=["User account updated successfully."],
    )
    
    # ==========================================================
# Change Password
# ==========================================================


class ChangePasswordRequest(BaseModel):
    """
    Request schema for changing the authenticated
    user's password.
    """

    current_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Current account password.",
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New account password.",
        examples=["MyNewStrongPassword123!"],
    )


# ==========================================================
# Forgot Password
# ==========================================================


class ForgotPasswordRequest(BaseModel):
    """
    Request schema for initiating password reset.
    """

    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=["john.doe@example.com"],
    )


# ==========================================================
# Reset Password
# ==========================================================


class ResetPasswordRequest(BaseModel):
    """
    Request schema for resetting a forgotten password.
    """

    token: str = Field(
        ...,
        description="Password reset token.",
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password.",
    )


# ==========================================================
# Email Verification
# ==========================================================


class VerifyEmailRequest(BaseModel):
    """
    Request schema for verifying a user's email.
    """

    token: str = Field(
        ...,
        description="Email verification token.",
    )


class ResendVerificationRequest(BaseModel):
    """
    Request schema for resending
    the email verification link.
    """

    email: EmailStr = Field(
        ...,
        description="Registered email address.",
    )


# ==========================================================
# Shared JWT Payload
# ==========================================================


class TokenPayload(BaseModel):
    """
    Shared JWT payload contract between
    FastAPI and NestJS.

    FastAPI:
        - Issues JWT

    NestJS:
        - Validates JWT
    """

    sub: str = Field(
        ...,
        description="Authenticated user identifier.",
        examples=["1"],
    )

    email: EmailStr = Field(
        ...,
        description="Authenticated user email.",
    )

    role: Literal["ADMIN", "MEMBER"] = Field(
        ...,
        description="Authenticated user role.",
    )

    aud: str = Field(
        ...,
        description="JWT audience.",
        examples=["team-productivity-users"],
    )

    type: Literal["access", "refresh"] = Field(
        ...,
        description="JWT token type.",
        examples=["access"],
    )

    exp: int = Field(
        ...,
        description="Expiration timestamp.",
    )


# ==========================================================
# Session Response
# ==========================================================


class SessionResponse(BaseModel):
    """
    Represents an active authenticated session.

    Future use:
    - Multi-device login
    - Session management
    - Security dashboard
    """

    session_id: str = Field(
        ...,
        description="Unique session identifier.",
    )

    device: str | None = Field(
        default=None,
        description="Client device.",
        examples=["Windows Desktop"],
    )

    ip_address: str | None = Field(
        default=None,
        description="Client IP address.",
        examples=["192.168.1.100"],
    )

    last_activity: datetime = Field(
        ...,
        description="Last activity timestamp.",
    )

    current: bool = Field(
        default=False,
        description="Whether this is the current session.",
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
        description="Session identifier to revoke.",
    )


# ==========================================================
# User Statistics
# ==========================================================


class UserStatistics(BaseModel):
    """
    User statistics for dashboards,
    administration and analytics.
    """

    total_users: int = Field(
        ...,
        description="Total registered users.",
        examples=[250],
    )

    active_users: int = Field(
        ...,
        description="Total active users.",
        examples=[240],
    )

    inactive_users: int = Field(
        ...,
        description="Total inactive users.",
        examples=[10],
    )

    verified_users: int = Field(
        ...,
        description="Users with verified email addresses.",
        examples=[225],
    )

    admin_users: int = Field(
        ...,
        description="Total administrators.",
        examples=[5],
    )

    member_users: int = Field(
        ...,
        description="Total members.",
        examples=[245],
    )

    new_users_today: int = Field(
        ...,
        description="Users registered today.",
        examples=[12],
    )