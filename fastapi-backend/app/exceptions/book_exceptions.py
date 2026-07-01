"""
Book domain exceptions.

Raised whenever book-related business rules or
Open Library operations fail.
"""


class BookException(Exception):
    """Base exception for all book-related errors."""

    default_message = "Book operation failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class BookNotFoundException(BookException):
    """Raised when a requested book cannot be found."""

    default_message = "Book not found."


class InvalidBookIdentifierException(BookException):
    """Raised when an invalid book identifier is provided."""

    default_message = "Invalid book identifier."


class BookAlreadyExistsException(BookException):
    """Raised when attempting to create a duplicate book."""

    default_message = "Book already exists."


class BookSearchException(BookException):
    """Raised when searching books fails."""

    default_message = "Book search failed."


class BookImportException(BookException):
    """Raised when importing book data fails."""

    default_message = "Book import failed."


class BookSyncException(BookException):
    """Raised when synchronizing books with external services fails."""

    default_message = "Book synchronization failed."


class BookMetadataException(BookException):
    """Raised when retrieving book metadata fails."""

    default_message = "Unable to retrieve book metadata."


__all__ = [
    "BookException",
    "BookNotFoundException",
    "InvalidBookIdentifierException",
    "BookAlreadyExistsException",
    "BookSearchException",
    "BookImportException",
    "BookSyncException",
    "BookMetadataException",
]