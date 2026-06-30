"""
Common reusable Pydantic schemas.

These schemas provide standardized request and response models that
are shared across the FastAPI backend.

Used by:

- Authentication
- Users
- Notes
- Books
- Health
- Notifications
- Analytics
- Activity Logs
- Future Task APIs

Architecture:

API Routes
      │
      ▼
Service Layer
      │
      ▼
Common Schemas
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Base ORM Schema
# ==========================================================


class ORMModel(BaseModel):
    """
    Base schema for ORM-backed response models.

    Every response schema that maps directly to a SQLAlchemy
    model should inherit from this class instead of BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
    )


# ==========================================================
# Timestamp Mixin
# ==========================================================


class TimestampMixin(ORMModel):
    """
    Reusable timestamp fields.

    Can be inherited by any ORM response model that exposes
    creation and modification timestamps.
    """

    created_at: datetime = Field(
        ...,
        description="Timestamp when the resource was created.",
    )

    updated_at: datetime = Field(
        ...,
        description="Timestamp when the resource was last updated.",
    )


# ==========================================================
# Message Response
# ==========================================================


class MessageResponse(BaseModel):
    """
    Generic success response.

    Example:

    {
        "success": true,
        "message": "Operation completed successfully."
    }
    """

    success: bool = Field(
        default=True,
        description="Whether the operation succeeded.",
    )

    message: str = Field(
        ...,
        description="Human-readable response message.",
        examples=["Operation completed successfully."],
    )


# ==========================================================
# Success Response
# ==========================================================


class SuccessResponse(MessageResponse):
    """
    Generic success response with optional payload.

    Can be reused by every endpoint that returns
    additional structured data.
    """

    data: Any | None = Field(
        default=None,
        description="Optional response payload.",
    )


# ==========================================================
# Error Response
# ==========================================================


class ErrorResponse(BaseModel):
    """
    Standard API error response.

    Used by the global exception handlers.

    Example:

    {
        "success": false,
        "error": "ValidationError",
        "message": "...",
        "details": {},
        "path": "/api/v1/users",
        "timestamp": "..."
    }
    """

    success: bool = Field(
        default=False,
        description="Whether the request succeeded.",
    )

    error: str = Field(
        ...,
        description="Application error type.",
        examples=["ValidationError"],
    )

    message: str = Field(
        ...,
        description="Human-readable error message.",
    )

    details: dict[str, Any] | list[Any] | None = Field(
        default=None,
        description="Additional error information.",
    )

    path: str | None = Field(
        default=None,
        description="API endpoint where the error occurred.",
        examples=["/api/v1/notes"],
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the error occurred.",
    )
    
    """
Common reusable Pydantic schemas.

These schemas provide standardized request and response models that
are shared across the FastAPI backend.

Used by:

- Authentication
- Users
- Notes
- Books
- Health
- Notifications
- Analytics
- Activity Logs
- Future Task APIs

Architecture:

API Routes
      │
      ▼
Service Layer
      │
      ▼
Common Schemas
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Base ORM Schema
# ==========================================================


class ORMModel(BaseModel):
    """
    Base schema for ORM-backed response models.

    Every response schema that maps directly to a SQLAlchemy
    model should inherit from this class instead of BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
    )


# ==========================================================
# Timestamp Mixin
# ==========================================================


class TimestampMixin(ORMModel):
    """
    Reusable timestamp fields.

    Can be inherited by any ORM response model that exposes
    creation and modification timestamps.
    """

    created_at: datetime = Field(
        ...,
        description="Timestamp when the resource was created.",
    )

    updated_at: datetime = Field(
        ...,
        description="Timestamp when the resource was last updated.",
    )


# ==========================================================
# Message Response
# ==========================================================


class MessageResponse(BaseModel):
    """
    Generic success response.

    Example:

    {
        "success": true,
        "message": "Operation completed successfully."
    }
    """

    success: bool = Field(
        default=True,
        description="Whether the operation succeeded.",
    )

    message: str = Field(
        ...,
        description="Human-readable response message.",
        examples=["Operation completed successfully."],
    )


# ==========================================================
# Success Response
# ==========================================================


class SuccessResponse(MessageResponse):
    """
    Generic success response with optional payload.

    Can be reused by every endpoint that returns
    additional structured data.
    """

    data: Any | None = Field(
        default=None,
        description="Optional response payload.",
    )


# ==========================================================
# Error Response
# ==========================================================


class ErrorResponse(BaseModel):
    """
    Standard API error response.

    Used by the global exception handlers.

    Example:

    {
        "success": false,
        "error": "ValidationError",
        "message": "...",
        "details": {},
        "path": "/api/v1/users",
        "timestamp": "..."
    }
    """

    success: bool = Field(
        default=False,
        description="Whether the request succeeded.",
    )

    error: str = Field(
        ...,
        description="Application error type.",
        examples=["ValidationError"],
    )

    message: str = Field(
        ...,
        description="Human-readable error message.",
    )

    details: dict[str, Any] | list[Any] | None = Field(
        default=None,
        description="Additional error information.",
    )

    path: str | None = Field(
        default=None,
        description="API endpoint where the error occurred.",
        examples=["/api/v1/notes"],
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the error occurred.",
    )
    
    # ==========================================================
# Health Response
# ==========================================================


class HealthResponse(BaseModel):
    """
    Health check response.

    Used by:
    - /health
    - Docker health checks
    - Kubernetes probes
    - Monitoring systems
    """

    success: bool = Field(
        default=True,
        description="Whether the service is healthy.",
    )

    service: str = Field(
        ...,
        description="Service name.",
        examples=["FastAPI Backend"],
    )

    status: str = Field(
        ...,
        description="Current service status.",
        examples=["healthy"],
    )

    version: str = Field(
        ...,
        description="Application version.",
        examples=["1.0.0"],
    )

    environment: str = Field(
        ...,
        description="Current runtime environment.",
        examples=["development"],
    )

    uptime_seconds: float | None = Field(
        default=None,
        description="Application uptime in seconds.",
        examples=[86400.52],
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Health check timestamp.",
    )


# ==========================================================
# Metadata
# ==========================================================


class Metadata(BaseModel):
    """
    Generic metadata object.

    Reused by:

    - Pagination
    - Analytics
    - Reports
    - Search Results
    - Future APIs
    """

    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Response generation timestamp.",
    )

    api_version: str | None = Field(
        default=None,
        description="API version.",
        examples=["v1"],
    )

    request_id: str | None = Field(
        default=None,
        description="Unique request identifier.",
    )

    execution_time_ms: float | None = Field(
        default=None,
        description="Execution time in milliseconds.",
        examples=[14.83],
    )


# ==========================================================
# API Status
# ==========================================================


class APIStatusResponse(BaseModel):
    """
    General API status response.

    Used by root endpoints and monitoring.
    """

    success: bool = Field(
        default=True,
        description="Whether the API is running.",
    )

    name: str = Field(
        ...,
        description="Application name.",
        examples=["Team Productivity Platform API"],
    )

    version: str = Field(
        ...,
        description="Application version.",
        examples=["1.0.0"],
    )

    environment: str = Field(
        ...,
        description="Deployment environment.",
        examples=["development"],
    )

    status: str = Field(
        ...,
        description="Current application status.",
        examples=["running"],
    )


# ==========================================================
# Resource Response
# ==========================================================


class ResourceResponse(MessageResponse):
    """
    Generic response for resource operations.

    Used after:

    - Create
    - Update
    - Delete
    - Restore
    """

    resource_id: int | None = Field(
        default=None,
        description="Affected resource identifier.",
        examples=[1],
    )


# ==========================================================
# Boolean Response
# ==========================================================


class BooleanResponse(BaseModel):
    """
    Generic boolean response.

    Used for:

    - Existence checks
    - Validation endpoints
    - Feature flags
    - Permission checks
    """

    success: bool = Field(
        default=True,
        description="Whether the operation succeeded.",
    )

    result: bool = Field(
        ...,
        description="Boolean operation result.",
        examples=[True],
    )
    
    