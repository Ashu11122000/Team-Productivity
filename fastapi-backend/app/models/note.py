from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Note(Base):
    """
    Note Model.

    FastAPI Ownership:
    - Notes Management
    - Knowledge Management
    - Open Library References

    Integrations:
    - Open Library API
    - NestJS Task Conversion

    Consumed by:
    - FastAPI
    - Next.js Frontend
    - Flutter Mobile Application
    - NestJS Backend
    """

    __tablename__ = "notes"

    __table_args__ = (
        Index("idx_notes_owner_id", "owner_id"),
        Index("idx_notes_created_at", "created_at"),
        Index("idx_notes_title", "title"),
    )

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ------------------------------------------------------------------
    # Note Content
    # ------------------------------------------------------------------

    title = Column(
        String(255),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    owner_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Open Library Integration
    # ------------------------------------------------------------------

    book_reference_id = Column(
        String(100),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Note Status
    # ------------------------------------------------------------------

    is_converted_to_task = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_archived = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_favorite = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Audit Fields
    # ------------------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_viewed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    owner = relationship(
        "User",
        back_populates="notes",
    )

    # ------------------------------------------------------------------
    # Object Representation
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Note("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"owner_id={self.owner_id}"
            f")"
        )

    def __str__(self) -> str:
        return self.title