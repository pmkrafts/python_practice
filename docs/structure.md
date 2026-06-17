# Repository Structure Reference

> Quick reference for the simplified project layout.  
> For full setup details, see [`base-structure-plan.md`](./base-structure-plan.md).

```
python-backend-ai-agent-coding-practice/
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── .env.example
│
├── .github/
│   └── workflows/
│       └── ci.yml               # ruff + pytest
│
├── docs/
│   ├── questions.md             # 25 project problem statements
│   ├── execution-plan.md        # Flexible build checklist
│   ├── structure.md             # This file
│   └── base-structure-plan.md   # Base structure + environment details
│
├── common/                      # Thin toolbox
│   ├── config.py
│   ├── exceptions.py
│   ├── database.py
│   └── utils.py
│
├── projects/                    # All 25 projects
│   ├── 01-task-management-api/
│   ├── 02-async-task-queue/
│   ├── ...
│   └── 25-production-ai-agent-service/
│
├── scripts/
│   ├── setup.py                 # Cross-platform env setup
│   ├── docker_up.py             # Start Postgres + Redis
│   └── test_all.py              # Run all project tests
│
└── docker/
    └── docker-compose.yml       # Postgres + Redis
```

## Per-Project Structure

```
projects/01-task-management-api/
├── main.py
├── models.py
├── schemas.py
├── router.py
├── service.py
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── requirements.txt       # optional
├── .env.example           # optional
└── README.md
```

## Conventions

- **Naming:** lowercase-hyphen directories, `snake_case` modules, `PascalCase` classes.
- **Async-first:** use `async`/`await` for I/O.
- **Import order:** stdlib → third-party → local/common.
- **Error handling:** raise `common.exceptions` subclasses; map to FastAPI handlers.
- **Testing:** one `conftest.py` per project; mock external services.

## Notes

- `common/` is intentionally small. Each project should own its agents, repositories, caches, and schemas where the learning happens.
- Kafka and Elasticsearch are not started by default. Projects that need them can provide a local `docker-compose.override.yml`.
- No mandatory `src/`, `alembic/`, or per-project `Dockerfile`.
