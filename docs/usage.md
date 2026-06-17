# Usage Guide

This guide explains how to set up the repository, create a new project, run it, and test it.

For the list of 25 practice problems, see [`docs/questions.md`](./questions.md).  
For the overall build plan, see [`docs/execution-plan.md`](./execution-plan.md).  
For base structure details, see [`docs/base-structure-plan.md`](./base-structure-plan.md).

---

## Overview

This repository is a **learning sandbox** for 25 machine-coding projects covering Backend Engineering and AI Agent Engineering with Python 3.11+.

- Each project lives under `projects/` and is **self-contained**.
- A thin `common/` toolbox holds genuinely reusable snippets (config, DB base/session, exceptions, small utilities).
- The default infrastructure is only **Postgres + Redis**. Kafka and Elasticsearch are added per-project when needed.

---

## Quick Start

```bash
# 1. Clone the repo (if you haven't already)
git clone https://github.com/pmkrafts/python_practice.git
cd python_practice

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Postgres + Redis
python scripts/docker_up.py

# 5. Create or open a project, then run it
cd projects/01-task-management-api
uvicorn main:app --reload
```

For the automated setup path, see [Environment Setup](#environment-setup) below.

---

## Creating a Virtual Environment

A virtual environment keeps the repo's dependencies isolated from your global Python installation. **This repo uses one `.venv` folder at the repository root, shared by all projects** — not a separate venv per project.

Why one root venv?

- The root `pyproject.toml` / `requirements.txt` contains shared dependencies (FastAPI, SQLAlchemy, Redis, pytest, etc.).
- All projects under `projects/` import from the same root venv.
- If a project needs extra packages (e.g., `langchain` for an AI project), install them into the same root venv or add them to the project's own `requirements.txt`.

### Manual creation

```bash
# Create the virtual environment
python -m venv .venv
```

### Activate the virtual environment

```bash
# Windows (Command Prompt / PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Once activated, your terminal prompt will usually show `(.venv)`.

### Deactivate

```bash
deactivate
```

### Using the setup script

You can also let `scripts/setup.py` create the virtual environment for you:

```bash
python scripts/setup.py
```

After it runs, activate the environment as shown above.

---

## Environment Setup

Use the cross-platform setup script:

```bash
python scripts/setup.py
```

This script:

1. Creates a `.venv` virtual environment if it doesn't exist.
2. Upgrades `pip`.
3. Installs dependencies from `requirements.txt`.
4. Copies `.env.example` to `.env` if `.env` doesn't exist.

Then activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### Alternative: uv

If you use [uv](https://docs.astral.sh/uv/):

```bash
uv sync --all-extras
```

---

## Starting Infrastructure

Start the shared services with:

```bash
python scripts/docker_up.py
```

This starts:

- **PostgreSQL** on `localhost:5432`
  - user: `postgres`
  - password: `postgres`
  - database: `practice`
- **Redis** on `localhost:6379`

To stop:

```bash
cd docker
docker-compose down
```

> **Note:** Kafka and Elasticsearch are **not** started by default. Projects that need them can provide a local `docker-compose.override.yml`.

---

## How to Create a New Project

1. Create a folder under `projects/` with a two-digit prefix and descriptive name:

   ```bash
   mkdir projects/01-task-management-api
   ```

2. Add the recommended files:

   ```
   projects/01-task-management-api/
   ├── main.py                # FastAPI app entry point
   ├── models.py              # SQLAlchemy models
   ├── schemas.py             # Pydantic request/response models
   ├── router.py              # API routes
   ├── service.py             # Business logic
   ├── tests/
   │   ├── conftest.py        # Fixtures
   │   └── test_tasks.py
   ├── requirements.txt       # Optional: project-specific deps
   ├── .env.example           # Optional: project-specific env vars
   └── README.md              # Problem statement + how to run
   ```

3. Import from `common/` only when it saves time:

   ```python
   from common.database import Base, get_session
   from common.exceptions import NotFoundException
   from common.utils import generate_uuid, utc_now
   ```

   Otherwise, write the code inside the project — the goal is practice, not DRY perfection.

### Minimal starter example

`main.py`:

```python
from fastapi import FastAPI

from router import router

app = FastAPI(title="Task Management API")
app.include_router(router, prefix="/tasks", tags=["tasks"])
```

`models.py`:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from common.database import Base, TimestampMixin


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String(50), default="todo")
```

`schemas.py`:

```python
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskOut(BaseModel):
    id: str
    title: str
    description: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)
```

`router.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_session
from common.exceptions import NotFoundException
from schemas import TaskCreate, TaskOut
from service import TaskService

router = APIRouter()


@router.post("", response_model=TaskOut)
async def create_task(
    payload: TaskCreate,
    session: AsyncSession = Depends(get_session),
):
    return await TaskService(session).create(payload)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: str,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await TaskService(session).get(task_id)
    except NotFoundException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
```

`service.py`:

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions import NotFoundException
from common.utils import generate_uuid, utc_now
from models import Task
from schemas import TaskCreate


class TaskService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, payload: TaskCreate) -> Task:
        task = Task(
            id=generate_uuid(),
            title=payload.title,
            description=payload.description,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: str) -> Task:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise NotFoundException(f"Task {task_id} not found")
        return task
```

`tests/test_tasks.py`:

```python
import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"
```

---

## How to Run a Project

From inside the project directory:

```bash
cd projects/01-task-management-api
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

You can also explore the interactive docs at `http://localhost:8000/docs`.

---

## How to Test

### Run all project tests

```bash
python scripts/test_all.py
```

This discovers all projects under `projects/` that contain a `tests/` folder and runs `pytest` across them.

### Run a single project

```bash
pytest projects/01-task-management-api -v
```

### Lint

```bash
ruff check .
```

### Format

```bash
ruff format .
```

---

## Using `common/` Helpers

| File | What it provides | Example import |
|------|------------------|----------------|
| `common/config.py` | `settings` object loaded from `.env` | `from common.config import settings` |
| `common/database.py` | `Base`, `TimestampMixin`, `get_session()` | `from common.database import Base, get_session` |
| `common/exceptions.py` | `AppException`, `NotFoundException`, `ValidationException`, `AuthException`, `ConflictException` | `from common.exceptions import NotFoundException` |
| `common/utils.py` | `utc_now()`, `to_iso()`, `generate_uuid()`, `hash_password()`, `verify_password()` | `from common.utils import generate_uuid, hash_password` |

---

## Conventions

- **Naming:**
  - Directories: lowercase with hyphens (`task-management-api`)
  - Modules: lowercase with underscores (`task_service.py`)
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `SCREAMING_SNAKE_CASE`

- **Imports:**
  1. Standard library
  2. Third-party packages
  3. Local / `common`

- **Async-first:**
  - Use `async`/`await` for I/O-bound operations.
  - Use SQLAlchemy 2.0 async API.
  - Use `httpx.AsyncClient` for HTTP calls.

- **Error handling:**
  - Raise `common.exceptions` subclasses from services.
  - Map exceptions to HTTP responses via FastAPI exception handlers.
  - Don't leak internal stack traces to API clients.

- **Testing:**
  - Keep one `conftest.py` per project.
  - Mock external services (LLMs, Redis, SMTP).
  - Focus on meaningful business-logic tests; coverage percentage is secondary.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'common'`

Make sure the virtual environment is activated and dependencies are installed:

```bash
python scripts/setup.py
.venv\Scripts\activate        # Windows
# or
source .venv/bin/activate     # macOS / Linux
```

### `Connection refused` to Postgres or Redis

Start the infrastructure:

```bash
python scripts/docker_up.py
```

Check that Docker Desktop is running and ports `5432` and `6379` are free.

### `uvicorn: command not found`

Install dependencies or activate the virtual environment:

```bash
.venv\Scripts\python -m uvicorn main:app --reload   # Windows
.venv/bin/python -m uvicorn main:app --reload       # macOS / Linux
```

### Missing AI/ML library (e.g., `langchain`, `sentence-transformers`)

Root dependencies are intentionally minimal. Add project-specific packages to the project's own `requirements.txt` or `pyproject.toml` and install them.

---

## Next Steps

1. Pick a project from [`docs/questions.md`](./questions.md).
2. Create it under `projects/` following the layout above.
3. Build it end-to-end, then add tests.
4. Run `ruff check .` and `pytest projects/XX-name` before moving on.

Happy coding!
