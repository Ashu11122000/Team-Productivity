"""
Book-related Pydantic schemas.

These schemas define request and response models used by the
Open Library integration and the local BookReference cache.

Used by:

- Open Library API integration
- Cached Book References
- Note ↔ Book relationships
- Book Search
- Analytics
- Future Recommendations

Architecture:

API Routes
      │
      ▼
Book Service
      │
      ▼
Book Repository
      │
      ▼
BookReference Model
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel, TimestampMixin


# ==========================================================
# Base Schema
# ==========================================================


class BookBase(ORMModel):
    """
    Base schema shared by all
    book-related request and response models.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Book title.",
        examples=["Clean Architecture"],
    )

    author: str | None = Field(
        default=None,
        max_length=255,
        description="Primary author name.",
        examples=["Robert C. Martin"],
    )

    publisher: str | None = Field(
        default=None,
        max_length=255,
        description="Publisher name.",
        examples=["Prentice Hall"],
    )

    publish_year: int | None = Field(
        default=None,
        ge=1000,
        le=9999,
        description="Year the book was published.",
        examples=[2017],
    )

    language: str | None = Field(
        default=None,
        max_length=20,
        description="Language code.",
        examples=["eng"],
    )


# ==========================================================
# Create Book
# ==========================================================


class BookCreate(BookBase):
    """
    Request schema for manually creating
    a cached book reference.
    """

    work_key: str = Field(
        ...,
        description="Open Library work key.",
        examples=["/works/OL45883W"],
    )

    edition_key: str | None = Field(
        default=None,
        description="Open Library edition key.",
        examples=["OL27448M"],
    )

    isbn: str | None = Field(
        default=None,
        max_length=20,
        description="ISBN-10 or ISBN-13.",
        examples=["9780134494166"],
    )

    cover_id: int | None = Field(
        default=None,
        description="Open Library cover identifier.",
        examples=[9251996],
    )


# ==========================================================
# Update Book
# ==========================================================


class BookUpdate(ORMModel):
    """
    Request schema for updating
    cached book metadata.

    Supports partial updates.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Updated title.",
    )

    author: str | None = Field(
        default=None,
        max_length=255,
        description="Updated author.",
    )

    publisher: str | None = Field(
        default=None,
        max_length=255,
        description="Updated publisher.",
    )

    publish_year: int | None = Field(
        default=None,
        ge=1000,
        le=9999,
        description="Updated publication year.",
    )

    language: str | None = Field(
        default=None,
        max_length=20,
        description="Updated language code.",
    )

    edition_key: str | None = Field(
        default=None,
        description="Updated edition key.",
    )

    isbn: str | None = Field(
        default=None,
        max_length=20,
        description="Updated ISBN.",
    )

    cover_id: int | None = Field(
        default=None,
        description="Updated cover identifier.",
    )


# ==========================================================
# Book Summary
# ==========================================================


class BookSummary(ORMModel):
    """
    Lightweight representation of a book.

    Used by:

    - Search results
    - Dashboard
    - Book picker
    - Note linking
    """

    id: int = Field(
        ...,
        description="Cached book identifier.",
        examples=[1],
    )

    work_key: str = Field(
        ...,
        description="Open Library work key.",
    )

    title: str = Field(
        ...,
        description="Book title.",
    )

    author: str | None = Field(
        default=None,
        description="Primary author.",
    )

    publish_year: int | None = Field(
        default=None,
        description="Publication year.",
    )

    cover_id: int | None = Field(
        default=None,
        description="Cover identifier.",
    )


# ==========================================================
# Book Response
# ==========================================================


class BookResponse(BookBase, TimestampMixin):
    """
    Complete cached book response.

    Returned by:

    - Get Book
    - Search Cached Books
    - Book Details
    """

    id: int = Field(
        ...,
        description="Cached book identifier.",
        examples=[1],
    )

    work_key: str = Field(
        ...,
        description="Open Library work key.",
    )

    edition_key: str | None = Field(
        default=None,
        description="Edition key.",
    )

    isbn: str | None = Field(
        default=None,
        description="ISBN.",
    )

    cover_id: int | None = Field(
        default=None,
        description="Open Library cover identifier.",
    )
    
    """
Book-related Pydantic schemas.

These schemas define request and response models used by the
Open Library integration and the local BookReference cache.

Used by:

- Open Library API integration
- Cached Book References
- Note ↔ Book relationships
- Book Search
- Analytics
- Future Recommendations

Architecture:

API Routes
      │
      ▼
Book Service
      │
      ▼
Book Repository
      │
      ▼
BookReference Model
"""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel, TimestampMixin


# ==========================================================
# Base Schema
# ==========================================================


class BookBase(ORMModel):
    """
    Base schema shared by all
    book-related request and response models.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Book title.",
        examples=["Clean Architecture"],
    )

    author: str | None = Field(
        default=None,
        max_length=255,
        description="Primary author name.",
        examples=["Robert C. Martin"],
    )

    publisher: str | None = Field(
        default=None,
        max_length=255,
        description="Publisher name.",
        examples=["Prentice Hall"],
    )

    publish_year: int | None = Field(
        default=None,
        ge=1000,
        le=9999,
        description="Year the book was published.",
        examples=[2017],
    )

    language: str | None = Field(
        default=None,
        max_length=20,
        description="Language code.",
        examples=["eng"],
    )


# ==========================================================
# Create Book
# ==========================================================


class BookCreate(BookBase):
    """
    Request schema for manually creating
    a cached book reference.
    """

    work_key: str = Field(
        ...,
        description="Open Library work key.",
        examples=["/works/OL45883W"],
    )

    edition_key: str | None = Field(
        default=None,
        description="Open Library edition key.",
        examples=["OL27448M"],
    )

    isbn: str | None = Field(
        default=None,
        max_length=20,
        description="ISBN-10 or ISBN-13.",
        examples=["9780134494166"],
    )

    cover_id: int | None = Field(
        default=None,
        description="Open Library cover identifier.",
        examples=[9251996],
    )


# ==========================================================
# Update Book
# ==========================================================


class BookUpdate(ORMModel):
    """
    Request schema for updating
    cached book metadata.

    Supports partial updates.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Updated title.",
    )

    author: str | None = Field(
        default=None,
        max_length=255,
        description="Updated author.",
    )

    publisher: str | None = Field(
        default=None,
        max_length=255,
        description="Updated publisher.",
    )

    publish_year: int | None = Field(
        default=None,
        ge=1000,
        le=9999,
        description="Updated publication year.",
    )

    language: str | None = Field(
        default=None,
        max_length=20,
        description="Updated language code.",
    )

    edition_key: str | None = Field(
        default=None,
        description="Updated edition key.",
    )

    isbn: str | None = Field(
        default=None,
        max_length=20,
        description="Updated ISBN.",
    )

    cover_id: int | None = Field(
        default=None,
        description="Updated cover identifier.",
    )


# ==========================================================
# Book Summary
# ==========================================================


class BookSummary(ORMModel):
    """
    Lightweight representation of a book.

    Used by:

    - Search results
    - Dashboard
    - Book picker
    - Note linking
    """

    id: int = Field(
        ...,
        description="Cached book identifier.",
        examples=[1],
    )

    work_key: str = Field(
        ...,
        description="Open Library work key.",
    )

    title: str = Field(
        ...,
        description="Book title.",
    )

    author: str | None = Field(
        default=None,
        description="Primary author.",
    )

    publish_year: int | None = Field(
        default=None,
        description="Publication year.",
    )

    cover_id: int | None = Field(
        default=None,
        description="Cover identifier.",
    )


# ==========================================================
# Book Response
# ==========================================================


class BookResponse(BookBase, TimestampMixin):
    """
    Complete cached book response.

    Returned by:

    - Get Book
    - Search Cached Books
    - Book Details
    """

    id: int = Field(
        ...,
        description="Cached book identifier.",
        examples=[1],
    )

    work_key: str = Field(
        ...,
        description="Open Library work key.",
    )

    edition_key: str | None = Field(
        default=None,
        description="Edition key.",
    )

    isbn: str | None = Field(
        default=None,
        description="ISBN.",
    )

    cover_id: int | None = Field(
        default=None,
        description="Open Library cover identifier.",
    )