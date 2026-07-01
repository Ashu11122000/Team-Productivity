"""
User session model.

Responsibilities:
- Track active user sessions.
- Support multiple logged-in devices.
- Enable logout from a single device.
- Enable logout from all devices.
- Store device metadata.
- Track session activity.
- Support future security analytics.

Architecture:

User
 │
 └──────────────► UserSession
                      │
                      ├── Device Information
                      ├── Browser
                      ├── Operating System
                      ├── IP Address
                      ├── User Agent
                      └── Last Activity
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


class UserSession(Base, BaseModelMixin):
    """
    Stores user login sessions.

    A user may have multiple active sessions,
    one for each logged-in device.
    """

    __tablename__ = "user_sessions"

    __table_args__ = (
        Index("idx_user_sessions_user", "user_id"),
        Index("idx_user_sessions_active", "is_active"),
        Index("idx_user_sessions_expires", "expires_at"),
        Index("idx_user_sessions_last_activity", "last_activity_at"),
        Index("idx_user_sessions_device", "device_id"),
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
    # Device Information
    # ------------------------------------------------------------------

    device_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    device_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    device_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    browser: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Client Information
    # ------------------------------------------------------------------

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Session State
    # ------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=30),
        nullable=False,
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    logged_out_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions",
        lazy="selectin",
    )

    # ------------------------------------------------------------------
    # Helper Properties
    # ------------------------------------------------------------------

    @property
    def is_expired(self) -> bool:
        """
        Return True if the session has expired.
        """
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def is_valid(self) -> bool:
        """
        Return True if the session is active and not expired.
        """
        return self.is_active and not self.is_expired

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def update_activity(self) -> None:
        """
        Update the last activity timestamp.
        """
        self.last_activity_at = datetime.now(timezone.utc)

    def logout(self) -> None:
        """
        Mark the session as logged out.
        """
        self.is_active = False
        self.logged_out_at = datetime.now(timezone.utc)

    def extend_session(self, days: int = 30) -> None:
        """
        Extend the session expiration.
        """
        self.expires_at = datetime.now(timezone.utc) + timedelta(days=days)

    # ------------------------------------------------------------------
    # Object Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<UserSession("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"device={self.device_name!r}, "
            f"active={self.is_active}"
            f")>"
        )

    def __str__(self) -> str:
        return f"Session {self.id}"