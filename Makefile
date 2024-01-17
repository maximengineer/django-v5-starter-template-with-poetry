.PHONY: install
install:
	poetry install

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: update
update: install migrate install-pre-commit ;

.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: runserver
runserver:
	poetry run python -m core.manage runserver

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files
