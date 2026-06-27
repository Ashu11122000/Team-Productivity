"""
Email background tasks.

This module contains reusable email-related tasks.

Current Responsibilities:
- Send verification emails
- Send password reset emails
- Send welcome emails

Future Responsibilities:
- Notification emails
- Workspace invitations
- Weekly summaries
- Team activity digests
- Marketing emails

These functions are intentionally framework-agnostic so they
can later be executed by Celery, RQ, Dramatiq, or FastAPI
BackgroundTasks without modification.
"""

from app.core.logging import logger
from app.integrations.email_client import EmailClient


def send_verification_email(
    recipient: str,
    verification_link: str,
) -> bool:
    """
    Send an email verification message.
    """

    logger.info(
        "Sending verification email.",
        recipient=recipient,
    )

    subject = "Verify your email"

    body = f"""
Welcome to Team Productivity Platform!

Please verify your email by clicking the link below:

{verification_link}

If you didn't create an account, you can safely ignore this email.
"""

    return EmailClient.send_email(
        recipient=recipient,
        subject=subject,
        body=body,
    )


def send_password_reset_email(
    recipient: str,
    reset_link: str,
) -> bool:
    """
    Send a password reset email.
    """

    logger.info(
        "Sending password reset email.",
        recipient=recipient,
    )

    subject = "Reset your password"

    body = f"""
A password reset request was received.

Reset your password using the link below:

{reset_link}

If you didn't request this, you can safely ignore this email.
"""

    return EmailClient.send_email(
        recipient=recipient,
        subject=subject,
        body=body,
    )


def send_welcome_email(
    recipient: str,
    full_name: str,
) -> bool:
    """
    Send a welcome email to a newly registered user.
    """

    logger.info(
        "Sending welcome email.",
        recipient=recipient,
    )

    subject = "Welcome to Team Productivity Platform"

    body = f"""
Hello {full_name},

Welcome to Team Productivity Platform!

We're excited to have you on board.

You can now begin organizing notes, tasks, and projects from one place.

Happy Productivity!
"""

    return EmailClient.send_email(
        recipient=recipient,
        subject=subject,
        body=body,
    )