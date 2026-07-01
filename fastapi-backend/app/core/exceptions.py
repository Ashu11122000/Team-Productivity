"""
Custom exceptions for the Team Productivity Platform.

Provides standardized API exceptions used across the application.
"""

from typing import Any

from fastapi import HTTPException, status


class APIException(HTTPException):
    """
    Base exception for all application exceptions.
    """

    def __init__(
        self,
        *,
        status_code: int,
        detail: str,
        error_code: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        self.error_code = error_code

        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )

class InvalidCredentialsException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            error_code="INVALID_CREDENTIALS",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            error_code="INVALID_TOKEN",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            error_code="TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnauthorizedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            error_code="UNAUTHORIZED",
            headers={"WWW-Authenticate": "Bearer"},
        )


class RefreshTokenExpiredException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired.",
            error_code="REFRESH_TOKEN_EXPIRED",
        )


class InactiveUserException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
            error_code="USER_INACTIVE",
        )


class EmailNotVerifiedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email address is not verified.",
            error_code="EMAIL_NOT_VERIFIED",
        )

class PermissionDeniedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
            error_code="PERMISSION_DENIED",
        )


class RoleNotAllowedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your role is not allowed to access this resource.",
            error_code="ROLE_NOT_ALLOWED",
        )

class UserAlreadyExistsException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
            error_code="USER_ALREADY_EXISTS",
        )


class UserNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
            error_code="USER_NOT_FOUND",
        )

class NoteNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
            error_code="NOTE_NOT_FOUND",
        )

class TaskNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
            error_code="TASK_NOT_FOUND",
        )

class ProjectNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
            error_code="PROJECT_NOT_FOUND",
        )

class ResourceNotFoundException(APIException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
            error_code="RESOURCE_NOT_FOUND",
        )


class ResourceAlreadyExistsException(APIException):
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists.",
            error_code="RESOURCE_ALREADY_EXISTS",
        )

class ValidationException(APIException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
            error_code="VALIDATION_ERROR",
        )


class BadRequestException(APIException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
            error_code="BAD_REQUEST",
        )

class FileTooLargeException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file exceeds the maximum allowed size.",
            error_code="FILE_TOO_LARGE",
        )


class UnsupportedFileTypeException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type.",
            error_code="UNSUPPORTED_FILE_TYPE",
        )

class BookNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
            error_code="BOOK_NOT_FOUND",
        )

class ExternalServiceException(APIException):
    def __init__(self, service: str) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{service} is currently unavailable.",
            error_code="EXTERNAL_SERVICE_ERROR",
        )

class RateLimitExceededException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
        )

class DatabaseException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed.",
            error_code="DATABASE_ERROR",
        )

class InternalServerException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
            error_code="INTERNAL_SERVER_ERROR",
        )