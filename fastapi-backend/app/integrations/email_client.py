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
from typing import Final


class EmailClient:
    """SMTP email client."""
    
    DEFAULT_TIMEOUT: Final[int] = 30

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

        if not settings.EMAIL_ENABLED:
            logger.warning(
                "Email sending is disabled.",
                recipient = recipient,
            )
            return False
        
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
                host = settings.MAIL_SERVER,
                port = settings.MAIL_PORT,
                timeout = EmailClient.DEFAULT_TIMEOUT,
            ) as smtp:

                if settings.MAIL_STARTTLS:
                    smtp.ehlo()
                    smtp.starttls(context=context)
                    smtp.ehlo()
                
                if settings.MAIL_USERNAME:
                    smtp.login(
                        settings.MAIL_USERNAME,
                        settings.MAIL_PASSWORD,
                    )

                smtp.send_message(message)

            logger.info(
                "Email sent successfully.",
                recipient=recipient,
                subject=subject,
                provider=settings.MAIL_SERVER
            )

            return True

        except smtplib.Exception as exc:
            logger.exception(
                "SMTP error while sending email.",
                recipient=recipient,
                subject=subject,
                error=str(exc),
            )

            return False
        
        except Exception as exc:
            logger.exception(
                "Unexpected email sending error.",
                recipient=recipient,
                subject=subject,
                error=str(exc),
            )
            
            return False