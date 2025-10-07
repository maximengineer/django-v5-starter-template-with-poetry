#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='python -m core.manage'

# Environment variables for controlling startup behavior
SKIP_MIGRATIONS=${SKIP_MIGRATIONS:-false}
SKIP_COLLECTSTATIC=${SKIP_COLLECTSTATIC:-false}

echo '========================================'
echo 'Waiting for PostgreSQL to be ready...'
echo '========================================'

# Wait for database to be ready with retry limit
RETRIES=30
until PGPASSWORD="${POSTGRES_PASSWORD}" psql \
    -h "${POSTGRES_HOST}" \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    -c '\q' 2>/dev/null; do
  RETRIES=$((RETRIES-1))
  if [ $RETRIES -eq 0 ]; then
    echo "❌ Failed to connect to PostgreSQL after 30 attempts (60 seconds)"
    echo "Please check your database configuration and ensure PostgreSQL is running."
    echo "Connection details: host=${POSTGRES_HOST}, user=${POSTGRES_USER}, db=${POSTGRES_DB}"
    exit 1
  fi
  echo "PostgreSQL is unavailable - sleeping ($RETRIES attempts remaining)"
  sleep 2
done

echo '✓ PostgreSQL is ready!'
echo ''

# Collectstatic (can be skipped for faster restarts)
if [ "$SKIP_COLLECTSTATIC" = "true" ]; then
  echo "⏭  Skipping collectstatic (SKIP_COLLECTSTATIC=true)"
else
  echo '========================================'
  echo 'Collecting static files...'
  echo '========================================'
  $RUN_MANAGE_PY collectstatic --no-input
  echo ''
fi

# Migrations (can be skipped for zero-downtime deployments)
if [ "$SKIP_MIGRATIONS" = "true" ]; then
  echo "⏭  Skipping migrations (SKIP_MIGRATIONS=true)"
else
  echo '========================================'
  echo 'Running database migrations...'
  echo '========================================'
  $RUN_MANAGE_PY migrate --no-input
  echo ''
fi

echo '========================================'
echo 'Starting application server...'
echo '========================================'

# Calculate optimal worker count based on available resources
# Formula: (2 * CPU cores) + 1, with memory-aware capping
if [ -z "$GUNICORN_WORKERS" ]; then
  # Get CPU count (default to 2 if unknown)
  CPU_CORES=$(nproc 2>/dev/null || echo "2")
  OPTIMAL_WORKERS=$((2 * CPU_CORES + 1))

  # Check available memory and cap workers if needed
  # Each Gunicorn worker typically uses 50-100MB base + request memory
  if [ -f /sys/fs/cgroup/memory/memory.limit_in_bytes ]; then
    # cgroups v1
    MEMORY_LIMIT=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes)
  elif [ -f /sys/fs/cgroup/memory.max ]; then
    # cgroups v2
    MEMORY_LIMIT=$(cat /sys/fs/cgroup/memory.max)
  else
    MEMORY_LIMIT="max"
  fi

  # If memory limit is set and numeric, calculate max workers
  # Assume 150MB per worker (conservative estimate)
  if [ "$MEMORY_LIMIT" != "max" ] && [ "$MEMORY_LIMIT" -gt 0 ] 2>/dev/null; then
    MEMORY_MB=$((MEMORY_LIMIT / 1024 / 1024))
    MAX_WORKERS=$((MEMORY_MB / 150))

    if [ $MAX_WORKERS -lt $OPTIMAL_WORKERS ]; then
      echo "⚠️  Memory limit detected: ${MEMORY_MB}MB"
      echo "   Capping workers from $OPTIMAL_WORKERS to $MAX_WORKERS to prevent OOM"
      GUNICORN_WORKERS=$MAX_WORKERS
    else
      GUNICORN_WORKERS=$OPTIMAL_WORKERS
    fi
  else
    GUNICORN_WORKERS=$OPTIMAL_WORKERS
  fi

  # Ensure at least 2 workers
  if [ $GUNICORN_WORKERS -lt 2 ]; then
    GUNICORN_WORKERS=2
  fi

  echo "ℹ️  Auto-detected ${CPU_CORES} CPU cores, using ${GUNICORN_WORKERS} workers"
fi

# Use gunicorn for production (better than daphne for WSGI)
exec gunicorn core.backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS} \
    --worker-class sync \
    --timeout ${GUNICORN_TIMEOUT:-60} \
    --access-logfile - \
    --error-logfile - \
    --log-level ${GUNICORN_LOG_LEVEL:-info}
