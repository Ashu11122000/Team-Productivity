from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Index, Integer, String

from app.db.base import Base


class BookReference(Base):
    """
    Cached Open Library book information.

    Purpose:
    - Reduce repeated Open Library API calls
    - Store metadata for referenced books
    - Link notes to books
    - Enable future analytics and search
    """

    __tablename__ = "book_references"

    __table_args__ = (
        Index("idx_book_reference_work_key", "work_key"),
        Index("idx_book_reference_title", "title"),
        Index("idx_book_reference_author", "author"),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Open Library identifiers

    work_key = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    edition_key = Column(
        String(100),
        nullable=True,
    )

    isbn = Column(
        String(20),
        nullable=True,
    )

    # Book metadata

    title = Column(
        String(500),
        nullable=False,
    )

    author = Column(
        String(255),
        nullable=True,
    )

    publisher = Column(
        String(255),
        nullable=True,
    )

    publish_year = Column(
        Integer,
        nullable=True,
    )

    language = Column(
        String(20),
        nullable=True,
    )

    cover_id = Column(
        Integer,
        nullable=True,
    )

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

    def __repr__(self) -> str:
        return (
            f"BookReference("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"work_key='{self.work_key}'"
            f")"
        )

    def __str__(self) -> str:
        return self.title