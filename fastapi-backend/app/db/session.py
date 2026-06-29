"""
Database configuration for the Team Productivity Platform.

Responsibilities:
- Create and manage the SQLAlchemy engine
- Provide database sessions to FastAPI routes and services
- Support PostgreSQL connectivity with connection pooling
- Share a single engine across the application

Architecture:
    Next.js / Flutter
        ↓
    FastAPI
        ↓
    SQLAlchemy ORM
        ↓
    PostgreSQL
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo = settings.DATABASE_ECHO,
    pool_pre_ping = True,
    pool_size = 10,
    max_overflow = 20,
    pool_recycle = 3600,
    future = True,
)

SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False,
    expire_on_commit = False,
    future = True
)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    
    Example:
    db: Session = Depends(get_db)
    
    A new session is created for every request and is automatically closed after the request completes.
    """
    
    db = SessionLocal()
    
    try:
        yield db
    finally: 
        db.close()
    
    