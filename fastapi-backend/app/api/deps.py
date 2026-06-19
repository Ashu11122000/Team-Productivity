# List of dependencies for FastAPI routes, including authentication, and role-based access control (RBAC) utilities
from typing import List

from fastapi import Depends, HTTPException, status

# OAuth2PasswordBearer for handling OAuth2 authentication, Session for database session management
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService

# OAuth2PasswordBearer instance for handling OAuth2 authentication, specifying the token URL for Login
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Retrieve authenticated user from JWT token.
    """

    payload = decode_access_token(token)

    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = UserService.get_user_by_email(
        db=db,
        email=email,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


# Role-Base Access Control (RBAC) Dependencies used for FastAPI routes to restricts access to endpoints based on user roles
def require_role(required_role: str):
    """
    Restrict endpoint to a single role.
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker


# Role-Base Access Control (RBAC) Dependencies used for FastAPI routes to restricts access to endpoints based on user roles
def require_roles(allowed_roles: List[str]):
    """
    Restrict endpoint to multiple roles.
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        return current_user

    return role_checker