"""
User-related Pydantic schemas.

Responsibilities:
- User registration
- Authentication
- JWT payloads
- User profile responses
- Password reset
- Email verification
- Refresh tokens
- Logout
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# User Registration
# ==========================================================

class UserCreate(BaseModel):
    """
    Request schema for user registration.
    """

    email: EmailStr = Field(
        ...,
        description="Unique user email address",
        examples=["john.doe@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
        examples=["StrongPassword123!"],
    )


# ==========================================================
# User Login
# ==========================================================

class UserLogin(BaseModel):
    """
    Login request.
    """

    email: EmailStr = Field(
        ...,
        description="Registered email",
        examples=["john.doe@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
    )


# ==========================================================
# JWT Responses
# ==========================================================

class TokenResponse(BaseModel):
    """
    Authentication response.
    """

    access_token: str

    refresh_token: str

    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Refresh access token.
    """

    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """
    Returned after refreshing tokens.
    """

    access_token: str

    refresh_token: str

    token_type: str = "bearer"


# ==========================================================
# Logout
# ==========================================================

class LogoutRequest(BaseModel):
    """
    Logout request.
    """

    refresh_token: str


# ==========================================================
# Forgot Password
# ==========================================================

class ForgotPasswordRequest(BaseModel):
    """
    Forgot password request.
    """

    email: EmailStr


# ==========================================================
# Reset Password
# ==========================================================

class ResetPasswordRequest(BaseModel):
    """
    Reset password request.
    """

    token: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


# ==========================================================
# Email Verification
# ==========================================================

class VerifyEmailRequest(BaseModel):
    """
    Verify email request.
    """

    token: str


class ResendVerificationRequest(BaseModel):
    """
    Resend verification email.
    """

    email: EmailStr


# ==========================================================
# User Response
# ==========================================================

class UserResponse(BaseModel):
    """
    Standard user response.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    email: EmailStr

    role: Literal["ADMIN", "MEMBER"]

    is_active: bool

    is_verified: bool

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Current Authenticated User
# ==========================================================

class CurrentUser(BaseModel):
    """
    Authenticated user context.
    """

    user_id: int

    email: EmailStr

    role: Literal["ADMIN", "MEMBER"]


# ==========================================================
# Shared JWT Payload
# ==========================================================

class TokenPayload(BaseModel):
    """
    JWT payload shared with NestJS.
    """

    sub: str

    email: EmailStr

    role: Literal["ADMIN", "MEMBER"]

    aud: str

    type: str

    exp: int


# ==========================================================
# Generic Message Response
# ==========================================================

class MessageResponse(BaseModel):
    """
    Generic success response.
    """

    success: bool = True

    message: str
