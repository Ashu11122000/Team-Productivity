"""
Notes domain exceptions.

Raised by the notes service whenever note-related
business rules are violated.
"""


class NoteException(Exception):
    """Base exception for note-related errors."""


class NoteNotFoundException(NoteException):
    """Raised when a requested note does not exist."""


class NoteAccessDeniedException(NoteException):
    """Raised when a user attempts to access another user's note."""


class NoteAlreadyArchivedException(NoteException):
    """Raised when archiving an already archived note."""


class NoteNotArchivedException(NoteException):
    """Raised when restoring a note that is not archived."""


class NoteAlreadyDeletedException(NoteException):
    """Raised when deleting an already deleted note."""


class InvalidNoteOperationException(NoteException):
    """Raised when an invalid operation is performed on a note."""


class EmptyNoteContentException(NoteException):
    """Raised when note content is empty."""


class NoteConversionException(NoteException):
    """
    Raised when converting a note into a task fails.
    """
    
__all__ = [
    "NoteException",
    "NoteNotFoundException",
    "NoteAccessDeniedException",
    "NoteAlreadyArchivedException",
    "NoteNotArchivedException",
    "NoteAlreadyDeletedException",
    "InvalidNoteOperationException",
    "EmptyNoteContentException",
    "NoteConversionException",
]