"""
Common SQLAlchemy model mixin.

Responsibilities:
- Provides shared audit fields for all database models.
- Tracks record creation, updates, and soft deletion.
- Supports logical activation/deactivation.
- Promotes consistency across all ORM entities.

Usage:

    class User(Base, BaseModelMixin):
        __tablename__ = "users"
        ...

Shared Fields:
- created_at
- updated_at
- deleted_at
- is_active
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class BaseModelMixin:
    """
    Reusable mixin providing common audit fields.

    This mixin should be inherited together with SQLAlchemy's
    declarative Base.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    @property
    def is_deleted(self) -> bool:
        """
        Return True if the record has been soft deleted.
        """
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        """
        Mark the record as soft deleted.
        """
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        """
        Restore a previously soft-deleted record.
        """
        self.deleted_at = None

    def activate(self) -> None:
        """
        Mark the record as active.
        """
        self.is_active = True

    def deactivate(self) -> None:
        """
        Mark the record as inactive.
        """
        self.is_active = False