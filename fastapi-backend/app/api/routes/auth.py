# FastAPI Authentication Routes
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.user_service import UserService

# FastAPI Router for Authentication Endpoints
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
    Create a new user account.

    Roles supported:
    - MEMBER (default)
    - ADMIN (future support)

    Authentication is managed by FastAPI and shared with NestJS
    through a common JWT strategy.
    """,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = UserService.get_user_by_email(
        db=db,
        email=user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    new_user = UserService.create_user(
        db=db,
        email=user.email,
        password=user.password,
    )

    return {
        "success": True,
        "message": "User registered successfully",
        "data": {
            "user_id": new_user.id,
            "email": new_user.email,
            "role": new_user.role,
        },
    }


@router.post(
    "/login",
    summary="Login user",
    description="""
    Authenticate a user and return a JWT access token.

    The same JWT is used by:
    - FastAPI
    - NestJS

    This enables shared authentication across services.
    """,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    db_user = UserService.get_user_by_email(
        db=db,
        email=user.email,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    if not verify_password(
        user.password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=str(db_user.id),
        email=db_user.email,
        role=db_user.role,
    )

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "role": db_user.role,
            },
        },
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user",
    description="""
    Return the currently authenticated user.

    Used by:
    - Next.js frontend
    - Role-based UI rendering
    - Profile pages
    - Permission checks
    """,
)
def get_me(
    current_user=Depends(get_current_user),
):
    return current_user