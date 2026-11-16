# Algorithmic Trading Simulator Backend

Starter folder structure for a FastAPI-based stock and cryptocurrency trading simulator.
The Python modules are intentionally scaffolds: each contains only a one-line comment
describing its intended responsibility.

## Planned stack
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Pydantic v2
- JWT authentication
- httpx for market-data requests
- pytest for testing

## Getting started

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure the values.
4. Create the PostgreSQL database named `trading_simulator` (or update `DATABASE_URL`).
5. Implement the database setup and application entry point.
6. Start the development server once `src/main.py` is implemented:
   `uvicorn src.main:app --reload`

## Architecture

- `src/core/`: settings, database connection, and security utilities
- `src/models/`: SQLAlchemy entities
- `src/schemas/`: Pydantic validation and serialization
- `src/services/`: business logic
- `src/api/`: FastAPI endpoints
- `tests/`: automated tests
- `alembic/`: database migration configuration and revisions

## Important
This repository is a structural scaffold, not a working application yet.
Add implementation, migrations, tests, and real environment configuration as the team develops it.
