# Implementation Plan: Todo CLI Core (Phase I)

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Build an in-memory command-line Todo application in Python 3.13+ using UV for environment management. The application implements five core CRUD operations (Add, View, Update, Delete, Mark Complete/Incomplete) through an interactive menu-driven CLI. Architecture follows clean separation: Domain Layer (Todo model) → Service Layer (business logic) → CLI Layer (user interaction).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory (Python list/dict, no persistence)
**Testing**: Manual CLI verification (no automated tests for Phase I)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project
**Performance Goals**: N/A (educational focus, not performance-critical)
**Constraints**: No external dependencies, no persistence, no async
**Scale/Scope**: Single user, ~100 todos max (in-memory reasonable limit)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | ✅ PASS | Spec exists at `specs/001-todo-cli-core/spec.md` with all requirements |
| II. Clean Architecture | ✅ PASS | Plan defines Domain → Service → CLI layers |
| III. Correctness Over Optimization | ✅ PASS | No optimization goals; focus on clarity |
| IV. Graceful CLI Behavior | ✅ PASS | Spec FR-012/13/14 require graceful error handling |
| V. Code Quality | ✅ PASS | PEP 8 compliance planned; simple structures |
| VI. Manual Verification | ✅ PASS | All features verifiable via CLI per spec |

**Gate Result**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── todo.py          # Todo dataclass
├── services/
│   ├── __init__.py
│   └── todo_service.py  # CRUD operations, ID generation, storage
├── cli/
│   ├── __init__.py
│   └── menu.py          # Interactive menu, input handling, display
└── main.py              # Entry point, application loop
```

**Structure Decision**: Single project structure selected. The application is a standalone CLI tool with no web/mobile components. Three-layer architecture (models → services → cli) enables future evolution to API endpoints while maintaining testability.

## Architecture

### Layer Responsibilities

```
┌─────────────────────────────────────────────┐
│                 CLI Layer                    │
│  (menu.py)                                  │
│  - Display menu options                     │
│  - Capture user input                       │
│  - Format output for display                │
│  - Handle input validation errors           │
└─────────────────┬───────────────────────────┘
                  │ calls
                  ▼
┌─────────────────────────────────────────────┐
│              Service Layer                   │
│  (todo_service.py)                          │
│  - CRUD operations                          │
│  - ID generation (auto-increment)           │
│  - In-memory storage (dict by ID)           │
│  - Business rule enforcement                │
└─────────────────┬───────────────────────────┘
                  │ uses
                  ▼
┌─────────────────────────────────────────────┐
│              Domain Layer                    │
│  (todo.py)                                  │
│  - Todo dataclass                           │
│  - Field definitions                        │
│  - No behavior (pure data)                  │
└─────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → CLI captures and validates format
2. **CLI → Service** → Service executes business logic
3. **Service → Storage** → In-memory dict updated
4. **Service → CLI** → Returns result/error
5. **CLI → User** → Displays formatted output

### Key Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Storage structure | `dict[int, Todo]` | O(1) lookup by ID; deletion doesn't require reindexing | List (O(n) lookup) |
| ID generation | Auto-increment counter | Simple, predictable, matches spec | UUID (overkill), length-based (gaps confuse users) |
| CLI interaction | Interactive menu loop | Beginner-friendly, discoverable, matches SC-009 | Command args (less discoverable) |
| File structure | Multi-module | Clean architecture, future-ready | Single file (doesn't scale) |

## Complexity Tracking

> No constitution violations requiring justification. Architecture is minimal and spec-compliant.

## Implementation Order

Per spec priority and dependency analysis:

1. **Setup** - Project structure, UV environment, entry point
2. **Domain Layer** - Todo dataclass
3. **Service Layer** - TodoService with storage
4. **Add Todo (P1)** - First feature, enables all others
5. **View Todos (P2)** - Visibility for testing other features
6. **Update Todo (P3)** - Modify existing todos
7. **Delete Todo (P4)** - Remove todos
8. **Mark Complete/Incomplete (P5)** - Toggle status
9. **CLI Polish** - Error messages, edge cases, exit handling

## Validation Checkpoints

After each feature, verify against spec acceptance scenarios:

| Feature | Validation |
|---------|------------|
| Add | Can add with title only; can add with title+description; rejects empty title |
| View | Shows empty message when no todos; lists all with status indicators |
| Update | Changes title; changes description; rejects empty title; handles missing ID |
| Delete | Removes todo; handles missing ID; IDs not reused |
| Mark | Toggles complete; toggles incomplete; handles missing ID |
