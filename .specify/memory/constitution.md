<!--
  Sync Impact Report
  ==================
  Version change: 3.0.0 → 3.1.0 (MINOR: Authentication approach clarified)

  Modified principles:
    - VIII. Authentication & Security → Changed from "Better Auth" to "JWT with python-jose + passlib"

  Modified sections:
    - "Technical Stack / Phase II" → Updated Authentication row to JWT
    - "User Entity (Phase II)" → Added hashed_password field, removed Better Auth reference
    - Styling → Changed from "TBD" to "Tailwind CSS"

  Added sections:
    - None

  Removed sections: None

  Templates requiring updates:
    - None (templates are generic)

  Follow-up TODOs:
    - Update plan.md to align with JWT auth approach ✅

  Amendment Notes (3.1.0):
    - MINOR change: Clarified authentication implementation
    - Changed from Better Auth SDK to custom JWT (python-jose + passlib)
    - Rationale: Custom JWT provides better FastAPI integration and avoids third-party SDK dependency
    - User entity now explicitly includes hashed_password field
    - This aligns constitution with actual implemented code

  Previous Amendment Notes (3.0.0):
    - MAJOR change: Phase II scope significantly expanded
    - Recurring tasks moved from Phase III to Phase II
    - Due dates with reminders moved from Phase III to Phase II
    - Browser notifications for reminders added to Phase II scope
    - Phase III now focuses solely on AI-powered intelligent features
-->

# The Evolution of Todo Constitution

## Project Vision

This project is designed to teach students how professional software systems evolve incrementally. Each phase builds on a stable foundation while preserving clean architecture, clarity, and maintainability.

AI is used not as a shortcut, but as a disciplined engineering tool that follows specifications, plans, and constraints.

### Phase Summary

| Phase | Level | Description | Status |
|-------|-------|-------------|--------|
| Phase I | Basic | In-memory CLI application | Completed |
| Phase II | Intermediate | Full-stack web application | Current |
| Phase III | Advanced | Intelligent features | Future |

### Current Phase

**Phase II — Intermediate Level** (Full-stack Web Application)

### Phase Isolation Rules

- Each phase MUST have a complete, stable implementation before the next phase begins
- Phase-specific code MUST NOT introduce regressions to prior phase functionality
- Features from future phases MUST NOT be implemented until explicitly specified
- When transitioning phases, the previous phase codebase serves as the stable foundation
- Phase II does NOT extend Phase I code; it is a new implementation following the same domain model

## AI Role Definition

Claude Code MUST act as a senior-level software engineer and product architect.

The AI MUST:
- Follow this constitution as the highest authority
- Implement only what is explicitly defined in approved specifications
- Never assume future features prematurely
- Ask for clarification when requirements are ambiguous
- Optimize for clarity, correctness, and extensibility
- Respect phase boundaries and isolation rules

## Core Principles

### I. Spec-Driven Development

Specifications are the single source of truth for all implementation work.

- Every feature MUST be defined in a separate, versioned specification before implementation begins
- Code MUST be reproducible solely from specifications
- Claude Code MUST refuse to write code that is not explicitly defined in a specification
- When requirements are ambiguous, Claude Code MUST request clarification before proceeding
- All changes MUST trace back to an approved specification
- Earlier phases MUST remain stable when later phases are added

**Rationale**: Spec-driven development ensures predictability, traceability, and prevents scope creep. It forces explicit decision-making upfront.

### II. Clean Architecture

The codebase MUST maintain strict separation of concerns to support future evolution.

**Phase I Layers (CLI)**:
- **Domain Layer (Models)**: Define data structures and domain rules (Todo entity)
- **Service Layer (Business Logic)**: Implement operations on domain models
- **Interface Layer (CLI)**: Handle user input/output, validation, and presentation

**Phase II Layers (Web Application)**:
- **Domain Layer (Models)**: Define data structures with SQLModel (User, Todo entities)
- **Service Layer (Business Logic)**: Implement operations on domain models
- **API Layer (REST)**: Handle HTTP requests, validation, and response formatting
- **Frontend Layer (Next.js)**: Handle user interface, state management, and API communication

Architectural constraints:
- Avoid monolithic functions
- Design for future evolution into distributed systems
- Each layer MUST be independently testable
- Dependencies flow inward (Interface → Services → Domain)

**Rationale**: Clean separation enables incremental evolution from a CLI app to web APIs, databases, and distributed systems without rewriting core logic.

### III. Correctness Over Optimization

Implementation priorities, in order:
1. **Correctness**: Code MUST produce accurate results
2. **Clarity**: Code MUST be readable and understandable
3. **Maintainability**: Code MUST be easy to modify and extend
4. Performance optimization is secondary in educational phases

Claude Code MUST:
- Prioritize working, correct code over clever solutions
- Avoid premature optimization
- Document any non-obvious logic
- Prefer explicit over implicit behavior

**Rationale**: Educational projects benefit more from understandable code than performant code. Optimization can be added in later phases.

### IV. Graceful User Interface Behavior

All user interfaces MUST provide a professional user experience.

**CLI (Phase I)**:
- Provide clear, user-friendly prompts
- Display meaningful success and error messages
- Handle invalid input gracefully with helpful guidance
- NEVER expose stack traces or internal errors to the user

**Web UI (Phase II)**:
- Modern, professional, colorful design
- Clean layout with subtle animations (hover, transitions, loading states)
- Fully responsive design (desktop + mobile)
- Clear feedback for all user actions (loading indicators, success/error states)
- Accessible design following WCAG guidelines

**Rationale**: Good UX builds trust and reduces user frustration, even in educational projects.

### V. Code Quality

All code MUST adhere to professional standards.

**Python (Backend)**:
- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Use descriptive naming conventions
- Keep functions small and single-purpose

**TypeScript (Frontend)**:
- Follow ESLint and Prettier configurations
- Use strict TypeScript mode
- Use descriptive naming conventions
- Keep components small and single-purpose

**General**:
- Avoid unnecessary abstraction
- Eliminate dead or unused code
- No hardcoded secrets or tokens (use .env)
- Prefer the smallest viable diff for any change
- Prefer readability over cleverness

**Rationale**: Consistent, clean code reduces cognitive load and makes the codebase accessible to learners.

### VI. Verification & Testing

All functionality MUST be verifiable.

**Phase I (CLI)**:
- Each specification MUST map to observable CLI behavior
- All user-visible behavior MUST be testable manually
- Feature completion is defined by full spec compliance

**Phase II (Web Application)**:
- Each specification MUST map to observable web behavior
- API endpoints MUST have contract tests
- Critical user flows MUST have integration tests
- Frontend components SHOULD have unit tests
- Feature completion is defined by full spec compliance plus passing tests

**Rationale**: Verification ensures that specifications translate to working features users can experience.

### VII. Web Architecture

Phase II MUST follow REST architecture principles.

- Backend and frontend MUST be separate, independently deployable applications
- Communication MUST occur via well-defined REST API endpoints
- API responses MUST use consistent JSON structure
- Error responses MUST include meaningful error codes and messages
- API versioning strategy MUST be defined before implementation
- CORS MUST be configured appropriately for frontend access

**Rationale**: REST architecture enables frontend/backend decoupling, scalability, and potential future mobile clients.

### VIII. Authentication & Security

Phase II MUST implement secure user authentication.

- Authentication MUST use JWT (JSON Web Tokens) with python-jose and passlib
- User signup and signin flows MUST be implemented
- All user data MUST be scoped to the authenticated user
- Passwords MUST be securely hashed using bcrypt (via passlib)
- API endpoints MUST validate JWT tokens via middleware
- Sensitive data MUST NOT be logged or exposed in error messages
- HTTPS MUST be used in production environments

**Rationale**: Custom JWT authentication provides full control over the auth flow, simpler integration with FastAPI, and avoids third-party SDK dependencies while maintaining security best practices.

## Technical Stack

### Phase I (Completed)

| Component | Technology | Notes |
|-----------|------------|-------|
| Language | Python 3.13+ | Modern Python features permitted |
| Environment | UV | Package and environment management |
| Interface | CLI | Text-based interaction only |
| Storage | In-memory | No persistence (intentional for Phase I) |

**Out of scope for Phase I:**
- File or database persistence
- Web frameworks or APIs
- Authentication or authorization
- Concurrency or asynchronous execution
- AI functionality inside the application

### Phase II (Current)

| Component | Technology | Notes |
|-----------|------------|-------|
| Backend Language | Python 3.13+ | FastAPI REST framework |
| Database | Neon Serverless PostgreSQL | Cloud-hosted, serverless |
| ORM / Data Layer | SQLModel | SQLAlchemy + Pydantic integration |
| Frontend Framework | Next.js | React with TypeScript |
| Frontend Language | TypeScript | Strict mode required |
| Authentication | JWT (python-jose + passlib) | Custom auth with bcrypt password hashing |
| API Architecture | REST | JSON request/response |
| Styling | Tailwind CSS | Utility-first CSS framework |

**Out of scope for Phase II:**
- Real-time features (WebSockets)
- Background job processing
- AI functionality inside the application
- Mobile applications

## Todo Domain Model

### Core Fields (Phase I)

Each Todo item MUST include:
- `id`: Integer, unique, auto-incremented
- `title`: Non-empty string
- `description`: Optional string
- `completed`: Boolean flag (default: False)

### Phase II Extensions

Additional fields for Phase II:
- `user_id`: Foreign key to User entity (required)
- `priority`: Enum (high / medium / low), default: medium
- `tags`: Array of strings (e.g., work, home, shopping)
- `due_date`: Optional date/time for task deadline
- `reminder_time`: Optional date/time for browser notification reminder
- `recurrence_pattern`: Optional enum (none / daily / weekly / monthly) for recurring tasks
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated)

### User Entity (Phase II)

Each User MUST include:
- `id`: UUID, unique, auto-generated
- `email`: Non-empty string, unique
- `name`: Optional string
- `hashed_password`: Bcrypt-hashed password (never stored in plain text)
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated)

### Domain Rules

**Phase I:**
- Todos exist only in memory for the lifetime of the program
- Todos can be created, read, updated, deleted, and marked complete/incomplete
- Deleting a Todo permanently removes it from the in-memory store
- IDs are never reused within a session

**Phase II:**
- Todos are persisted in Neon PostgreSQL
- Todos are scoped to the authenticated user
- Users can only access their own todos
- Deleting a Todo permanently removes it from the database
- IDs are UUIDs, globally unique

## Feature Progression Rules

### Basic Level — Core Essentials (Phase I - Completed)

These features form the mandatory MVP foundation:
1. **Add Task**: Create a new todo with title and optional description
2. **View Task List**: Display all todos with their status
3. **Update Task**: Modify title and/or description of existing todo
4. **Delete Task**: Remove a todo from the store
5. **Mark Complete/Incomplete**: Toggle the completed status

### Intermediate Level — Organization & Usability (Phase II - Current)

These features are NOW in scope for Phase II:
- **User Authentication**: Signup and signin via Better Auth
- **Task Priorities**: Assign high / medium / low priority
- **Tags/Categories**: Label tasks (e.g., work, home, shopping)
- **Search**: Find tasks by keyword in title/description
- **Filter**: View tasks by status, priority, or tags
- **Sort**: Order tasks by title, priority, due date, or creation date
- **Due Dates**: Set optional due dates on todos with visual overdue indicators
- **Reminders**: Browser notifications for todos with reminder times (when permission granted)
- **Recurring Tasks**: Automatic regeneration of todos on daily/weekly/monthly schedules
- **Responsive Web UI**: Modern, professional interface for desktop and mobile

### Advanced Level — Intelligent Features (Phase III - Future)

These features are strictly OUT OF SCOPE until Phase III:
- Intelligent scheduling or suggestions
- AI-powered features (smart categorization, priority suggestions)
- Natural language task creation
- Calendar integration with external services

## Success Criteria

### Phase I Completion Requirements (Completed)

Phase I is considered complete when:
- All five Basic Level features work correctly via CLI
- The application runs reliably without crashes
- User input is validated gracefully
- All functionality is manually verifiable
- Code follows all principles defined in this constitution
- Architecture supports future phase expansion

### Phase II Completion Requirements

Phase II is considered complete when:
- User authentication works correctly (signup, signin, signout)
- All Intermediate Level features work correctly via web UI
- Due dates display correctly with visual overdue indicators
- Recurring tasks automatically regenerate on schedule completion
- Browser notifications deliver reminders when scheduled (with permission)
- API endpoints pass contract tests
- Critical user flows pass integration tests
- Web UI is responsive on desktop and mobile devices
- Web UI follows modern design principles with animations
- All user data is properly scoped and isolated
- Application is deployable to production environment
- Code follows all principles defined in this constitution

## Governance

This constitution supersedes all other development practices for this project.

### Amendment Process

1. Propose amendment with rationale
2. Document impact on existing specifications and code
3. Update constitution with new version number
4. Update dependent artifacts if affected
5. Record amendment in Prompt History

### Versioning Policy

Constitution versions follow semantic versioning:
- **MAJOR**: Backward-incompatible changes to principles or governance (new phases, tech stack changes)
- **MINOR**: New principles added or material guidance expansion
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

- All implementation work MUST verify compliance with this constitution
- Complexity beyond what is specified MUST be justified
- Claude Code MUST cite this constitution when refusing out-of-scope requests

**Version**: 3.1.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2026-01-03
