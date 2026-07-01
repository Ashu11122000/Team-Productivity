"""
Note model.

Responsibilities:
- Store user notes.
- Support personal knowledge management.
- Integrate with Open Library references.
- Support conversion of notes into tasks.
- Serve Next.js, Flutter, and NestJS clients.

Architecture:

User
 │
 ├──────────────┐
 ▼              ▼
Note ───────► BookReference
 │
 ├── Future: Comments
 ├── Future: Attachments
 ├── Future: Favorites
 └── Future: Activity Logs
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_model import BaseModelMixin

if TYPE_CHECKING:
    from app.models.book_reference import BookReference
    from app.models.user import User


class Note(Base, BaseModelMixin):
    """
    User note.

    FastAPI Ownership:
    - Notes Management
    - Knowledge Management
    - Open Library Integration

    Consumed By:
    - FastAPI
    - Next.js
    - Flutter
    - NestJS (Task Conversion)
    """

    __tablename__ = "notes"

    __table_args__ = (
        Index("idx_notes_owner_id", "owner_id"),
        Index("idx_notes_title", "title"),
        Index("idx_notes_created_at", "created_at"),
        Index("idx_notes_archived", "is_archived"),
        Index("idx_notes_favorite", "is_favorite"),
        Index("idx_notes_task_conversion", "is_converted_to_task"),
        Index("idx_notes_book_reference", "book_reference_id"),
    )

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ------------------------------------------------------------------
    # Note Content
    # ------------------------------------------------------------------

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    owner_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Open Library Integration
    # ------------------------------------------------------------------

    book_reference_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "book_references.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Note Status
    # ------------------------------------------------------------------

    is_converted_to_task: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Activity
    # ------------------------------------------------------------------

    last_viewed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="notes",
        lazy="selectin",
    )

    book_reference: Mapped["BookReference | None"] = relationship(
        "BookReference",
        lazy="selectin",
    )

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def mark_as_converted(self) -> None:
        """
        Mark this note as converted into a task.
        """
        self.is_converted_to_task = True

    def archive(self) -> None:
        """
        Archive the note.
        """
        self.is_archived = True

    def unarchive(self) -> None:
        """
        Restore an archived note.
        """
        self.is_archived = False

    def mark_as_favorite(self) -> None:
        """
        Mark the note as favorite.
        """
        self.is_favorite = True

    def remove_from_favorites(self) -> None:
        """
        Remove the note from favorites.
        """
        self.is_favorite = False

    def update_last_viewed(self) -> None:
        """
        Update the last viewed timestamp.
        """
        self.last_viewed_at = datetime.utcnow()

    # ------------------------------------------------------------------
    # Object Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<Note("
            f"id={self.id}, "
            f"title={self.title!r}, "
            f"owner_id={self.owner_id}"
            f")>"
        )

    def __str__(self) -> str:
        return self.title