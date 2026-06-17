# Python Backend + AI Agent Coding Practice

A collection of 25 machine-coding projects designed to practice Backend Engineering and AI Agent Engineering skills using modern Python 3.11+.

## Overview

This repository is organized into three phases:

- **Phase 1: Core Python & Backend Fundamentals** (Projects 1–8)
- **Phase 2: Backend System Design & Reliability** (Projects 9–15)
- **Phase 3: AI Agent Engineer Focus** (Projects 16–25)

Each project is self-contained and lives under `projects/`. A thin `common/` toolbox holds only the snippets that are genuinely reused across most projects.

## Quick Start

```bash
# 1. Set up the environment
python scripts/setup.py

# 2. Start shared infrastructure (Postgres + Redis)
python scripts/docker_up.py

# 3. Run all project tests
python scripts/test_all.py

# 4. Run linting
ruff check .
```

## Repository Structure

```
python-backend-ai-agent-coding-practice/
├── common/                  # Thin toolbox (~4 small files)
├── docs/                    # Plans, structure, and problem statements
├── projects/                # All 25 projects
│   ├── 01-task-management-api/
│   ├── 02-async-task-queue/
│   └── ...
├── scripts/                 # Cross-platform Python scripts
├── docker/                  # Postgres + Redis docker-compose
└── .github/                 # CI/CD workflows
```

## Documentation

- [`docs/usage.md`](./docs/usage.md) — How to use the repo, create projects, run, and test
- [`docs/execution-plan.md`](./docs/execution-plan.md) — Flexible build checklist
- [`docs/base-structure-plan.md`](./docs/base-structure-plan.md) — Base structure and environment details
- [`docs/structure.md`](./docs/structure.md) — Quick structure reference
- [`docs/questions.md`](./docs/questions.md) — 25 project problem statements

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis
- **AI Agents:** LangChain, LangGraph, sentence-transformers, FAISS/Chroma (per-project)
- **Testing:** pytest, pytest-asyncio, httpx
- **Tooling:** ruff, optional mypy
- **DevOps:** Docker, docker-compose, GitHub Actions

## Project Index

| # | Project | Phase |
|---|---------|-------|
| 01 | Task Management API | Phase 1 |
| 02 | Async Task Queue | Phase 1 |
| 03 | Authentication & Authorization | Phase 1 |
| 04 | SQLAlchemy Repository Pattern | Phase 1 |
| 05 | Redis Caching Layer | Phase 1 |
| 06 | WebSocket Real-time Chat | Phase 1 |
| 07 | File Upload & Processing | Phase 1 |
| 08 | Rate Limiter & API Gateway | Phase 1 |
| 09 | Event-Driven Order Service | Phase 2 |
| 10 | Distributed Locking & Idempotency | Phase 2 |
| 11 | Batch Processing Pipeline | Phase 2 |
| 12 | Search Service with Elasticsearch | Phase 2 |
| 13 | GraphQL API Layer | Phase 2 |
| 14 | Observability & Logging | Phase 2 |
| 15 | CI/CD Simulation + Config Management | Phase 2 |
| 16 | Basic LLM Tool-Calling Agent | Phase 3 |
| 17 | RAG Pipeline from Scratch | Phase 3 |
| 18 | Multi-Agent Orchestrator | Phase 3 |
| 19 | Agent Memory System | Phase 3 |
| 20 | Autonomous Planner Agent | Phase 3 |
| 21 | Dynamic Tool Registry | Phase 3 |
| 22 | Agent Evaluation Harness | Phase 3 |
| 23 | LangGraph Stateful Workflow | Phase 3 |
| 24 | AI Agent + Backend Integration | Phase 3 |
| 25 | Production-Grade AI Agent Service | Phase 3 |

## License

[MIT](./LICENSE)
