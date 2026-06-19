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

# relationship is used to define relationships between SQLAlchemy models
from sqlalchemy.orm import relationship

from app.db.base import Base


class Note(Base):
    __tablename__ = "notes"

    # Indexes for optimizing queries on frequency accessed columns like owner_id, created_at, and title
    __table_args__ = (
        Index("idx_notes_owner_id", "owner_id"),
        Index("idx_notes_created_at", "created_at"),
        Index("idx_notes_title", "title"),
    )

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Note Data
    title = Column(
        String(255),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=True,
    )

    # Ownership
    owner_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Open Library Integration
    book_reference_id = Column(
        String(100),
        nullable=True,
    )

    # NestJS Integration
    is_converted_to_task = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Audit Fields
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

    # Relationships
    owner = relationship(
        "User",
        back_populates="notes",
    )

    # Representation of the Not Object for debugging and logging purposes
    def __repr__(self) -> str:
        
        # Return a string representation of the Note object, including its ID, title, and owner ID
        return (
            f"<Note("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"owner_id={self.owner_id}"
            f")>"
        )