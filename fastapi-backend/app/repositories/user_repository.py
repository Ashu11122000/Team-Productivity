"""
User Repository

Responsibilities:
- Encapsulate all database operations for the User model.
- Keep business logic out of the data access layer.
- Provide reusable CRUD operations for services.

Architecture:

API Route
    ↓
Service
    ↓
UserRepository
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository responsible for all User database operations.

    This repository should only perform persistence operations.
    Business rules belong in the service layer.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # ==========================================================
    # CREATE OPERATIONS
    # ==========================================================

    def create(self, user: User) -> User:
        """
        Persist a new user.

        Args:
            user: User model instance.

        Returns:
            Newly created user.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ==========================================================
    # READ OPERATIONS
    # ==========================================================

    def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by primary key.

        Args:
            user_id: User ID.

        Returns:
            User instance or None.
        """
        return (
            self.db.query(User)
            .filter(
                User.id == user_id,
                User.deleted_at.is_(None),
            )
            .first()
        )

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email address.

        Args:
            email: User email.

        Returns:
            User instance or None.
        """
        return (
            self.db.query(User)
            .filter(
                User.email == email,
                User.deleted_at.is_(None),
            )
            .first()
        )

    def get_by_refresh_token_hash(
        self,
        token_hash: str,
    ) -> User | None:
        """
        Retrieve a user by refresh token hash.

        Args:
            token_hash: Stored refresh token hash.

        Returns:
            User or None.
        """
        return (
            self.db.query(User)
            .filter(
                User.refresh_token_hash == token_hash,
                User.deleted_at.is_(None),
            )
            .first()
        )

    def email_exists(self, email: str) -> bool:
        """
        Check whether an email already exists.

        Args:
            email: Email address.

        Returns:
            True if email exists.
        """
        return (
            self.db.query(User.id)
            .filter(
                User.email == email,
                User.deleted_at.is_(None),
            )
            .first()
            is not None
        )

    # ==========================================================
    # LIST OPERATIONS
    # ==========================================================

    def list_users(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = False,
    ) -> Sequence[User]:
        """
        Retrieve users with pagination.

        Args:
            skip: Records to skip.
            limit: Maximum records.
            active_only: Only active users.

        Returns:
            List of users.
        """
        query = (
            self.db.query(User)
            .filter(User.deleted_at.is_(None))
        )

        if active_only:
            query = query.filter(User.is_active.is_(True))

        return (
            query.order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_verified_users(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve verified users.

        Args:
            skip: Pagination offset.
            limit: Pagination size.

        Returns:
            List of verified users.
        """
        return (
            self.db.query(User)
            .filter(
                User.is_verified.is_(True),
                User.deleted_at.is_(None),
            )
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        keyword: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Search users.

        Currently searches:
        - email
        - role
        """
        pattern = f"%{keyword}%"

        return (
            self.db.query(User)
            .filter(
                User.deleted_at.is_(None),
                or_(
                    User.email.ilike(pattern),
                    User.role.ilike(pattern),
                ),
            )
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================================
    # COUNT OPERATIONS
    # ==========================================================

    def count_users(self) -> int:
        """
        Count total active (non-deleted) users.
        """
        return (
            self.db.query(func.count(User.id))
            .filter(User.deleted_at.is_(None))
            .scalar()
            or 0
        )

    def count_active_users(self) -> int:
        """
        Count active users.
        """
        return (
            self.db.query(func.count(User.id))
            .filter(
                User.deleted_at.is_(None),
                User.is_active.is_(True),
            )
            .scalar()
            or 0
        )

    def count_verified_users(self) -> int:
        """
        Count verified users.
        """
        return (
            self.db.query(func.count(User.id))
            .filter(
                User.deleted_at.is_(None),
                User.is_verified.is_(True),
            )
            .scalar()
            or 0
        )
        
            # ==========================================================
    # UPDATE OPERATIONS
    # ==========================================================

    def update(self, user: User) -> User:
        """
        Persist changes made to a user.

        Args:
            user: Updated User instance.

        Returns:
            Updated user.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    def save(self, user: User) -> User:
        """
        Save any changes made to a user.

        Alias for update().
        """
        return self.update(user)

    def update_last_login(self, user: User) -> User:
        """
        Update the user's last login timestamp.
        """
        user.last_login_at = func.now()

        self.db.commit()
        self.db.refresh(user)

        return user

    def update_refresh_token_hash(
        self,
        user: User,
        token_hash: str | None,
    ) -> User:
        """
        Store or clear the refresh token hash.
        """
        user.refresh_token_hash = token_hash

        self.db.commit()
        self.db.refresh(user)

        return user

    # ==========================================================
    # ACCOUNT STATUS
    # ==========================================================

    def activate(self, user: User) -> User:
        """
        Activate a user account.
        """
        user.is_active = True

        self.db.commit()
        self.db.refresh(user)

        return user

    def deactivate(self, user: User) -> User:
        """
        Deactivate a user account.
        """
        user.is_active = False

        self.db.commit()
        self.db.refresh(user)

        return user

    def verify_user(self, user: User) -> User:
        """
        Mark the user's email as verified.
        """
        user.is_verified = True

        self.db.commit()
        self.db.refresh(user)

        return user

    # ==========================================================
    # DELETE OPERATIONS
    # ==========================================================

    def soft_delete(self, user: User) -> User:
        """
        Soft delete a user.

        The record remains in the database.
        """
        user.deleted_at = func.now()
        user.is_active = False

        self.db.commit()
        self.db.refresh(user)

        return user

    def restore(self, user: User) -> User:
        """
        Restore a previously soft-deleted user.
        """
        user.deleted_at = None
        user.is_active = True

        self.db.commit()
        self.db.refresh(user)

        return user

    def hard_delete(self, user: User) -> None:
        """
        Permanently delete a user.
        """
        self.db.delete(user)
        self.db.commit()

    # ==========================================================
    # ROLE OPERATIONS
    # ==========================================================

    def update_role(
        self,
        user: User,
        role: str,
    ) -> User:
        """
        Update the user's role.
        """
        user.role = role

        self.db.commit()
        self.db.refresh(user)

        return user

    # ==========================================================
    # EXISTENCE HELPERS
    # ==========================================================

    def exists(self, user_id: int) -> bool:
        """
        Check whether a user exists.
        """
        return (
            self.db.query(User.id)
            .filter(
                User.id == user_id,
                User.deleted_at.is_(None),
            )
            .first()
            is not None
        )

    def is_email_available(
        self,
        email: str,
    ) -> bool:
        """
        Check whether an email address is available.
        """
        return not self.email_exists(email)

    # ==========================================================
    # FILTER OPERATIONS
    # ==========================================================

    def get_active_users(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve active users.
        """
        return (
            self.db.query(User)
            .filter(
                User.deleted_at.is_(None),
                User.is_active.is_(True),
            )
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_inactive_users(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve inactive users.
        """
        return (
            self.db.query(User)
            .filter(
                User.deleted_at.is_(None),
                User.is_active.is_(False),
            )
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_role(
        self,
        role: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Retrieve users belonging to a role.
        """
        return (
            self.db.query(User)
            .filter(
                User.deleted_at.is_(None),
                User.role == role,
            )
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================================
    # BULK OPERATIONS
    # ==========================================================

    def deactivate_all(self) -> int:
        """
        Deactivate all active users.

        Returns:
            Number of affected rows.
        """
        affected = (
            self.db.query(User)
            .filter(
                User.deleted_at.is_(None),
                User.is_active.is_(True),
            )
            .update(
                {User.is_active: False},
                synchronize_session=False,
            )
        )

        self.db.commit()

        return affected

    # ==========================================================
    # SESSION HELPERS
    # ==========================================================

    def flush(self) -> None:
        """
        Flush pending changes.
        """
        self.db.flush()

    def refresh(self, user: User) -> None:
        """
        Refresh a user instance.
        """
        self.db.refresh(user)

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        self.db.rollback()

    # ==========================================================
    # GENERIC DELETE
    # ==========================================================

    def delete(self, user: User) -> None:
        """
        Alias for hard_delete().
        """
        self.hard_delete(user)