"""
Refresh Token Repository

Responsibilities:
- Persist refresh tokens.
- Manage refresh token lifecycle.
- Support secure session management.
- Provide token lookup and validation.

Architecture:

API Route
      ↓
Auth Service
      ↓
RefreshTokenRepository
      ↓
SQLAlchemy ORM
      ↓
PostgreSQL
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    """
    Repository responsible for RefreshToken persistence.

    Business logic belongs in the authentication service.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # ==========================================================
    # CREATE OPERATIONS
    # ==========================================================

    def create(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        """
        Persist a refresh token.
        """
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token

    # ==========================================================
    # READ OPERATIONS
    # ==========================================================

    def get_by_id(
        self,
        token_id: int,
    ) -> RefreshToken | None:
        """
        Retrieve a refresh token by ID.
        """
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.id == token_id,
            )
            .first()
        )

    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """
        Retrieve a refresh token using its hash.
        """
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash,
            )
            .first()
        )

    def get_active_token(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """
        Retrieve an active refresh token.
        """
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
            .first()
        )

    def get_user_tokens(
        self,
        user_id: int,
    ) -> Sequence[RefreshToken]:
        """
        Retrieve every refresh token belonging to a user.
        """
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
            )
            .order_by(
                RefreshToken.created_at.desc()
            )
            .all()
        )

    def get_active_user_tokens(
        self,
        user_id: int,
    ) -> Sequence[RefreshToken]:
        """
        Retrieve active refresh tokens for a user.
        """
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
            .order_by(
                RefreshToken.created_at.desc()
            )
            .all()
        )

    def get_expired_tokens(self) -> Sequence[RefreshToken]:
        """
        Retrieve expired refresh tokens.
        """
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.expires_at <= datetime.now(timezone.utc),
            )
            .all()
        )

    # ==========================================================
    # VALIDATION METHODS
    # ==========================================================

    def exists(
        self,
        token_hash: str,
    ) -> bool:
        """
        Check whether a refresh token exists.
        """
        return (
            self.db.query(RefreshToken.id)
            .filter(
                RefreshToken.token_hash == token_hash,
            )
            .first()
            is not None
        )

    def is_active(
        self,
        token_hash: str,
    ) -> bool:
        """
        Determine whether a refresh token is active.
        """
        return (
            self.db.query(RefreshToken.id)
            .filter(
                RefreshToken.token_hash == token_hash,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
            .first()
            is not None
        )

    def is_expired(
        self,
        token: RefreshToken,
    ) -> bool:
        """
        Check whether a refresh token has expired.
        """
        return token.expires_at <= datetime.now(timezone.utc)

    # ==========================================================
    # COUNT OPERATIONS
    # ==========================================================

    def count_tokens(
        self,
        user_id: int,
    ) -> int:
        """
        Count refresh tokens for a user.
        """
        return (
            self.db.query(func.count(RefreshToken.id))
            .filter(
                RefreshToken.user_id == user_id,
            )
            .scalar()
            or 0
        )

    def count_active_tokens(
        self,
        user_id: int,
    ) -> int:
        """
        Count active refresh tokens.
        """
        return (
            self.db.query(func.count(RefreshToken.id))
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
            .scalar()
            or 0
        )

    def count_revoked_tokens(
        self,
        user_id: int,
    ) -> int:
        """
        Count revoked refresh tokens.
        """
        return (
            self.db.query(func.count(RefreshToken.id))
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(True),
            )
            .scalar()
            or 0
        )
            # ==========================================================
    # UPDATE OPERATIONS
    # ==========================================================

    def update(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        """
        Persist changes to a refresh token.
        """
        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token

    def save(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        """
        Alias for update().
        """
        return self.update(refresh_token)

    # ==========================================================
    # TOKEN REVOCATION
    # ==========================================================

    def revoke(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        """
        Revoke a refresh token.
        """

        refresh_token.is_revoked = True
        refresh_token.revoked_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token

    def revoke_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """
        Revoke a refresh token using its hash.
        """

        token = self.get_by_token_hash(token_hash)

        if token is None:
            return None

        return self.revoke(token)

    def revoke_all_for_user(
        self,
        user_id: int,
    ) -> int:
        """
        Revoke every active refresh token belonging to a user.

        Used for:
        - Logout from all devices
        - Password reset
        - Security events

        Returns:
            Number of affected rows.
        """

        affected = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
            )
            .update(
                {
                    RefreshToken.is_revoked: True,
                    RefreshToken.revoked_at: datetime.now(timezone.utc),
                },
                synchronize_session=False,
            )
        )

        self.db.commit()

        return affected

    # ==========================================================
    # DELETE OPERATIONS
    # ==========================================================

    def delete_expired(self) -> int:
        """
        Permanently delete expired refresh tokens.

        Intended for scheduled cleanup tasks.
        """

        affected = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.expires_at <= datetime.now(timezone.utc),
            )
            .delete(
                synchronize_session=False,
            )
        )

        self.db.commit()

        return affected

    def delete_revoked(self) -> int:
        """
        Delete revoked refresh tokens.
        """

        affected = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.is_revoked.is_(True),
            )
            .delete(
                synchronize_session=False,
            )
        )

        self.db.commit()

        return affected

    def hard_delete(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        """
        Permanently remove a refresh token.
        """

        self.db.delete(refresh_token)
        self.db.commit()

    def delete(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        """
        Alias for hard_delete().
        """

        self.hard_delete(refresh_token)

    # ==========================================================
    # BULK OPERATIONS
    # ==========================================================

    def cleanup(self) -> int:
        """
        Remove expired and revoked refresh tokens.

        Returns:
            Number of deleted rows.
        """

        affected = (
            self.db.query(RefreshToken)
            .filter(
                (RefreshToken.expires_at <= datetime.now(timezone.utc))
                | (RefreshToken.is_revoked.is_(True))
            )
            .delete(
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
        Flush pending database changes.
        """
        self.db.flush()

    def refresh(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        """
        Refresh a RefreshToken instance.
        """
        self.db.refresh(refresh_token)

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        self.db.rollback()

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        self.db.commit()

    # ==========================================================
    # SQLALCHEMY HELPERS
    # ==========================================================

    def add(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        """
        Add a refresh token to the session.
        """
        self.db.add(refresh_token)

    def merge(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        """
        Merge a detached RefreshToken instance.
        """
        return self.db.merge(refresh_token)

    def detach(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        """
        Detach a RefreshToken from the current session.
        """
        self.db.expunge(refresh_token)

    def close(self) -> None:
        """
        Close the database session.
        """
        self.db.close()