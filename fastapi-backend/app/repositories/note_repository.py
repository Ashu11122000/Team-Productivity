"""
Note Repository.

Responsibilities:
- Encapsulate all database operations for the Note model.
- Keep business logic out of the data access layer.
- Provide reusable CRUD operations for the service layer.

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

from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.note import Note


class NoteRepository:
    """
    Repository responsible for all Note persistence operations.

    This repository contains only persistence logic.
    Business rules belong inside the service layer.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # ==========================================================
    # INTERNAL HELPERS
    # ==========================================================

    def _commit(
        self,
        note: Note | None = None,
    ) -> None:
        """
        Commit the current transaction.

        Automatically refreshes the supplied note.
        Rolls back on failure.
        """

        try:
            self.db.commit()

            if note is not None:
                self.db.refresh(note)

        except Exception:
            self.db.rollback()
            raise

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        self.db.rollback()

    def flush(self) -> None:
        """
        Flush pending SQL statements.
        """
        self.db.flush()

    def refresh(
        self,
        note: Note,
    ) -> None:
        """
        Refresh a Note instance.
        """
        self.db.refresh(note)

    # ==========================================================
    # CREATE OPERATIONS
    # ==========================================================

    def create(
        self,
        note: Note,
    ) -> Note:
        """
        Persist a new note.

        Args:
            note:
                Note model instance.

        Returns:
            Newly created Note.
        """

        self.db.add(note)
        self._commit(note)

        return note

    # ==========================================================
    # READ OPERATIONS
    # ==========================================================

    def get_by_id(
        self,
        note_id: int,
    ) -> Note | None:
        """
        Retrieve a note by primary key.

        Soft-deleted notes are ignored.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.id == note_id,
                Note.deleted_at.is_(None),
            )
            .first()
        )

    def get_user_note(
        self,
        note_id: int,
        owner_id: int,
    ) -> Note | None:
        """
        Retrieve a user's specific note.

        Deleted notes are ignored.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.id == note_id,
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .first()
        )

    def get_all_by_owner(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve every non-deleted note
        belonging to a user.

        Includes:
        - Archived notes
        - Favorites
        - Converted notes
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .order_by(
                Note.created_at.desc(),
            )
            .all()
        )

    def exists(
        self,
        note_id: int,
    ) -> bool:
        """
        Check whether a note exists.

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

    def get_by_book_reference(
        self,
        reference_id: str,
    ) -> Sequence[Note]:
        """
        Retrieve notes linked to an
        Open Library reference.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.book_reference_id == reference_id,
                Note.deleted_at.is_(None),
            )
            .order_by(
                Note.updated_at.desc(),
            )
            .all()
        )
        
            # ==========================================================
    # FILTER OPERATIONS
    # ==========================================================

    def get_active_notes(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve all active (non-archived) notes
        belonging to a user.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(False),
            )
            .order_by(
                Note.updated_at.desc(),
            )
            .all()
        )

    def get_archived_notes(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve archived notes.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(True),
            )
            .order_by(
                Note.updated_at.desc(),
            )
            .all()
        )

    def get_favorite_notes(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve favorite notes.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(True),
            )
            .order_by(
                Note.updated_at.desc(),
            )
            .all()
        )

    def get_converted_notes(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve notes already converted
        into tasks.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_converted_to_task.is_(True),
            )
            .order_by(
                Note.updated_at.desc(),
            )
            .all()
        )

    def get_notes_with_book_reference(
        self,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Retrieve notes linked to an
        Open Library book.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.book_reference_id.is_not(None),
            )
            .order_by(
                Note.updated_at.desc(),
            )
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
            .order_by(
                Note.updated_at.desc(),
            )
            .limit(limit)
            .all()
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
        """

        pattern = f"%{keyword}%"

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                or_(
                    Note.title.ilike(pattern),
                    Note.content.ilike(pattern),
                ),
            )
            .order_by(
                Note.updated_at.desc(),
            )
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
        Retrieve paginated notes.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .order_by(
                Note.updated_at.desc(),
            )
            .offset(skip)
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
        Count all non-deleted notes
        belonging to a user.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .count()
        )

    def count_active_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count active (non-archived) notes.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(False),
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

    def count_converted_notes(
        self,
        owner_id: int,
    ) -> int:
        """
        Count notes already converted
        into tasks.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_converted_to_task.is_(True),
            )
            .count()
        )

    def count_notes_with_book_reference(
        self,
        owner_id: int,
    ) -> int:
        """
        Count notes linked to an
        Open Library reference.
        """

        return (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.book_reference_id.is_not(None),
            )
            .count()
        )

    # ==========================================================
    # EXISTENCE HELPERS
    # ==========================================================

    def has_archived_notes(
        self,
        owner_id: int,
    ) -> bool:
        """
        Check whether the user has
        archived notes.
        """

        return self.count_archived_notes(owner_id) > 0

    def has_favorite_notes(
        self,
        owner_id: int,
    ) -> bool:
        """
        Check whether the user has
        favorite notes.
        """

        return self.count_favorite_notes(owner_id) > 0

    def has_converted_notes(
        self,
        owner_id: int,
    ) -> bool:
        """
        Check whether the user has
        converted notes.
        """

        return self.count_converted_notes(owner_id) > 0

    def has_book_reference_notes(
        self,
        owner_id: int,
    ) -> bool:
        """
        Check whether the user has
        notes linked to books.
        """

        return self.count_notes_with_book_reference(owner_id) > 0
    
        # ==========================================================
    # UPDATE OPERATIONS
    # ==========================================================

    def update(
        self,
        note: Note,
    ) -> Note:
        """
        Persist changes made to a note.

        Args:
            note: Updated Note instance.

        Returns:
            Updated Note.
        """

        self._commit(note)

        return note

    def save(
        self,
        note: Note,
    ) -> Note:
        """
        Alias for update().

        Returns:
            Updated Note.
        """

        return self.update(note)

    def update_title(
        self,
        note: Note,
        title: str,
    ) -> Note:
        """
        Update the title of a note.

        Args:
            note: Note instance.
            title: New title.

        Returns:
            Updated Note.
        """

        note.title = title

        self._commit(note)

        return note

    def update_content(
        self,
        note: Note,
        content: str | None,
    ) -> Note:
        """
        Update note content.

        Args:
            note: Note instance.
            content: New content.

        Returns:
            Updated Note.
        """

        note.content = content

        self._commit(note)

        return note

    def update_note(
        self,
        note: Note,
        *,
        title: str | None = None,
        content: str | None = None,
    ) -> Note:
        """
        Update one or more editable note fields.

        Args:
            note: Note instance.
            title: Optional new title.
            content: Optional new content.

        Returns:
            Updated Note.
        """

        if title is not None:
            note.title = title

        if content is not None:
            note.content = content

        self._commit(note)

        return note

    def update_book_reference(
        self,
        note: Note,
        reference_id: str | None,
    ) -> Note:
        """
        Attach or remove an Open Library reference.

        Args:
            note: Note instance.
            reference_id: Open Library reference.

        Returns:
            Updated Note.
        """

        note.book_reference_id = reference_id

        self._commit(note)

        return note

    def update_last_viewed(
        self,
        note: Note,
    ) -> Note:
        """
        Update the last viewed timestamp.

        Returns:
            Updated Note.
        """

        note.last_viewed_at = datetime.now(
            timezone.utc,
        )

        self._commit(note)

        return note

    def convert_to_task(
        self,
        note: Note,
    ) -> Note:
        """
        Mark the note as converted to a task.

        Returns:
            Updated Note.
        """

        note.is_converted_to_task = True

        self._commit(note)

        return note

    def remove_task_conversion(
        self,
        note: Note,
    ) -> Note:
        """
        Remove the task conversion flag.

        Returns:
            Updated Note.
        """

        note.is_converted_to_task = False

        self._commit(note)

        return note

    def touch(
        self,
        note: Note,
    ) -> Note:
        """
        Refresh the note's updated_at timestamp.

        SQLAlchemy's onupdate will automatically
        update updated_at when committing.

        Returns:
            Updated Note.
        """

        self._commit(note)

        return note
    
        # ==========================================================
    # STATUS OPERATIONS
    # ==========================================================

    def archive(
        self,
        note: Note,
    ) -> Note:
        """
        Archive a note.

        Args:
            note: Note instance.

        Returns:
            Updated Note.
        """

        note.is_archived = True

        self._commit(note)

        return note

    def restore(
        self,
        note: Note,
    ) -> Note:
        """
        Restore an archived note.

        Args:
            note: Note instance.

        Returns:
            Updated Note.
        """

        note.is_archived = False

        self._commit(note)

        return note

    def favorite(
        self,
        note: Note,
    ) -> Note:
        """
        Mark a note as favorite.

        Args:
            note: Note instance.

        Returns:
            Updated Note.
        """

        note.is_favorite = True

        self._commit(note)

        return note

    def unfavorite(
        self,
        note: Note,
    ) -> Note:
        """
        Remove favorite status from a note.

        Args:
            note: Note instance.

        Returns:
            Updated Note.
        """

        note.is_favorite = False

        self._commit(note)

        return note

    def archive_all(
        self,
        owner_id: int,
    ) -> int:
        """
        Archive all active notes belonging to a user.

        Args:
            owner_id: User ID.

        Returns:
            Number of affected rows.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(False),
            )
            .update(
                {
                    Note.is_archived: True,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def restore_all(
        self,
        owner_id: int,
    ) -> int:
        """
        Restore all archived notes.

        Args:
            owner_id: User ID.

        Returns:
            Number of affected rows.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(True),
            )
            .update(
                {
                    Note.is_archived: False,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def favorite_all(
        self,
        owner_id: int,
    ) -> int:
        """
        Mark all notes as favorite.

        Args:
            owner_id: User ID.

        Returns:
            Number of affected rows.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(False),
            )
            .update(
                {
                    Note.is_favorite: True,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def unfavorite_all(
        self,
        owner_id: int,
    ) -> int:
        """
        Remove favorite status from all notes.

        Args:
            owner_id: User ID.

        Returns:
            Number of affected rows.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(True),
            )
            .update(
                {
                    Note.is_favorite: False,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected
    
        # ==========================================================
    # DELETE OPERATIONS
    # ==========================================================

    def soft_delete(
        self,
        note: Note,
    ) -> Note:
        """
        Soft delete a note.

        The record remains in the database but is hidden
        from normal application queries.

        Args:
            note: Note instance.

        Returns:
            Updated Note.
        """

        note.deleted_at = datetime.now(timezone.utc)

        self._commit(note)

        return note

    def restore_deleted(
        self,
        note: Note,
    ) -> Note:
        """
        Restore a previously soft-deleted note.

        Args:
            note: Note instance.

        Returns:
            Updated Note.
        """

        note.deleted_at = None

        self._commit(note)

        return note

    def hard_delete(
        self,
        note: Note,
    ) -> None:
        """
        Permanently remove a note.

        WARNING:
            This operation cannot be undone.

        Args:
            note: Note instance.
        """

        self.db.delete(note)

        self._commit()

    def delete(
        self,
        note: Note,
    ) -> None:
        """
        Alias for hard_delete().

        Args:
            note: Note instance.
        """

        self.hard_delete(note)

    def delete_all_archived(
        self,
        owner_id: int,
    ) -> int:
        """
        Permanently delete all archived notes
        belonging to a user.

        Args:
            owner_id: User ID.

        Returns:
            Number of deleted notes.
        """

        archived_notes = (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(True),
            )
            .all()
        )

        affected = len(archived_notes)

        for note in archived_notes:
            self.db.delete(note)

        self._commit()

        return affected

    # ==========================================================
    # RESTORE HELPERS
    # ==========================================================

    def restore_all_deleted(
        self,
        owner_id: int,
    ) -> int:
        """
        Restore every soft-deleted note
        belonging to a user.

        Returns:
            Number of restored notes.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.owner_id == owner_id,
                Note.deleted_at.is_not(None),
            )
            .update(
                {
                    Note.deleted_at: None,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected
    
        # ==========================================================
    # BULK OPERATIONS
    # ==========================================================

    def bulk_archive(
        self,
        note_ids: list[int],
        owner_id: int,
    ) -> int:
        """
        Archive multiple notes.

        Args:
            note_ids: List of note IDs.
            owner_id: Note owner.

        Returns:
            Number of affected rows.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.id.in_(note_ids),
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(False),
            )
            .update(
                {
                    Note.is_archived: True,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def bulk_restore(
        self,
        note_ids: list[int],
        owner_id: int,
    ) -> int:
        """
        Restore multiple archived notes.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.id.in_(note_ids),
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_archived.is_(True),
            )
            .update(
                {
                    Note.is_archived: False,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def bulk_favorite(
        self,
        note_ids: list[int],
        owner_id: int,
    ) -> int:
        """
        Mark multiple notes as favorite.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.id.in_(note_ids),
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(False),
            )
            .update(
                {
                    Note.is_favorite: True,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def bulk_unfavorite(
        self,
        note_ids: list[int],
        owner_id: int,
    ) -> int:
        """
        Remove favorite status from multiple notes.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.id.in_(note_ids),
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_favorite.is_(True),
            )
            .update(
                {
                    Note.is_favorite: False,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def bulk_soft_delete(
        self,
        note_ids: list[int],
        owner_id: int,
    ) -> int:
        """
        Soft delete multiple notes.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.id.in_(note_ids),
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
            )
            .update(
                {
                    Note.deleted_at: datetime.now(timezone.utc),
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected

    def bulk_hard_delete(
        self,
        note_ids: list[int],
        owner_id: int,
    ) -> int:
        """
        Permanently delete multiple notes.

        Returns:
            Number of deleted notes.
        """

        notes = (
            self.db.query(Note)
            .filter(
                Note.id.in_(note_ids),
                Note.owner_id == owner_id,
            )
            .all()
        )

        affected = len(notes)

        for note in notes:
            self.db.delete(note)

        self._commit()

        return affected

    def bulk_convert_to_task(
        self,
        note_ids: list[int],
        owner_id: int,
    ) -> int:
        """
        Mark multiple notes as converted to tasks.
        """

        affected = (
            self.db.query(Note)
            .filter(
                Note.id.in_(note_ids),
                Note.owner_id == owner_id,
                Note.deleted_at.is_(None),
                Note.is_converted_to_task.is_(False),
            )
            .update(
                {
                    Note.is_converted_to_task: True,
                },
                synchronize_session=False,
            )
        )

        self._commit()

        return affected
    
        # ==========================================================
    # DASHBOARD / STATISTICS
    # ==========================================================

    def get_dashboard_statistics(
        self,
        owner_id: int,
    ) -> dict[str, int]:
        """
        Retrieve dashboard statistics for a user.

        Returns:
            Dictionary containing various note counts.
        """

        return {
            "total_notes": self.count_notes(owner_id),
            "active_notes": self.count_active_notes(owner_id),
            "archived_notes": self.count_archived_notes(owner_id),
            "favorite_notes": self.count_favorite_notes(owner_id),
            "converted_notes": self.count_converted_notes(owner_id),
            "book_reference_notes": self.count_notes_with_book_reference(owner_id),
        }

    # ==========================================================
    # SESSION HELPERS
    # ==========================================================

    def expunge(
        self,
        note: Note,
    ) -> None:
        """
        Remove a note instance from the current session.
        """

        self.db.expunge(note)

    def expunge_all(self) -> None:
        """
        Remove all tracked instances from the current session.
        """

        self.db.expunge_all()

    def close(self) -> None:
        """
        Close the current database session.
        """

        self.db.close()

    # ==========================================================
    # FUTURE EXTENSION HOOKS
    # ==========================================================

    def duplicate_note(self) -> None:
        """
        Future:
        Duplicate an existing note.
        """
        raise NotImplementedError

    def export_note(self) -> None:
        """
        Future:
        Export a note as PDF/Markdown.
        """
        raise NotImplementedError

    def import_note(self) -> None:
        """
        Future:
        Import notes from external sources.
        """
        raise NotImplementedError

    def generate_summary(self) -> None:
        """
        Future:
        AI-powered note summarization.
        """
        raise NotImplementedError

    def generate_embeddings(self) -> None:
        """
        Future:
        AI semantic search support.
        """
        raise NotImplementedError

    def sync_with_open_library(self) -> None:
        """
        Future:
        Synchronize note metadata with Open Library.
        """
        raise NotImplementedError

    def share_note(self) -> None:
        """
        Future:
        Share notes with other users.
        """
        raise NotImplementedError

    def lock_note(self) -> None:
        """
        Future:
        Lock a note against editing.
        """
        raise NotImplementedError

    def unlock_note(self) -> None:
        """
        Future:
        Unlock a previously locked note.
        """
        raise NotImplementedError