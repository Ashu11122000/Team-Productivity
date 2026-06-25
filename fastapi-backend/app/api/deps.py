from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieve the currently authenticated user from the HWT access token.
    """
    
    payload = decode_access_token(token)
    subject = payload.get("sub")
    
    if subject is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid access token.")
    
    # Currently "sub" stores the user's email.
    # Later this can be changed to user_id without changing route logic.
    user = UserService.get_user_by_email(db = db, email = subject)
    
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found.")
    
    if not user.is_active:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "User account is inactive.")
    
    return user

def require_role(required_role: str) -> Callable:
    """
    Restrict an endpoint to a single role.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Insufficient permissions.")
        
        return current_user
    
    return role_checker

def require_roles(allowed_roles: list[str]) -> Callable:
    """
    Restrict an endpoint to multiple roles.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Access Denied")
        
        return current_user
    
    return role_checker

