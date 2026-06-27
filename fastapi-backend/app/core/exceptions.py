"""
Custom exceptions for the Team Productivity Platform.

Responsibilities:
- Standardize API exceptions.
- Reduce duplicate HTTPException code.
- Improve readability.
- Centralize business exceptions.
"""

from fastapi import HTTPException, status


class APIException(HTTPException):
    """
    Base exception for all custom API exceptions.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
        )

# Authentication Exceptions
class InvalidCredentialsException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )


class InvalidTokenException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        )


class UnauthorizedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )


class InactiveUserException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

# Authorization Exceptions
class PermissionDeniedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )


class RoleNotAllowedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your role is not allowed to access this resource.",
        )

# User Exceptions
class UserAlreadyExistsException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        )


class UserNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

# Note Exceptions
class NoteNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )

# Resource Exceptions
class ResourceNotFoundException(APIException):
    def __init__(
        self,
        resource: str = "Resource",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
        )


class ResourceAlreadyExistsException(APIException):
    def __init__(
        self,
        resource: str = "Resource",
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists.",
        )
        
# Validation Exceptions
class ValidationException(APIException):
    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


class BadRequestException(APIException):
    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

# File Exceptions
class FileTooLargeException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file exceeds the maximum allowed size.",
        )


class UnsupportedFileTypeException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type.",
        )

# External Service Exceptions
class ExternalServiceException(APIException):
    def __init__(
        self,
        service: str,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{service} is currently unavailable.",
        )

# Rate Limiting
class RateLimitExceededException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )