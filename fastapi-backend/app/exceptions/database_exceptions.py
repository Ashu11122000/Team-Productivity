"""
Database domain exceptions.

Raised whenever a database operation or persistence
layer encounters an error.

These exceptions are independent of SQLAlchemy and FastAPI.
"""


class DatabaseException(Exception):
    """Base exception for all database-related errors."""

    default_message = "Database operation failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class DatabaseConnectionException(DatabaseException):
    """Raised when a database connection cannot be established."""

    default_message = "Unable to connect to the database."


class DatabaseTransactionException(DatabaseException):
    """Raised when a database transaction fails."""

    default_message = "Database transaction failed."


class DatabaseCommitException(DatabaseException):
    """Raised when committing a transaction fails."""

    default_message = "Failed to commit database transaction."


class DatabaseRollbackException(DatabaseException):
    """Raised when rolling back a transaction fails."""

    default_message = "Failed to rollback database transaction."


class DatabaseIntegrityException(DatabaseException):
    """Raised when a database integrity constraint is violated."""

    default_message = "Database integrity constraint violated."


class DuplicateRecordException(DatabaseException):
    """Raised when attempting to insert a duplicate record."""

    default_message = "Duplicate record already exists."


class RecordNotFoundException(DatabaseException):
    """Raised when a requested database record does not exist."""

    default_message = "Database record not found."


class ForeignKeyConstraintException(DatabaseException):
    """Raised when a foreign key constraint fails."""

    default_message = "Foreign key constraint violation."


class UniqueConstraintException(DatabaseException):
    """Raised when a unique constraint is violated."""

    default_message = "Unique constraint violation."


class DatabaseTimeoutException(DatabaseException):
    """Raised when a database operation times out."""

    default_message = "Database operation timed out."


class DatabaseMigrationException(DatabaseException):
    """Raised when a database migration fails."""

    default_message = "Database migration failed."


__all__ = [
    "DatabaseException",
    "DatabaseConnectionException",
    "DatabaseTransactionException",
    "DatabaseCommitException",
    "DatabaseRollbackException",
    "DatabaseIntegrityException",
    "DuplicateRecordException",
    "RecordNotFoundException",
    "ForeignKeyConstraintException",
    "UniqueConstraintException",
    "DatabaseTimeoutException",
    "DatabaseMigrationException",
]