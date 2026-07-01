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
from sqlalchemy import Metadata
from sqlalchemy.orm import DeclarativeBase # type: ignore

# Naming Convention
# Using a naming convention ensures consistent constraints/indexes names and helps with debugging

NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = Metadata(naming_convention=NAMING_CONVENTION)

class Base(DeclarativeBase):
    
    """Base Class for all SQLAlchemy ORM models"""
    metadata = metadata
    
__all__ = ["Base", "metadata"] 