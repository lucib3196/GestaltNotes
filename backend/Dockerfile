# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.13.7
# Github
ARG GH_PACKAGE_TOKEN
FROM python:${PYTHON_VERSION}-slim as backend
RUN if [ -n "$GH_PACKAGE_TOKEN" ]; then \
      echo "GH_PACKAGE_TOKEN is available"; \
    else \
      echo "ERROR: GH_PACKAGE_TOKEN is missing or empty"; \
      exit 1; \
    fi
# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/backend

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
# Install ssh for git
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Check 
RUN test -n "$GH_PACKAGE_TOKEN" \
    && git config --global credential.helper \
       '!f() { printf "%s\n" "username=x-access-token" "password=$GH_PACKAGE_TOKEN"; }; f' \
    && uv sync --frozen --no-install-project \
    && git config --global --unset credential.helper

RUN mkdir -p /opt/venv /app \
    && chown -R appuser:appuser /opt/venv /app

USER appuser

RUN mkdir -p /opt/venv /app \
    && chown -R appuser:appuser /opt/venv /app

COPY backend/pyproject.toml backend/uv.lock ./
COPY packages /app/packages

RUN uv sync --frozen --no-install-project

COPY backend/ .

RUN uv sync --frozen

EXPOSE 8000