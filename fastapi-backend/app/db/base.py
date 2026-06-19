"""
    Base SQLAlchemy model for the Team Productivity Platform.
    
    Responsibilities:
    - Acts as the root ORM model for all database entities
    - Provides shared SQLAlchemy metadata
    - Used by Alembic migrations
    - Shared across:
        - Authentication
        - Users
        - Notes
        - Future FastAPI modules
    
    Ownership:
    - FastAPI owns the database schema for:
        - Users
        - Notes
    
    Architecture:
        ↓
    FastAPI
        ↓
    SQLAlchemy ORM
        ↓
    PostgreSQL
"""
from sqlalchemy.orm import DeclarativeBase # type: ignore

class Base(DeclarativeBase):
    
    """Base Class for all SQLAlchemy ORM models"""
    pass