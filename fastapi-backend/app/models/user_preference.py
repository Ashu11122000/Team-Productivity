"""
User preference model.

Responsibilities:
- Store user-specific application preferences.
- Manage UI and localization settings.
- Store notification preferences.
- Support future customization options.

Architecture:

User
 │
 └──────────────► UserPreference
                      │
                      ├── Theme
                      ├── Language
                      ├── Timezone
                      ├── Notifications
                      └── Future Preferences
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
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


class UserPreference(Base, BaseModelMixin):
    """
    Stores user-specific application preferences.
    """

    __tablename__ = "user_preferences"

    __table_args__ = (
        Index("idx_user_preferences_user", "user_id"),
        Index("idx_user_preferences_language", "language"),
        Index("idx_user_preferences_timezone", "timezone"),
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
        unique=True,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Appearance
    # ------------------------------------------------------------------

    theme: Mapped[str] = mapped_column(
        String(20),
        default="system",
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Localization
    # ------------------------------------------------------------------

    language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        default="Asia/Kolkata",
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Notification Preferences
    # ------------------------------------------------------------------

    email_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    push_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    in_app_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    mention_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    deadline_reminders: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    user: Mapped["User"] = relationship(
        "User",
        back_populates="preferences",
        lazy="selectin",
    )

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def enable_all_notifications(self) -> None:
        """
        Enable all notification preferences.
        """
        self.email_notifications = True
        self.push_notifications = True
        self.in_app_notifications = True
        self.mention_notifications = True
        self.deadline_reminders = True

    def disable_all_notifications(self) -> None:
        """
        Disable all notification preferences.
        """
        self.email_notifications = False
        self.push_notifications = False
        self.in_app_notifications = False
        self.mention_notifications = False
        self.deadline_reminders = False

    def __repr__(self) -> str:
        return (
            f"<UserPreference("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"theme={self.theme!r}, "
            f"language={self.language!r}"
            f")>"
        )

    def __str__(self) -> str:
        return f"Preferences for User {self.user_id}"