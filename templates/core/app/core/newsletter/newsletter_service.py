# newsletter_service.py

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import jinja2
import pytz
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.ai.prompts import CONTENT_SUMMARY_PROMPT, SUBJECT_LINE_PROMPT
from app.core.config.config import settings
from app.core.config.logger import logger
from app.core.messaging.message_service import MessageService
from app.core.user.user_service import UserService
from app.db import database


class NewsletterService:
    def __init__(self, message_service: MessageService):
        self.db: Session = database.SessionLocal()
        self.message_service = message_service
        self.template_dir = Path(__file__).parent.parent.parent.parent / "templates"
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir), autoescape=True
        )

    async def render_newsletter_template(self, template_data: Dict) -> str:
        """Render the newsletter HTML template."""
        template = self.template_env.get_template("newsletter.html")
        return template.render(**template_data)

    async def generate_subject_line(self, summary: str) -> str:
        """Generate a subject line for the newsletter based on summary."""
        prompt = SUBJECT_LINE_PROMPT.format(summary=summary)
        try:
            from app.core.ai.ai_config import get_model

            response = get_model().generate_content(prompt)
            subject_line = response.text.strip()
            return subject_line
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_now_in_user_tz(self, timezone_str: str) -> str:
        """Format current timestamp in user's timezone."""
        user_tz = pytz.timezone(timezone_str)
        now = datetime.now().astimezone(user_tz)
        return now.strftime("%B %d, %Y")

    async def schedule_immediate_newsletter(self, email: str):
        """Schedule an immediate newsletter for a specific user."""
        try:
            # Fetch user details and preferences
            user_service = UserService(self.db)
            user_details = await user_service.get_user_details(email)

            # Generate message content

            # TOOD: get actual content
            message_payload = {
                "subject": "Hello this is the immediate subject",
                "body": "Hello this is the body",
            }
            message_data = self.message_service.get_message_data(
                user_details, message_payload, datetime.now().timestamp()
            )

            # Enqueue message with status "sent immediately"
            success = self.message_service.enqueue_message(
                user_details["user_id"], datetime.now(), message_data
            )

            if success:
                logger.info(f"Newsletter scheduled for immediate send to {email}")
                return {"status": "scheduled for immediate sending"}
            else:
                raise HTTPException(status_code=500, detail="Failed to send newsletter")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def generate_newsletter_content(self, email: str) -> Optional[Dict]:
        """Main function to generate newsletter content."""
        try:
            logger.info("Generating newsletter content. This will take a while...")

            # Get Input source summary
            summary_content = await self.generate_input_summary()

            # Fetch user data and preferences
            user_service = UserService(self.db)

            is_premium = user_service.verify_premium_status(email)
            if not is_premium:
                raise HTTPException(
                    status_code=403, detail="User is not a premium member"
                )

            user_data = await user_service.get_user_details(email)
            newsletter_prefs = await self.get_newsletter_preferences(
                user_data["user_id"]
            )

            # Prepare template data
            template_data = {
                "summary": summary_content,
                "logo_data": f"{settings.APP_URL or ''}/images/logo.png",
                "app_url": settings.APP_URL or "",
                "prep_for": user_data["full_name"],
                "prep_by": settings.APP_NAME,
                "timestamp": self.get_now_in_user_tz(newsletter_prefs["timezone"]),
            }

            # Render newsletter
            newsletter_content = await self.render_newsletter_template(template_data)

            # Generate subject line
            subject_line = await self.generate_subject_line(summary_content)

            return {"html_content": newsletter_content, "subject_line": subject_line}

        except Exception as e:
            logger.error(f"Error generating newsletter content: {str(e)}")
            raise e

    async def generate_input_summary(self) -> str:
        """Generate a summary of the input content."""
        try:
            access_token = "TOKEN"
            all_content = f"OBTAINED CONTENT USING TOKEN {access_token}"
            processed_messages = await self.preprocess_messages(all_content)

            # Get response from AI
            prompt = CONTENT_SUMMARY_PROMPT.format(content=processed_messages)
            from app.core.ai.ai_config import get_model

            response = get_model().generate_content(prompt)
            raw_text = response.text.strip()

            # Remove backticks and check for html tags
            if raw_text.startswith("```html"):
                cleaned_text = raw_text[7:-3].strip()  # Remove ```html and ending ```
            else:
                cleaned_text = raw_text

            return cleaned_text
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def preprocess_messages(self, content: str) -> str:
        """Preprocess the input content."""
        # TODO: Add preprocessing logic here
        return content

    async def get_newsletter_preferences(self, user_id: str) -> Dict:
        """Fetch newsletter preferences for a user."""
        try:
            # Mock data for demonstration
            return {"user_id": "123", "pref_hour": "10", "timezone": "UTC"}
        except Exception as e:
            logger.error(f"Error fetching newsletter preferences: {str(e)}")
            raise ValueError("Newsletter preferences not found")
