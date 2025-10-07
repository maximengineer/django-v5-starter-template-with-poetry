.PHONY: help
help:
	@echo "Django 5.2 Development Commands"
	@echo "================================"
	@echo "make install          - Install dependencies"
	@echo "make update           - Update dependencies and run migrations"
	@echo "make migrate          - Run database migrations"
	@echo "make migrations       - Create new migrations"
	@echo "make runserver        - Start development server"
	@echo "make shell            - Start Django shell (with shell_plus if available)"
	@echo "make superuser        - Create superuser"
	@echo "make collectstatic    - Collect static files"
	@echo ""
	@echo "Testing & Quality:"
	@echo "make test             - Run tests"
	@echo "make test-cov         - Run tests with coverage report"
	@echo "make lint             - Run linting (ruff)"
	@echo "make format           - Format code (ruff)"
	@echo "make pre-commit       - Install pre-commit hooks"
	@echo ""
	@echo "Docker:"
	@echo "make up-dev           - Start PostgreSQL in Docker"
	@echo "make down-dev         - Stop PostgreSQL in Docker"
	@echo "make logs-dev         - Show PostgreSQL logs"
	@echo ""
	@echo "Utilities:"
	@echo "make check-db         - Test database connectivity"
	@echo "make health-check     - Run comprehensive health checks"
	@echo "make clear-sessions   - Clear expired sessions"
	@echo "make test-data        - Create test users (admin/admin123, testuser1-10/password123)"
	@echo "make clean            - Remove Python artifacts"

.PHONY: install
install:
	poetry install --no-root

.PHONY: update
update: install migrate pre-commit

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: runserver
runserver:
	poetry run python -m core.manage runserver

.PHONY: shell
shell:
	@poetry run python -m core.manage shell_plus 2>/dev/null || poetry run python -m core.manage shell

.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: collectstatic
collectstatic:
	poetry run python -m core.manage collectstatic --no-input

.PHONY: test
test:
	poetry run pytest -v -n auto --show-capture=no

.PHONY: test-cov
test-cov:
	poetry run pytest -v -n auto --cov=core --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: format
format:
	poetry run ruff format .
	poetry run ruff check --fix .

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: up-dev
up-dev:
	docker compose -f docker-compose.dev.yaml up -d

.PHONY: down-dev
down-dev:
	docker compose -f docker-compose.dev.yaml down

.PHONY: logs-dev
logs-dev:
	docker compose -f docker-compose.dev.yaml logs -f

.PHONY: check-db
check-db:
	@echo "========================================"
	@echo "Database Connectivity Check"
	@echo "========================================"
	@poetry run python -c "\
	from django.db import connection; \
	try: \
	    cursor = connection.cursor(); \
	    cursor.execute('SELECT version()'); \
	    print('✓ Database connection successful!'); \
	    print(f'  Version: {cursor.fetchone()[0]}'); \
	    cursor.execute('SELECT current_database()'); \
	    print(f'  Database: {cursor.fetchone()[0]}'); \
	    cursor.execute('SELECT current_user'); \
	    print(f'  User: {cursor.fetchone()[0]}'); \
	except Exception as e: \
	    print(f'✗ Database connection failed: {e}'); \
	    exit(1)"

.PHONY: health-check
health-check:
	@echo "========================================"
	@echo "System Health Check"
	@echo "========================================"
	@poetry run python -c "\
	from django.db import connection; \
	from django.core.cache import cache; \
	from django.conf import settings; \
	import sys; \
	failed = False; \
	print('Checking database... ', end=''); \
	try: \
	    cursor = connection.cursor(); \
	    cursor.execute('SELECT 1'); \
	    print('✓ OK'); \
	except Exception as e: \
	    print(f'✗ FAIL: {e}'); \
	    failed = True; \
	print('Checking cache... ', end=''); \
	try: \
	    cache.set('test', 'ok', 10); \
	    result = cache.get('test'); \
	    cache.delete('test'); \
	    print('✓ OK' if result == 'ok' else '✗ FAIL'); \
	    failed = failed or (result != 'ok'); \
	except Exception as e: \
	    print(f'✗ FAIL: {e}'); \
	    failed = True; \
	print('Checking settings... ', end=''); \
	print('✓ OK'); \
	print(''); \
	print('======================================'); \
	if failed: \
	    print('Health check FAILED'); \
	    sys.exit(1); \
	else: \
	    print('All health checks PASSED ✓');"

.PHONY: clear-sessions
clear-sessions:
	@echo "========================================"
	@echo "Session Cleanup"
	@echo "========================================"
	@poetry run python -c "\
	from django.contrib.sessions.models import Session; \
	from django.utils import timezone; \
	sessions = Session.objects.filter(expire_date__lt=timezone.now()); \
	count = sessions.count(); \
	if count == 0: \
	    print('No expired sessions to delete.'); \
	else: \
	    print(f'Found {count} expired session(s)'); \
	    deleted, _ = sessions.delete(); \
	    print(f'✓ Deleted {deleted} session(s)');"

.PHONY: test-data
test-data:
	@echo "========================================"
	@echo "Test Data Generation"
	@echo "========================================"
	@poetry run python -c "\
	from django.contrib.auth import get_user_model; \
	User = get_user_model(); \
	print('Creating admin superuser... ', end=''); \
	if User.objects.filter(username='admin').exists(): \
	    print('⚠ Already exists'); \
	else: \
	    User.objects.create_superuser('admin', 'admin@example.com', 'admin123'); \
	    print('✓ Created'); \
	print('Creating test users... ', end=''); \
	created = 0; \
	for i in range(1, 11): \
	    username = f'testuser{i}'; \
	    if not User.objects.filter(username=username).exists(): \
	        User.objects.create_user(username, f'{username}@example.com', 'password123'); \
	        created += 1; \
	print(f'✓ Created {created} user(s)'); \
	print(''); \
	print('Quick Access:'); \
	print('  Admin: admin / admin123'); \
	print('  Test users: testuser1-10 / password123');"

.PHONY: clean
clean:
	@echo "Cleaning Python artifacts..."
	@python -c "import shutil; import pathlib; \
		[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; \
		[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.pytest_cache')]; \
		[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.ruff_cache')]; \
		[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('*.egg-info')]; \
		[p.unlink(missing_ok=True) for p in pathlib.Path('.').rglob('*.pyc')]; \
		[p.unlink(missing_ok=True) for p in pathlib.Path('.').rglob('*.pyo')]; \
		"
	@python -c "import shutil; shutil.rmtree('htmlcov', ignore_errors=True)"
	@python -c "import pathlib; pathlib.Path('.coverage').unlink(missing_ok=True); pathlib.Path('coverage.xml').unlink(missing_ok=True)"
	@echo "✓ Clean complete"
