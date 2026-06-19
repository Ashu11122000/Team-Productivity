# List and Optional are used for type hinting
from typing import List, Optional

# FastAPI imports for creating API routes, handling dependencies, and managing HTTP exceptions and status codes
# Query is used for query parameters in PI endpoints
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.note import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.services.note_service import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Note",
)
def create_note_api(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NoteService.create_note(
        db=db,
        user_id=current_user.id,
        note_data=note,
    )


@router.get(
    "",
    response_model=List[NoteResponse],
    summary="Get Notes",
)
def get_notes_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    sort_by: str = Query(default="newest"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total, notes = NoteService.get_notes(
        db=db,
        current_user=current_user,
        page=page,
        limit=limit,
        search=search,
        sort_by=sort_by,
    )

    return notes


@router.get(
    "/admin/all",
    response_model=List[NoteResponse],
    summary="Get All Notes (Admin)",
)
def get_all_notes_admin_api(
    page: int = Query(
        1,
        ge=1,
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    total, notes = NoteService.get_all_notes_admin(
        db=db,
        current_user=current_user,
        page=page,
        limit=limit,
    )

    return notes


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Get Note By ID",
)
def get_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NoteService.get_note_by_id(
        db=db,
        current_user=current_user,
        note_id=note_id,
    )


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Update Note",
)
def update_note_api(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NoteService.update_note(
        db=db,
        current_user=current_user,
        note_id=note_id,
        note_data=note_data,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Note",
)
def delete_note_api(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    NoteService.delete_note(
        db=db,
        current_user=current_user,
        note_id=note_id,
    )

    return None


@router.post(
    "/{note_id}/convert-to-task",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Convert Note To Task",
)
def convert_note_to_task_api(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NoteService.convert_note_to_task(
        db=db,
        current_user=current_user,
        note_id=note_id,
    )