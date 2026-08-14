import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


class EmailSender:

    @staticmethod
    def send_email(
        recipient: str,
        subject: str,
        body: str
    ):

        message = MIMEMultipart()

        message["From"] = settings.EMAIL_FROM
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(
            MIMEText(
                body,
                "plain"
            )
        )

        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD
            )

            server.send_message(
                message
            )