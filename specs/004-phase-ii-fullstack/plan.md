# Implementation Plan: Phase II Full-Stack Todo Application

**Branch**: `004-phase-ii-fullstack` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-phase-ii-fullstack/spec.md`

## Summary

Build a production-quality full-stack Todo web application with user authentication, persistent storage, and comprehensive task management features. The application consists of a Python/FastAPI REST backend with Neon PostgreSQL database and a Next.js/React/TypeScript frontend. Features include basic CRUD operations, priorities, tags, search/filter/sort, due dates with reminders, and recurring tasks.

## Technical Context

**Language/Version**: Python 3.13+ (Backend), TypeScript 5.x (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, python-jose, passlib, Next.js 14+, React 18+, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (Backend), Jest/Vitest + React Testing Library (Frontend)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 years)
**Project Type**: Web application (separate frontend + backend)
**Performance Goals**: <500ms search response, <3s initial load, 100 concurrent users
**Constraints**: No WebSockets, no background jobs, no AI features, browser notifications only
**Scale/Scope**: Single-tenant multi-user, ~100 concurrent users, 3 main pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Spec-Driven Development | All features defined in spec.md | PASS |
| II. Clean Architecture | Domain → Service → API/Frontend layers | PASS |
| III. Correctness Over Optimization | Educational priority, no premature optimization | PASS |
| IV. Graceful User Interface | Modern, responsive, animated UI specified | PASS |
| V. Code Quality | Python PEP 8, TypeScript strict mode | PASS |
| VI. Verification & Testing | Contract tests + integration tests required | PASS |
| VII. Web Architecture | REST API, separate frontend/backend | PASS |
| VIII. Authentication & Security | JWT (python-jose + passlib), user-scoped data | PASS |

**Constitution Version**: 3.1.0 (amended to use JWT authentication instead of Better Auth)

## Project Structure

### Documentation (this feature)

```text
specs/004-phase-ii-fullstack/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
│   └── openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLModel entities (User, Todo, Tag)
│   ├── services/        # Business logic (TodoService, AuthService)
│   ├── api/             # FastAPI routes and middleware
│   │   ├── routes/      # Endpoint handlers
│   │   ├── middleware/  # Auth middleware, error handling
│   │   └── deps/        # Dependency injection
│   └── core/            # Configuration, database connection
├── tests/
│   ├── contract/        # API contract tests
│   ├── integration/     # End-to-end API tests
│   └── unit/            # Service layer tests
├── alembic/             # Database migrations
├── pyproject.toml
└── .env.example

frontend/
├── src/
│   ├── app/             # Next.js App Router pages
│   │   ├── (auth)/      # Signup, Signin pages
│   │   └── dashboard/   # Main todo dashboard
│   ├── components/      # React components
│   │   ├── ui/          # Base UI components (Button, Input, etc.)
│   │   ├── todo/        # Todo-specific components
│   │   └── layout/      # Layout components (Header, Sidebar)
│   ├── lib/             # Utilities, API client, auth helpers
│   ├── hooks/           # Custom React hooks
│   └── types/           # TypeScript type definitions
├── tests/
│   ├── components/      # Component unit tests
│   └── e2e/             # End-to-end tests (optional)
├── package.json
├── tailwind.config.ts
└── .env.local.example
```

**Structure Decision**: Web application structure selected per constitution Principle II (Clean Architecture) and Principle VII (Web Architecture). Backend and frontend are separate, independently deployable applications communicating via REST API.

## Complexity Tracking

> No constitution violations requiring justification.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Two projects (backend + frontend) | Required by constitution | Principle VII mandates separate, independently deployable applications |
| SQLModel ORM | Constitution-specified | Simpler than raw SQLAlchemy, Pydantic integration |
| JWT + passlib | Constitution-specified | Custom auth with bcrypt password hashing |
| Tailwind CSS | Recommended in constitution | Modern, utility-first CSS framework |

## Generated Artifacts

### Phase 0: Research

- [research.md](./research.md) - Technology stack decisions and best practices

### Phase 1: Design & Contracts

- [data-model.md](./data-model.md) - Database entities, relationships, validation rules
- [contracts/openapi.yaml](./contracts/openapi.yaml) - OpenAPI 3.1 specification for REST API
- [quickstart.md](./quickstart.md) - Local development setup guide

## API Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/signup` | POST | Create new user account |
| `/auth/signin` | POST | Authenticate user |
| `/auth/signout` | POST | End user session |
| `/auth/me` | GET | Get current user profile |
| `/todos` | GET | List todos (with filters, search, sort) |
| `/todos` | POST | Create new todo |
| `/todos/{id}` | GET | Get specific todo |
| `/todos/{id}` | PATCH | Update todo |
| `/todos/{id}` | DELETE | Delete todo |
| `/todos/{id}/complete` | POST | Mark complete (triggers recurrence) |
| `/todos/{id}/incomplete` | POST | Mark incomplete |
| `/tags` | GET | List user's tags |
| `/tags` | POST | Create new tag |
| `/tags/{id}` | DELETE | Delete tag |

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | FastAPI | Async, OpenAPI docs, Pydantic integration |
| ORM | SQLModel | Constitution-specified, simpler than raw SQLAlchemy |
| Auth | JWT (python-jose + passlib) | Custom auth, better FastAPI integration |
| Frontend | Next.js App Router | Modern, SSR-capable, React Server Components |
| Styling | Tailwind + shadcn/ui | Rapid development, consistent design |
| Recurring tasks | Generate on completion | No background jobs required |
| Reminders | Client-side scheduling | Browser Notifications API, no push server |
| API versioning | URL path `/api/v1/` | Simple, explicit versioning strategy |

## Next Steps

Run `/sp.tasks` to generate the implementation task list based on this plan and the feature specification.
