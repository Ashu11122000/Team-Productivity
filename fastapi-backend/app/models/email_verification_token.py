"""
Email verification token model.

Responsibilities:
- Store hashed email verification tokens.
- Verify newly registered users.
- Support email verification token expiration.
- Prevent token reuse.
- Allow secure email verification flow.

Architecture:

User
 │
 └──────────────► EmailVerificationToken
                      │
                      ├── Token Hash
                      ├── Expiration
                      ├── Verification Status
                      └── One-time Use
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


class EmailVerificationToken(Base, BaseModelMixin):
    """
    Stores hashed email verification tokens.
    """

    __tablename__ = "email_verification_tokens"

    __table_args__ = (
        Index("idx_email_verification_user", "user_id"),
        Index("idx_email_verification_hash", "token_hash"),
        Index("idx_email_verification_expires", "expires_at"),
        Index("idx_email_verification_used", "is_used"),
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
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=24),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Verification Status
    # ------------------------------------------------------------------

    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    user: Mapped["User"] = relationship(
        "User",
        back_populates="email_verification_tokens",
        lazy="selectin",
    )

    # ------------------------------------------------------------------
    # Helper Properties
    # ------------------------------------------------------------------

    @property
    def is_expired(self) -> bool:
        """
        Return True if the verification token has expired.
        """
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def is_valid(self) -> bool:
        """
        Return True if the token is usable.
        """
        return not self.is_used and not self.is_expired

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def mark_used(self) -> None:
        """
        Mark the verification token as used.
        """
        self.is_used = True
        self.verified_at = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Object Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<EmailVerificationToken("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"used={self.is_used}"
            f")>"
        )

    def __str__(self) -> str:
        return f"EmailVerificationToken({self.id})"