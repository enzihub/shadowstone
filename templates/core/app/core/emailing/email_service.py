# email_service.py

import os

import mailtrap as mt
from dotenv import load_dotenv

from app.core.config.logger import logger

load_dotenv()


class EmailService:
    def __init__(self):
        self.token = os.getenv("MAILTRAP_API_TOKEN")
        if not self.token:
            raise ValueError("Mailtrap API token not found")
        self.client = mt.MailtrapClient(token=self.token)
        self.from_email = os.getenv("FROM_EMAIL", "hello@demomailtrap.com")
        self.from_name = os.getenv("FROM_NAME", "Your App Name")

    # async def send_email(self, email_subject: str, user_token: UserToken, html_content: str) -> bool:
    async def send_email(
        self, email_subject: str, email: str, html_content: str
    ) -> bool:
        try:
            mail = mt.Mail(
                sender=mt.Address(email=self.from_email, name=self.from_name),
                to=[mt.Address(email=email)],
                subject=email_subject,
                html=html_content,
            )

            response = self.client.send(mail)
            logger.info(f"Email sent successfully to {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {email}: {str(e)}")
            return False
