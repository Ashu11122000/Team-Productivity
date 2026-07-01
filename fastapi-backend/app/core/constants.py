"""
Application-wide constants for Team Productivity Platform.

This module centralizes all reusable constants used throughout the
application to avoid hard-coded values.

Categories:
- API
- Authentication
- User Roles
- Permissions
- Task Management
- Project Management
- Pagination
- File Uploads
- HTTP
- Responses
- Environment
- Cache
- Integrations
"""

API_V1_PREFIX = "/api/v1"

BEARER_TOKEN_TYPE = "bearer"

ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer"

ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_TEAM_LEAD = "team_lead"
ROLE_EMPLOYEE = "employee"

ALL_ROLES = (
    ROLE_ADMIN,
    ROLE_MANAGER,
    ROLE_TEAM_LEAD,
    ROLE_EMPLOYEE,
)

PERMISSION_CREATE = "create"
PERMISSION_READ = "read"
PERMISSION_UPDATE = "update"
PERMISSION_DELETE = "delete"

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

PROJECT_STATUS_PLANNING = "planning"
PROJECT_STATUS_ACTIVE = "active"
PROJECT_STATUS_ON_HOLD = "on_hold"
PROJECT_STATUS_COMPLETED = "completed"
PROJECT_STATUS_ARCHIVED = "archived"

PROJECT_STATUSES = (
    PROJECT_STATUS_PLANNING,
    PROJECT_STATUS_ACTIVE,
    PROJECT_STATUS_ON_HOLD,
    PROJECT_STATUS_COMPLETED,
    PROJECT_STATUS_ARCHIVED,
)

NOTE_ACTIVE = "active"
NOTE_ARCHIVED = "archived"
NOTE_DELETED = "deleted"

NOTE_STATUSES = (
    NOTE_ACTIVE,
    NOTE_ARCHIVED,
    NOTE_DELETED,
)

ASCENDING = "asc"
DESCENDING = "desc"

SORT_ORDERS = (
    ASCENDING,
    DESCENDING,
)

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

MAX_UPLOAD_SIZE_MB = 25
BYTES_PER_MB = 1024 * 1024

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

HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_PATCH = "PATCH"
HTTP_DELETE = "DELETE"

SUCCESS = "Success"
CREATED = "Created successfully."
UPDATED = "Updated successfully."
DELETED = "Deleted successfully."

INVALID_CREDENTIALS = "Invalid email or password."
ACCESS_DENIED = "Access denied."
UNAUTHORIZED = "Unauthorized."
RESOURCE_NOT_FOUND = "Resource not found."
VALIDATION_ERROR = "Validation failed."
INTERNAL_SERVER_ERROR = "Internal server error."

ENV_DEVELOPMENT = "development"
ENV_TESTING = "testing"
ENV_STAGING = "staging"
ENV_PRODUCTION = "production"

USER_CACHE_PREFIX = "user"
NOTE_CACHE_PREFIX = "note"
BOOK_CACHE_PREFIX = "book"
TASK_CACHE_PREFIX = "task"

OPEN_LIBRARY_SEARCH = "/search.json"
OPEN_LIBRARY_BOOK = "/works"

SERVICE_STATUS_HEALTHY = "healthy"
SERVICE_STATUS_UNHEALTHY = "unhealthy"

NOTIFICATION_IN_APP = "in_app"
NOTIFICATION_EMAIL = "email"
NOTIFICATION_PUSH = "push"

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

__all__ = [
    "API_V1_PREFIX",
    "ACCESS_TOKEN",
    "REFRESH_TOKEN",
    "ALL_ROLES",
    "TASK_STATUSES",
    "TASK_PRIORITIES",
    "PROJECT_STATUSES",
    "NOTE_STATUSES",
    "SORT_ORDERS",
    "DEFAULT_PAGE",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "IMAGE_EXTENSIONS",
    "DOCUMENT_EXTENSIONS",
]