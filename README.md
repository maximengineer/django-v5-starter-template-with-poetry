# Django v5.2 Starter Template

A modern, production-ready Django 5.2 starter template with best practices built-in.

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

- Python 3.13+
- Poetry 1.8+
- Docker & Docker Compose (for local database)

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
   # Edit .env with your settings
   ```

4. **Start PostgreSQL**
   ```bash
   make up-dev
   ```

5. **Run migrations**
   ```bash
   make migrate
   ```

6. **Create superuser** (optional)
   ```bash
   make superuser
   ```

7. **Run development server**
   ```bash
   make runserver
   ```

Visit http://localhost:8000

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

1. **Set environment variables**
   - `DJANGO_ENV=prod` - Use production settings
   - `SECRET_KEY` - Django secret key (50+ characters)
   - `ALLOWED_HOSTS` - Comma-separated domains
   - `CSRF_TRUSTED_ORIGINS` - Comma-separated HTTPS origins
   - Database credentials
   - `REDIS_URL` - Redis connection URL (optional, for caching)
   - `USE_S3=True` - Enable S3 for media files (optional)
   - AWS credentials (if using S3)

2. **Build and deploy**
   ```bash
   docker compose build
   docker compose up -d
   ```

3. **Verify deployment**
   ```bash
   # Check health endpoint
   curl http://localhost:8000/health/

   # Run system checks
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

Production security settings are enabled in `core/backend/settings/prod.py`:

- HTTPS redirect
- HSTS headers (1 year)
- Secure cookies
- CSRF protection
- CORS configuration
- Rate limiting
- Django system checks for security validation

All security settings are configured with safe defaults and can be customized via environment variables.

## Contributing

1. Install pre-commit hooks: `make pre-commit`
2. Run tests: `make test`
3. Format code: `make format`
4. Check code quality: `make lint`

## License

MIT

## Support

For detailed upgrade information, see `UPGRADE_PLAN.md`.
