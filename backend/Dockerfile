# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.13.7
FROM python:${PYTHON_VERSION}-slim as backend

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/backend

# Prevent Python from writing pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --uid "${UID}" \
    appuser \
    && mkdir -p /home/appuser \
    && chown -R appuser:appuser /home/appuser

# Install system dependencies for psycopg2 and other build tools
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/venv /app \
    && chown -R appuser:appuser /opt/venv /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,id=s/3cd0b9f3-5bfa-401f-b948-766dc243efb4-/root/.cache/uv,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY . .

RUN --mount=type=cache,id=s/3cd0b9f3-5bfa-401f-b948-766dc243efb4-/root/.cache/uv,target=/root/.cache/uv \
    uv sync --frozen 

USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8000","--forwarded-allow-ips", "*"]
