"""
Note Repository

Responsibilities:
- Encapsulate all database operations for the Note model.
- Keep persistence logic separate from business logic.
- Provide reuseable CRUD operations for the service layer.

Architecture:

API Route
    ↓
Service
    ↓
NoteRepository
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL
"""

from __future__ import annotations
from typing import Sequence
from sqlalchemy.orm import Session
from app.models.note import Note

class NoteRepository:
    """
    Repository responsible for all Note persistence operations.
    This repository should contains only database-related logic.
    Business rules belong in the service layer.
    """
    def __init__(self, db: Session) -> None:
        self.db = db
        
    # Create Operations
    def create(self, note: Note) -> Note:
        """
        Persist a new note.

        Args:
            note (Note): Note model instance.

        Returns:
            Note: Newly created note.
        """
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        
        return note
    
    # Read Operations
    def get_by_id(self, note_id: int) -> Note | None:
        """
        Retrieve a note by its primary key.
        
        Soft-deleted notes are ignored.

        Args:
            note_id (int): Note ID

        Returns:
            Note | None: Note instances or None
        """
        return (
            self.db.query(Note).filter(Note.id == note_id, Note.deleted_at.is_(None)).first()
        )
        
    def get_user_notes(self, note_id: int, owner_id: int) -> Note | None:
        """
        Retrieve a note belonging to a specific user.

        Args:
            note_id (int): Note ID
            owner_id(int): User ID

        Returns:
            Note | None: Note instance or None
        """
        return (self.db.query(Note).filter(Note.id == note_id, Note.owner_id == owner_id, Note.deleted_at.is_(None)).first())
    
    def get_all_by_owner(self, owner_id: int) -> Sequence[Note]:
        """
        Retrieve all notes owned by user.
        
        Archived notes are included.
        Deleted notes are excluded. 
        """
        return (
            self.db.query(Note).filter(Note.owner_id == owner_id, Note.deleted_at.is_(None)).order_by(Note.created_at.desc()).all()
        )
        
    def get_active_notes(self, owner_id: int) -> Sequence[Note]:
        """
        Retrieve active (non-archived notes).

        Args:
            owner_id (int): User ID

        Returns:
            Sequence[Note]: List of active notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(False),
            )
            .order_by(Note.updated_at.desc())
            .all()
        )

    def get_archived_notes(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve archived notes.

        Args:
            owner_id: User ID.

        Returns:
            List of archived notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(True),
            )
            .order_by(Note.updated_at.desc())
            .all()
        )

    def get_favorite_notes(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve favorite notes.

        Args:
            owner_id: User ID.

        Returns:
            List of favorite notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(True),
            )
            .order_by(Note.updated_at.desc())
            .all()
        )

    def get_notes_with_book_reference(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve notes linked to Open Library books.

        Args:
            owner_id: User ID.

        Returns:
            Notes containing book references.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.book_reference_id.is_not(None),
            )
            .order_by(Note.updated_at.desc())
            .all()
        )

    def get_converted_notes(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve notes already converted into tasks.

        Args:
            owner_id: User ID.

        Returns:
            Converted notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_converted_to_task.is_(True),
            )
            .order_by(Note.updated_at.desc())
            .all()
        )

    def exists(
        self,
        note_id: int,
    ) -> bool:
        """
        Check whether a note exists.

        Args:
            note_id: Note ID.

        Returns:
            True if the note exists.
        """
        return (
            self.db.query(Note.id)
            .filter(
                Note.id == note_id,
                Note.deleted_at.is_(None),
            )
            .first()
            is not None
        )
        
            # ==========================================================
    # SEARCH OPERATIONS
    # ==========================================================

    def search(
        self,
        owner_id: int,
        keyword: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Note]:
        """
        Search notes by title or content.

        Args:
            owner_id: Owner ID.
            keyword: Search keyword.
            skip: Pagination offset.
            limit: Maximum records.

        Returns:
            Matching notes.
        """
        pattern = f"%{keyword}%"

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                (
                    Note.title.ilike(pattern)
                    | Note.content.ilike(pattern)
                ),
            )
            .order_by(Note.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================================
    # PAGINATION
    # ==========================================================

    def list_notes(
        self,
        owner_id: int,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Note]:
        """
        Retrieve notes with pagination.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .order_by(Note.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_recent_notes(
        self,
        owner_id: int,
        *,
        limit: int = 10,
    ) -> Sequence[Note]:
        """
        Retrieve recently updated notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .order_by(Note.updated_at.desc())
            .limit(limit)
            .all()
        )

    # ==========================================================
    # COUNT OPERATIONS
    # ==========================================================

    def count_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count user's notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .count()
        )

    def count_archived_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count archived notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(True),
            )
            .count()
        )

    def count_favorite_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count favorite notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(True),
            )
            .count()
        )

    # ==========================================================
    # UPDATE OPERATIONS
    # ==========================================================

    def update(
        self,
        note: Note,
    ) -> Note:
        """
        Persist changes to a note.
        """
        self.db.commit()
        self.db.refresh(note)

        return note

    def save(
        self,
        note: Note,
    ) -> Note:
        """
        Alias for update().
        """
        return self.update(note)

    def update_title(
        self,
        note: Note,
        title: str,
    ) -> Note:
        """
        Update note title.
        """
        note.title = title

        self.db.commit()
        self.db.refresh(note)

        return note

    def update_content(
        self,
        note: Note,
        content: str | None,
    ) -> Note:
        """
        Update note content.
        """
        note.content = content

        self.db.commit()
        self.db.refresh(note)

        return note

    def update_book_reference(
        self,
        note: Note,
        reference_id: str | None,
    ) -> Note:
        """
        Attach or remove an Open Library reference.
        """
        note.book_reference_id = reference_id

        self.db.commit()
        self.db.refresh(note)

        return note

    def update_last_viewed(
        self,
        note: Note,
    ) -> Note:
        """
        Update last viewed timestamp.
        """
        from datetime import datetime, timezone

        note.last_viewed_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(note)

        return note

    def convert_to_task(
        self,
        note: Note,
    ) -> Note:
        """
        Mark a note as converted to a task.
        """
        note.is_converted_to_task = True

        self.db.commit()
        self.db.refresh(note)

        return note

    def remove_task_conversion(
        self,
        note: Note,
    ) -> Note:
        """
        Remove task conversion flag.
        """
        note.is_converted_to_task = False

        self.db.commit()
        self.db.refresh(note)

        return note
    
        # ==========================================================
    # SEARCH OPERATIONS
    # ==========================================================

    def search(
        self,
        owner_id: int,
        keyword: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Note]:
        """
        Search notes by title or content.

        Args:
            owner_id: Owner ID.
            keyword: Search keyword.
            skip: Pagination offset.
            limit: Maximum records.

        Returns:
            Matching notes.
        """
        pattern = f"%{keyword}%"

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                (
                    Note.title.ilike(pattern)
                    | Note.content.ilike(pattern)
                ),
            )
            .order_by(Note.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================================
    # PAGINATION
    # ==========================================================

    def list_notes(
        self,
        owner_id: int,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Note]:
        """
        Retrieve notes with pagination.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .order_by(Note.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_recent_notes(
        self,
        owner_id: int,
        *,
        limit: int = 10,
    ) -> Sequence[Note]:
        """
        Retrieve recently updated notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .order_by(Note.updated_at.desc())
            .limit(limit)
            .all()
        )

    # ==========================================================
    # COUNT OPERATIONS
    # ==========================================================

    def count_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count user's notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .count()
        )

    def count_archived_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count archived notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(True),
            )
            .count()
        )

    def count_favorite_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count favorite notes.
        """
        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(True),
            )
            .count()
        )

    # ==========================================================
    # UPDATE OPERATIONS
    # ==========================================================

    def update(
        self,
        note: Note,
    ) -> Note:
        """
        Persist changes to a note.
        """
        self.db.commit()
        self.db.refresh(note)

        return note

    def save(
        self,
        note: Note,
    ) -> Note:
        """
        Alias for update().
        """
        return self.update(note)

    def update_title(
        self,
        note: Note,
        title: str,
    ) -> Note:
        """
        Update note title.
        """
        note.title = title

        self.db.commit()
        self.db.refresh(note)

        return note

    def update_content(
        self,
        note: Note,
        content: str | None,
    ) -> Note:
        """
        Update note content.
        """
        note.content = content

        self.db.commit()
        self.db.refresh(note)

        return note

    def update_book_reference(
        self,
        note: Note,
        reference_id: str | None,
    ) -> Note:
        """
        Attach or remove an Open Library reference.
        """
        note.book_reference_id = reference_id

        self.db.commit()
        self.db.refresh(note)

        return note

    def update_last_viewed(
        self,
        note: Note,
    ) -> Note:
        """
        Update last viewed timestamp.
        """
        from datetime import datetime, timezone

        note.last_viewed_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(note)

        return note

    def convert_to_task(
        self,
        note: Note,
    ) -> Note:
        """
        Mark a note as converted to a task.
        """
        note.is_converted_to_task = True

        self.db.commit()
        self.db.refresh(note)

        return note

    def remove_task_conversion(
        self,
        note: Note,
    ) -> Note:
        """
        Remove task conversion flag.
        """
        note.is_converted_to_task = False

        self.db.commit()
        self.db.refresh(note)

        return note