"""FastAPI entry point for the -core service."""
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # noqa: E402
from starlette.middleware.cors import CORSMiddleware  # noqa: E402

from app.core.api.routes import router  # noqa: E402
from app.core.config.config import settings  # noqa: E402
from app.core.config.logger import logger  # noqa: E402
from app.db.redis_service import RedisService  # noqa: E402

if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=1.0)

if settings.GEMINI_API_KEY:
    import google.generativeai as genai

    genai.configure(api_key=settings.GEMINI_API_KEY)

app = FastAPI(title=f"{settings.APP_NAME} core API")
app.redis_service = RedisService()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o for o in [settings.APP_URL] if o] or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    if app.redis_service.check_connection():
        logger.info("Redis connection established")
    else:
        logger.warning("Redis is not reachable at REDIS_URL; queued messages will not work")


@app.on_event("shutdown")
async def shutdown_event():
    try:
        app.redis_service.client.close()
    except Exception as e:  # pragma: no cover
        logger.error(f"Redis shutdown error: {e}")
