"""
Authentication Service

Responsibilities
----------------
- User Registration
- User Authentication
- JWT Access Token Generation
- Refresh Token Rotation
- Logout
- Logout From All Devices
- Password Reset
- Email Verification
- Session Management

Architecture

API Routes
      │
      ▼
AuthService
      │
      ▼
Repositories
      │
      ▼
Security Utilities
      │
      ▼
Database
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import (
    BEARER_TOKEN_TYPE,
    ROLE_MEMBER,
)
from app.core.logging import logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    generate_secure_token,
    get_current_utc_time,
    hash_password,
    hash_refresh_token,
    verify_password,
)

from app.integrations.email_client import EmailClient

from app.models.refresh_token import RefreshToken
from app.models.user import User

from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.user_repository import UserRepository

from app.schemas.auth import (
    LoginResponse,
    LogoutResponse,
    PasswordResetResponse,
    RefreshTokenResponse,
)

from app.schemas.user import (
    ForgotPasswordRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    ResendVerificationRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    VerifyEmailRequest,
)

from app.exceptions.auth_exceptions import (
    AuthenticationException,
    EmailAlreadyVerifiedException,
    EmailVerificationException,
    InactiveUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    PasswordResetException,
    RefreshTokenException,
)

from app.exceptions.user_exceptions import (
    DuplicateEmailException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


class AuthService:
    """
    Authentication Service.

    Business logic for:

    - User Registration
    - Login
    - Refresh Tokens
    - Logout
    - Password Reset
    - Email Verification

    Repositories are responsible only for persistence.
    All business rules belong here.
    """

    def __init__(
        self,
        db: Session,
    ) ->None:
        """
        Initialize the authentication service.

        Args:
            db:
                SQLAlchemy database session.
        """

        self.db = db

        self.user_repository = UserRepository(db)

        self.refresh_token_repository = (
            RefreshTokenRepository(db)
        )

        self.email_client = EmailClient()

        logger.debug(
            "AuthService initialized.",
        )