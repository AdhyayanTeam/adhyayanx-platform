# ADX Platform

Business Operations Platform backend.

## Structure

```
api/              FastAPI entry point and HTTP layer
kernel/           Bootstrap, DI container, lifecycle
platform/         Industry-agnostic runtime (contracts, events, orgs, etc.)
usecases/         Cross-domain orchestration
blueprints/       Solution Blueprints (academy, etc.)
dhara/            AI compute plane client SDK
infrastructure/   Technical implementations (postgres, redis, queues)
foundation/       Cross-cutting utilities and base types
```

## Development

```bash
uv sync --dev
uv run uvicorn api.main:app --reload
```

## Migrations

```bash
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"
```
