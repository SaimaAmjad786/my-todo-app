# Research: Todo CLI Core (Phase I)

**Feature**: 001-todo-cli-core
**Date**: 2025-12-26
**Status**: Complete

## Research Questions

This section documents research conducted to resolve technical decisions for the implementation plan.

### 1. Python Dataclass vs NamedTuple vs Regular Class

**Decision**: Use `@dataclass` from Python's standard library

**Rationale**:
- Built into Python 3.7+ (we're using 3.13+)
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Mutable by default (needed for updates)
- Type hints integrated
- Educational value: demonstrates modern Python patterns

**Alternatives Considered**:
- `NamedTuple`: Immutable, less suitable for update operations
- Regular class: More boilerplate, no educational benefit
- `TypedDict`: Dictionary-based, less structured

**Example**:
```python
from dataclasses import dataclass, field

@dataclass
class Todo:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

### 2. In-Memory Storage Structure

**Decision**: Use `dict[int, Todo]` with separate counter for ID generation

**Rationale**:
- O(1) lookup, update, delete by ID
- Deletion doesn't affect other IDs
- Counter ensures IDs are never reused (per spec FR-003)
- Simple iteration with `.values()`

**Alternatives Considered**:
- `list[Todo]`: O(n) lookup, deletion shifts indices
- `OrderedDict`: Unnecessary ordering overhead
- Database-like library (SQLite): Out of scope for Phase I

**Implementation Pattern**:
```python
class TodoService:
    def __init__(self):
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1
```

### 3. CLI Input Handling

**Decision**: Use built-in `input()` with try/except for robustness

**Rationale**:
- No external dependencies required
- Simple, readable code
- Handles Ctrl+C (KeyboardInterrupt) gracefully
- Sufficient for interactive menu pattern

**Alternatives Considered**:
- `argparse`: Better for command-line args, not interactive menus
- `click`: External dependency, overkill for Phase I
- `rich`/`prompt_toolkit`: External dependencies, beyond scope

**Error Handling Pattern**:
```python
def get_integer_input(prompt: str) -> int | None:
    try:
        return int(input(prompt))
    except ValueError:
        return None
```

### 4. Menu Display Pattern

**Decision**: Numbered menu with while loop

**Rationale**:
- Intuitive for beginners
- Clear mapping: number → action
- Easy to extend for future features
- Matches SC-009 (first-time users succeed without docs)

**Menu Structure**:
```
=== Todo Application ===
1. Add Todo
2. View All Todos
3. Update Todo
4. Delete Todo
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6):
```

### 5. Output Formatting

**Decision**: Simple text with checkbox indicators `[ ]` / `[x]`

**Rationale**:
- Universal, works in any terminal
- No color dependencies
- Clear visual distinction
- Matches spec assumption #4

**Display Format**:
```
ID: 1 [x] Buy groceries
      Description: From the farmers market

ID: 2 [ ] Write report
```

### 6. Error Message Strategy

**Decision**: User-friendly messages without technical details

**Rationale**:
- Matches FR-012, FR-014 (no stack traces)
- Actionable guidance for users
- Consistent tone throughout

**Error Messages**:
| Scenario | Message |
|----------|---------|
| Empty title | "Error: Title cannot be empty." |
| Todo not found | "Error: Todo with ID {id} not found." |
| Invalid ID format | "Error: Please enter a valid number." |
| Invalid menu choice | "Error: Please enter a number between 1 and 6." |

### 7. UV Project Setup

**Decision**: Minimal pyproject.toml with no external dependencies

**Rationale**:
- UV handles virtual environment creation
- No dependencies to install
- Simple `uv run` execution
- Ready for future dependency additions

**pyproject.toml structure**:
```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "Phase I In-Memory Todo CLI Application"
requires-python = ">=3.13"

[project.scripts]
todo = "src.main:main"
```

## Resolved Clarifications

All technical context questions have been resolved. No NEEDS CLARIFICATION items remain.

| Question | Resolution |
|----------|------------|
| Storage structure | dict[int, Todo] |
| ID generation | Auto-increment counter, never reuse |
| CLI style | Interactive menu loop |
| File structure | Multi-module (models/services/cli) |
| Dependencies | Standard library only |

## References

- Python dataclasses: https://docs.python.org/3/library/dataclasses.html
- UV documentation: https://docs.astral.sh/uv/
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
