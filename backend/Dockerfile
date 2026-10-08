# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.13.7
FROM python:${PYTHON_VERSION}-slim as backend

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Prevent Python from writing pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_NO_CACHE=1

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

USER appuser

# COPY --chown=appuser:appuser pyproject.toml uv.lock ./
COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project

# COPY --chown=appuser:appuser . .

# Copy the source code into the container.
COPY . /app
WORKDIR /app


RUN uv sync --locked --no-editable
# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000","--forwarded-allow-ips", "*"]
