"""
Application-wide constants for Team Productivity Platform.

Responsibilities:
- API Versioning
- Authentication constants
- User roles
- Token types
- pagination defaults
- File upload limits
- Allowed file extensions
- Content types
- Feature flags
"""

# API
API_V1_PREFIX = "/api/v1"

# Authentication
BEARER_TOKEN_TYPE = "bearer"
ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"

# User Roles
ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_TEAM_LEAD = "team_lead"
ROLE_MEMBER = "member"

ALL_ROLES = (
    ROLE_ADMIN,
    ROLE_MANAGER,
    ROLE_TEAM_LEAD,
    ROLE_MEMBER,
)

# Task Status
TASK_STATUS_BACKLOG = "backlog"
TASK_STATUS_TODO = "todo"
TASK_STATUS_IN_PROGRESS = "in_progress"
TASK_STATUS_REVIEW = "review"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_CANCELLED = "cancelled"

TASK_STATUSES = (
    TASK_STATUS_BACKLOG,
    TASK_STATUS_TODO,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_REVIEW,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_CANCELLED,
)

# Task Priority
TASK_PRIORITY_LOW = "low"
TASK_PRIORITY_MEDIUM = "medium"
TASK_PRIORITY_HIGH = "high"
TASK_PRIORITY_CRITICAL = "critical"

TASK_PRIORITIES = (
    TASK_PRIORITY_LOW,
    TASK_PRIORITY_MEDIUM,
    TASK_PRIORITY_HIGH,
    TASK_PRIORITY_CRITICAL,
)

# Pagination
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File Upload
MAX_UPLOAD_SIZE_MB = 25

IMAGE_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "svg",
    "webp",
)

DOCUMENT_EXTENSIONS = (
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "ppt",
    "pptx",
)

# Content Types
IMAGE_CONTENT_TYPES = (
    "image/jpeg",
    "image/png",
    "image/svg+xml",
    "image/webp",
)

DOCUMENT_CONTENT_TYPES = (
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
)

# Note Status
NOTE_ACTIVE = "active"
NOTE_ARCHIVED = "archived"
NOTE_DELETED = "deleted"

# Sort Order
ASCENDING = "asc"
DESCENDING = "desc"

# Response Messages
SUCCESS = "Success"
CREATED = "Created successfully."
UPDATED = "Updated successfully."
DELETED = "Deleted successfully."

INVALID_CREDENTIALS = "Invalid email or password."
ACCESS_DENIED = "Access denied."
UNAUTHORIZED = "Unauthorized."
RESOURCE_NOT_FOUND = "Resource not found."

# HTTP Headers
AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer"

# Environment
ENV_DEVELOPMENT = "development"
ENV_STAGING = "staging"
ENV_PRODUCTION = "production"

# Cache Keys
USER_CACHE_PREFIX = "user"
NOTE_CACHE_PREFIX = "note"
BOOK_CACHE_PREFIX = "book"

# Open Library
OPEN_LIBRARY_SEARCH = "/search.json"
OPEN_LIBRARY_BOOK = "/works"

# Health Checks
SERVICE_STATUS_HEALTHY = "healthy"
SERVICE_STATUS_UNHEALTHY = "unhealthy"