"""
Note-related Pydantic schemas.

This module defines request and response schemas used by the
Notes module of the Team Productivity Platform.

Features:
- Note CRUD
- Search
- Pagination
- Archive / Restore
- Favorites
- Soft Delete
- Note → Task Conversion
- Open Library Book References
- Statistics

Architecture:

API Routes
      │
      ▼
Note Service
      │
      ▼
Note Repository
      │
      ▼
SQLAlchemy Models
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Base Schema
# ==========================================================


class NoteBase(BaseModel):
    """
    Base schema shared by all note-related request
    and response models.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Note title.",
        examples=["Learning React"],
    )

    content: str | None = Field(
        default=None,
        description="Detailed note content.",
        examples=[
            (
                "React hooks, state management, component lifecycle, "
                "and performance optimization notes."
            )
        ],
    )


# ==========================================================
# Create Note
# ==========================================================


class NoteCreate(NoteBase):
    """
    Request schema for creating a new note.
    """

    book_reference_id: int | None = Field(
        default=None,
        description=(
            "Optional cached BookReference identifier associated "
            "with this note."
        ),
        examples=[1],
    )


# ==========================================================
# Update Note
# ==========================================================


class NoteUpdate(BaseModel):
    """
    Request schema for updating an existing note.

    Supports partial updates.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Updated note title.",
    )

    content: str | None = Field(
        default=None,
        description="Updated note content.",
    )

    book_reference_id: int | None = Field(
        default=None,
        description="Updated BookReference identifier.",
        examples=[1],
    )


# ==========================================================
# Note Summary
# ==========================================================


class NoteSummary(BaseModel):
    """
    Lightweight representation of a note.

    Used for:
    - Dashboard
    - Search results
    - Sidebar
    - Recent notes
    - Related notes

    Avoids returning the complete note content.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique note identifier.",
        examples=[1],
    )

    title: str = Field(
        ...,
        description="Note title.",
    )

    owner_id: int = Field(
        ...,
        description="Owner user identifier.",
        examples=[1],
    )

    is_archived: bool = Field(
        ...,
        description="Whether the note is archived.",
        examples=[False],
    )

    is_favorite: bool = Field(
        ...,
        description="Whether the note is marked as favorite.",
        examples=[False],
    )

    is_deleted: bool = Field(
        ...,
        description="Whether the note has been soft deleted.",
        examples=[False],
    )

    is_converted_to_task: bool = Field(
        ...,
        description="Whether the note has been converted into task(s).",
        examples=[False],
    )

    updated_at: datetime = Field(
        ...,
        description="Last modification timestamp.",
    )
    
    # ==========================================================
# Note Response
# ==========================================================


class NoteResponse(NoteBase):
    """
    Standard note response returned by the API.

    Compatible with SQLAlchemy ORM models.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique note identifier.",
        examples=[1],
    )

    owner_id: int = Field(
        ...,
        description="Owner user identifier.",
        examples=[1],
    )

    book_reference_id: int | None = Field(
        default=None,
        description="Associated BookReference identifier.",
        examples=[1],
    )

    is_archived: bool = Field(
        ...,
        description="Whether the note is archived.",
        examples=[False],
    )

    is_favorite: bool = Field(
        ...,
        description="Whether the note is marked as favorite.",
        examples=[False],
    )

    is_deleted: bool = Field(
        ...,
        description="Whether the note has been soft deleted.",
        examples=[False],
    )

    is_converted_to_task: bool = Field(
        ...,
        description="Whether the note has been converted into one or more tasks.",
        examples=[False],
    )

    created_at: datetime = Field(
        ...,
        description="Timestamp when the note was created.",
    )

    updated_at: datetime = Field(
        ...,
        description="Timestamp when the note was last updated.",
    )


# ==========================================================
# Note List Item
# ==========================================================


class NoteListItem(BaseModel):
    """
    Lightweight note representation used in:

    - Dashboard
    - Recent Notes
    - Sidebar
    - Search Results
    - Pagination

    Reduces payload size by omitting the full content.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique note identifier.",
        examples=[1],
    )

    title: str = Field(
        ...,
        description="Note title.",
    )

    owner_id: int = Field(
        ...,
        description="Owner user identifier.",
    )

    book_reference_id: int | None = Field(
        default=None,
        description="Associated BookReference identifier.",
    )

    is_archived: bool = Field(
        ...,
        description="Archive status.",
    )

    is_favorite: bool = Field(
        ...,
        description="Favorite status.",
    )

    is_deleted: bool = Field(
        ...,
        description="Soft delete status.",
    )

    is_converted_to_task: bool = Field(
        ...,
        description="Whether converted into task(s).",
    )

    updated_at: datetime = Field(
        ...,
        description="Last modification timestamp.",
    )


# ==========================================================
# Paginated Notes Response
# ==========================================================


class PaginatedNotesResponse(BaseModel):
    """
    Paginated response returned by the Notes API.
    """

    total: int = Field(
        ...,
        description="Total matching notes.",
        examples=[125],
    )

    page: int = Field(
        ...,
        description="Current page number.",
        examples=[1],
    )

    limit: int = Field(
        ...,
        description="Number of records per page.",
        examples=[10],
    )

    total_pages: int = Field(
        ...,
        description="Total available pages.",
        examples=[13],
    )

    has_next: bool = Field(
        ...,
        description="Whether another page exists.",
        examples=[True],
    )

    has_previous: bool = Field(
        ...,
        description="Whether a previous page exists.",
        examples=[False],
    )

    items: list[NoteListItem] = Field(
        ...,
        description="List of notes.",
    )


# ==========================================================
# Note Search Request
# ==========================================================


class NoteSearchRequest(BaseModel):
    """
    Request schema for searching notes.
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Search keyword.",
        examples=["React"],
    )

    include_archived: bool = Field(
        default=False,
        description="Include archived notes.",
    )

    include_deleted: bool = Field(
        default=False,
        description="Include soft-deleted notes.",
    )

    favorites_only: bool = Field(
        default=False,
        description="Return only favorite notes.",
    )

    converted_only: bool = Field(
        default=False,
        description="Return only notes converted to tasks.",
    )

    page: int = Field(
        default=1,
        ge=1,
        description="Page number.",
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Records per page.",
    )
    
    # ==========================================================
# Archive Note Response
# ==========================================================


class ArchiveNoteResponse(BaseModel):
    """
    Response returned after successfully archiving a note.
    """

    success: bool = Field(
        default=True,
        description="Whether the archive operation succeeded.",
    )

    note_id: int = Field(
        ...,
        description="Archived note identifier.",
        examples=[1],
    )

    is_archived: bool = Field(
        default=True,
        description="Current archive status.",
    )

    message: str = Field(
        default="Note archived successfully.",
        description="Operation result message.",
    )


# ==========================================================
# Restore Note Response
# ==========================================================


class RestoreNoteResponse(BaseModel):
    """
    Response returned after restoring an archived or
    soft-deleted note.
    """

    success: bool = Field(
        default=True,
        description="Whether the restore operation succeeded.",
    )

    note_id: int = Field(
        ...,
        description="Restored note identifier.",
        examples=[1],
    )

    is_archived: bool = Field(
        default=False,
        description="Current archive status.",
    )

    is_deleted: bool = Field(
        default=False,
        description="Current soft delete status.",
    )

    message: str = Field(
        default="Note restored successfully.",
        description="Operation result message.",
    )


# ==========================================================
# Favorite Note Response
# ==========================================================


class FavoriteNoteResponse(BaseModel):
    """
    Response returned after marking or unmarking
    a note as favorite.
    """

    success: bool = Field(
        default=True,
        description="Whether the operation succeeded.",
    )

    note_id: int = Field(
        ...,
        description="Affected note identifier.",
        examples=[1],
    )

    is_favorite: bool = Field(
        ...,
        description="Favorite status after operation.",
    )

    message: str = Field(
        ...,
        description="Operation result message.",
        examples=[
            "Note added to favorites.",
            "Note removed from favorites.",
        ],
    )


# ==========================================================
# Delete Note Response
# ==========================================================


class DeleteNoteResponse(BaseModel):
    """
    Response returned after deleting a note.

    Supports both soft delete and hard delete.
    """

    success: bool = Field(
        default=True,
        description="Whether the delete operation succeeded.",
    )

    note_id: int = Field(
        ...,
        description="Deleted note identifier.",
    )

    deleted: bool = Field(
        default=True,
        description="Whether the note is deleted.",
    )

    permanent: bool = Field(
        default=False,
        description="True for hard delete, False for soft delete.",
    )

    message: str = Field(
        ...,
        description="Operation result message.",
    )


# ==========================================================
# Note → Task Conversion
# ==========================================================


class NoteToTaskResponse(BaseModel):
    """
    Response returned after converting a note
    into a task.
    """

    success: bool = Field(
        default=True,
        description="Whether task conversion succeeded.",
    )

    note_id: int = Field(
        ...,
        description="Source note identifier.",
    )

    task_created: bool = Field(
        ...,
        description="Whether a task was successfully created.",
    )

    task_id: int | None = Field(
        default=None,
        description="Created task identifier (future NestJS integration).",
        examples=[101],
    )

    message: str = Field(
        ...,
        description="Conversion result message.",
    )


# ==========================================================
# Note Statistics
# ==========================================================


class NoteStatistics(BaseModel):
    """
    Statistics about a user's notes.

    Used for dashboards and analytics.
    """

    total_notes: int = Field(
        ...,
        description="Total notes.",
        examples=[150],
    )

    active_notes: int = Field(
        ...,
        description="Total active notes.",
        examples=[120],
    )

    archived_notes: int = Field(
        ...,
        description="Archived notes.",
        examples=[15],
    )

    favorite_notes: int = Field(
        ...,
        description="Favorite notes.",
        examples=[28],
    )

    deleted_notes: int = Field(
        ...,
        description="Soft deleted notes.",
        examples=[5],
    )

    converted_notes: int = Field(
        ...,
        description="Notes converted to tasks.",
        examples=[32],
    )


# ==========================================================
# Bulk Operations
# ==========================================================


class BulkNoteOperationResponse(BaseModel):
    """
    Response returned after bulk operations.

    Examples:
    - Bulk archive
    - Bulk restore
    - Bulk delete
    - Bulk favorite
    """

    success: bool = Field(
        default=True,
        description="Whether the bulk operation succeeded.",
    )

    affected_count: int = Field(
        ...,
        description="Number of affected notes.",
        examples=[25],
    )

    message: str = Field(
        ...,
        description="Operation result message.",
    )