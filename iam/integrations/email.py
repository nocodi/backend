import logging
import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class EmailClient(ABC):
    @abstractmethod
    def send(self, target: str, subject: str, text: str) -> None:
        raise NotImplementedError


class SMTPClient(EmailClient):
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587

    def __init__(self, from_email: str, password: str):
        self.from_email = from_email
        self.password = password
        self.__conn: Optional[smtplib.SMTP] = None

    @property
    def conn(self) -> smtplib.SMTP:
        if self.__conn is None or self.__conn.noop()[0] != 250:
            self.__conn = smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT)
            self.__conn.starttls()  # Upgrade the connection to secure
            self.__conn.login(self.from_email, self.password)  # Authenticate
        logger.info("SMTP connection established.")
        return self.__conn

    def send(self, target: str, subject: str, text: str) -> None:
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = target
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "html"))

        try:
            # Send the email using the existing connection
            self.conn.sendmail(self.from_email, target, msg.as_string())
            logger.info(f"Email sent to {target} with subject '{subject}'")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise

    def close(self) -> None:
        """Close the SMTP connection."""
        try:
            self.conn.quit()
            logger.info("SMTP connection closed.")
        except Exception as e:
            logger.error(f"Failed to close SMTP connection: {e}")


class MockEmailClient(SMTPClient):
    def __init__(self) -> None:
        pass

    def send(self, target: str, subject: str, text: str) -> None:
        # logger.debug(f"Mock email sent to {target} with subject '{subject}'")
        pass


email_client: EmailClient
if settings.TESTING or settings.DEBUG:
    email_client = MockEmailClient()
else:
    email_client = SMTPClient(
        from_email=settings.SMTP_FROM_EMAIL,
        password=settings.SMTP_PASSWORD,
    )
