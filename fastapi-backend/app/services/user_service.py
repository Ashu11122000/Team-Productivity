"""
User Service

Business Logic Layer for User Management.

Responsibilities
----------------
- User registration
- User retrieval
- User activation/deactivation
- RBAC validation
- Email verification
- Password management
- Refresh token management
- User lifecycle management

Architecture
------------
API Routes
      │
      ▼
UserService
      │
      ▼
UserRepository
      │
      ▼
SQLAlchemy ORM
      │
      ▼
PostgreSQL
"""

from __future__ import annotations

from typing import Sequence

from fastapi import HTTPException, status
from structlog import get_logger

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = get_logger(__name__)

DEFAULT_ROLE = "MEMBER"
ADMIN_ROLE = "ADMIN"


class UserService:
    """
    Service responsible for all user-related business logic.

    This service should never communicate with SQLAlchemy
    directly. All persistence operations are delegated to
    UserRepository.
    """

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    @staticmethod
    def _raise_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    @staticmethod
    def _raise_email_exists() -> None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    @staticmethod
    def _raise_inactive() -> None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    @staticmethod
    def _raise_admin_required() -> None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    # =====================================================
    # CREATE OPERATIONS
    # =====================================================

    def create_user(
        self,
        *,
        email: str,
        password: str,
        role: str = DEFAULT_ROLE,
    ) -> User:
        """
        Register a new user.

        Business Rules
        --------------
        - Email must be unique.
        - Password must be hashed.
        - New users are active by default.
        - Email is initially unverified.
        """

        if self.repository.email_exists(email):
            logger.warning(
                "User registration failed: email already exists",
                email=email,
            )
            self._raise_email_exists()

        user = User(
            email=email,
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
            is_verified=False,
        )

        created_user = self.repository.create(user)

        logger.info(
            "User created successfully",
            user_id=created_user.id,
            email=created_user.email,
        )

        return created_user

    # =====================================================
    # READ OPERATIONS
    # =====================================================

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User:
        """
        Retrieve user by ID.
        """

        user = self.repository.get_by_id(user_id)

        if user is None:
            self._raise_not_found()

        return user

    def get_user_by_email(
        self,
        email: str,
    ) -> User:
        """
        Retrieve user by email.
        """

        user = self.repository.get_by_email(email)

        if user is None:
            self._raise_not_found()

        return user

    def get_active_user_by_id(
        self,
        user_id: int,
    ) -> User:
        """
        Retrieve an active user.

        Used by:

        - Authentication
        - JWT validation
        - Current user endpoint
        """

        user = self.get_user_by_id(user_id)

        if not user.is_active:
            self._raise_inactive()

        return user

    # =====================================================
    # LIST OPERATIONS
    # =====================================================

    def list_users(
        self,
        *,
        page: int = 1,
        limit: int = 20,
        active_only: bool = False,
    ) -> tuple[int, Sequence[User]]:
        """
        Retrieve paginated users.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        users = self.repository.list_users(
            skip=skip,
            limit=limit,
            active_only=active_only,
        )

        total = self.repository.count_users()

        return total, users

    def search_users(
        self,
        keyword: str,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[int, Sequence[User]]:
        """
        Search users by email or role.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        users = self.repository.search(
            keyword=keyword,
            skip=skip,
            limit=limit,
        )

        return len(users), users

    def get_verified_users(
        self,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve verified users.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        return self.repository.list_verified_users(
            skip=skip,
            limit=limit,
        )
            # =====================================================
    # RBAC VALIDATION
    # =====================================================

    def validate_admin(
        self,
        current_user: User,
    ) -> None:
        """
        Validate that the current user has administrator privileges.

        Raises:
            HTTPException: If the user is not an administrator.
        """
        if current_user.role.upper() != ADMIN_ROLE:
            logger.warning(
                "Admin access denied",
                user_id=current_user.id,
                email=current_user.email,
                role=current_user.role,
            )
            self._raise_admin_required()

    def validate_user_access(
        self,
        current_user: User,
        target_user_id: int,
    ) -> None:
        """
        Validate whether the current user can access another user's
        resources.

        Rules:
        - Administrators can access any user.
        - Users can access only their own resources.
        """

        if current_user.role.upper() == ADMIN_ROLE:
            return

        if current_user.id != target_user_id:
            logger.warning(
                "Unauthorized user access",
                current_user_id=current_user.id,
                target_user_id=target_user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

    # =====================================================
    # ACCOUNT STATUS
    # =====================================================

    def activate_user(
        self,
        *,
        current_user: User,
        user_id: int,
    ) -> User:
        """
        Activate a user account.

        Admin only.
        """

        self.validate_admin(current_user)

        user = self.get_user_by_id(user_id)

        if user.is_active:
            return user

        activated_user = self.repository.activate(user)

        logger.info(
            "User activated",
            admin_id=current_user.id,
            user_id=activated_user.id,
        )

        return activated_user

    def deactivate_user(
        self,
        *,
        current_user: User,
        user_id: int,
    ) -> User:
        """
        Deactivate a user account.

        Admin only.
        """

        self.validate_admin(current_user)

        user = self.get_user_by_id(user_id)

        if not user.is_active:
            return user

        deactivated_user = self.repository.deactivate(user)

        logger.info(
            "User deactivated",
            admin_id=current_user.id,
            user_id=deactivated_user.id,
        )

        return deactivated_user

    def verify_user(
        self,
        user_id: int,
    ) -> User:
        """
        Mark a user's email as verified.
        """

        user = self.get_user_by_id(user_id)

        if user.is_verified:
            return user

        verified_user = self.repository.verify_user(user)

        logger.info(
            "User verified",
            user_id=verified_user.id,
        )

        return verified_user

    # =====================================================
    # ROLE MANAGEMENT
    # =====================================================

    def update_role(
        self,
        *,
        current_user: User,
        user_id: int,
        role: str,
    ) -> User:
        """
        Update a user's role.

        Admin only.
        """

        self.validate_admin(current_user)

        user = self.get_user_by_id(user_id)

        updated_user = self.repository.update_role(
            user=user,
            role=role.upper(),
        )

        logger.info(
            "User role updated",
            admin_id=current_user.id,
            user_id=updated_user.id,
            role=updated_user.role,
        )

        return updated_user

    # =====================================================
    # LOGIN / SESSION MANAGEMENT
    # =====================================================

    def update_last_login(
        self,
        user: User,
    ) -> User:
        """
        Update the user's last successful login timestamp.
        """

        updated_user = self.repository.update_last_login(user)

        logger.info(
            "Last login updated",
            user_id=updated_user.id,
        )

        return updated_user

    def update_refresh_token_hash(
        self,
        *,
        user: User,
        token_hash: str | None,
    ) -> User:
        """
        Store or clear the user's refresh token hash.

        Supports refresh-token rotation and logout.
        """

        updated_user = self.repository.update_refresh_token_hash(
            user=user,
            token_hash=token_hash,
        )

        logger.debug(
            "Refresh token hash updated",
            user_id=updated_user.id,
        )

        return updated_user
    
        # =====================================================
    # PASSWORD MANAGEMENT
    # =====================================================

    def change_password(
        self,
        *,
        user: User,
        new_password: str,
    ) -> User:
        """
        Change a user's password.

        Business Rules
        --------------
        - Password is always stored as a secure hash.
        - Services are responsible for validating the old
          password before calling this method.
        """

        user.hashed_password = hash_password(new_password)

        updated_user = self.repository.update(user)

        logger.info(
            "Password changed",
            user_id=updated_user.id,
        )

        return updated_user

    # =====================================================
    # DELETE OPERATIONS
    # =====================================================

    def soft_delete_user(
        self,
        *,
        current_user: User,
        user_id: int,
    ) -> User:
        """
        Soft delete a user.

        The record remains in the database but becomes
        inaccessible to normal application queries.

        Admin only.
        """

        self.validate_admin(current_user)

        user = self.get_user_by_id(user_id)

        deleted_user = self.repository.soft_delete(user)

        logger.info(
            "User soft deleted",
            admin_id=current_user.id,
            user_id=deleted_user.id,
        )

        return deleted_user

    def restore_user(
        self,
        *,
        current_user: User,
        user_id: int,
    ) -> User:
        """
        Restore a previously soft-deleted user.

        Admin only.
        """

        self.validate_admin(current_user)

        user = self.get_user_by_id(user_id)

        restored_user = self.repository.restore(user)

        logger.info(
            "User restored",
            admin_id=current_user.id,
            user_id=restored_user.id,
        )

        return restored_user

    def delete_user(
        self,
        *,
        current_user: User,
        user_id: int,
    ) -> None:
        """
        Permanently delete a user.

        WARNING
        -------
        This operation cannot be undone.

        Admin only.
        """

        self.validate_admin(current_user)

        user = self.get_user_by_id(user_id)

        self.repository.hard_delete(user)

        logger.warning(
            "User permanently deleted",
            admin_id=current_user.id,
            deleted_user_id=user.id,
        )

    # =====================================================
    # INFORMATION HELPERS
    # =====================================================

    def user_exists(
        self,
        user_id: int,
    ) -> bool:
        """
        Check whether a user exists.
        """

        return self.repository.exists(user_id)

    def email_available(
        self,
        email: str,
    ) -> bool:
        """
        Check whether an email address is available.
        """

        return self.repository.is_email_available(email)

    def get_active_users(
        self,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve active users.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        return self.repository.get_active_users(
            skip=skip,
            limit=limit,
        )

    def get_inactive_users(
        self,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve inactive users.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        return self.repository.get_inactive_users(
            skip=skip,
            limit=limit,
        )

    def get_users_by_role(
        self,
        *,
        role: str,
        page: int = 1,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve users belonging to a specific role.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        return self.repository.get_by_role(
            role=role.upper(),
            skip=skip,
            limit=limit,
        )

    # =====================================================
    # BULK OPERATIONS
    # =====================================================

    def deactivate_all_users(
        self,
        *,
        current_user: User,
    ) -> int:
        """
        Deactivate all active users.

        Admin only.

        Returns:
            Number of affected users.
        """

        self.validate_admin(current_user)

        affected = self.repository.deactivate_all()

        logger.warning(
            "Bulk user deactivation completed",
            admin_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    # =====================================================
    # FUTURE EXTENSION POINTS
    # =====================================================

    def assign_permissions(self) -> None:
        """
        Future:
        - Permission system
        - RBAC expansion
        """
        raise NotImplementedError

    def enable_mfa(self) -> None:
        """
        Future:
        - Multi-factor authentication
        """
        raise NotImplementedError

    def disable_mfa(self) -> None:
        """
        Future:
        - Disable multi-factor authentication
        """
        raise NotImplementedError

    def lock_account(self) -> None:
        """
        Future:
        - Temporary account lock
        - Brute-force protection
        """
        raise NotImplementedError

    def unlock_account(self) -> None:
        """
        Future:
        - Unlock user account
        """
        raise NotImplementedError

    def resend_verification_email(self) -> None:
        """
        Future:
        - Background email queue
        - SMTP / SendGrid / SES integration
        """
        raise NotImplementedError

    def send_password_reset_email(self) -> None:
        """
        Future:
        - Password reset workflow
        """
        raise NotImplementedError