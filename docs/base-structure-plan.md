# Base Structure & Environment Plan

> Simplified foundation for the Python backend + AI agent coding practice repository.  
> Treat this as a **learning sandbox**, not a production monorepo.

---

## 1. Goals

- Keep the repository lightweight and easy to navigate.
- Share only genuinely reusable snippets through a thin `common/` toolbox.
- Let each project own its code, tests, and dependencies.
- Minimize setup friction: one command to install, one command to start infra.

---

## 2. Simplified Repository Structure

```
python-backend-ai-agent-coding-practice/
├── README.md                    # Overview, setup guide, project index
├── LICENSE
├── .gitignore
├── pyproject.toml               # Root dependencies + tool configs
├── requirements.txt             # Fallback flat dependency list
├── .env.example                 # Global env template
│
├── .github/
│   └── workflows/
│       └── ci.yml               # Single workflow: ruff + pytest
│
├── docs/
│   ├── questions.md             # 25 project problem statements
│   ├── execution-plan.md        # Flexible build checklist
│   ├── structure.md             # Quick structure reference
│   └── base-structure-plan.md   # This file
│
├── common/                      # Thin toolbox (~5 small files)
│   ├── __init__.py
│   ├── config.py                # Pydantic-settings loader
│   ├── exceptions.py            # Small exception hierarchy
│   ├── database.py              # SQLAlchemy Base + session helper
│   └── utils.py                 # UTC now, UUID helper, password hash
│
├── projects/                    # All 25 projects live here
│   ├── 01-task-management-api/
│   ├── 02-async-task-queue/
│   ├── 03-auth-service/
│   ├── ...
│   └── 25-production-ai-agent-service/
│
├── scripts/
│   ├── setup.py                 # Cross-platform setup script
│   ├── test_all.py              # Run all project tests
│   └── docker_up.py             # Start Postgres + Redis
│
└── docker/
    └── docker-compose.yml       # Postgres + Redis only
```

### What changed from the previous plan

- `common/` reduced from 7 sub-packages to 5 small files.
- Docker compose reduced from 4 services to 2 (Postgres + Redis).
- CI merged into a single workflow.
- Pre-commit hooks removed.
- Phase directories flattened into a single `projects/` folder.
- Per-project structure lightened (no mandatory `src/`, `alembic/`, or `Dockerfile`).

---

## 3. Simplified `common/` Layer

`common/` is a thin toolbox, not a framework. It contains only code that is genuinely reused by most projects.

| File | Purpose | Approximate Lines |
|------|---------|-------------------|
| `config.py` | `pydantic-settings` base config loader | ~25 |
| `exceptions.py` | `AppException`, `NotFoundException`, `ValidationException` | ~20 |
| `database.py` | SQLAlchemy `Base`, `TimestampMixin`, `get_session()` | ~35 |
| `utils.py` | `utc_now()`, `generate_uuid()`, password hash helpers | ~25 |

### What was removed

- Generic `Repository[T]` — each project writes its own queries.
- Multi-level cache — projects that need caching use `redis` directly.
- Agent base classes, tool registries, memory interfaces, prompt templates — these are learning goals, not pre-built frameworks.
- Response envelopes — return Pydantic models directly from FastAPI.
- `common/tests/conftest.py` — each project keeps its own fixtures.

### Example `common/database.py`

```python
"""Minimal SQLAlchemy base + session helper."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from common.config import settings


class Base(DeclarativeBase):
    type_annotation_map = {str: String(255)}


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
```

---

## 4. Minimal Root Files and Dependencies

### `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "python-backend-ai-agent-coding-practice"
version = "0.1.0"
description = "25 Python machine coding projects"
requires-python = ">=3.11"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "pydantic-settings",
    "sqlalchemy[asyncio]",
    "alembic",
    "asyncpg",
    "redis",
    "httpx",
    "python-dotenv",
    "pytest",
    "pytest-asyncio",
]

[project.optional-dependencies]
dev = [
    "ruff",
    "mypy",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]

[tool.mypy]
python_version = "3.11"
strict = false
warn_unused_ignores = true
exclude = [".venv"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["projects"]
pythonpath = ["common"]
```

### What changed

- Removed `langchain`, `langgraph`, `sentence-transformers`, `faiss-cpu`, `loguru`, `respx`, `pre-commit`, `pytest-cov`, `types-redis` from root deps.
- Projects that need AI/ML libraries add them to their own `requirements.txt` or `pyproject.toml`.
- `mypy` strict mode disabled to reduce practice friction.
- No `pre-commit` hooks at the root.

---

## 5. Simplified Docker Setup

### `docker/docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:16
    container_name: practice-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: practice
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: practice-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### What changed

- Removed Kafka and Elasticsearch from the default stack.
- Projects that need them can add a local `docker-compose.override.yml`.
- No `Dockerfile.base` — each project that needs Docker writes its own simple `Dockerfile`.

---

## 6. Simplified CI/CD

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - run: uv sync --all-extras

      - name: Lint
        run: uv run ruff check .

      - name: Test
        run: uv run pytest projects/
```

### What changed

- Single workflow only.
- No Postgres/Redis service containers in CI — tests use SQLite or mocked services.
- No Codecov upload.
- No separate `lint-test.yml`.

---

## 7. Per-Project Structure

Each project is self-contained. No mandatory `src/`, `alembic/`, or `Dockerfile`.

```
projects/01-task-management-api/
├── main.py                # FastAPI app entry point
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic request/response models
├── router.py              # API routes
├── service.py             # Business logic
├── database.py            # Project-specific DB setup (if needed)
├── tests/
│   ├── conftest.py        # Fixtures
│   └── test_*.py
├── requirements.txt       # Optional: project-specific deps
├── .env.example           # Optional: project-specific env vars
└── README.md              # Problem statement + how to run
```

### Guidelines

- Import from `common` only when it genuinely saves time (e.g., `from common.database import Base, get_session`).
- Otherwise, write the code inside the project — the goal is practice, not DRY perfection.
- `main.py` should be runnable directly: `uvicorn main:app --reload`.
- Keep tests in a `tests/` folder with a local `conftest.py`.

---

## 8. Cross-Platform Scripts

Replace bash scripts with Python scripts so they work on Windows, macOS, and Linux without modification.

### `scripts/setup.py`

```python
"""Set up the development environment."""

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("$ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    repo_root = Path(__file__).parent.parent
    if not (repo_root / ".venv").exists():
        run([sys.executable, "-m", "venv", str(repo_root / ".venv")])

    pip = repo_root / ".venv" / "Scripts" / "pip.exe"
    if not pip.exists():
        pip = repo_root / ".venv" / "bin" / "pip"

    run([str(pip), "install", "--upgrade", "pip"])
    run([str(pip), "install", "-r", str(repo_root / "requirements.txt")])

    if not (repo_root / ".env").exists() and (repo_root / ".env.example").exists():
        (repo_root / ".env").write_text((repo_root / ".env.example").read_text())

    print("✅ Setup complete")


if __name__ == "__main__":
    main()
```

### `scripts/docker_up.py`

```python
"""Start shared infrastructure (Postgres + Redis)."""

import subprocess
from pathlib import Path


def main() -> None:
    compose_file = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
    subprocess.run(
        ["docker-compose", "-f", str(compose_file), "up", "-d"],
        check=True,
    )
    print("✅ Postgres and Redis started")


if __name__ == "__main__":
    main()
```

### `scripts/test_all.py`

```python
"""Run tests for all projects."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    projects_dir = Path(__file__).parent.parent / "projects"
    test_dirs = [str(d) for d in projects_dir.iterdir() if d.is_dir()]
    if not test_dirs:
        print("No projects found")
        return

    subprocess.run([sys.executable, "-m", "pytest", *test_dirs, "-v"], check=True)


if __name__ == "__main__":
    main()
```

---

## 9. Setup Checklist

- [ ] Create root files: `README.md`, `LICENSE`, `.gitignore`, `pyproject.toml`, `.env.example`
- [ ] Create `.github/workflows/ci.yml`
- [ ] Create `common/` with `config.py`, `exceptions.py`, `database.py`, `utils.py`
- [ ] Create `docker/docker-compose.yml` (Postgres + Redis)
- [ ] Add `scripts/setup.py`, `scripts/docker_up.py`, `scripts/test_all.py`
- [ ] Create `projects/` folder and add `01-task-management-api/`
- [ ] Install dependencies: `pip install -r requirements.txt` or `uv sync --all-extras`
- [ ] Run `ruff check .` and `pytest` to verify
- [ ] Commit and push to `main`

---

## 10. Conventions

### Naming

- Directories: lowercase with hyphens (`task-management-api`)
- Python modules: lowercase with underscores (`task_service.py`)
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`

### Imports

```python
# Standard library
import asyncio
from typing import List

# Third-party
from fastapi import FastAPI
from sqlalchemy import select

# Local / common
from common.database import Base
```

### Async-First

- Use `async`/`await` for I/O-bound operations.
- Use SQLAlchemy 2.0 async API.
- Use `httpx.AsyncClient` for HTTP calls.

### Error Handling

- Raise `common.exceptions.AppException` subclasses from services.
- Map exceptions to HTTP responses via FastAPI exception handlers.
- Do not leak internal stack traces to API clients.

### Testing

- One `conftest.py` per project.
- Mock external services (LLMs, Redis, SMTP).
- Aim for meaningful tests on business logic; coverage percentage is secondary in a practice repo.

---

## 11. Next Steps

1. Implement this simplified base structure.
2. Build **Project 01 (Task Management API)** first to validate the structure.
3. Refine `common/` utilities only when a second project genuinely needs the same code.
4. Use Project 01 as the blueprint for conventions across all 25 projects.
