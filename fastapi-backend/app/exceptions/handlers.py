"""
Global exception handlers for the Team Productivity Platform.

Responsibilities:
- Convert domain exceptions into HTTP responses.
- Return standardized API error responses.
- Log unexpected errors.
- Register all application exception handlers.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from pydantic import ValidationError

from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
)

# Authentication Exceptions
from app.exceptions.auth_exceptions import (
    AuthenticationException,
    EmailAlreadyVerifiedException,
    EmailVerificationException,
    ExpiredTokenException,
    ForbiddenException,
    InactiveUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    PasswordResetException,
    RefreshTokenException,
    UnauthorizedException,
)

# User Exceptions
from app.exceptions.user_exceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    InvalidUserOperationException,
    UserAlreadyActiveException,
    UserAlreadyExistsException,
    UserAlreadyInactiveException,
    UserException,
    UserNotFoundException,
    UserProfileException,
)

# Note Exceptions
from app.exceptions.note_exceptions import (
    EmptyNoteContentException,
    InvalidNoteOperationException,
    NoteAccessDeniedException,
    NoteAlreadyArchivedException,
    NoteAlreadyDeletedException,
    NoteConversionException,
    NoteException,
    NoteNotArchivedException,
    NoteNotFoundException,
)

logger = get_logger(__name__)


# ==============================================================================
# RESPONSE BUILDER
# ==============================================================================


def error_response(
    *,
    status_code: int,
    message: str,
    error: str,
) -> JSONResponse:
    """
    Build a standardized error response.
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "error": error,
        },
    )


# ==============================================================================
# AUTHENTICATION
# ==============================================================================


async def authentication_exception_handler(
    request: Request,
    exc: AuthenticationException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_credentials_exception_handler(
    request: Request,
    exc: InvalidCredentialsException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_token_exception_handler(
    request: Request,
    exc: InvalidTokenException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def expired_token_exception_handler(
    request: Request,
    exc: ExpiredTokenException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def refresh_token_exception_handler(
    request: Request,
    exc: RefreshTokenException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def unauthorized_exception_handler(
    request: Request,
    exc: UnauthorizedException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def forbidden_exception_handler(
    request: Request,
    exc: ForbiddenException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def inactive_user_exception_handler(
    request: Request,
    exc: InactiveUserException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_already_verified_exception_handler(
    request: Request,
    exc: EmailAlreadyVerifiedException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_verification_exception_handler(
    request: Request,
    exc: EmailVerificationException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def password_reset_exception_handler(
    request: Request,
    exc: PasswordResetException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


# ==============================================================================
# USERS
# ==============================================================================


async def user_exception_handler(
    request: Request,
    exc: UserException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def user_not_found_exception_handler(
    request: Request,
    exc: UserNotFoundException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def user_already_exists_exception_handler(
    request: Request,
    exc: UserAlreadyExistsException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def duplicate_email_exception_handler(
    request: Request,
    exc: DuplicateEmailException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def duplicate_username_exception_handler(
    request: Request,
    exc: DuplicateUsernameException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def user_already_active_exception_handler(
    request: Request,
    exc: UserAlreadyActiveException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def user_already_inactive_exception_handler(
    request: Request,
    exc: UserAlreadyInactiveException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def user_profile_exception_handler(
    request: Request,
    exc: UserProfileException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_user_operation_exception_handler(
    request: Request,
    exc: InvalidUserOperationException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


# ==============================================================================
# NOTES
# ==============================================================================


async def note_exception_handler(
    request: Request,
    exc: NoteException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def note_not_found_exception_handler(
    request: Request,
    exc: NoteNotFoundException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def note_access_denied_exception_handler(
    request: Request,
    exc: NoteAccessDeniedException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def note_already_archived_exception_handler(
    request: Request,
    exc: NoteAlreadyArchivedException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def note_not_archived_exception_handler(
    request: Request,
    exc: NoteNotArchivedException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def note_already_deleted_exception_handler(
    request: Request,
    exc: NoteAlreadyDeletedException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_note_operation_exception_handler(
    request: Request,
    exc: InvalidNoteOperationException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def empty_note_content_exception_handler(
    request: Request,
    exc: EmptyNoteContentException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def note_conversion_exception_handler(
    request: Request,
    exc: NoteConversionException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )
    
    # ==============================================================================
# BOOKS
# ==============================================================================

from app.exceptions.book_exceptions import (
    BookAlreadyExistsException,
    BookException,
    BookImportException,
    BookMetadataException,
    BookNotFoundException,
    BookSearchException,
    BookSyncException,
    InvalidBookIdentifierException,
)


async def book_exception_handler(
    request: Request,
    exc: BookException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def book_not_found_exception_handler(
    request: Request,
    exc: BookNotFoundException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_book_identifier_exception_handler(
    request: Request,
    exc: InvalidBookIdentifierException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def book_already_exists_exception_handler(
    request: Request,
    exc: BookAlreadyExistsException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def book_search_exception_handler(
    request: Request,
    exc: BookSearchException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def book_import_exception_handler(
    request: Request,
    exc: BookImportException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def book_sync_exception_handler(
    request: Request,
    exc: BookSyncException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def book_metadata_exception_handler(
    request: Request,
    exc: BookMetadataException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


# ==============================================================================
# EMAIL
# ==============================================================================

from app.exceptions.email_exceptions import (
    EmailConfigurationException,
    EmailDeliveryException,
    EmailException,
    EmailSendException,
    EmailTemplateException,
    EmailVerificationSendException,
    InvalidEmailRecipientException,
    PasswordResetEmailException,
)


async def email_exception_handler(
    request: Request,
    exc: EmailException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_send_exception_handler(
    request: Request,
    exc: EmailSendException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_template_exception_handler(
    request: Request,
    exc: EmailTemplateException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_email_recipient_exception_handler(
    request: Request,
    exc: InvalidEmailRecipientException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_configuration_exception_handler(
    request: Request,
    exc: EmailConfigurationException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_delivery_exception_handler(
    request: Request,
    exc: EmailDeliveryException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_verification_send_exception_handler(
    request: Request,
    exc: EmailVerificationSendException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def password_reset_email_exception_handler(
    request: Request,
    exc: PasswordResetEmailException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


# ==============================================================================
# FILES
# ==============================================================================

from app.exceptions.file_exceptions import (
    FileAlreadyExistsException,
    FileDeleteException,
    FileDownloadException,
    FileException,
    FileNotFoundException,
    FilePermissionException,
    FileProcessingException,
    FileStorageException,
    FileTooLargeException,
    FileUploadException,
    InvalidFileTypeException,
)


async def file_exception_handler(
    request: Request,
    exc: FileException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_not_found_exception_handler(
    request: Request,
    exc: FileNotFoundException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_upload_exception_handler(
    request: Request,
    exc: FileUploadException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_download_exception_handler(
    request: Request,
    exc: FileDownloadException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_delete_exception_handler(
    request: Request,
    exc: FileDeleteException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_too_large_exception_handler(
    request: Request,
    exc: FileTooLargeException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_file_type_exception_handler(
    request: Request,
    exc: InvalidFileTypeException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_storage_exception_handler(
    request: Request,
    exc: FileStorageException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_permission_exception_handler(
    request: Request,
    exc: FilePermissionException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_processing_exception_handler(
    request: Request,
    exc: FileProcessingException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def file_already_exists_exception_handler(
    request: Request,
    exc: FileAlreadyExistsException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )
    
    # ==============================================================================
# INTEGRATIONS
# ==============================================================================

from app.exceptions.integration_exceptions import (
    ExternalServiceTimeoutException,
    ExternalServiceUnavailableException,
    IntegrationException,
    InvalidExternalResponseException,
    OpenLibraryException,
    RedisConnectionException,
    StorageProviderException,
    ThirdPartyAuthenticationException,
)


async def integration_exception_handler(
    request: Request,
    exc: IntegrationException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def external_service_unavailable_exception_handler(
    request: Request,
    exc: ExternalServiceUnavailableException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def external_service_timeout_exception_handler(
    request: Request,
    exc: ExternalServiceTimeoutException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_external_response_exception_handler(
    request: Request,
    exc: InvalidExternalResponseException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_502_BAD_GATEWAY,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def open_library_exception_handler(
    request: Request,
    exc: OpenLibraryException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def redis_connection_exception_handler(
    request: Request,
    exc: RedisConnectionException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def storage_provider_exception_handler(
    request: Request,
    exc: StorageProviderException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def third_party_authentication_exception_handler(
    request: Request,
    exc: ThirdPartyAuthenticationException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc),
        error=exc.__class__.__name__,
    )


# ==============================================================================
# BACKGROUND TASKS
# ==============================================================================

from app.exceptions.task_exceptions import (
    CleanupTaskException,
    EmailTaskException,
    NotificationTaskException,
    ScheduledTaskNotFoundException,
    TaskCancellationException,
    TaskException,
    TaskExecutionException,
    TaskSchedulingException,
    TaskTimeoutException,
)


async def task_exception_handler(
    request: Request,
    exc: TaskException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def task_execution_exception_handler(
    request: Request,
    exc: TaskExecutionException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def task_scheduling_exception_handler(
    request: Request,
    exc: TaskSchedulingException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def task_cancellation_exception_handler(
    request: Request,
    exc: TaskCancellationException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def task_timeout_exception_handler(
    request: Request,
    exc: TaskTimeoutException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def notification_task_exception_handler(
    request: Request,
    exc: NotificationTaskException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def cleanup_task_exception_handler(
    request: Request,
    exc: CleanupTaskException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def email_task_exception_handler(
    request: Request,
    exc: EmailTaskException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def scheduled_task_not_found_exception_handler(
    request: Request,
    exc: ScheduledTaskNotFoundException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        message=str(exc),
        error=exc.__class__.__name__,
    )
    
    # ==============================================================================
# VALIDATION
# ==============================================================================

from app.exceptions.validation_exceptions import (
    InvalidDateException,
    InvalidEmailException,
    InvalidFieldException,
    InvalidFileExtensionException,
    InvalidFilterException,
    InvalidInputException,
    InvalidOperationException,
    InvalidPaginationException,
    InvalidPasswordException,
    InvalidSortFieldException,
    InvalidUUIDException,
    InvalidUsernameException,
    RequiredFieldException,
    ValidationException,
)


async def validation_exception_handler(
    request: Request,
    exc: ValidationException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def required_field_exception_handler(
    request: Request,
    exc: RequiredFieldException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_field_exception_handler(
    request: Request,
    exc: InvalidFieldException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_input_exception_handler(
    request: Request,
    exc: InvalidInputException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_email_exception_handler(
    request: Request,
    exc: InvalidEmailException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_password_exception_handler(
    request: Request,
    exc: InvalidPasswordException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_username_exception_handler(
    request: Request,
    exc: InvalidUsernameException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_uuid_exception_handler(
    request: Request,
    exc: InvalidUUIDException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_date_exception_handler(
    request: Request,
    exc: InvalidDateException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_file_extension_exception_handler(
    request: Request,
    exc: InvalidFileExtensionException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_pagination_exception_handler(
    request: Request,
    exc: InvalidPaginationException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_sort_field_exception_handler(
    request: Request,
    exc: InvalidSortFieldException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_filter_exception_handler(
    request: Request,
    exc: InvalidFilterException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def invalid_operation_exception_handler(
    request: Request,
    exc: InvalidOperationException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        error=exc.__class__.__name__,
    )


# ==============================================================================
# DATABASE
# ==============================================================================

from app.exceptions.database_exceptions import (
    DatabaseCommitException,
    DatabaseConnectionException,
    DatabaseException,
    DatabaseIntegrityException,
    DatabaseMigrationException,
    DatabaseRollbackException,
    DatabaseTimeoutException,
    DatabaseTransactionException,
    DuplicateRecordException,
    ForeignKeyConstraintException,
    RecordNotFoundException,
    UniqueConstraintException,
)


async def database_exception_handler(
    request: Request,
    exc: DatabaseException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def database_connection_exception_handler(
    request: Request,
    exc: DatabaseConnectionException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def database_transaction_exception_handler(
    request: Request,
    exc: DatabaseTransactionException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def database_commit_exception_handler(
    request: Request,
    exc: DatabaseCommitException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def database_rollback_exception_handler(
    request: Request,
    exc: DatabaseRollbackException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def database_integrity_exception_handler(
    request: Request,
    exc: DatabaseIntegrityException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def duplicate_record_exception_handler(
    request: Request,
    exc: DuplicateRecordException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def record_not_found_exception_handler(
    request: Request,
    exc: RecordNotFoundException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def foreign_key_constraint_exception_handler(
    request: Request,
    exc: ForeignKeyConstraintException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def unique_constraint_exception_handler(
    request: Request,
    exc: UniqueConstraintException,
) -> JSONResponse:
    logger.warning(str(exc))
    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def database_timeout_exception_handler(
    request: Request,
    exc: DatabaseTimeoutException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        message=str(exc),
        error=exc.__class__.__name__,
    )


async def database_migration_exception_handler(
    request: Request,
    exc: DatabaseMigrationException,
) -> JSONResponse:
    logger.error(str(exc))
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        error=exc.__class__.__name__,
    )
    
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:

    logger.warning(
        "HTTP Exception",
        path=request.url.path,
        method=request.method,
        status_code=exc.status_code,
        detail=exc.detail,
    )

    return error_response(
        status_code=exc.status_code,
        message=str(exc.detail),
        error=exc.__class__.__name__,
    )


# ==============================================================================
# REQUEST VALIDATION
# ==============================================================================


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle FastAPI request validation errors.
    """

    logger.warning(
        "Request validation failed",
        path=request.url.path,
        method=request.method,
        errors=exc.errors(),
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Request validation failed.",
            "error": "RequestValidationError",
            "details": exc.errors(),
        },
    )


# ==============================================================================
# PYDANTIC VALIDATION
# ==============================================================================


async def pydantic_validation_exception_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    """

    logger.warning(
        "Pydantic validation failed",
        path=request.url.path,
        method=request.method,
        errors=exc.errors(),
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed.",
            "error": "ValidationError",
            "details": exc.errors(),
        },
    )
    
    # ==============================================================================
# SQLALCHEMY EXCEPTIONS
# ==============================================================================


async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    """
    Handle SQLAlchemy integrity errors.
    """

    logger.exception(
        "Database integrity error",
        path=request.url.path,
        method=request.method,
        error=str(exc),
    )

    return error_response(
        status_code=status.HTTP_409_CONFLICT,
        message="Database integrity constraint violated.",
        error="IntegrityError",
    )


async def operational_error_handler(
    request: Request,
    exc: OperationalError,
) -> JSONResponse:
    """
    Handle SQLAlchemy operational errors.
    """

    logger.exception(
        "Database operational error",
        path=request.url.path,
        method=request.method,
        error=str(exc),
    )

    return error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message="Database service is currently unavailable.",
        error="OperationalError",
    )


async def sqlalchemy_error_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    """
    Handle generic SQLAlchemy errors.
    """

    logger.exception(
        "SQLAlchemy error",
        path=request.url.path,
        method=request.method,
        error=str(exc),
    )

    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="A database error occurred.",
        error="SQLAlchemyError",
    )


# ==============================================================================
# UNEXPECTED EXCEPTIONS
# ==============================================================================


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Catch all unhandled exceptions.

    This handler should always be registered last.
    """

    logger.exception(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        exception_type=exc.__class__.__name__,
        error=str(exc),
    )

    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="An unexpected internal server error occurred.",
        error=exc.__class__.__name__,
    )
    
    # ==============================================================================
# REGISTER EXCEPTION HANDLERS
# ==============================================================================


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application exception handlers.

    This function should be called once during application startup.

    Example:
        from app.exceptions.handlers import register_exception_handlers

        app = FastAPI()

        register_exception_handlers(app)
    """

    # ==========================================================================
    # AUTHENTICATION EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        AuthenticationException,
        authentication_exception_handler,
    )

    app.add_exception_handler(
        InvalidCredentialsException,
        invalid_credentials_exception_handler,
    )

    app.add_exception_handler(
        InvalidTokenException,
        invalid_token_exception_handler,
    )

    app.add_exception_handler(
        ExpiredTokenException,
        expired_token_exception_handler,
    )

    app.add_exception_handler(
        RefreshTokenException,
        refresh_token_exception_handler,
    )

    app.add_exception_handler(
        UnauthorizedException,
        unauthorized_exception_handler,
    )

    app.add_exception_handler(
        ForbiddenException,
        forbidden_exception_handler,
    )

    app.add_exception_handler(
        InactiveUserException,
        inactive_user_exception_handler,
    )

    app.add_exception_handler(
        EmailAlreadyVerifiedException,
        email_already_verified_exception_handler,
    )

    app.add_exception_handler(
        EmailVerificationException,
        email_verification_exception_handler,
    )

    app.add_exception_handler(
        PasswordResetException,
        password_reset_exception_handler,
    )

    # ==========================================================================
    # USER EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        UserException,
        user_exception_handler,
    )

    app.add_exception_handler(
        UserNotFoundException,
        user_not_found_exception_handler,
    )

    app.add_exception_handler(
        UserAlreadyExistsException,
        user_already_exists_exception_handler,
    )

    app.add_exception_handler(
        UserAlreadyActiveException,
        user_already_active_exception_handler,
    )

    app.add_exception_handler(
        UserAlreadyInactiveException,
        user_already_inactive_exception_handler,
    )

    app.add_exception_handler(
        UserProfileException,
        user_profile_exception_handler,
    )

    app.add_exception_handler(
        InvalidUserOperationException,
        invalid_user_operation_exception_handler,
    )

    app.add_exception_handler(
        DuplicateEmailException,
        duplicate_email_exception_handler,
    )

    app.add_exception_handler(
        DuplicateUsernameException,
        duplicate_username_exception_handler,
    )

    # ==========================================================================
    # NOTE EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        NoteException,
        note_exception_handler,
    )

    app.add_exception_handler(
        NoteNotFoundException,
        note_not_found_exception_handler,
    )

    app.add_exception_handler(
        NoteAccessDeniedException,
        note_access_denied_exception_handler,
    )

    app.add_exception_handler(
        NoteAlreadyArchivedException,
        note_already_archived_exception_handler,
    )

    app.add_exception_handler(
        NoteNotArchivedException,
        note_not_archived_exception_handler,
    )

    app.add_exception_handler(
        NoteAlreadyDeletedException,
        note_already_deleted_exception_handler,
    )

    app.add_exception_handler(
        InvalidNoteOperationException,
        invalid_note_operation_exception_handler,
    )

    app.add_exception_handler(
        EmptyNoteContentException,
        empty_note_content_exception_handler,
    )

    app.add_exception_handler(
        NoteConversionException,
        note_conversion_exception_handler,
    )
    
        # ==========================================================================
    # BOOK EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        BookException,
        book_exception_handler,
    )

    app.add_exception_handler(
        BookNotFoundException,
        book_not_found_exception_handler,
    )

    app.add_exception_handler(
        InvalidBookIdentifierException,
        invalid_book_identifier_exception_handler,
    )

    app.add_exception_handler(
        BookAlreadyExistsException,
        book_already_exists_exception_handler,
    )

    app.add_exception_handler(
        BookSearchException,
        book_search_exception_handler,
    )

    app.add_exception_handler(
        BookImportException,
        book_import_exception_handler,
    )

    app.add_exception_handler(
        BookSyncException,
        book_sync_exception_handler,
    )

    app.add_exception_handler(
        BookMetadataException,
        book_metadata_exception_handler,
    )

    # ==========================================================================
    # EMAIL EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        EmailException,
        email_exception_handler,
    )

    app.add_exception_handler(
        EmailSendException,
        email_send_exception_handler,
    )

    app.add_exception_handler(
        EmailTemplateException,
        email_template_exception_handler,
    )

    app.add_exception_handler(
        InvalidEmailRecipientException,
        invalid_email_recipient_exception_handler,
    )

    app.add_exception_handler(
        EmailConfigurationException,
        email_configuration_exception_handler,
    )

    app.add_exception_handler(
        EmailDeliveryException,
        email_delivery_exception_handler,
    )

    app.add_exception_handler(
        EmailVerificationSendException,
        email_verification_send_exception_handler,
    )

    app.add_exception_handler(
        PasswordResetEmailException,
        password_reset_email_exception_handler,
    )

    # ==========================================================================
    # FILE EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        FileException,
        file_exception_handler,
    )

    app.add_exception_handler(
        FileNotFoundException,
        file_not_found_exception_handler,
    )

    app.add_exception_handler(
        FileUploadException,
        file_upload_exception_handler,
    )

    app.add_exception_handler(
        FileDownloadException,
        file_download_exception_handler,
    )

    app.add_exception_handler(
        FileDeleteException,
        file_delete_exception_handler,
    )

    app.add_exception_handler(
        FileTooLargeException,
        file_too_large_exception_handler,
    )

    app.add_exception_handler(
        InvalidFileTypeException,
        invalid_file_type_exception_handler,
    )

    app.add_exception_handler(
        FileStorageException,
        file_storage_exception_handler,
    )

    app.add_exception_handler(
        FilePermissionException,
        file_permission_exception_handler,
    )

    app.add_exception_handler(
        FileProcessingException,
        file_processing_exception_handler,
    )

    app.add_exception_handler(
        FileAlreadyExistsException,
        file_already_exists_exception_handler,
    )

    # ==========================================================================
    # INTEGRATION EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        IntegrationException,
        integration_exception_handler,
    )

    app.add_exception_handler(
        ExternalServiceUnavailableException,
        external_service_unavailable_exception_handler,
    )

    app.add_exception_handler(
        ExternalServiceTimeoutException,
        external_service_timeout_exception_handler,
    )

    app.add_exception_handler(
        InvalidExternalResponseException,
        invalid_external_response_exception_handler,
    )

    app.add_exception_handler(
        OpenLibraryException,
        open_library_exception_handler,
    )

    app.add_exception_handler(
        RedisConnectionException,
        redis_connection_exception_handler,
    )

    app.add_exception_handler(
        StorageProviderException,
        storage_provider_exception_handler,
    )

    app.add_exception_handler(
        ThirdPartyAuthenticationException,
        third_party_authentication_exception_handler,
    )

    # ==========================================================================
    # TASK EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        TaskException,
        task_exception_handler,
    )

    app.add_exception_handler(
        TaskExecutionException,
        task_execution_exception_handler,
    )

    app.add_exception_handler(
        TaskSchedulingException,
        task_scheduling_exception_handler,
    )

    app.add_exception_handler(
        TaskCancellationException,
        task_cancellation_exception_handler,
    )

    app.add_exception_handler(
        TaskTimeoutException,
        task_timeout_exception_handler,
    )

    app.add_exception_handler(
        NotificationTaskException,
        notification_task_exception_handler,
    )

    app.add_exception_handler(
        CleanupTaskException,
        cleanup_task_exception_handler,
    )

    app.add_exception_handler(
        EmailTaskException,
        email_task_exception_handler,
    )

    app.add_exception_handler(
        ScheduledTaskNotFoundException,
        scheduled_task_not_found_exception_handler,
    )
    
        # ==========================================================================
    # VALIDATION EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        ValidationException,
        validation_exception_handler,
    )

    app.add_exception_handler(
        RequiredFieldException,
        required_field_exception_handler,
    )

    app.add_exception_handler(
        InvalidFieldException,
        invalid_field_exception_handler,
    )

    app.add_exception_handler(
        InvalidInputException,
        invalid_input_exception_handler,
    )

    app.add_exception_handler(
        InvalidEmailException,
        invalid_email_exception_handler,
    )

    app.add_exception_handler(
        InvalidPasswordException,
        invalid_password_exception_handler,
    )

    app.add_exception_handler(
        InvalidUsernameException,
        invalid_username_exception_handler,
    )

    app.add_exception_handler(
        InvalidUUIDException,
        invalid_uuid_exception_handler,
    )

    app.add_exception_handler(
        InvalidDateException,
        invalid_date_exception_handler,
    )

    app.add_exception_handler(
        InvalidFileExtensionException,
        invalid_file_extension_exception_handler,
    )

    app.add_exception_handler(
        InvalidPaginationException,
        invalid_pagination_exception_handler,
    )

    app.add_exception_handler(
        InvalidSortFieldException,
        invalid_sort_field_exception_handler,
    )

    app.add_exception_handler(
        InvalidFilterException,
        invalid_filter_exception_handler,
    )

    app.add_exception_handler(
        InvalidOperationException,
        invalid_operation_exception_handler,
    )

    # ==========================================================================
    # DATABASE EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        DatabaseException,
        database_exception_handler,
    )

    app.add_exception_handler(
        DatabaseConnectionException,
        database_connection_exception_handler,
    )

    app.add_exception_handler(
        DatabaseTransactionException,
        database_transaction_exception_handler,
    )

    app.add_exception_handler(
        DatabaseCommitException,
        database_commit_exception_handler,
    )

    app.add_exception_handler(
        DatabaseRollbackException,
        database_rollback_exception_handler,
    )

    app.add_exception_handler(
        DatabaseIntegrityException,
        database_integrity_exception_handler,
    )

    app.add_exception_handler(
        DuplicateRecordException,
        duplicate_record_exception_handler,
    )

    app.add_exception_handler(
        RecordNotFoundException,
        record_not_found_exception_handler,
    )

    app.add_exception_handler(
        ForeignKeyConstraintException,
        foreign_key_constraint_exception_handler,
    )

    app.add_exception_handler(
        UniqueConstraintException,
        unique_constraint_exception_handler,
    )

    app.add_exception_handler(
        DatabaseTimeoutException,
        database_timeout_exception_handler,
    )

    app.add_exception_handler(
        DatabaseMigrationException,
        database_migration_exception_handler,
    )

    # ==========================================================================
    # FASTAPI EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,
    )

    app.add_exception_handler(
        ValidationError,
        pydantic_validation_exception_handler,
    )

    # ==========================================================================
    # SQLALCHEMY EXCEPTIONS
    # ==========================================================================

    app.add_exception_handler(
        IntegrityError,
        integrity_error_handler,
    )

    app.add_exception_handler(
        OperationalError,
        operational_error_handler,
    )

    app.add_exception_handler(
        SQLAlchemyError,
        sqlalchemy_error_handler,
    )

    # ==========================================================================
    # FALLBACK EXCEPTION
    # ==========================================================================

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )