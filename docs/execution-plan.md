# Python Backend + AI Agent Coding Practice — Execution Plan

> Derived from [`docs/structure.md`](./structure.md) and [`docs/questions.md`](./questions.md).  
> Goal: Build 25 machine-coding projects across backend fundamentals, reliability patterns, and AI agent engineering.

---

## 1. Objectives

- Build all **25 practice projects** listed in `questions.md` using modern Python 3.11+.
- Keep the shared `common/` layer **thin** — only genuinely reusable snippets.
- Let each project own its structure, tests, and project-specific dependencies.
- Maintain lightweight CI/CD, Docker, and tooling that does not get in the way of learning.

---

## 2. Repository Setup

Complete these once before starting projects.

| Step | Task | Deliverable |
|------|------|-------------|
| 2.1 | Initialize repository root | `README.md`, `LICENSE`, `.gitignore` |
| 2.2 | Set up Python packaging | `pyproject.toml`, `requirements.txt` |
| 2.3 | Add CI workflow | `.github/workflows/ci.yml` |
| 2.4 | Create thin `common/` layer | `common/config.py`, `exceptions.py`, `database.py`, `utils.py` |
| 2.5 | Add cross-platform scripts | `scripts/setup.py`, `scripts/docker_up.py`, `scripts/test_all.py` |
| 2.6 | Add Docker support | `docker/docker-compose.yml` (Postgres + Redis) |
| 2.7 | Add global env template | `.env.example` |

### Root Tech Stack

- **Runtime:** Python 3.11+
- **Web framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 + Alembic (when migrations are needed)
- **Cache:** Redis
- **DB:** PostgreSQL
- **Testing:** pytest, pytest-asyncio, httpx
- **Config:** pydantic-settings, python-dotenv
- **Linting:** ruff, optional mypy

AI/ML libraries (`langchain`, `langgraph`, `sentence-transformers`, etc.) are added per-project, not in root.

---

## 3. Shared `common/` Layer

Build only the essentials before Project 01. Expand later only when a second project genuinely needs the same code.

```
common/
├── config.py                # Pydantic-settings loader
├── exceptions.py            # AppException, NotFoundException, ValidationException
├── database.py              # SQLAlchemy Base, TimestampMixin, get_session()
└── utils.py                 # utc_now, generate_uuid, password hashing
```

### Implementation Tasks

1. **config.py**
   - `Settings` class with `database_url`, `redis_url`, `secret_key`, `debug`.

2. **exceptions.py**
   - `AppException`, `NotFoundException`, `ValidationException`, `AuthException`.

3. **database.py**
   - `Base`, `TimestampMixin`, `get_session()` async context manager.

4. **utils.py**
   - `utc_now()`, `generate_uuid()`, `hash_password()`, `verify_password()`.

---

## 4. Project List

### Phase 1: Core Python & Backend Fundamentals (Problems 1–8)

| # | Project | Key Learning |
|---|---------|--------------|
| 01 | `01-task-management-api` | FastAPI CRUD, Pydantic v2, pagination/filtering |
| 02 | `02-async-task-queue` | Asyncio + Redis queue, retries, status polling |
| 03 | `03-auth-service` | JWT + RBAC + password hashing |
| 04 | `04-sqlalchemy-repository` | Repository pattern, relationships, soft delete |
| 05 | `05-redis-caching` | Multi-level cache, TTL, invalidation |
| 06 | `06-websocket-chat` | WebSocket rooms, real-time state |
| 07 | `07-file-processing` | Streaming uploads, background processing |
| 08 | `08-rate-limiter` | Token bucket + sliding window |

### Phase 2: Backend System Design & Reliability (Problems 9–15)

| # | Project | Key Learning |
|---|---------|--------------|
| 09 | `09-event-driven-order-service` | Event-driven architecture |
| 10 | `10-idempotency-locking` | Distributed locks + idempotency |
| 11 | `11-batch-processing` | Large-scale batch processing |
| 12 | `12-elasticsearch-search` | Full-text + faceted search |
| 13 | `13-graphql-layer` | GraphQL over REST |
| 14 | `14-observability` | Logging, tracing, metrics |
| 15 | `15-config-management` | Env-specific config + secrets |

### Phase 3: AI Agent Engineer Focus (Problems 16–25)

| # | Project | Key Learning |
|---|---------|--------------|
| 16 | `16-basic-llm-agent` | Tool-calling agent |
| 17 | `17-rag-pipeline` | RAG from scratch |
| 18 | `18-multi-agent-orchestrator` | Supervisor routing |
| 19 | `19-agent-memory-system` | Short + long-term memory |
| 20 | `20-autonomous-planner-agent` | ReAct / Plan-and-Execute |
| 21 | `21-dynamic-tool-registry` | Runtime tool discovery |
| 22 | `22-agent-evaluation-harness` | Agent benchmarking |
| 23 | `23-langgraph-workflow` | Stateful graph workflows |
| 24 | `24-agent-fastapi-integration` | Agent as API |
| 25 | `25-production-ai-agent-service` | Production hardening |

---

## 5. Flexible Schedule

Work through projects at your own pace. Use this as a rough guide, not a rigid deadline.

| Pace | Suggested cadence |
|------|-------------------|
| Intensive | 1 project per day |
| Steady | 1–2 projects per week |
| Relaxed | 1 project per week |

### Suggested order

1. Set up the base structure.
2. Build **Project 01** end-to-end as the reference template.
3. Use Project 01 to establish conventions for all later projects.
4. Progress through phases in order, but feel free to skip or revisit projects based on your goals.

---

## 6. Quality & Evaluation Criteria

For every project, verify against these criteria before marking complete:

1. **Code quality & structure** — consistent layout, type hints, docstrings, separation of concerns.
2. **Edge cases & error handling** — validation, exceptions, retries, timeouts, graceful failures.
3. **Performance & scalability** — async where appropriate, efficient queries, caching, batching.
4. **Test coverage** — unit + integration tests, happy path + failure cases, mocks for external services.
5. **Documentation** — README with problem, run steps, architecture notes, and solution highlights.
6. **Production readiness** — env config, logging, Docker, health checks, observability where applicable.

---

## 7. Reusable Workflow per Project

1. **Read the problem** from `questions.md`.
2. **Create project folder** under `projects/`.
3. **Add project files**: `main.py`, `models.py`, `schemas.py`, `router.py`, `service.py`, `tests/`, `README.md`.
4. **Import from `common/` only when it genuinely saves time** (e.g., `Base`, `get_session`, `AppException`).
5. **Implement core functionality** (domain → service → API/tests).
6. **Add tests** (unit first, integration second).
7. **Run lint + tests**: `ruff check .` and `pytest projects/XX-project-name`.
8. **Update root README** project index.

---

## 8. Next Immediate Actions

1. Complete the base repository setup.
2. Build the thin `common/` layer.
3. Implement **Project 01** end-to-end as the reference template.
4. Use Project 01 to validate and refine conventions before continuing.

---

## 9. Copy-Paste Project Prompt

When asking an LLM to generate a starter for any project, use:

```
You are an expert Python interviewer for Backend + AI Agent Engineer roles. Generate a complete machine coding problem for: [Problem Title].

Include:
- Clear requirements
- Input/Output format
- Edge cases
- Expected deliverables (models, endpoints, classes, etc.)
- Bonus points for production readiness

Use modern Python 3.11+ best practices.
```
