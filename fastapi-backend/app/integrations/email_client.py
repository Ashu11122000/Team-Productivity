"""
Email client for sending emails.

This module centralizes all outbound email functionality used by the
Team Productivity Platform.

Future Uses:
- Email Verification
- Password Reset
- Welcome Emails
- Notifications
- Workspace Invitations
"""

from email.message import EmailMessage
import smtplib
import ssl

from app.core.config import settings
from app.core.logging import logger


class EmailClient:
    """SMTP email client."""

    @staticmethod
    def send_email(
        *,
        recipient: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> bool:
        """
        Send an email.

        Args:
            recipient: Recipient email address.
            subject: Email subject.
            body: Email body.
            html: Whether the body contains HTML.

        Returns:
            True if email was sent successfully.
        """

        message = EmailMessage()

        message["From"] = settings.MAIL_FROM
        message["To"] = recipient
        message["Subject"] = subject

        if html:
            message.add_alternative(body, subtype="html")
        else:
            message.set_content(body)

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP(
                settings.MAIL_SERVER,
                settings.MAIL_PORT,
            ) as smtp:

                if settings.MAIL_STARTTLS:
                    smtp.starttls(context=context)

                smtp.login(
                    settings.MAIL_USERNAME,
                    settings.MAIL_PASSWORD,
                )

                smtp.send_message(message)

            logger.info(
                "Email sent successfully.",
                recipient=recipient,
                subject=subject,
            )

            return True

        except Exception as exc:
            logger.exception(
                "Failed to send email.",
                recipient=recipient,
                error=str(exc),
            )

            return False