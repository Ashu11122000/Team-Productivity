"""
User model.

Responsibilities:
- Authentication
- Authorization
- User management
- JWT identity source
- Own notes and refresh tokens

Architecture:

User
 │
 ├────────────► Note
 │
 ├────────────► RefreshToken
 │
 └────────────► Future:
                - UserPreference
                - UserSession
                - ActivityLog
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_model import BaseModelMixin

if TYPE_CHECKING:
    from .note import Note
    from .refresh_token import RefreshToken
    from .user_preference import UserPreference
    from .user_session import UserSession
    from .email_verification_token import EmailVerificationToken
    from .password_reset_token import PasswordResetToken


class User(Base, BaseModelMixin):
    """
    User model.

    FastAPI Ownership:
    - Authentication
    - Authorization
    - User Management

    JWT Source of Truth:
    - id
    - email
    - role
    """

    __tablename__ = "users"

    __table_args__ = (
        Index("idx_users_email", "email"),
        Index("idx_users_role", "role"),
        Index("idx_users_active", "is_active"),
        Index("idx_users_verified", "is_verified"),
    )

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # User Status
    # ------------------------------------------------------------------

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="Member",
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",  
    )
    
    preferences: Mapped["UserPreference | None"] = relationship(
        "UserPreference",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
        lazy="selectin", 
    )
    
    email_verification_tokens: Mapped[list["EmailVerificationToken"]] = relationship(
        "EmailVerificationToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin", 
    )
    
    password_reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(
        "PasswordResetToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin", 
    )
    
    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    notes: Mapped[list["Note"]] = relationship(
        "Note",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def mark_verified(self) -> None:
        """
        Mark the user as verified.
        """
        self.is_verified = True

    def update_last_login(self) -> None:
        """
        Update the last login timestamp.
        """
        self.last_login_at = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Object Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<User("
            f"id={self.id}, "
            f"email={self.email!r}, "
            f"role={self.role!r}"
            f")>"
        )

    def __str__(self) -> str:
        return self.email