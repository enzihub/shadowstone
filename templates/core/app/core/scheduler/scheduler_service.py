# scheduler_service.py

from datetime import datetime
from typing import Dict, List

from sqlalchemy.orm import Session

from app.core.config.logger import logger
from app.core.messaging.message_service import MessageService
from app.db import database


class SchedulerService:
    def __init__(self, message_service: MessageService):
        self.message_service = message_service

    async def get_users_for_scheduling(
        self, db: Session, lookahead_minutes: int
    ) -> List[Dict]:
        """
        Calls the stored procedure with dynamic target hours and maps messages
        """
        try:
            # Mock data
            # TODO: get these from database for the app
            return [
                {
                    "user_id": "123",
                    "email": "someone@example.com",
                    "phone": "+1 555 0100",
                    "timezone": "UTC",
                    "scheduled_for": datetime.now().isoformat(),
                }
            ]
        except Exception as e:
            logger.error(f"Error fetching users for scheduling: {str(e)}")
            return []

    async def produce_messages_async(self):
        """Async logic for scheduling newsletters"""
        db = database.SessionLocal()
        try:
            users = await self.get_users_for_scheduling(db, 60)
            for user in users:
                try:
                    target_time = datetime.fromisoformat(user["scheduled_for"])
                    # Check existing newsletters
                    existing_newsletters = self.message_service.get_user_messages(
                        user["user_id"]
                    )
                    if any(
                        abs(float(n["scheduled_time"]) - target_time.timestamp()) < 3600
                        for n in existing_newsletters
                    ):
                        logger.info(
                            f"Message already scheduled for {user['user_id']} at {target_time}"
                        )
                        continue

                    # Generate message payload
                    message_payload = {
                        "subject": "Hello this is the subject",
                        "body": "Hello this is the body",
                    }

                    message_data = self.message_service.get_message_data(
                        user, message_payload, target_time.timestamp()
                    )

                    # Enqueue message using the ACTUAL target time
                    success = self.message_service.enqueue_message(
                        user["user_id"], target_time, message_data
                    )

                    if success:
                        logger.info(
                            f"Scheduled message for {user['user_id']} at {target_time}"
                        )
                    else:
                        logger.error(f"Failed to schedule for {user['user_id']}")

                except Exception as e:
                    logger.error(f"Error processing {user['user_id']}: {str(e)}")

        except Exception as e:
            logger.error(f"Producer error: {str(e)}")
        finally:
            db.close()

    async def consume_messages_async(self):
        """Async logic for processing and sending messages"""
        try:
            # Get pending messages using the service
            messages = self.message_service.get_pending_messages()
            for message in messages:
                logger.info(f"Processing message {message.id}")
                try:
                    # Send the message
                    success = await self.message_service.send_user_message(
                        message.email, message.payload
                    )

                    if success:
                        # Mark as sent using the service
                        self.message_service.mark_message_sent(message.id)
                        logger.info(f"Message sent successfully to {message.phone}")
                    else:
                        logger.error(f"Failed to send message to {message.email}")

                except Exception as e:
                    logger.error(f"Error processing message {message.id}: {str(e)}")

        except Exception as e:
            logger.error(f"Async consumer error: {str(e)}")
