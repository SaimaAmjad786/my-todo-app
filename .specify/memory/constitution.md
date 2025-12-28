<!--
  Sync Impact Report
  ==================
  Version change: 1.0.0 → 1.1.0 (MINOR: Added phased feature progression and success criteria)

  Modified principles:
    - None renamed; all original principles retained

  Added sections:
    - Project Vision section
    - AI Role Definition section
    - Feature Progression Rules (Basic/Intermediate/Advanced levels)
    - Success Criteria (Phase I)
    - Future Phases summary

  Removed sections: None

  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ (no updates needed - Constitution Check is generic)
    - .specify/templates/spec-template.md ✅ (no updates needed - aligns with spec-driven approach)
    - .specify/templates/tasks-template.md ✅ (no updates needed - task structure compatible)

  Follow-up TODOs: None
-->

# The Evolution of Todo Constitution

## Project Vision

This project is designed to teach students how professional software systems evolve incrementally. Each phase builds on a stable foundation while preserving clean architecture, clarity, and maintainability.

AI is used not as a shortcut, but as a disciplined engineering tool that follows specifications, plans, and constraints.

### Current Phase

**Phase I — Basic Level** (Core Essentials, CLI-based, In-Memory)

### Future Phases

- Phase II — Intermediate Level (Organization & Usability)
- Phase III — Advanced Level (Intelligent Features)

## AI Role Definition

Claude Code MUST act as a senior-level Python software engineer and product architect.

The AI MUST:
- Follow this constitution as the highest authority
- Implement only what is explicitly defined in approved specifications
- Never assume future features prematurely
- Ask for clarification when requirements are ambiguous
- Optimize for clarity, correctness, and extensibility

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

- **Domain Layer (Models)**: Define data structures and domain rules (Todo entity)
- **Service Layer (Business Logic)**: Implement operations on domain models
- **Interface Layer (CLI)**: Handle user input/output, validation, and presentation

Architectural constraints:
- Avoid monolithic functions
- Design for future evolution into APIs, persistent storage, and distributed systems
- Each layer MUST be independently testable
- Dependencies flow inward (CLI → Services → Domain)

**Rationale**: Clean separation enables incremental evolution from a CLI app to web APIs, databases, and distributed systems without rewriting core logic.

### III. Correctness Over Optimization

Implementation priorities, in order:
1. **Correctness**: Code MUST produce accurate results
2. **Clarity**: Code MUST be readable and understandable
3. **Maintainability**: Code MUST be easy to modify and extend
4. Optimization is NOT a priority for Phase I

Claude Code MUST:
- Prioritize working, correct code over clever solutions
- Avoid premature optimization
- Document any non-obvious logic
- Prefer explicit over implicit behavior

**Rationale**: Educational projects benefit more from understandable code than performant code. Optimization can be added in later phases.

### IV. Graceful CLI Behavior

The command-line interface MUST provide a professional user experience.

- Provide clear, user-friendly prompts
- Display meaningful success and error messages
- Handle invalid input gracefully with helpful guidance
- NEVER expose stack traces or internal errors to the user
- Ensure all actions are explicit and predictable
- Confirm destructive operations before execution

**Rationale**: Good CLI UX builds trust and reduces user frustration, even in educational projects.

### V. Code Quality

All code MUST adhere to professional Python standards.

- Follow PEP 8 style guidelines
- Use descriptive naming conventions (variables, functions, classes)
- Keep functions small and single-purpose
- Avoid unnecessary abstraction
- Eliminate dead or unused code
- No hardcoded secrets or tokens (use .env if needed)
- Prefer the smallest viable diff for any change
- Prefer readability over cleverness

**Rationale**: Consistent, clean code reduces cognitive load and makes the codebase accessible to learners.

### VI. Manual Verification

All functionality MUST be verifiable through the CLI.

- Each specification MUST map to observable CLI behavior
- Feature completion is defined by full spec compliance
- All user-visible behavior MUST be testable manually
- No hidden or undocumented features

**Rationale**: Manual verification ensures that specifications translate to working features users can experience.

## Technical Stack

Phase I technology constraints:

| Component | Technology | Notes |
|-----------|------------|-------|
| Language | Python 3.13+ | Modern Python features permitted |
| Environment | UV | Package and environment management |
| Interface | CLI | Text-based interaction only |
| Storage | In-memory | No persistence (intentional for Phase I) |

Out of scope for Phase I:
- File or database persistence
- Web frameworks or APIs
- Authentication or authorization
- Concurrency or asynchronous execution
- AI functionality inside the application

## Todo Domain Model

### Core Fields (Phase I)

Each Todo item MUST include:
- `id`: Integer, unique, auto-incremented
- `title`: Non-empty string
- `description`: Optional string
- `completed`: Boolean flag (default: False)

### Future-Compatible Fields

These fields are NOT implemented until explicitly specified in later phases:
- `priority`: high / medium / low
- `tags` / `category`: work, personal, shopping, health, general
- `due_date`: Date string
- `recurrence`: Recurrence rules

### Domain Rules

- Todos exist only in memory for the lifetime of the program
- Todos can be created, read, updated, deleted, and marked complete/incomplete
- Deleting a Todo permanently removes it from the in-memory store
- IDs are never reused within a session

## Feature Progression Rules

### Basic Level — Core Essentials (Phase I)

These features form the mandatory MVP foundation:
1. **Add Task**: Create a new todo with title and optional description
2. **View Task List**: Display all todos with their status
3. **Update Task**: Modify title and/or description of existing todo
4. **Delete Task**: Remove a todo from the store
5. **Mark Complete/Incomplete**: Toggle the completed status

### Intermediate Level — Organization & Usability (Phase II)

These features may ONLY be implemented when explicitly specified:
- Task priorities (high / medium / low)
- Tags or categories (e.g., work, home)
- Search by keyword
- Filter by status, priority, or date
- Sort tasks (by title, priority, due date)

### Advanced Level — Intelligent Features (Phase III)

These features are strictly OUT OF SCOPE until a later phase:
- Recurring tasks (daily, weekly, custom rules)
- Due dates with time-based reminders
- Notification mechanisms (platform-dependent)
- Intelligent scheduling or suggestions

## Success Criteria

### Phase I Completion Requirements

Phase I is considered complete when:
- All five Basic Level features work correctly via CLI
- The application runs reliably without crashes
- User input is validated gracefully
- All functionality is manually verifiable
- Code follows all principles defined in this constitution
- Architecture supports future phase expansion

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
- **MAJOR**: Backward-incompatible changes to principles or governance
- **MINOR**: New principles added or material guidance expansion
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

- All implementation work MUST verify compliance with this constitution
- Complexity beyond what is specified MUST be justified
- Claude Code MUST cite this constitution when refusing out-of-scope requests

**Version**: 1.1.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-27
