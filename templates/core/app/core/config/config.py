import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env",), env_file_encoding="utf-8",
                                      case_sensitive=True, extra="ignore")

    ENVIRONMENT: str = "development"
    APP_NAME: str = "My SaaS"
    APP_URL: Optional[str] = None  # the -web app, used for links and CORS

    # Database and queue
    DATABASE_URL: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    PRODUCE_INTERVAL_SECONDS: Optional[int] = None
    CONSUME_INTERVAL_SECONDS: Optional[int] = None

    # Rate limits
    RATE_LIMIT_WINDOW_SECONDS: int = 86400
    RATE_LIMIT_X: int = 1
    RATE_LIMIT_THREADS: int = 1
    RATE_LIMIT_LINKEDIN: int = 1

    # Optional services: leave blank to turn off
    GEMINI_API_KEY: Optional[str] = None
    CLERK_SECRET_KEY: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    MAILTRAP_API_TOKEN: Optional[str] = None
    EMAIL_SUBJECT: Optional[str] = None
    FROM_EMAIL: Optional[str] = None
    FROM_NAME: Optional[str] = None


class DevelopmentConfig(BaseConfig):
    model_config = SettingsConfigDict(env_file=(".env", ".env.development"), extra="ignore", case_sensitive=True)


class ProductionConfig(BaseConfig):
    model_config = SettingsConfigDict(env_file=(".env", ".env.production"), extra="ignore", case_sensitive=True)


class TestConfig(BaseConfig):
    model_config = SettingsConfigDict(env_file=(".env.test",), extra="ignore", case_sensitive=True)


@lru_cache()
def get_settings() -> BaseConfig:
    """Pick the config class from ENVIRONMENT (development, production or test)."""
    environment = os.getenv("ENVIRONMENT", "development")
    return {"development": DevelopmentConfig, "production": ProductionConfig,
            "test": TestConfig}.get(environment, DevelopmentConfig)()


settings = get_settings()
