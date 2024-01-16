.PHONY: install
install:
	poetry install

.PHONY: update
update: install migrate ;

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: runserver
runserver:
	poetry run python -m core.manage runserver
