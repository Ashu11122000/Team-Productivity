"""
Book reference model.

Stores cached metadata from the Open Library API.

Responsibilities:
- Cache Open Library search results.
- Reduce external API requests.
- Store book metadata for notes.
- Support future analytics and recommendations.
- Enable linking notes to books.

Architecture:

Open Library API
        │
        ▼
BookReference
        │
        ▼
Notes / Analytics / Search
"""

from __future__ import annotations

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base_model import BaseModelMixin


class BookReference(Base, BaseModelMixin):
    """
    Cached Open Library book information.
    """

    __tablename__ = "book_references"

    __table_args__ = (
        Index("idx_book_reference_work_key", "work_key"),
        Index("idx_book_reference_title", "title"),
        Index("idx_book_reference_author", "author"),
        Index("idx_book_reference_isbn", "isbn"),
        Index("idx_book_reference_publish_year", "publish_year"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # -------------------------------------------------------------------------
    # Open Library identifiers
    # -------------------------------------------------------------------------

    work_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    edition_key: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    isbn: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Book metadata
    # -------------------------------------------------------------------------

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    author: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    publisher: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    publish_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    cover_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<BookReference("
            f"id={self.id}, "
            f"title={self.title!r}, "
            f"work_key={self.work_key!r}"
            f")>"
        )

    def __str__(self) -> str:
        return self.title