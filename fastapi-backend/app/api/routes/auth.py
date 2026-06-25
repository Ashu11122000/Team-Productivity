from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import (create_access_token, verify_password)
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (UserCreate, UserLogin, UserResponse)
from app.services.user_service import UserService

router = APIRouter(prefix = "/auth", tags = ["Authentication"])

@router.post(
    "/register",
    status_code = status.HTTP_201_CREATED,
    summary = "Register a new user",
    description = """
    Register a new user account.
    
    This endpoint is responsible for creating users in the FastAPI Identity Service.
    
    The generated account can later authenticate with both FastAPI and NestJS using the shared JWT authentication strategy.
    """
)
def register(user: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing_user = UserService.get_user_by_email(db = db, email = user.email)
    
    if existing_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email is already registered.")
    
    new_user = UserService.create_user(db = db, email = user.email, password = user.password)
    
    return {
        "success": True,
        "message": "User registered successfully",
        "data": {
            "id": new_user.id,
            "email": new_user.email,
            "role": new_user.role,
        },
    }

@router.post(
    "/login",
    summary = "Authenticate user",
    description = """
    Authenticate a user and return a JWT access token.
    
    This JWT is trusted by: 
    - FastAPI
    - NestJS
    
    allowing both services to share a common authentication system.
    """
)
def login(user: UserLogin, db: Session = Depends(get_db)) -> dict:
    db_user = UserService.get_user_by_email(db = db, email = user.email)
    
    if db_user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid email and password.")
    
    if not db_user.is_active:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "User account is inactive.")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid email or password")
    
    access_token = create_access_token(
        user_id = str(db_user.id),
        email = db_user.email,
        role = db_user.role,
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
    summary = "Get current authenticated user",
    description = """
    Return the currently authenticated user's profile.

    Used by:
    - Next.js Web Application
    - Flutter Mobile Application
    - Profile Screen
    - Role-Based UI
    - Permission checks
    """
)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user