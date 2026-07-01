"""
Password reset token model.

Responsibilities:
- Store hashed password reset tokens.
- Support secure password reset workflow.
- Prevent token reuse.
- Handle token expiration.
- Maintain audit history for reset requests.

Architecture:

User
 │
 └──────────────► PasswordResetToken
                      │
                      ├── Token Hash
                      ├── Expiration
                      ├── One-time Use
                      └── Reset History
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_model import BaseModelMixin

if TYPE_CHECKING:
    from app.models.user import User


class PasswordResetToken(Base, BaseModelMixin):
    """
    Stores hashed password reset tokens.
    """

    __tablename__ = "password_reset_tokens"

    __table_args__ = (
        Index("idx_password_reset_user", "user_id"),
        Index("idx_password_reset_hash", "token_hash"),
        Index("idx_password_reset_expires", "expires_at"),
        Index("idx_password_reset_used", "is_used"),
    )

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Token Information
    # ------------------------------------------------------------------

    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=30),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Reset Status
    # ------------------------------------------------------------------

    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    user: Mapped["User"] = relationship(
        "User",
        back_populates="password_reset_tokens",
        lazy="selectin",
    )

    # ------------------------------------------------------------------
    # Helper Properties
    # ------------------------------------------------------------------

    @property
    def is_expired(self) -> bool:
        """
        Return True if the password reset token has expired.
        """
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def is_valid(self) -> bool:
        """
        Return True if the token can still be used.
        """
        return not self.is_used and not self.is_expired

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def mark_used(self) -> None:
        """
        Mark the password reset token as used.
        """
        self.is_used = True
        self.used_at = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Object Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<PasswordResetToken("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"used={self.is_used}"
            f")>"
        )

    def __str__(self) -> str:
        return f"PasswordResetToken({self.id})"