"""
File domain exceptions.

Raised whenever file upload, download,
storage, or processing operations fail.
"""


class FileException(Exception):
    """Base exception for all file-related errors."""

    default_message = "File operation failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class FileNotFoundException(FileException):
    """Raised when a requested file cannot be found."""

    default_message = "File not found."


class FileUploadException(FileException):
    """Raised when file upload fails."""

    default_message = "File upload failed."


class FileDownloadException(FileException):
    """Raised when file download fails."""

    default_message = "File download failed."


class FileDeleteException(FileException):
    """Raised when deleting a file fails."""

    default_message = "File deletion failed."


class FileTooLargeException(FileException):
    """Raised when an uploaded file exceeds the allowed size."""

    default_message = "Uploaded file exceeds the maximum allowed size."


class InvalidFileTypeException(FileException):
    """Raised when an uploaded file type is not supported."""

    default_message = "Unsupported file type."


class FileStorageException(FileException):
    """Raised when storing a file fails."""

    default_message = "File storage operation failed."


class FilePermissionException(FileException):
    """Raised when file permissions prevent an operation."""

    default_message = "Insufficient permission to access the file."


class FileProcessingException(FileException):
    """Raised when file processing fails."""

    default_message = "File processing failed."


class FileAlreadyExistsException(FileException):
    """Raised when attempting to store a duplicate file."""

    default_message = "File already exists."


__all__ = [
    "FileException",
    "FileNotFoundException",
    "FileUploadException",
    "FileDownloadException",
    "FileDeleteException",
    "FileTooLargeException",
    "InvalidFileTypeException",
    "FileStorageException",
    "FilePermissionException",
    "FileProcessingException",
    "FileAlreadyExistsException",
]