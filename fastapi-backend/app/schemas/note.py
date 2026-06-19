from datetime import datetime
from typing import Optional

# ConfigDict and Field are used for Pydantic model configuration and field definitions
from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Note title",
        examples=["Learning React"],
    )

    content: Optional[str] = Field(
        default=None,
        description="Detailed note content",
        examples=[
            "React hooks, state management, and component lifecycle notes"
        ],
    )


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Updated note title",
    )

    content: Optional[str] = Field(
        default=None,
        description="Updated note content",
    )


class NoteResponse(NoteBase):
    # from_attributes=True allows Pydantic to read data from ORM models directly
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique note identifier",
        examples=[1],
    )

    owner_id: int = Field(
        ...,
        description="User ID of the note owner",
        examples=[1],
    )

    book_reference_id: Optional[str] = Field(
        default=None,
        description="Optional Open Library book reference ID",
        examples=["OL45883W"],
    )

    is_converted_to_task: bool = Field(
        ...,
        description="Whether the note has been converted into task(s)",
        examples=[False],
    )

    created_at: datetime = Field(
        ...,
        description="Timestamp when the note was created",
    )

    updated_at: datetime = Field(
        ...,
        description="Timestamp when the note was last updated",
    )


class PaginatedNotesResponse(BaseModel):
    total: int = Field(
        # ... means this field is required
        ...,
        description="Total matching notes",
        examples=[125],
    )

    page: int = Field(
        ...,
        description="Current page",
        examples=[1],
    )

    limit: int = Field(
        ...,
        description="Records per page",
        examples=[10],
    )

    items: list[NoteResponse]


class NoteToTaskResponse(BaseModel):
    note_id: int = Field(
        ...,
        description="Source note ID",
    )

    task_created: bool = Field(
        ...,
        description="Whether task creation succeeded",
    )

    message: str = Field(
        ...,
        description="Conversion result message",
    )