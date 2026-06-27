# secure-waypoint

A FastAPI backend for secure authentication and user management. It includes
role-based access control, user CRUD endpoints, token refresh, Docker-based
local services, Alembic migration scaffolding, and a small developer workflow
for linting, testing, and CI.

## Features

- Authentication and authorization with Basic login, Bearer access tokens, and
  refresh tokens.
- Role-based access control for user, moderator, and admin actions.
- User CRUD endpoints, `/me`, username search, pagination, and creation-year
  filtering.
- OpenAPI documentation at `/docs` and ReDoc at `/redoc`.
- Docker Compose services for the API, PostgreSQL, and Nginx.
- Separate local PostgreSQL test service in `docker-compose.test.yml`.
- Alembic scaffolding for async SQLAlchemy migrations.
- GitHub Actions CI for Ruff, Black formatting through pre-commit, and pytest
  coverage against PostgreSQL.

## Requirements

- Docker or Docker Compose for local database services.
- Poetry for Python dependency management.
- Python 3.12 is used by the Docker image and CI.

## Setup

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

Install dependencies:

```bash
make install
```

Start the application stack:

```bash
docker-compose up -d --build
```

Initialize the database and create the initial admin user:

```bash
docker-compose exec api python -m cli db init
```

The API is available at `http://localhost:8000`. Nginx proxies it at
`http://localhost`.

The ASGI application target is `core.server:app`. `main.py` is kept as a
direct-run convenience wrapper and does not start Uvicorn on import.

## Developer Commands

The Makefile provides the common local workflow:

```bash
make install       # poetry install
make format        # ruff autofix and Black through pre-commit
make lint          # ruff check
make test          # pytest
make coverage      # coverage run -m pytest, then coverage report
make pre-commit    # pre-commit run --all-files
make ci            # local CI subset: lint and coverage
```

Pass focused pytest arguments with `PYTEST_ARGS`:

```bash
make test PYTEST_ARGS='tests/api/v1/test_tokens.py'
```

`make typecheck` runs `mypy .`, but it is not part of the default CI target yet
because the current strict mypy baseline is not clean.

## Test Database

Tests expect a PostgreSQL database whose name is the configured `POSTGRES_DB`
with `-test` appended. The test Compose file creates that database with local
defaults:

```bash
make db-test-up
make test
make db-test-down
```

By default this uses:

- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=postgres`
- `POSTGRES_HOST=localhost`
- `POSTGRES_PORT=5432`
- `POSTGRES_DB=secure_waypoint`

Override those variables in the shell or when invoking `make` if needed.

## Migrations

Alembic is configured in `alembic.ini` and `alembic/env.py`. The migration
environment imports `app.models.Base.metadata` and reads the async PostgreSQL
URL from `core.config.config.SQLALCHEMY_DATABASE_URI`.

Create a migration:

```bash
poetry run alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```bash
poetry run alembic upgrade head
```

## API Notes

Login uses Basic authentication:

```bash
curl -X POST http://localhost:8000/api/v1/tokens \
  -H 'Authorization: Basic <base64 username:password>'
```

Refresh tokens are submitted in the request body while the current access token
is passed as the Bearer token:

```bash
curl -X PUT http://localhost:8000/api/v1/tokens \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Content-Type: application/json' \
  -d '{"refresh_token":"<refresh-token>"}'
```

Refresh tokens are type-checked and bound to the same user as the access token.

## CI

GitHub Actions is configured at `.github/workflows/ci.yml`. It runs on pushes
and pull requests, starts a PostgreSQL service, installs Poetry dependencies,
then runs:

- `poetry run ruff check .`
- `poetry run pre-commit run black --all-files`
- `poetry run coverage run -m pytest`
- `poetry run coverage report`
