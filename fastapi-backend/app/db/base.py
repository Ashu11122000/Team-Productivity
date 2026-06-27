"""
    Base SQLAlchemy model for the Team Productivity Platform.
    
    Responsibilities:
    - Provides the root declarative base for all SQLAlchemy ORM Models. 
    - Provides shared SQLAlchemy metadata across all database entities.
    - Used Alembic for database migrations
    - Serves as the foundation for all FastAPI-owned database models

    - Shared across:
        - Authentication
        - Users
        - Notes
        - Refresh Tokens
        - Books References
        - User Preferences
        - Profiles
        - Sessions
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