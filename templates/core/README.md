# Core API (FastAPI)

The `-core` part of a ShadowStone project: a FastAPI service with a Redis-backed
message queue, Celery workers for scheduled jobs, SQLAlchemy models that match the
web app's tables, and an optional Gemini summary + Mailtrap email pipeline.

```bash
docker compose up -d redis            # Redis on 127.0.0.1:${REDIS_PORT:-6379}
uv run uvicorn main:app --reload --port 8000
open http://localhost:8000/docs
```

Postgres comes from the web component (`../<name>-web`, `docker compose up -d`).
`.env` was written by `ss create`; every optional service stays off while its key is blank.

| Route | What it does |
| --- | --- |
| `GET /` | service name and environment |
| `GET /health` | checks Postgres and Redis |
| `GET /queue` | messages waiting in Redis |
| `POST /welcome` | queues a welcome message (called by the web app) |
| `POST /send-newsletter?email=` | queues a newsletter for one user |

Workers: `uv run celery -A app.core.scheduler.job_tasks worker` and `... beat`.
Tests: `uv run pytest`.
