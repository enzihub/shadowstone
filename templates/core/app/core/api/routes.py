from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

from app.core.config.config import settings
from app.core.config.logger import logger
from app.core.messaging.message_service import MessageService
from app.core.newsletter.newsletter_service import NewsletterService
from app.db import database
from app.db.redis_service import RedisService

router = APIRouter()

redis_service = RedisService()
message_service = MessageService(redis_service)
newsletter_service = NewsletterService(message_service)


@router.get("/")
async def root():
    return {"service": f"{settings.APP_NAME} core", "environment": settings.ENVIRONMENT, "docs": "/docs"}


@router.get("/health")
async def health():
    """Report whether Postgres and Redis answer."""
    db_ok = True
    try:
        with database.engine.connect() as conn:
            conn.execute(text("select 1"))
    except Exception as e:
        logger.warning(f"database check failed: {e}")
        db_ok = False
    redis_ok = bool(redis_service.check_connection())
    status = "ok" if db_ok and redis_ok else "degraded"
    return {"status": status, "database": db_ok, "redis": redis_ok}


@router.get("/queue")
async def queue():
    """Messages waiting in the Redis queue."""
    pending = message_service.get_pending_messages()
    return {"pending": len(pending), "items": [m.id for m in pending][:20]}


@router.post("/send-newsletter")
async def send_newsletter(email: str):
    """Queue a newsletter for one user right now."""
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    logger.info(f"Newsletter requested for {email}")
    return await newsletter_service.schedule_immediate_newsletter(email)


class Welcome(BaseModel):
    phone: str
    email: str = ""


@router.post("/welcome")
async def welcome(body: Welcome):
    """Queue a welcome message. The web app calls this when a user saves a phone number."""
    now = datetime.now()
    user = {"user_id": body.phone, "email": body.email, "phone": body.phone}
    data = message_service.get_message_data(
        user, {"subject": f"Welcome to {settings.APP_NAME}", "body": f"Welcome to {settings.APP_NAME}."}, now.timestamp()
    )
    if not message_service.enqueue_message(body.phone, now, data):
        raise HTTPException(status_code=503, detail="Could not reach Redis")
    return {"queued": True, "id": data.id}
