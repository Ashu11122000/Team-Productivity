from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.core.config import settings
from app.core.logging import logger

from app.api.routes import auth, users, notes, books, health

# Application Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.

    Future:
    - Redis Connection
    - Sentry Initialization
    - Background Workers
    - Scheduler
    """

    logger.info("Starting Team Productivity Platform FastAPI Service")

    yield

    logger.info("Shutting down Team Productivity Platform FastAPI Service")

# FastAPI Application
app = FastAPI(
    title="Team Productivity Platform API",
    description="""
    FastAPI Identity & Knowledge Service

    Responsibilities:
    - Authentication
    - User Management
    - Notes Management
    - Books Integration
    - Refresh Tokens
    - User Profiles

    Consumed by:
    - Next.js Web Application
    - Flutter Mobile Application

    Shared JWT Authentication with NestJS.
    """,
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "success": True,
        "service": "FastAPI",
        "name": "Team Productivity Platform",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "status": "running",
    }

# API Route Registration
API_PREFIX = "/api/v1"

# Health
app.include_router(
    health.router,
    prefix=API_PREFIX,
    tags=["Health"],
)

# Authentication
app.include_router(
    auth.router,
    prefix=API_PREFIX,
    tags=["Authentication"],
)

# Users
app.include_router(
    users.router,
    prefix=API_PREFIX,
    tags=["Users"],
)

# Notes
app.include_router(
    notes.router,
    prefix=API_PREFIX,
    tags=["Notes"],
)

# Books
app.include_router(
    books.router,
    prefix=API_PREFIX,
    tags=["Books"],
)