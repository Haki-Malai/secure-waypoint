POETRY ?= poetry
COMPOSE ?= $(shell if command -v docker-compose >/dev/null 2>&1; then printf docker-compose; else printf 'docker compose'; fi)
COMPOSE_TEST_FILE ?= docker-compose.test.yml
PYTEST_ARGS ?=
APP_DEBUG ?= false

export ENVIRONMENT ?= testing
export DEBUG := $(APP_DEBUG)
export SECRET_KEY ?= local-test-secret
export POSTGRES_USER ?= postgres
export POSTGRES_PASSWORD ?= postgres
export POSTGRES_HOST ?= localhost
export POSTGRES_PORT ?= 5432
export POSTGRES_DB ?= secure_waypoint
export ADMIN_USERNAME ?= admin
export ADMIN_PASSWORD ?= admin

.PHONY: install format lint typecheck test coverage pre-commit ci db-up db-down db-test-up db-test-down

install:
	$(POETRY) install

format:
	$(POETRY) run ruff check --fix .
	$(POETRY) run pre-commit run black --all-files

lint:
	$(POETRY) run ruff check .

typecheck:
	$(POETRY) run mypy .

test:
	$(POETRY) run pytest $(PYTEST_ARGS)

coverage:
	$(POETRY) run coverage run -m pytest $(PYTEST_ARGS)
	$(POETRY) run coverage report

pre-commit:
	$(POETRY) run pre-commit run --all-files

ci: lint coverage

db-up: db-test-up

db-down: db-test-down

db-test-up:
	$(COMPOSE) -f $(COMPOSE_TEST_FILE) up -d

db-test-down:
	$(COMPOSE) -f $(COMPOSE_TEST_FILE) down -v
