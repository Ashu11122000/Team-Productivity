from datetime import datetime, timezone
from sqlalchemy import (Boolean, Column, DateTime, Integer, String, Index)
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    """
    User Model
    
    FastAPI Ownership:
    - Authentication
    - Authorization
    - User Management
    
    JWT Source of Truth:
    - id
    - email
    - role
    
    Consumed by:
    - FastAPI 
    - NestJS
    - Next.js Frontend
    """
    
    __tablename__ = "users"
    
    __table_args = (
        Index("idx_users_email", "email"),
        Index("idx_users_role", "role"),
        Index("idx_users_active", "is_active"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    role = Column(String(50), default="Member", nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc), nullable=False)
    
    updated_at = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    notes = relationship("Note", back_populates="owner", cascade = "all, delete-orphan", passive_deletes = True)
    
    def __repr__(self) -> str:
        return (
            f"<user("
            f"id={self.id}"
            f"email='{self.email}',"
            f"role='{self.role}'"
            f")>"
        )