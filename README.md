# Django v5.2 Starter Template

A modern, production-ready Django 5.2 starter template with best practices built-in.

**Perfect for:** Building web applications, REST APIs, SaaS products, or any Django-based project. This template provides a solid foundation with authentication, database setup, API documentation, and deployment configuration already configured.

**What you get:** A fully configured Django project with PostgreSQL database, REST API with documentation, Docker support, automated testing, and production deployment ready.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [What's Next?](#whats-next)
- [Settings Configuration](#settings-configuration)
- [Available Commands](#available-commands)
- [Docker Deployment](#docker-deployment)
- [Health Check](#health-check)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Django 5.2 Features & Best Practices](#django-52-features--best-practices)
- [Project Structure](#project-structure)
- [Production Deployment](#production-deployment)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

### Core Framework
- **Django 5.2.7 LTS** - Long-term support until April 2028
- **Python 3.13** - Latest Python with JIT compiler and performance improvements
- **PostgreSQL 18** - Latest PostgreSQL with improved I/O performance and query optimization
- **Poetry** - Modern Python dependency management

### API & Documentation
- **Django REST Framework** - Full-featured API framework with pagination, filtering, and throttling
- **drf-spectacular** - OpenAPI 3.0 schema with Swagger UI (`/api/schema/swagger-ui/`) and ReDoc
- **CORS Headers** - Cross-origin resource sharing support for frontend integration

### Performance & Caching
- **Redis Support** - Optional Redis caching (AWS ElastiCache ready) with fallback to local memory
- **Connection Pooling** - psycopg3 with PostgreSQL connection pooling
- **WhiteNoise** - Compressed static file serving
- **Rate Limiting** - django-ratelimit for DDoS protection and API abuse prevention

### Storage & Media
- **AWS S3 Integration** - Optional S3 storage for production media files (install separately: `poetry add django-storages[s3] boto3`)
- **Local File Storage** - Default for development and production

### Development Tools
- **Ruff** - Ultra-fast Python linter and formatter (100x faster than flake8)
- **Django Extensions** - Enhanced shell_plus and utilities
- **Django Debug Toolbar** - Development debugging tools
- **Pre-commit hooks** - Automated code quality checks

### DevOps & Deployment
- **Docker & Docker Compose** - Multi-stage builds with PostgreSQL 18 and Redis 7
- **GitHub Actions CI/CD** - Automated testing and deployment
- **Health Check Endpoint** - `/health/` with database connectivity verification
- **Custom System Checks** - Security and configuration validation
- **Gunicorn** - Production-ready WSGI server with configurable workers

## Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.13.7 | Runtime |
| Django | 5.2.7 LTS | Web framework |
| PostgreSQL | 18 | Database |
| Redis | 7-alpine | Cache (optional) |
| Poetry | 1.8.4 | Dependency management |
| Ruff | 0.8+ | Linting & formatting |
| pytest | 8.3+ | Testing |
| Gunicorn | 23.0+ | WSGI server |
| DRF | 3.15+ | REST API framework |
| drf-spectacular | 0.27+ | API documentation |

## Quick Start

### Prerequisites

**New to Django?** No problem! Here's what you need to install:

1. **Python 3.13+** - Download from [python.org](https://www.python.org/downloads/)
   ```bash
   # Check your Python version
   python --version  # or python3 --version
   ```

2. **Poetry** - Python dependency manager ([installation guide](https://python-poetry.org/docs/#installation))
   ```bash
   # Install Poetry (Linux/macOS/Windows)
   curl -sSL https://install.python-poetry.org | python3 -

   # Verify installation
   poetry --version
   ```

3. **Docker Desktop** - For running PostgreSQL locally ([download here](https://www.docker.com/products/docker-desktop/))
   ```bash
   # Verify installation
   docker --version
   docker compose version
   ```

**Alternative:** If you don't want to use Docker, you can install PostgreSQL directly on your system, but Docker is recommended for easier setup.

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd django-v5-starter-template-with-poetry
   ```

2. **Install dependencies**
   ```bash
   poetry install --no-root
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   The `.env` file contains important settings. For local development, the defaults work fine. Key settings:
   - `DJANGO_ENV=dev` - Use development settings
   - `DEBUG=True` - Show detailed error pages
   - `POSTGRES_HOST=localhost` - Database is running on your machine
   - `SECRET_KEY` - Optional in dev (auto-generated with a warning)

   **Tip:** You can generate a secure SECRET_KEY anytime with:
   ```bash
   poetry run python -m core.manage generate_secret_key
   ```

4. **Start PostgreSQL**
   ```bash
   make up-dev
   ```

5. **Run migrations**
   ```bash
   make migrate
   ```

6. **Create superuser**
   ```bash
   make superuser
   ```

7. **Run development server**
   ```bash
   make runserver
   ```

   The server will start at http://localhost:8000

### What's Next?

**Explore your new Django application:**

1. **Home Page** - http://localhost:8000
   - Basic welcome page (customize in `core/templates/home.html`)

2. **Admin Interface** - http://localhost:8000/admin/
   - Log in with the superuser you created
   - Manage users, groups, and sessions

3. **API Documentation** - http://localhost:8000/api/schema/swagger-ui/
   - Interactive API documentation (Swagger UI)
   - Try out API endpoints directly in your browser
   - Alternative: http://localhost:8000/api/schema/redoc/ (ReDoc view)

4. **Health Check** - http://localhost:8000/health/
   - Monitor application status and database connectivity
   - Returns JSON: `{"status": "healthy", "database": "connected", "version": "5.2"}`

**Start Building:**

- Add your models in `core/backend/models.py`
- Create API views in `core/backend/views.py`
- Add templates in `core/templates/`
- Write tests in `core/backend/tests/`

**Common Commands:**

```bash
# Create database migrations after model changes
make migrations

# Apply migrations to database
make migrate

# Run tests
make test

# Run tests with coverage report
make test-cov

# Format code
make format

# Run linter
make lint

# Open Django shell (with shell_plus if available)
make shell

# Create test data (admin user + 10 test users)
make test-data
```

## Settings Configuration

Settings use a simple, standard Django structure in `core/backend/settings/`:

- `base.py` - Base settings for all environments (Django core, logging, security, caching)
- `dev.py` - Development settings (imports from base.py)
- `prod.py` - Production settings (imports from base.py)
- `test.py` - Test settings (imports from base.py, uses SQLite in-memory)

### Environment Selection

Set `DJANGO_ENV` to choose your environment:

```bash
# Development (default)
DJANGO_ENV=dev python manage.py runserver

# Production
DJANGO_ENV=prod python manage.py check --deploy

# Testing (automatic via pytest)
pytest
```

Or use the full module path:
```bash
export DJANGO_SETTINGS_MODULE=core.backend.settings.prod
```

All settings can be overridden via environment variables (see `.env.example`).

## Available Commands

Run `make help` to see all available commands:

### Development
- `make install` - Install dependencies
- `make update` - Update dependencies and run migrations
- `make migrate` - Run database migrations
- `make migrations` - Create new migrations
- `make runserver` - Start development server
- `make shell` - Start Django shell (with shell_plus)
- `make superuser` - Create superuser

### Testing & Quality
- `make test` - Run tests
- `make test-cov` - Run tests with coverage report
- `make lint` - Run linting (ruff)
- `make format` - Auto-format code (ruff)
- `make pre-commit` - Install pre-commit hooks

### Docker
- `make up-dev` - Start PostgreSQL in Docker
- `make down-dev` - Stop PostgreSQL
- `make logs-dev` - Show PostgreSQL logs

### Utilities
- `make check-db` - Test database connectivity
- `make health-check` - Run comprehensive health checks
- `make clear-sessions` - Clear expired sessions
- `make test-data` - Create test users (admin/admin123, testuser1-10/password123)
- `make clean` - Remove Python artifacts
- `make collectstatic` - Collect static files

## Docker Deployment

### Build and run with Docker Compose

```bash
# Production
docker compose up -d

# Development (database only)
docker compose -f docker-compose.dev.yaml up -d
```

### Environment Variables for Docker

Set in `.env` file or via `docker-compose.yaml`:

```bash
POSTGRES_DB=backend_db
POSTGRES_USER=backend_user
POSTGRES_PASSWORD=backend_password
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

## Health Check

The application includes a health check endpoint at `/health/`:

```bash
curl http://localhost:8000/health/
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "5.2"
}
```

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test
poetry run pytest core/path/to/test_file.py -v
```

## Code Quality

This project uses **Ruff** for linting and formatting (replaces flake8, isort, yapf):

```bash
# Check code
make lint

# Auto-format
make format
```

Pre-commit hooks run automatically on commit. Install them with:
```bash
make pre-commit
```

## Django 5.2 Features & Best Practices

- **PostgreSQL Connection Pooling** - psycopg3 with connection pooling for better performance
- **WhiteNoise Static Files** - Compressed static file serving with manifest caching
- **Enhanced Admin Interface** - Customized admin with better branding
- **Health Check Endpoint** - `/health/` with database connectivity verification
- **Django System Checks** - Custom security and configuration validation
- **REST API** - DRF with OpenAPI documentation, pagination, and rate limiting
- **Redis Caching** - Optional Redis support with AWS ElastiCache compatibility
- **AWS S3 Storage** - Optional S3 integration for production media files
- **CORS Support** - Configured for frontend/API integration
- **Rate Limiting** - Protection against DDoS and API abuse

## Project Structure

```
.
├── core/
│   ├── backend/
│   │   ├── settings/          # Django settings
│   │   │   ├── __init__.py    # Router (uses DJANGO_ENV)
│   │   │   ├── base.py        # Common settings
│   │   │   ├── dev.py         # Development
│   │   │   ├── prod.py        # Production
│   │   │   └── test.py        # Testing
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── general/               # Shared utilities
│   ├── static/                # Static files
│   ├── templates/             # Django templates
│   └── manage.py
├── local/                     # Local overrides (gitignored)
├── scripts/
│   └── entrypoint.sh         # Docker entrypoint
├── .github/
│   └── workflows/            # GitHub Actions CI/CD
├── docker-compose.yaml       # Production
├── docker-compose.dev.yaml   # Development
├── Dockerfile                # Multi-stage build
├── pyproject.toml            # Poetry dependencies & config
├── Makefile                  # Common commands
└── README.md
```

## Production Deployment

### Required Environment Variables

Create a `.env` file with the following settings:

```bash
# Core Settings
DJANGO_ENV=prod
DEBUG=False

# SECRET_KEY - REQUIRED (50+ characters, use generate_secret_key command)
SECRET_KEY=your-long-random-secret-key-here-at-least-50-characters

# Domains - REQUIRED
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database - REQUIRED
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db  # or your database host
POSTGRES_PORT=5432

# Redis Cache - REQUIRED (avoids production warnings)
REDIS_URL=redis://redis:6379/0  # or your Redis host

# Security - REQUIRED for HTTPS deployments
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
USE_HTTPS=True

# Optional: AWS S3 for media files
# USE_S3=True
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_STORAGE_BUCKET_NAME=your-bucket-name
# AWS_S3_REGION_NAME=us-east-1
```

### Build and Deploy

```bash
# Build images
docker compose build

# Deploy
docker compose up -d
```

### Verify Deployment

```bash
# Check health endpoint
curl https://yourdomain.com/health/

# Run system checks (should have no errors)
docker compose exec app python -m core.manage check --deploy
```

### Zero-Downtime Deployments

For zero-downtime deployments, use the `SKIP_MIGRATIONS` and `SKIP_COLLECTSTATIC` environment variables:

```bash
# Step 1: Deploy new code with migrations skipped
docker compose build
SKIP_MIGRATIONS=true SKIP_COLLECTSTATIC=true docker compose up -d

# Step 2: Run migrations separately (if needed)
docker compose exec app python -m core.manage migrate

# Step 3: Restart to run collectstatic (if static files changed)
docker compose restart app
```

This allows you to:
- Deploy new application code without downtime
- Run migrations in a controlled manner
- Avoid unnecessary collectstatic runs on every restart

### Optional Production Services

**AWS ElastiCache (Redis)**
```bash
# Set in .env or environment
REDIS_URL=redis://your-elasticache-endpoint:6379/0
```

**AWS S3 (Media Files)**
```bash
# Set in .env or environment
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

See production settings in `core/backend/settings/prod.py` for all available configuration options.

## Security

Production security settings in `core/backend/settings/prod.py`:

- **HTTPS redirect** - Configurable via `SECURE_SSL_REDIRECT` (default: False for local testing)
- **HSTS headers** - Configurable via `SECURE_HSTS_SECONDS` (default: 0)
- **Secure cookies** - Configurable via `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE`
- **CSRF protection** - Set `CSRF_TRUSTED_ORIGINS` for your domains
- **CORS configuration** - Set `CORS_ALLOWED_ORIGINS` for your frontend
- **Rate limiting** - Enabled by default with django-ratelimit
- **Redis cache** - Set `REDIS_URL` to enable Redis caching (recommended for production)

**Important:** The security settings default to disabled for local testing. Enable them in production by setting the environment variables in your `.env` file as shown in the [Production Deployment](#production-deployment) section.

Django system checks will warn you about any security issues when you run:
```bash
python -m core.manage check --deploy
```

## Troubleshooting

### Common Issues for Beginners

#### "poetry: command not found"

Poetry is not installed or not in your PATH.

**Solution:**
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add this to your ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

#### "docker: command not found" or "Cannot connect to Docker daemon"

Docker is not installed or not running.

**Solution:**
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Start Docker Desktop
3. Verify: `docker --version`

#### "make: command not found" (Windows)

Windows doesn't have `make` by default.

**Solution - Option 1 (Recommended):** Use Poetry directly:
```bash
# Instead of: make migrate
poetry run python -m core.manage migrate

# Instead of: make runserver
poetry run python -m core.manage runserver

# Instead of: make test
poetry run pytest
```

**Solution - Option 2:** Install `make` for Windows:
- Install via Chocolatey: `choco install make`
- Or use WSL2 (Windows Subsystem for Linux)

#### Database connection errors: "connection refused" or "could not connect to server"

PostgreSQL is not running or connection settings are wrong.

**Solution:**
```bash
# Check if PostgreSQL container is running
docker ps

# If not running, start it
make up-dev

# Check connection settings in .env
# For local dev: POSTGRES_HOST=localhost
# For Docker prod: POSTGRES_HOST=db
```

#### "ModuleNotFoundError" or "No module named 'django'"

Dependencies are not installed or wrong Python environment.

**Solution:**
```bash
# Install dependencies
poetry install --no-root

# Verify Poetry is using correct Python version
poetry env info

# If needed, recreate virtual environment with Python 3.13
poetry env use python3.13
poetry install --no-root
```

#### "SECRET_KEY" warnings in development

This is expected! The default development SECRET_KEY shows a warning to remind you to set your own.

**Solution (optional):**
```bash
# Generate a secure key
poetry run python -m core.manage generate_secret_key

# Add to .env file
SECRET_KEY=<generated-key-here>
```

#### Port 8000 already in use

Another application is using port 8000.

**Solution:**
```bash
# Find what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
poetry run python -m core.manage runserver 8001
```

#### Tests failing with database errors

Test database permissions or configuration issue.

**Solution:**
```bash
# Tests use in-memory SQLite by default (no PostgreSQL needed)
# If still failing, try:
poetry run pytest -v  # Verbose output to see exact error

# Clear pytest cache
rm -rf .pytest_cache
poetry run pytest
```

#### Static files not loading (CSS/JS missing)

Static files haven't been collected.

**Solution:**
```bash
# Development: Static files are served automatically
# Just run: make runserver

# Production: Collect static files
make collectstatic
# Or: poetry run python -m core.manage collectstatic
```

#### "django.core.exceptions.ImproperlyConfigured"

Settings configuration error, usually missing environment variables.

**Solution:**
```bash
# Check your .env file exists
ls -la .env

# Verify DJANGO_ENV is set
cat .env | grep DJANGO_ENV

# For production, ensure all required variables are set:
# - SECRET_KEY (50+ characters)
# - ALLOWED_HOSTS
# - Database credentials
# - REDIS_URL
```

### Getting Help

- **Django Documentation**: https://docs.djangoproject.com/en/5.2/
- **Django Tutorial**: https://docs.djangoproject.com/en/5.2/intro/tutorial01/
- **Poetry Documentation**: https://python-poetry.org/docs/
- **Docker Documentation**: https://docs.docker.com/get-started/

**Still stuck?** Check the error message carefully - Django's error pages in DEBUG mode are very helpful and usually tell you exactly what's wrong!

## License

MIT
