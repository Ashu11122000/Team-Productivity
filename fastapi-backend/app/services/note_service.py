"""
Note Service.

Business Logic Layer for Notes.

Responsibilities
----------------
- Note management
- Ownership validation
- RBAC validation
- Search
- Pagination
- Archive management
- Favorites
- Task conversion
- Open Library integration

Architecture
------------
API Routes
      │
      ▼
NoteService
      │
      ▼
NoteRepository
      │
      ▼
SQLAlchemy ORM
      │
      ▼
PostgreSQL
"""

from __future__ import annotations

from typing import Sequence

from fastapi import HTTPException, status
from structlog import get_logger

from app.models.note import Note
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
)

logger = get_logger(__name__)

ADMIN_ROLE = "ADMIN"


class NoteService:
    """
    Service responsible for all note-related
    business logic.

    The service must never communicate with
    SQLAlchemy directly.

    All persistence operations are delegated
    to NoteRepository.
    """

    def __init__(
        self,
        repository: NoteRepository,
    ) -> None:
        self.repository = repository

    # ==========================================================
    # PRIVATE HELPERS
    # ==========================================================

    @staticmethod
    def _raise_not_found() -> None:
        """
        Raise 404 when a note cannot be found.
        """

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    @staticmethod
    def _raise_access_denied() -> None:
        """
        Raise 403 when the user cannot
        access a note.
        """

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this note.",
        )

    @staticmethod
    def _raise_admin_required() -> None:
        """
        Raise 403 when admin privileges
        are required.
        """

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    @staticmethod
    def _raise_archived() -> None:
        """
        Raise when attempting to modify
        an archived note.
        """

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Archived notes cannot be modified.",
        )

    @staticmethod
    def _raise_already_converted() -> None:
        """
        Raise when attempting to convert
        a note twice.
        """

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Note has already been converted into a task.",
        )

    # ==========================================================
    # VALIDATION
    # ==========================================================

    def validate_admin(
        self,
        current_user: User,
    ) -> None:
        """
        Validate administrator access.
        """

        if current_user.role.upper() != ADMIN_ROLE:
            logger.warning(
                "Admin access denied",
                user_id=current_user.id,
                email=current_user.email,
            )

            self._raise_admin_required()

    def validate_note_access(
        self,
        *,
        current_user: User,
        note: Note,
    ) -> None:
        """
        Validate ownership.

        Admins may access every note.
        Owners may access their own notes.
        """

        is_admin = (
            current_user.role.upper()
            == ADMIN_ROLE
        )

        is_owner = (
            note.owner_id
            == current_user.id
        )

        if not (is_admin or is_owner):
            logger.warning(
                "Unauthorized note access",
                current_user=current_user.id,
                owner_id=note.owner_id,
                note_id=note.id,
            )

            self._raise_access_denied()

    # ==========================================================
    # READ OPERATIONS
    # ==========================================================

    def get_note_by_id(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Retrieve a note and validate access.
        """

        note = self.repository.get_by_id(
            note_id,
        )

        if note is None:
            self._raise_not_found()

        self.validate_note_access(
            current_user=current_user,
            note=note,
        )

        return note
    
        # ==========================================================
    # CREATE OPERATIONS
    # ==========================================================

    def create_note(
        self,
        *,
        current_user: User,
        note_data: NoteCreate,
    ) -> Note:
        """
        Create a new note.

        Business Rules
        --------------
        - Every note belongs to the authenticated user.
        - Notes are active by default.
        - Notes are not archived.
        - Notes are not favorites.
        """

        note = Note(
            title=note_data.title,
            content=note_data.content,
            owner_id=current_user.id,
        )

        created_note = self.repository.create(note)

        logger.info(
            "Note created",
            note_id=created_note.id,
            owner_id=current_user.id,
        )

        return created_note

    # ==========================================================
    # LIST OPERATIONS
    # ==========================================================

    def list_notes(
        self,
        *,
        current_user: User,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[int, Sequence[Note]]:
        """
        Retrieve paginated notes.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        notes = self.repository.list_notes(
            owner_id=current_user.id,
            skip=skip,
            limit=limit,
        )

        total = self.repository.count_notes(
            current_user.id,
        )

        return total, notes

    def search_notes(
        self,
        *,
        current_user: User,
        keyword: str,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[int, Sequence[Note]]:
        """
        Search notes.
        """

        page = max(page, 1)
        limit = max(1, min(limit, 100))

        skip = (page - 1) * limit

        notes = self.repository.search(
            owner_id=current_user.id,
            keyword=keyword,
            skip=skip,
            limit=limit,
        )

        return len(notes), notes

    # ==========================================================
    # FILTER OPERATIONS
    # ==========================================================

    def get_active_notes(
        self,
        *,
        current_user: User,
    ) -> Sequence[Note]:
        """
        Retrieve active notes.
        """

        return self.repository.get_active_notes(
            current_user.id,
        )

    def get_archived_notes(
        self,
        *,
        current_user: User,
    ) -> Sequence[Note]:
        """
        Retrieve archived notes.
        """

        return self.repository.get_archived_notes(
            current_user.id,
        )

    def get_favorite_notes(
        self,
        *,
        current_user: User,
    ) -> Sequence[Note]:
        """
        Retrieve favorite notes.
        """

        return self.repository.get_favorite_notes(
            current_user.id,
        )

    def get_converted_notes(
        self,
        *,
        current_user: User,
    ) -> Sequence[Note]:
        """
        Retrieve notes already converted
        into tasks.
        """

        return self.repository.get_converted_notes(
            current_user.id,
        )

    def get_notes_with_book_reference(
        self,
        *,
        current_user: User,
    ) -> Sequence[Note]:
        """
        Retrieve notes linked to Open Library.
        """

        return self.repository.get_notes_with_book_reference(
            current_user.id,
        )

    def get_recent_notes(
        self,
        *,
        current_user: User,
        limit: int = 10,
    ) -> Sequence[Note]:
        """
        Retrieve recently updated notes.
        """

        limit = max(1, min(limit, 50))

        return self.repository.list_recent_notes(
            owner_id=current_user.id,
            limit=limit,
        )

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def get_dashboard_statistics(
        self,
        *,
        current_user: User,
    ) -> dict[str, int]:
        """
        Retrieve dashboard statistics
        for the authenticated user.
        """

        return self.repository.get_dashboard_statistics(
            current_user.id,
        )
        
            # ==========================================================
    # UPDATE OPERATIONS
    # ==========================================================

    def update_note(
        self,
        *,
        current_user: User,
        note_id: int,
        note_data: NoteUpdate,
    ) -> Note:
        """
        Update a note.

        Business Rules
        --------------
        - Only owner or admin may update.
        - Archived notes cannot be updated.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        if note.is_archived:
            self._raise_archived()

        update_data = note_data.model_dump(
            exclude_unset=True,
        )

        updated_note = self.repository.update_note(
            note,
            title=update_data.get("title"),
            content=update_data.get("content"),
        )

        logger.info(
            "Note updated",
            note_id=updated_note.id,
            owner_id=current_user.id,
        )

        return updated_note

    # ==========================================================
    # ARCHIVE OPERATIONS
    # ==========================================================

    def archive_note(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Archive a note.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        if note.is_archived:
            return note

        archived_note = self.repository.archive(note)

        logger.info(
            "Note archived",
            note_id=archived_note.id,
            owner_id=current_user.id,
        )

        return archived_note

    def restore_note(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Restore an archived note.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        if not note.is_archived:
            return note

        restored_note = self.repository.restore(note)

        logger.info(
            "Note restored",
            note_id=restored_note.id,
            owner_id=current_user.id,
        )

        return restored_note

    # ==========================================================
    # FAVORITE OPERATIONS
    # ==========================================================

    def favorite_note(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Mark a note as favorite.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        if note.is_favorite:
            return note

        favorite_note = self.repository.favorite(note)

        logger.info(
            "Note marked as favorite",
            note_id=favorite_note.id,
            owner_id=current_user.id,
        )

        return favorite_note

    def unfavorite_note(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Remove favorite status.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        if not note.is_favorite:
            return note

        unfavorite_note = self.repository.unfavorite(note)

        logger.info(
            "Favorite removed",
            note_id=unfavorite_note.id,
            owner_id=current_user.id,
        )

        return unfavorite_note

    # ==========================================================
    # VIEW OPERATIONS
    # ==========================================================

    def update_last_viewed(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Update the note's last viewed timestamp.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        return self.repository.update_last_viewed(note)

    # ==========================================================
    # TASK CONVERSION
    # ==========================================================

    def convert_note_to_task(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> dict:
        """
        Prepare a note for NestJS task conversion.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        if note.is_converted_to_task:
            self._raise_already_converted()

        converted_note = self.repository.convert_to_task(
            note,
        )

        logger.info(
            "Note converted to task",
            note_id=converted_note.id,
            owner_id=current_user.id,
        )

        return {
            "note_id": converted_note.id,
            "task_created": False,
            "message": (
                "Task conversion flag updated. "
                "NestJS task creation pending."
            ),
        }

    def remove_task_conversion(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Remove task conversion flag.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        if not note.is_converted_to_task:
            return note

        updated_note = self.repository.remove_task_conversion(
            note,
        )

        logger.info(
            "Task conversion removed",
            note_id=updated_note.id,
            owner_id=current_user.id,
        )

        return updated_note
    
        # ==========================================================
    # DELETE OPERATIONS
    # ==========================================================

    def soft_delete_note(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> Note:
        """
        Soft delete a note.

        Business Rules
        --------------
        - Only the owner or an administrator may delete a note.
        - Soft-deleted notes remain in the database.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        deleted_note = self.repository.soft_delete(note)

        logger.info(
            "Note soft deleted",
            note_id=deleted_note.id,
            owner_id=current_user.id,
        )

        return deleted_note

    def restore_deleted_note(
        self,
        *,
        current_user: User,
        note: Note,
    ) -> Note:
        """
        Restore a previously soft-deleted note.

        NOTE:
        -----
        This method expects a Note instance that may already be
        soft-deleted. A repository helper such as
        get_by_id_including_deleted() is recommended.
        """

        self.validate_note_access(
            current_user=current_user,
            note=note,
        )

        if note.deleted_at is None:
            return note

        restored_note = self.repository.restore_deleted(note)

        logger.info(
            "Soft deleted note restored",
            note_id=restored_note.id,
            owner_id=current_user.id,
        )

        return restored_note

    def delete_note(
        self,
        *,
        current_user: User,
        note_id: int,
    ) -> None:
        """
        Permanently delete a note.

        WARNING
        -------
        This operation cannot be undone.
        """

        note = self.get_note_by_id(
            current_user=current_user,
            note_id=note_id,
        )

        self.repository.hard_delete(note)

        logger.warning(
            "Note permanently deleted",
            note_id=note.id,
            owner_id=current_user.id,
        )

    # ==========================================================
    # DELETE HELPERS
    # ==========================================================

    def delete_archived_notes(
        self,
        *,
        current_user: User,
    ) -> int:
        """
        Permanently delete every archived note owned
        by the current user.

        Returns:
            Number of deleted notes.
        """

        deleted = self.repository.delete_all_archived(
            current_user.id,
        )

        logger.warning(
            "Archived notes permanently deleted",
            owner_id=current_user.id,
            deleted_count=deleted,
        )

        return deleted

    def restore_all_deleted_notes(
        self,
        *,
        current_user: User,
    ) -> int:
        """
        Restore every soft-deleted note belonging
        to the current user.

        Returns:
            Number of restored notes.
        """

        restored = self.repository.restore_all_deleted(
            current_user.id,
        )

        logger.info(
            "All soft deleted notes restored",
            owner_id=current_user.id,
            restored_count=restored,
        )

        return restored
    
        # ==========================================================
    # BULK OPERATIONS
    # ==========================================================

    def bulk_archive_notes(
        self,
        *,
        current_user: User,
        note_ids: list[int],
    ) -> int:
        """
        Archive multiple notes.

        Returns:
            Number of archived notes.
        """

        if not note_ids:
            return 0

        affected = self.repository.bulk_archive(
            note_ids=note_ids,
            owner_id=current_user.id,
        )

        logger.info(
            "Bulk archive completed",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def bulk_restore_notes(
        self,
        *,
        current_user: User,
        note_ids: list[int],
    ) -> int:
        """
        Restore multiple archived notes.
        """

        if not note_ids:
            return 0

        affected = self.repository.bulk_restore(
            note_ids=note_ids,
            owner_id=current_user.id,
        )

        logger.info(
            "Bulk restore completed",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def bulk_favorite_notes(
        self,
        *,
        current_user: User,
        note_ids: list[int],
    ) -> int:
        """
        Mark multiple notes as favorite.
        """

        if not note_ids:
            return 0

        affected = self.repository.bulk_favorite(
            note_ids=note_ids,
            owner_id=current_user.id,
        )

        logger.info(
            "Bulk favorite completed",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def bulk_unfavorite_notes(
        self,
        *,
        current_user: User,
        note_ids: list[int],
    ) -> int:
        """
        Remove favorite status from multiple notes.
        """

        if not note_ids:
            return 0

        affected = self.repository.bulk_unfavorite(
            note_ids=note_ids,
            owner_id=current_user.id,
        )

        logger.info(
            "Bulk unfavorite completed",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def bulk_soft_delete_notes(
        self,
        *,
        current_user: User,
        note_ids: list[int],
    ) -> int:
        """
        Soft delete multiple notes.
        """

        if not note_ids:
            return 0

        affected = self.repository.bulk_soft_delete(
            note_ids=note_ids,
            owner_id=current_user.id,
        )

        logger.warning(
            "Bulk soft delete completed",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def bulk_hard_delete_notes(
        self,
        *,
        current_user: User,
        note_ids: list[int],
    ) -> int:
        """
        Permanently delete multiple notes.

        WARNING:
            This operation cannot be undone.
        """

        if not note_ids:
            return 0

        affected = self.repository.bulk_hard_delete(
            note_ids=note_ids,
            owner_id=current_user.id,
        )

        logger.warning(
            "Bulk hard delete completed",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def bulk_convert_notes_to_tasks(
        self,
        *,
        current_user: User,
        note_ids: list[int],
    ) -> int:
        """
        Convert multiple notes into tasks.

        Returns:
            Number of converted notes.
        """

        if not note_ids:
            return 0

        affected = self.repository.bulk_convert_to_task(
            note_ids=note_ids,
            owner_id=current_user.id,
        )

        logger.info(
            "Bulk note-to-task conversion completed",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected
    
        # ==========================================================
    # ADMIN OPERATIONS
    # ==========================================================

    def get_note_statistics(
        self,
        *,
        current_user: User,
    ) -> dict[str, int]:
        """
        Retrieve statistics for the current user's notes.
        """

        return self.repository.get_dashboard_statistics(
            current_user.id,
        )

    def get_all_user_notes(
        self,
        *,
        current_user: User,
        owner_id: int,
    ) -> Sequence[Note]:
        """
        Admin-only.

        Retrieve all notes belonging to another user.
        """

        self.validate_admin(current_user)

        return self.repository.get_all_by_owner(owner_id)

    def archive_all_notes(
        self,
        *,
        current_user: User,
    ) -> int:
        """
        Archive every active note belonging
        to the current user.
        """

        affected = self.repository.archive_all(
            current_user.id,
        )

        logger.info(
            "Archived all notes",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def restore_all_notes(
        self,
        *,
        current_user: User,
    ) -> int:
        """
        Restore every archived note belonging
        to the current user.
        """

        affected = self.repository.restore_all(
            current_user.id,
        )

        logger.info(
            "Restored all archived notes",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def favorite_all_notes(
        self,
        *,
        current_user: User,
    ) -> int:
        """
        Mark every note as favorite.
        """

        affected = self.repository.favorite_all(
            current_user.id,
        )

        logger.info(
            "Favorited all notes",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    def unfavorite_all_notes(
        self,
        *,
        current_user: User,
    ) -> int:
        """
        Remove favorite status from every note.
        """

        affected = self.repository.unfavorite_all(
            current_user.id,
        )

        logger.info(
            "Removed favorite status from all notes",
            owner_id=current_user.id,
            affected_rows=affected,
        )

        return affected

    # ==========================================================
    # UTILITY METHODS
    # ==========================================================

    def note_exists(
        self,
        note_id: int,
    ) -> bool:
        """
        Check whether a note exists.
        """

        return self.repository.exists(note_id)

    def get_note_by_book_reference(
        self,
        *,
        current_user: User,
        reference_id: str,
    ) -> Sequence[Note]:
        """
        Retrieve notes linked to a specific
        Open Library reference.
        """

        notes = self.repository.get_by_book_reference(
            reference_id,
        )

        if current_user.role.upper() == ADMIN_ROLE:
            return notes

        return [
            note
            for note in notes
            if note.owner_id == current_user.id
        ]

    # ==========================================================
    # SESSION HELPERS
    # ==========================================================

    def refresh_note(
        self,
        note: Note,
    ) -> None:
        """
        Refresh a Note instance.
        """

        self.repository.refresh(note)

    def flush(self) -> None:
        """
        Flush pending SQL statements.
        """

        self.repository.flush()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """

        self.repository.rollback()

    # ==========================================================
    # END OF SERVICE
    # ==========================================================