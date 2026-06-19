from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.routes import auth, note

from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.note import Note

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Team Productivity Platform API",
    description="""
    FastAPI Service

    Responsibilities:
    - Authentication
    - User Management
    - Notes Management
    - Open Library Integration
    - Notes → Task Conversion

    Consumed by Next.js Frontend.
    Shared JWT Authentication with NestJS.
    """,
    version="1.0.0",
    debug=settings.DEBUG,
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "FastAPI",
        "name": "Team Productivity Platform",
        "status": "running",
        "version": "1.0.0",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }

# Authentication Routes
app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Authentication"],
)

# Notes Routes
app.include_router(
    note.router,
    prefix="/api/v1",
    tags=["Notes"],
)