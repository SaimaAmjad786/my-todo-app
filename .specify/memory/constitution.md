<!--
  Sync Impact Report
  ==================
  Version change: 3.1.0 → 4.0.0 (MAJOR: Phase III scope defined with AI Chatbot architecture)

  Modified principles:
    - Phase Summary table → Phase II marked "Completed", Phase III marked "Current"
    - Current Phase → Changed from Phase II to Phase III
    - VIII. Authentication & Security → Extended to include Phase III auth continuity

  Modified sections:
    - "Technical Stack" → Added Phase III stack (OpenAI Agents SDK, MCP, ChatKit)
    - "Feature Progression Rules / Advanced Level" → Now IN SCOPE with detailed features
    - "Success Criteria" → Added Phase III completion requirements
    - "Todo Domain Model" → Added Phase III extensions (Conversation, Message entities)
    - "Out of scope for Phase II" → Moved AI functionality to Phase III

  Added sections:
    - "Phase III Layers (AI Chatbot)" under Clean Architecture
    - "Conversation Entity (Phase III)"
    - "Message Entity (Phase III)"
    - "MCP Tools Definition"
    - "Phase III Completion Requirements"

  Removed sections: None

  Templates requiring updates:
    - .specify/templates/plan-template.md → No changes needed (generic)
    - .specify/templates/spec-template.md → No changes needed (generic)
    - .specify/templates/tasks-template.md → No changes needed (generic)

  Follow-up TODOs:
    - Create Phase III feature specification (/sp.specify)
    - Create Phase III implementation plan (/sp.plan)
    - Create Phase III tasks (/sp.tasks)

  Amendment Notes (4.0.0):
    - MAJOR change: Phase III scope fully defined
    - AI Chatbot using MCP (Model Context Protocol) with OpenAI Agents SDK
    - Frontend: OpenAI ChatKit
    - Backend: FastAPI (existing, extended)
    - AI Logic: OpenAI Agents SDK
    - Tools: Official MCP SDK for todo operations
    - Stateless architecture with all state in Neon PostgreSQL
    - Authentication continues with existing Better Auth/JWT
    - New entities: Conversation, Message for chat persistence
-->

# The Evolution of Todo Constitution

## Project Vision

This project is designed to teach students how professional software systems evolve incrementally. Each phase builds on a stable foundation while preserving clean architecture, clarity, and maintainability.

AI is used not as a shortcut, but as a disciplined engineering tool that follows specifications, plans, and constraints.

### Phase Summary

| Phase | Level | Description | Status |
|-------|-------|-------------|--------|
| Phase I | Basic | In-memory CLI application | Completed |
| Phase II | Intermediate | Full-stack web application | Completed |
| Phase III | Advanced | AI-powered conversational chatbot | Current |

### Current Phase

**Phase III — Advanced Level** (AI-Powered Conversational Todo Chatbot)

### Phase Isolation Rules

- Each phase MUST have a complete, stable implementation before the next phase begins
- Phase-specific code MUST NOT introduce regressions to prior phase functionality
- Features from future phases MUST NOT be implemented until explicitly specified
- When transitioning phases, the previous phase codebase serves as the stable foundation
- Phase II does NOT extend Phase I code; it is a new implementation following the same domain model
- Phase III extends Phase II by adding AI chatbot capabilities while preserving existing todo functionality

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

**Phase III Layers (AI Chatbot)**:
- **Domain Layer (Models)**: Extend with Conversation and Message entities via SQLModel
- **Service Layer (Business Logic)**: Existing todo services remain unchanged
- **MCP Tools Layer**: MCP server exposing todo operations as tools for AI agent
- **AI Agent Layer (OpenAI Agents SDK)**: Process natural language, invoke MCP tools, manage conversation flow
- **API Layer (REST)**: Extended with chat endpoints for conversation management
- **Frontend Layer (ChatKit)**: OpenAI ChatKit for conversational UI

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

**Chat UI (Phase III)**:
- Conversational interface using OpenAI ChatKit
- Clear distinction between user messages and AI responses
- Loading indicators during AI processing
- Error messages displayed inline in conversation
- Chat history persistence and resumption
- Natural language input with no required syntax

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

**Phase III (AI Chatbot)**:
- Each specification MUST map to observable chat behavior
- MCP tools MUST have unit tests verifying correct todo operations
- AI agent responses MUST be validated against expected behavior patterns
- Conversation persistence MUST be verified across server restarts
- Integration tests MUST verify end-to-end chat flows

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

Phase II and Phase III MUST implement secure user authentication.

- Authentication MUST use JWT (JSON Web Tokens) with python-jose and passlib
- User signup and signin flows MUST be implemented
- All user data MUST be scoped to the authenticated user
- Passwords MUST be securely hashed using bcrypt (via passlib)
- API endpoints MUST validate JWT tokens via middleware
- Sensitive data MUST NOT be logged or exposed in error messages
- HTTPS MUST be used in production environments
- Phase III conversations MUST be scoped to authenticated users
- AI responses MUST NOT leak data from other users

**Rationale**: Custom JWT authentication provides full control over the auth flow, simpler integration with FastAPI, and avoids third-party SDK dependencies while maintaining security best practices.

### IX. Stateless AI Architecture

Phase III MUST be fully stateless with all state persisted in the database.

- AI agent MUST NOT maintain in-memory state between requests
- All conversation state MUST be stored in Neon PostgreSQL
- Chat history MUST be retrievable and resumable after server restart
- MCP tools MUST operate on database-persisted todos
- Each request MUST be independently processable with conversation context loaded from database

**Rationale**: Stateless architecture enables horizontal scaling, fault tolerance, and simpler deployment without sticky sessions.

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

### Phase II (Completed)

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

### Phase III (Current)

| Component | Technology | Notes |
|-----------|------------|-------|
| Backend Language | Python 3.13+ | FastAPI (extended from Phase II) |
| Database | Neon Serverless PostgreSQL | Same as Phase II, extended schema |
| ORM / Data Layer | SQLModel | Extended with Conversation, Message models |
| AI Framework | OpenAI Agents SDK | Agent orchestration and tool calling |
| Tool Protocol | MCP (Model Context Protocol) | Official MCP SDK for tool exposure |
| Chat Frontend | OpenAI ChatKit | Conversational UI component library |
| Authentication | JWT (python-jose + passlib) | Continued from Phase II |
| API Architecture | REST | Extended with chat endpoints |

**Out of scope for Phase III:**
- Voice input/output
- Multi-modal AI (images, files)
- Real-time collaborative editing
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

### Conversation Entity (Phase III)

Each Conversation MUST include:
- `id`: UUID, unique, auto-generated
- `user_id`: Foreign key to User entity (required)
- `title`: Optional string (auto-generated from first message or user-provided)
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated on new message)

### Message Entity (Phase III)

Each Message MUST include:
- `id`: UUID, unique, auto-generated
- `conversation_id`: Foreign key to Conversation entity (required)
- `role`: Enum (user / assistant / system)
- `content`: Non-empty string (message text)
- `tool_calls`: Optional JSON (MCP tool invocations made by assistant)
- `tool_results`: Optional JSON (results from MCP tool executions)
- `created_at`: Timestamp (auto-generated)

### MCP Tools Definition

The MCP server MUST expose these tools for the AI agent:

- `add_todo`: Create a new todo with title, optional description, priority, tags, due_date
- `list_todos`: Retrieve todos with optional filters (status, priority, tags, search query)
- `get_todo`: Retrieve a specific todo by ID
- `update_todo`: Modify an existing todo's fields
- `delete_todo`: Remove a todo permanently
- `complete_todo`: Mark a todo as completed
- `uncomplete_todo`: Mark a todo as incomplete

All MCP tools MUST:
- Operate on the authenticated user's todos only
- Return structured JSON responses
- Include error information on failure
- Be idempotent where applicable

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

**Phase III:**
- All Phase II domain rules continue to apply
- Conversations are persisted in Neon PostgreSQL
- Conversations are scoped to the authenticated user
- Users can only access their own conversations
- Messages within a conversation are ordered by creation timestamp
- Conversations can be resumed after server restart by loading message history

## Feature Progression Rules

### Basic Level — Core Essentials (Phase I - Completed)

These features form the mandatory MVP foundation:
1. **Add Task**: Create a new todo with title and optional description
2. **View Task List**: Display all todos with their status
3. **Update Task**: Modify title and/or description of existing todo
4. **Delete Task**: Remove a todo from the store
5. **Mark Complete/Incomplete**: Toggle the completed status

### Intermediate Level — Organization & Usability (Phase II - Completed)

These features are implemented in Phase II:
- **User Authentication**: Signup and signin via JWT
- **Task Priorities**: Assign high / medium / low priority
- **Tags/Categories**: Label tasks (e.g., work, home, shopping)
- **Search**: Find tasks by keyword in title/description
- **Filter**: View tasks by status, priority, or tags
- **Sort**: Order tasks by title, priority, due date, or creation date
- **Due Dates**: Set optional due dates on todos with visual overdue indicators
- **Reminders**: Browser notifications for todos with reminder times (when permission granted)
- **Recurring Tasks**: Automatic regeneration of todos on daily/weekly/monthly schedules
- **Responsive Web UI**: Modern, professional interface for desktop and mobile

### Advanced Level — AI-Powered Conversational Interface (Phase III - Current)

These features are NOW in scope for Phase III:
- **Natural Language Todo Management**: Users interact via conversational text
- **AI-Powered Task Operations**: Add, list, update, delete, complete todos via chat
- **MCP Tool Integration**: AI agent uses MCP tools for all todo operations
- **Conversation Persistence**: Chat history stored in database, resumable after restart
- **Context-Aware Responses**: AI understands conversation context for follow-up queries
- **ChatKit Interface**: Modern conversational UI using OpenAI ChatKit

**Strictly OUT OF SCOPE for Phase III:**
- Intelligent scheduling or automatic priority suggestions
- Smart categorization or tag recommendations
- Calendar integration with external services
- Voice input or output
- Multi-modal interactions (images, files)

## Success Criteria

### Phase I Completion Requirements (Completed)

Phase I is considered complete when:
- All five Basic Level features work correctly via CLI
- The application runs reliably without crashes
- User input is validated gracefully
- All functionality is manually verifiable
- Code follows all principles defined in this constitution
- Architecture supports future phase expansion

### Phase II Completion Requirements (Completed)

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

### Phase III Completion Requirements

Phase III is considered complete when:
- Users can interact with todos via natural language chat
- AI correctly interprets and executes todo operations (add, list, update, delete, complete)
- MCP tools are properly exposed and invokable by the AI agent
- Conversations persist in the database
- Users can resume previous conversations after server restart
- Chat UI displays conversation history correctly
- AI responses are contextually appropriate and accurate
- All operations respect user authentication scope
- Integration tests verify end-to-end chat flows
- Application remains stateless (no in-memory state between requests)
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

**Version**: 4.0.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2026-01-18
