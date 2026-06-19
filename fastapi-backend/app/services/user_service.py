from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User

DEFAULT_ROLE = "MEMBER"
ADMIN_ROLE = "ADMIN"

class UserService:
    """
    User service layer.
    
    Responsibilities:
    - User creation
    - User retrieval
    - RBAC support
    - Admin user management support
    - Shared JWT identity source
    """
    
    @staticmethod
    def create_user(db: Session, email: str, password: str, role: str = DEFAULT_ROLE) -> User:
        """
        Create a new user
        """
        existing_user = UserService.get_user_by_email(db = db, email = email)
        
        if existing_user:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email already registered")
        
        user = User(email = email, hashed_password = hash_password(password), role = role, is_active = True)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """
        Get user by email
        """
        return (db.query(User).filter(User.email==email).first())
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """
        Get user by ID
        """
        
        return (db.query(User).filter(User.id == user_id).first())
    
    @staticmethod
    def get_active_user_by_id(db: Session, user_id: int) -> User:
        """
        Retrieve active user by ID.
        
        Used by: 
        - JWT authentication
        - Current user endpoint
        - NestJS validation compatibility
        """
        user = UserService.get_user_by_id(db = db, user_id = user_id)
        
        if not user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
        
        if not user.is_active:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Inactive User Account")
        
        return user
    
    @staticmethod
    def get_all_users(db: Session, page: int = 1, limit: int = 10) -> tuple[int, list[User]]:
        """
        Admin Dashboard support.
        
        Future usage:
        - User management
        - Analytics
        - Monitoring
        """
        query = db.query(User)
        total = query.count()
        
        users = (query.order_by(User. created_at.desc()).offset((page-1) * limit).limit(limit).all())
        
        return total, users
    
    @staticmethod
    def validate_admin(current_user: User) -> None:
        """
        Admin RBAC validation
        """
        
        if current_user.role != ADMIN_ROLE:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Admin access denied")
        
    @staticmethod
    def deactivate_user(db: Session, current_user: User, user_id: int) -> User:
        """
        Admin-only user deactivation
        """
        
        UserService.validate_admin(current_user = current_user)
        
        user = UserService.get_active_user_by_id(db = db, user_id = user_id)
        
        user.is_active = False
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def activate_user(db: Session, current_user: User, user_id: int) -> User:
        """
        Admin-only user activation
        """
        
        UserService.validate_admin(current_user = current_user)
        
        user = UserService.get_user_by_id(db = db, user_id = user_id)
        
        if not user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
        
        user.is_active = True
        
        db.commit()
        db.refresh(user)
        
        return True