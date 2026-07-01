"""
Background task domain exceptions.

Raised whenever scheduled jobs, background tasks,
or asynchronous processing fails.

Examples:
- APScheduler jobs
- Cleanup tasks
- Notification jobs
- Email queue
- Future Celery workers
"""


class TaskException(Exception):
    """Base exception for all background task errors."""

    default_message = "Background task failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class TaskExecutionException(TaskException):
    """Raised when execution of a background task fails."""

    default_message = "Background task execution failed."


class TaskSchedulingException(TaskException):
    """Raised when scheduling a background task fails."""

    default_message = "Unable to schedule background task."


class TaskCancellationException(TaskException):
    """Raised when cancelling a background task fails."""

    default_message = "Unable to cancel background task."


class TaskTimeoutException(TaskException):
    """Raised when a task exceeds its execution time."""

    default_message = "Background task timed out."


class NotificationTaskException(TaskException):
    """Raised when notification delivery tasks fail."""

    default_message = "Notification task failed."


class CleanupTaskException(TaskException):
    """Raised when cleanup jobs fail."""

    default_message = "Cleanup task failed."


class EmailTaskException(TaskException):
    """Raised when background email delivery fails."""

    default_message = "Email delivery task failed."


class ScheduledTaskNotFoundException(TaskException):
    """Raised when a scheduled task cannot be found."""

    default_message = "Scheduled task not found."


__all__ = [
    "TaskException",
    "TaskExecutionException",
    "TaskSchedulingException",
    "TaskCancellationException",
    "TaskTimeoutException",
    "NotificationTaskException",
    "CleanupTaskException",
    "EmailTaskException",
    "ScheduledTaskNotFoundException",
]