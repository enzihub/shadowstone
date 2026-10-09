FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock* /app/
RUN uv sync --no-dev --no-install-project
COPY . /app
ENV PATH="/app/.venv/bin:$PATH" PORT=8000 HOST=0.0.0.0 PYTHONPATH=/app PYTHONUNBUFFERED=1 ENVIRONMENT=production
EXPOSE ${PORT}
CMD ["sh", "-c", "uvicorn main:app --host ${HOST} --port ${PORT} --workers 1"]
