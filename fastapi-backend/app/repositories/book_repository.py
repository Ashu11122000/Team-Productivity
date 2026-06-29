"""
Book Repository

Responsibilities:
- Encapsulate all database operations for BookReference.
- Cache Open Library book metadata.
- Reduce repeated external API calls.
- Keep persistence logic separate from business logic.

Architecture:

API Route
      ↓
Book Service
      ↓
BookRepository
      ↓
SQLAlchemy ORM
      ↓
PostgreSQL
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.book_reference import BookReference


class BookRepository:
    """
    Repository responsible for all BookReference
    persistence operations.

    Business logic belongs in the service layer.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # ==========================================================
    # CREATE OPERATIONS
    # ==========================================================

    def create(
        self,
        book: BookReference,
    ) -> BookReference:
        """
        Persist a new cached book.
        """
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)

        return book

    # ==========================================================
    # READ OPERATIONS
    # ==========================================================

    def get_by_id(
        self,
        book_id: int,
    ) -> BookReference | None:
        """
        Retrieve a book by ID.
        """
        return (
            self.db.query(BookReference)
            .filter(BookReference.id == book_id)
            .first()
        )

    def get_by_work_key(
        self,
        work_key: str,
    ) -> BookReference | None:
        """
        Retrieve a cached Open Library work.
        """
        return (
            self.db.query(BookReference)
            .filter(BookReference.work_key == work_key)
            .first()
        )

    def get_by_edition_key(
        self,
        edition_key: str,
    ) -> BookReference | None:
        """
        Retrieve by edition key.
        """
        return (
            self.db.query(BookReference)
            .filter(BookReference.edition_key == edition_key)
            .first()
        )

    def get_by_isbn(
        self,
        isbn: str,
    ) -> BookReference | None:
        """
        Retrieve a book using ISBN.
        """
        return (
            self.db.query(BookReference)
            .filter(BookReference.isbn == isbn)
            .first()
        )

    def exists(
        self,
        work_key: str,
    ) -> bool:
        """
        Check whether a cached book exists.
        """
        return (
            self.db.query(BookReference.id)
            .filter(BookReference.work_key == work_key)
            .first()
            is not None
        )

    # ==========================================================
    # SEARCH OPERATIONS
    # ==========================================================

    def search(
        self,
        keyword: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[BookReference]:
        """
        Search cached books.

        Searches:
        - title
        - author
        - publisher
        """
        pattern = f"%{keyword}%"

        return (
            self.db.query(BookReference)
            .filter(
                or_(
                    BookReference.title.ilike(pattern),
                    BookReference.author.ilike(pattern),
                    BookReference.publisher.ilike(pattern),
                )
            )
            .order_by(BookReference.title.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_title(
        self,
        title: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[BookReference]:
        """
        Search books by title.
        """
        return (
            self.db.query(BookReference)
            .filter(
                BookReference.title.ilike(f"%{title}%")
            )
            .order_by(BookReference.title.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_author(
        self,
        author: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[BookReference]:
        """
        Search books by author.
        """
        return (
            self.db.query(BookReference)
            .filter(
                BookReference.author.ilike(f"%{author}%")
            )
            .order_by(BookReference.author.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================================
    # PAGINATION
    # ==========================================================

    def list_books(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[BookReference]:
        """
        Retrieve cached books with pagination.
        """
        return (
            self.db.query(BookReference)
            .order_by(BookReference.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_recent_books(
        self,
        *,
        limit: int = 10,
    ) -> Sequence[BookReference]:
        """
        Retrieve recently cached books.
        """
        return (
            self.db.query(BookReference)
            .order_by(BookReference.created_at.desc())
            .limit(limit)
            .all()
        )

    # ==========================================================
    # COUNT OPERATIONS
    # ==========================================================

    def count_books(self) -> int:
        """
        Count cached books.
        """
        return (
            self.db.query(func.count(BookReference.id))
            .scalar()
            or 0
        )

    def count_by_author(
        self,
        author: str,
    ) -> int:
        """
        Count books for an author.
        """
        return (
            self.db.query(func.count(BookReference.id))
            .filter(BookReference.author == author)
            .scalar()
            or 0
        )

    def count_by_language(
        self,
        language: str,
    ) -> int:
        """
        Count books for a language.
        """
        return (
            self.db.query(func.count(BookReference.id))
            .filter(BookReference.language == language)
            .scalar()
            or 0
        )
        
            # ==========================================================
    # UPDATE OPERATIONS
    # ==========================================================

    def update(
        self,
        book: BookReference,
    ) -> BookReference:
        """
        Persist changes to a cached book.
        """
        self.db.commit()
        self.db.refresh(book)

        return book

    def save(
        self,
        book: BookReference,
    ) -> BookReference:
        """
        Alias for update().
        """
        return self.update(book)

    def update_metadata(
        self,
        book: BookReference,
        *,
        title: str | None = None,
        author: str | None = None,
        publisher: str | None = None,
        publish_year: int | None = None,
        language: str | None = None,
        cover_id: int | None = None,
        edition_key: str | None = None,
        isbn: str | None = None,
    ) -> BookReference:
        """
        Update cached book metadata.
        """

        if title is not None:
            book.title = title

        if author is not None:
            book.author = author

        if publisher is not None:
            book.publisher = publisher

        if publish_year is not None:
            book.publish_year = publish_year

        if language is not None:
            book.language = language

        if cover_id is not None:
            book.cover_id = cover_id

        if edition_key is not None:
            book.edition_key = edition_key

        if isbn is not None:
            book.isbn = isbn

        self.db.commit()
        self.db.refresh(book)

        return book

    # ==========================================================
    # OPEN LIBRARY HELPERS
    # ==========================================================

    def get_or_create(
        self,
        book: BookReference,
    ) -> BookReference:
        """
        Return an existing cached book if present;
        otherwise create a new cache entry.
        """

        existing = self.get_by_work_key(book.work_key)

        if existing:
            return existing

        return self.create(book)

    def update_cover(
        self,
        book: BookReference,
        cover_id: int | None,
    ) -> BookReference:
        """
        Update cover image identifier.
        """

        book.cover_id = cover_id

        self.db.commit()
        self.db.refresh(book)

        return book

    # ==========================================================
    # DELETE OPERATIONS
    # ==========================================================

    def hard_delete(
        self,
        book: BookReference,
    ) -> None:
        """
        Permanently remove a cached book.
        """

        self.db.delete(book)
        self.db.commit()

    def delete(
        self,
        book: BookReference,
    ) -> None:
        """
        Alias for hard_delete().
        """

        self.hard_delete(book)

    # ==========================================================
    # BULK OPERATIONS
    # ==========================================================

    def delete_all(self) -> int:
        """
        Remove every cached book.

        Returns:
            Number of deleted rows.
        """

        affected = (
            self.db.query(BookReference)
            .delete(
                synchronize_session=False,
            )
        )

        self.db.commit()

        return affected

    # ==========================================================
    # SESSION HELPERS
    # ==========================================================

    def flush(self) -> None:
        """
        Flush pending changes.
        """
        self.db.flush()

    def refresh(
        self,
        book: BookReference,
    ) -> None:
        """
        Refresh a BookReference instance.
        """
        self.db.refresh(book)

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        self.db.rollback()

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        self.db.commit()

    # ==========================================================
    # SQLALCHEMY HELPERS
    # ==========================================================

    def add(
        self,
        book: BookReference,
    ) -> None:
        """
        Add a book to the current session.
        """
        self.db.add(book)

    def merge(
        self,
        book: BookReference,
    ) -> BookReference:
        """
        Merge a detached book instance.
        """
        return self.db.merge(book)

    def detach(
        self,
        book: BookReference,
    ) -> None:
        """
        Remove a book from the session.
        """
        self.db.expunge(book)

    def close(self) -> None:
        """
        Close the database session.
        """
        self.db.close()