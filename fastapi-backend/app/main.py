from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.routes import auth, books, health, notes, users
from app.core.config import settings
from app.lifespan import lifespan

from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.response_time import ResponseTimeMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware

app = FastAPI(
    title="Team Productivity Platform API",
    description="""
FastAPI Identity & Knowledge Service

Responsibilities

• Authentication
• User Management
• Notes Management
• Books Integration
• Refresh Tokens
• User Profiles

Consumed By

• Next.js Web Application
• Flutter Mobile Application

Shared JWT Authentication with NestJS.
""",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ResponseTimeMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "success": True,
        "service": "FastAPI",
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
    }

# API Routes
API_PREFIX = settings.API_V1_PREFIX

app.include_router(
    health.router,
    prefix=API_PREFIX,
    tags=["Health"],
)

app.include_router(
    auth.router,
    prefix=API_PREFIX,
    tags=["Authentication"],
)

app.include_router(
    users.router,
    prefix=API_PREFIX,
    tags=["Users"],
)

app.include_router(
    notes.router,
    prefix=API_PREFIX,
    tags=["Notes"],
)

app.include_router(
    books.router,
    prefix=API_PREFIX,
    tags=["Books"],
)