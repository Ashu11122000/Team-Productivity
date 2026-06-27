"""
Reusable FastAPI dependencies.

This module provides authentication and authorization dependencies
used across the Team Productivity Platform.

Responsibilities:
- Retrieve the authenticated user
- Validate active users
- Enforce role-based access control (RBAC)

Future Extensions:
- Permission-based authorization
- Workspace membership validation
- Team membership validation
"""

from collections.abc import Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import logger
from app.core.security import decode_access_token
from app.db.session import get_db
from app.exceptions.auth_exceptions import (
    InactiveUserException,
    InvalidTokenException,
)
from app.exceptions.user_exceptions import UserNotFoundException
from app.models.user import User
from app.services.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Retrieve the authenticated user from the JWT access token.

    Raises:
        InvalidTokenException:
            If the JWT is invalid or does not contain a subject.

        UserNotFoundException:
            If the authenticated user does not exist.
    """

    payload = decode_access_token(token)

    subject = payload.get("sub")

    if not subject:
        logger.warning(
            "JWT authentication failed: missing subject.",
        )
        raise InvalidTokenException()

    # Currently, the JWT subject contains the user's email.
    # This can later be changed to a user ID without changing
    # any route logic.
    user = UserService.get_user_by_email(
        db=db,
        email=subject,
    )

    if user is None:
        logger.warning(
            "Authenticated user not found.",
            email=subject,
        )
        raise UserNotFoundException()

    logger.info(
        "User authenticated successfully.",
        user_id=user.id,
    )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure the authenticated user is active.

    Raises:
        InactiveUserException:
            If the user's account is inactive.
    """

    if not current_user.is_active:
        logger.warning(
            "Inactive user attempted authentication.",
            user_id=current_user.id,
        )
        raise InactiveUserException()

    return current_user


def require_role(
    required_role: str,
) -> Callable[..., User]:
    """
    Restrict an endpoint to a single role.

    Example:
        @router.get(...)
        async def endpoint(
            current_user: User = Depends(require_role("admin"))
        ):
            ...
    """

    def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role != required_role:
            logger.warning(
                "Role authorization failed.",
                user_id=current_user.id,
                required_role=required_role,
                actual_role=current_user.role,
            )
            raise InvalidTokenException(
                "Insufficient permissions."
            )

        return current_user

    return role_checker


def require_roles(
    allowed_roles: list[str],
) -> Callable[..., User]:
    """
    Restrict an endpoint to multiple roles.

    Example:
        Depends(require_roles(["admin", "manager"]))
    """

    def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            logger.warning(
                "Role authorization failed.",
                user_id=current_user.id,
                allowed_roles=allowed_roles,
                actual_role=current_user.role,
            )
            raise InvalidTokenException(
                "Insufficient permissions."
            )

        return current_user

    return role_checker