"""
Reusable pagination schemas.

These schemas provide standardized pagination models used
across the FastAPI backend.

Used by:

- Users
- Notes
- Books
- Analytics
- Notifications
- Activity Logs
- Future APIs

Supports:

- Offset pagination
- Generic paginated responses
- Sorting
- Future cursor pagination

Architecture:

API Routes
      │
      ▼
Services
      │
      ▼
Repositories
      │
      ▼
Pagination Schemas
"""

from __future__ import annotations

from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


# ==========================================================
# Generic Type
# ==========================================================

T = TypeVar("T")


# ==========================================================
# Sort Direction
# ==========================================================


class SortDirection(str, Enum):
    """
    Supported sorting directions.
    """

    ASC = "asc"
    DESC = "desc"


# ==========================================================
# Pagination Parameters
# ==========================================================


class PaginationParams(BaseModel):
    """
    Standard pagination request parameters.

    Used by every paginated endpoint.
    """

    page: int = Field(
        default=1,
        ge=1,
        description="Page number.",
        examples=[1],
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of records per page.",
        examples=[10],
    )


# ==========================================================
# Sorting Parameters
# ==========================================================


class SortParams(BaseModel):
    """
    Sorting options.

    Example:

    ?sort_by=created_at&sort_direction=desc
    """

    sort_by: str | None = Field(
        default=None,
        description="Database field used for sorting.",
        examples=["created_at"],
    )

    sort_direction: SortDirection = Field(
        default=SortDirection.DESC,
        description="Sorting direction.",
    )


# ==========================================================
# Pagination Metadata
# ==========================================================


class PaginationMetadata(BaseModel):
    """
    Metadata returned with every paginated response.
    """

    page: int = Field(
        ...,
        ge=1,
        description="Current page.",
        examples=[1],
    )

    limit: int = Field(
        ...,
        ge=1,
        description="Items per page.",
        examples=[10],
    )

    total: int = Field(
        ...,
        ge=0,
        description="Total matching records.",
        examples=[253],
    )

    total_pages: int = Field(
        ...,
        ge=0,
        description="Total number of pages.",
        examples=[26],
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
    
    # ==========================================================
# Generic Paginated Response
# ==========================================================


class PaginatedResponse(GenericModel, Generic[T]):
    """
    Generic paginated response.

    Can be reused by every paginated endpoint.

    Examples:

        PaginatedResponse[UserResponse]

        PaginatedResponse[NoteListItem]

        PaginatedResponse[BookResponse]
    """

    items: list[T] = Field(
        ...,
        description="Current page of records.",
    )

    metadata: PaginationMetadata = Field(
        ...,
        description="Pagination metadata.",
    )


# ==========================================================
# Offset Pagination
# ==========================================================


class OffsetPagination(PaginationParams):
    """
    Offset-based pagination.

    Provides helper properties for repositories.
    """

    @property
    def offset(self) -> int:
        """
        SQL OFFSET value.
        """
        return (self.page - 1) * self.limit

    @property
    def end(self) -> int:
        """
        Last record position.

        Mainly useful for debugging
        and analytics.
        """
        return self.offset + self.limit


# ==========================================================
# Cursor Pagination Request
# ==========================================================


class CursorPagination(BaseModel):
    """
    Cursor pagination request.

    Reserved for future APIs handling
    very large datasets.

    Example:

        GET /notes?cursor=abc123&limit=20
    """

    cursor: str | None = Field(
        default=None,
        description="Opaque pagination cursor.",
    )

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum records to return.",
    )


# ==========================================================
# Cursor Page Response
# ==========================================================


class CursorPage(GenericModel, Generic[T]):
    """
    Cursor pagination response.

    Suitable for infinite scrolling,
    mobile feeds and high-volume APIs.
    """

    items: list[T] = Field(
        ...,
        description="Records in the current page.",
    )

    next_cursor: str | None = Field(
        default=None,
        description="Cursor for the next page.",
    )

    previous_cursor: str | None = Field(
        default=None,
        description="Cursor for the previous page.",
    )

    has_next: bool = Field(
        ...,
        description="Whether another page exists.",
    )

    has_previous: bool = Field(
        ...,
        description="Whether a previous page exists.",
    )


# ==========================================================
# Pagination Utility
# ==========================================================


class PaginationUtils:
    """
    Helper utilities for pagination.

    Used by repositories and services.
    """

    @staticmethod
    def build_metadata(
        *,
        page: int,
        limit: int,
        total: int,
    ) -> PaginationMetadata:
        """
        Build PaginationMetadata from
        pagination values.
        """

        total_pages = (
            (total + limit - 1) // limit
            if limit > 0
            else 0
        )

        return PaginationMetadata(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )