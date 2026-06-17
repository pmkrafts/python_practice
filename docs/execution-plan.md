# Python Backend + AI Agent Coding Practice — Execution Plan

> Derived from [`docs/structure.md`](./structure.md) and [`docs/questions.md`](./questions.md).
> Goal: Build a production-quality monorepo containing 25 machine-coding projects across backend fundamentals, reliability patterns, and AI agent engineering.

---

## 1. Objectives

- Build all **25 practice projects** listed in `questions.md` using modern Python 3.11+.
- Use a **shared, reusable `common/` layer** for base classes, logging, DB, cache, schemas, and agent utilities.
- Maintain **consistent project structure** per project as defined in `structure.md`.
- Include **tests, documentation, Docker support, and CI/CD** for portfolio quality.
- Practice **backend + AI agent engineering** skills interview-ready form.

---

## 2. Repository Setup (Week 0)

| Step | Task | Deliverable |
|------|------|-------------|
| 2.1 | Initialize repository root with README, LICENSE, .gitignore | `README.md`, `LICENSE`, `.gitignore` |
| 2.2 | Set up global Python packaging | `pyproject.toml`, `requirements.txt` |
| 2.3 | Configure GitHub Actions workflows | `.github/workflows/ci.yml`, `.github/workflows/lint-test.yml` |
| 2.4 | Add issue/PR templates | `.github/ISSUE_TEMPLATE/` |
| 2.5 | Add shared scripts | `scripts/setup-env.sh`, `scripts/run-all-tests.sh`, `scripts/lint-all.sh` |
| 2.6 | Add Docker support | `docker/Dockerfile.base`, `docker/docker-compose.yml` |
| 2.7 | Add global environment example | `.env.example` |

### Root Tech Stack

- **Runtime:** Python 3.11+
- **Web framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 + Alembic
- **Cache/Broker:** Redis
- **DB:** PostgreSQL
- **AI/ML:** LangChain / LangGraph, sentence-transformers, FAISS/Chroma
- **Testing:** pytest, httpx, respx
- **Logging:** loguru + OpenTelemetry
- **Config:** pydantic-settings, python-dotenv

---

## 3. Shared `common/` Layer (Week 0–1)

Build the shared utilities **before** starting individual projects so every project can reuse them.

```
common/
├── core/                 # Base classes, custom exceptions, logging, app config
├── utils/                # Generic helpers (datetime, hashing, id generation, etc.)
├── database/             # SQLAlchemy Base, session manager, repository base
├── cache/                # Redis client wrapper, multi-level cache, decorators
├── agents/               # Agent base class, shared tools, memory helpers, prompts
├── schemas/              # Shared Pydantic schemas (pagination, response envelope)
└── tests/                # Shared test fixtures and helpers
```

### Implementation Tasks

1. **core**
   - `exceptions.py`: AppException, NotFoundException, ValidationException, AuthException
   - `logging.py`: Structured JSON logger using loguru
   - `config.py`: Pydantic-settings base config loader

2. **database**
   - `base.py`: SQLAlchemy declarative base, mixin columns (id, created_at, updated_at, deleted_at)
   - `session.py`: Async session manager + dependency
   - `repository.py`: Generic CRUD repository with soft-delete support

3. **cache**
   - `redis_client.py`: Async Redis connection pool
   - `cache.py`: Cache-aside helper + `@cached(ttl=...)` decorator
   - `multi_level_cache.py`: In-memory LRU + Redis fallback

4. **agents**
   - `base_agent.py`: Abstract agent interface
   - `tool.py`: Tool decorator / registry helper
   - `memory.py`: Conversation buffer + vector memory interfaces

5. **schemas**
   - `pagination.py`: Page, PaginatedResponse
   - `envelope.py`: API response envelope

---

## 4. Phase 1: Core Python & Backend Fundamentals (Problems 1–8)

Target: **Weeks 1–3** (≈ 2–3 projects per week)

| # | Project | Key Learning | Must Implement |
|---|---------|--------------|----------------|
| 01 | `01-task-management-api` | FastAPI CRUD, Pydantic v2, pagination/filtering | CRUD endpoints, query params, rate-limit middleware |
| 02 | `02-async-task-queue` | Asyncio + Redis queue, retries, status polling | Worker, task registry, retry/backoff, `/tasks/{id}` status |
| 03 | `03-auth-service` | JWT + RBAC + password hashing | Register/login, access/refresh tokens, role guard |
| 04 | `04-sqlalchemy-repository` | Repository pattern, relationships, soft delete | User/Order repos, complex queries, migrations |
| 05 | `05-redis-caching` | Multi-level cache, TTL, invalidation | Cache-aside, memory+Redis, invalidation API |
| 06 | `06-websocket-chat` | WebSocket rooms, real-time state | Rooms, typing indicator, message persistence |
| 07 | `07-file-processing` | Streaming uploads, background processing | Chunked upload, "virus scan" simulation, async resize/convert |
| 08 | `08-rate-limiter` | Token bucket + sliding window | Middleware, per-user/global limits, Redis backing |

### Per-Project Checklist

- [ ] `src/` with api, core, db, schemas, services, utils
- [ ] `tests/` with unit + integration folders and `conftest.py`
- [ ] `main.py` entrypoint
- [ ] `requirements.txt` or `pyproject.toml`
- [ ] `.env.example`
- [ ] `README.md` (problem statement, run instructions, highlights)
- [ ] `Dockerfile`
- [ ] Reuse `common/` where applicable
- [ ] pytest suite passes

---

## 5. Phase 2: Backend System Design & Reliability (Problems 9–15)

Target: **Weeks 4–6** (≈ 2–3 projects per week)

| # | Project | Key Learning | Must Implement |
|---|---------|--------------|----------------|
| 09 | `09-event-driven-order-service` | Event-driven architecture | Order service, event publisher/consumer, inventory + notification handlers |
| 10 | `10-idempotency-locking` | Distributed locks + idempotency | Redis locks, `Idempotency-Key` header, request-id tracking |
| 11 | `11-batch-processing` | Large-scale batch processing | CSV/JSON ingestion, chunked processing, progress tracking, failure recovery |
| 12 | `12-elasticsearch-search` | Full-text + faceted search | ES index, search endpoint, filters/facets |
| 13 | `13-graphql-layer` | GraphQL over REST | Strawberry/Ariadne schema, resolvers, mutations |
| 14 | `14-observability` | Logging, tracing, metrics | Structured logs, OpenTelemetry traces, `/metrics` Prometheus endpoint |
| 15 | `15-config-management` | Env-specific config + secrets | Config loader, dotenv + vault simulation, validation |

### Integration Notes

- Reuse `common/database` for all DB-backed projects.
- Reuse `common/cache` for Redis-backed projects.
- Use `docker/docker-compose.yml` to spin up Postgres, Redis, Kafka/RabbitMQ, Elasticsearch as needed.

---

## 6. Phase 3: AI Agent Engineer Focus (Problems 16–25)

Target: **Weeks 7–11** (≈ 2 projects per week)

| # | Project | Key Learning | Must Implement |
|---|---------|--------------|----------------|
| 16 | `16-basic-llm-agent` | Tool-calling agent | Agent with calculator, search-sim, weather tools |
| 17 | `17-rag-pipeline` | RAG from scratch | Chunking, embeddings, vector store (FAISS/Chroma), retrieval + generation |
| 18 | `18-multi-agent-orchestrator` | Supervisor routing | Researcher, Writer, Critic agents + supervisor |
| 19 | `19-agent-memory-system` | Short + long-term memory | Conversation buffer, vector memory, graph memory, summarization |
| 20 | `20-autonomous-planner-agent` | ReAct / Plan-and-Execute | Goal decomposition, reasoning loop, execution trace |
| 21 | `21-dynamic-tool-registry` | Runtime tool discovery | Decorator-based registry, dynamic registration, tool metadata |
| 22 | `22-agent-evaluation-harness` | Agent benchmarking | Accuracy, latency, token usage, safety test cases + report |
| 23 | `23-langgraph-workflow` | Stateful graph workflows | Customer support graph: triage → fetch → respond → escalate |
| 24 | `24-agent-fastapi-integration` | Agent as API | FastAPI streaming endpoint, callbacks, session handling |
| 25 | `25-production-ai-agent-service` | Production hardening | Retries, fallback models, cost tracking, HITL, audit logging |

### AI Layer Reuse

- `common/agents/base_agent.py`: shared agent lifecycle
- `common/agents/tool.py`: shared `@tool` registry used by projects 16, 21, 24, 25
- `common/agents/memory.py`: shared memory interfaces used by projects 18, 19, 23
- `common/agents/prompts.py`: reusable prompt templates

---

## 7. Suggested Weekly Schedule

| Week | Focus |
|------|-------|
| 0 | Repo setup, `common/` foundation, CI/CD, Docker |
| 1 | Projects 01, 02 |
| 2 | Projects 03, 04 |
| 3 | Projects 05, 06, 07 |
| 4 | Projects 08, 09 |
| 5 | Projects 10, 11 |
| 6 | Projects 12, 13, 14 |
| 7 | Projects 15, 16 |
| 8 | Projects 17, 18 |
| 9 | Projects 19, 20 |
| 10 | Projects 21, 22 |
| 11 | Projects 23, 24, 25 |
| 12 | Final polish: README table of contents, cross-project integration, portfolio review |

> Adjust pace to 1 project per day for intensive sprints, or 1 project per week for steady progress.

---

## 8. Quality & Evaluation Criteria

For every project, verify against these criteria before marking complete:

1. **Code quality & structure** — consistent layout, type hints, docstrings, separation of concerns.
2. **Edge cases & error handling** — validation, exceptions, retries, timeouts, graceful failures.
3. **Performance & scalability** — async where appropriate, efficient queries, caching, batching.
4. **Test coverage** — unit + integration tests, happy path + failure cases, mocks for external services.
5. **Documentation** — README with problem, run steps, architecture notes, and solution highlights.
6. **Production readiness** — env config, logging, Docker, health checks, observability where applicable.

---

## 9. Reusable Workflow per Project

1. **Read the problem** from `questions.md`.
2. **Create project folder** under the correct phase.
3. **Copy the per-project structure** from `structure.md`.
4. **Wire in `common/` imports** where applicable.
5. **Implement core functionality** (domain → service → API/tests).
6. **Add tests** (unit first, integration second).
7. **Add README + `.env.example` + Dockerfile**.
8. **Run lint + tests** via root scripts.
9. **Update root README** table of contents.

---

## 10. Next Immediate Actions

1. Complete **Step 2 (Repository Setup)** and **Step 3 (`common/` layer)**.
2. Implement **Project 01** end-to-end as the reference template.
3. Use Project 01 as the blueprint for structure and conventions for all subsequent projects.
4. After every phase, run `scripts/run-all-tests.sh` and `scripts/lint-all.sh`.

---

## 11. Copy-Paste Project Prompt

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
