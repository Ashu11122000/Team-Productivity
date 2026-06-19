"""
Database configuration for the Team Productivity Platform.

Responsibilities:
- Create and manage the SQLAlchemy engine.
- Provide database sessions to FastAPI routes and services.
- Support PostgreSQL connectivity.
- Enable connection pooling for production workloads.
- Serve FastAPI-owned modules:
    - Authentication
    - Users 
    - Notes
    - Open Library integrations
    
Architecture:
    Next.js Frontend
        ↓
    FastAPI
        ↓
    SQLAlchemy ORM
        ↓
    PostgreSQL
    
NestJS may connect to the same PostgreSQL instance using its own ORM (TypeORM/Prisma) but does not depend on this module.
"""

# Generator for type hinting, quote_plus for URL encoding, SQLAlchemy imports for engine and session management
from collections.abc import Generator

# quote_plus for URL encoding, SQLAlchemy imports for engine and session management
from urllib.parse import quote_plus

# create_engine for creating the SQLAlchemy engine, Session and sessionmaker for managing database sessions
from sqlalchemy import create_engine

# Session and sessionmaker for managing database sessions
from sqlalchemy.orm import Session, sessionmaker

# Importing settings from the core configuration to access database credentials and other configurations
from app.core.config import settings

# Database password is URL-encoded to ensure special characters do not break the connection string
password = quote_plus(settings.DB_PASSWORD)

# Constructing the DATABASE_URL using the settings from the configuration, ensuring compatibility with SQLAlchemy and PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:{password}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Debugging output to verify the constructed DATABASE_URL
print("=" * 80)
print("DATABASE_URL =", DATABASE_URL)
print("=" * 80)

# SQLAlchemy Engine for managing database connections, with connection pooling and other performance optimizations
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=settings.DEBUG,
)

# Session Factory for creating new database sessions, with autocommit and autoflush disabled for transaction safety
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,    # Used for transaction safety
    autoflush=False,    # Used for transaction safety
    expire_on_commit=False,
)

# Dependency used in FastAPI routes to provide a database session for each request, ensures proper cleanup and transaction management
def get_db() -> Generator[Session, None, None]: 
    """
    FastAPI database dependency.
    
    Usage:
        db: Session = Depends(get_db)
        
    Ensures:
        - Session creation per request
        - Automatic cleanup
        - Transaction safety
    """
    db = SessionLocal()
    
    try: 
        yield db     # yield the session to the route handler, allowing it to perform database operations
        
    finally:
        db.close()