# Multi-stage build for smaller image size
FROM python:3.13-slim-bookworm AS builder

WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

# Runtime stage
FROM python:3.13-slim-bookworm

WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=. \
    PATH="/opt/project/.venv/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/project/.venv /opt/project/.venv

# Copy application code
COPY core core
COPY local local
COPY scripts/entrypoint.sh /entrypoint.sh
COPY scripts/docker-healthcheck.py /app/scripts/docker-healthcheck.py

RUN chmod +x /entrypoint.sh

# Health check - uses dedicated script with error logging
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python /app/scripts/docker-healthcheck.py

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
