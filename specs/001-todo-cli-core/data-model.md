# Data Model: Todo CLI Core (Phase I)

**Feature**: 001-todo-cli-core
**Date**: 2025-12-26
**Source**: spec.md (Key Entities), constitution.md (Todo Domain Model)

## Entities

### Todo

Represents a task item that the user wants to track.

```python
@dataclass
class Todo:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

#### Fields

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `id` | `int` | Yes | Auto-generated | Unique, positive integer, never reused |
| `title` | `str` | Yes | N/A | Non-empty, max 500 characters |
| `description` | `str` | No | `""` | Max 500 characters |
| `completed` | `bool` | No | `False` | `True` or `False` |

#### Validation Rules

1. **Title validation**:
   - MUST NOT be empty or whitespace-only
   - MUST NOT exceed 500 characters
   - MAY contain special characters, quotes, unicode

2. **Description validation**:
   - MAY be empty
   - MUST NOT exceed 500 characters
   - MAY contain special characters, quotes, unicode

3. **ID validation**:
   - MUST be positive integer
   - MUST be unique within session
   - MUST NOT be reused after deletion

#### State Transitions

```
                    create
    [Not Exists] ──────────► [Incomplete]
                                  │
                    mark_complete │ ◄──────┐
                                  ▼        │ mark_incomplete
                             [Complete] ───┘
                                  │
                    delete        │
                                  ▼
                            [Deleted]
```

**Valid Transitions**:
- Create: Not Exists → Incomplete
- Mark Complete: Incomplete → Complete
- Mark Incomplete: Complete → Incomplete
- Update: Incomplete ↔ Incomplete (title/description change)
- Update: Complete ↔ Complete (title/description change)
- Delete: Any → Deleted (terminal state)

## Storage Schema

### In-Memory Store

```python
class TodoStore:
    """In-memory storage for Todo entities."""

    _todos: dict[int, Todo]  # ID → Todo mapping
    _next_id: int            # Auto-increment counter
```

#### Invariants

1. `_next_id` MUST always be greater than any existing ID in `_todos`
2. `_todos` keys MUST match the `id` field of their values
3. No two todos can have the same ID
4. `_next_id` MUST only increment (never decrement or reset)

## Operations

### Create (Add Todo)

**Input**: `title: str`, `description: str = ""`
**Output**: `Todo` (newly created)
**Side Effects**: Increments `_next_id`, adds to `_todos`

```
Pre-conditions:
  - title is non-empty after stripping whitespace
  - title length <= 500
  - description length <= 500

Post-conditions:
  - New Todo exists in _todos with unique ID
  - _next_id has incremented by 1
  - Todo.completed == False
```

### Read (View Todos)

**Input**: None
**Output**: `list[Todo]` (all todos, ordered by ID)
**Side Effects**: None

```
Pre-conditions: None

Post-conditions:
  - Returns all todos currently in storage
  - Original storage unchanged
```

### Update

**Input**: `id: int`, `title: str | None`, `description: str | None`
**Output**: `Todo` (updated) or `None` (not found)
**Side Effects**: Modifies existing Todo in `_todos`

```
Pre-conditions:
  - id exists in _todos
  - if title provided: non-empty after stripping, length <= 500
  - if description provided: length <= 500

Post-conditions:
  - Todo fields updated as specified
  - id and completed unchanged unless explicitly modified
```

### Delete

**Input**: `id: int`
**Output**: `bool` (success/failure)
**Side Effects**: Removes Todo from `_todos`

```
Pre-conditions:
  - id exists in _todos

Post-conditions:
  - Todo with given id no longer in _todos
  - id will never be reused
  - _next_id unchanged
```

### Mark Complete / Incomplete

**Input**: `id: int`, `completed: bool`
**Output**: `Todo` (updated) or `None` (not found)
**Side Effects**: Modifies `completed` field of existing Todo

```
Pre-conditions:
  - id exists in _todos

Post-conditions:
  - Todo.completed == completed (parameter value)
  - Other fields unchanged
```

## Relationships

Phase I has no relationships between entities. The Todo entity is standalone.

Future phases may introduce:
- User → Todo (ownership)
- Todo → Tags (categorization)
- Todo → Project (grouping)

## Data Volume Assumptions

| Metric | Expected Range | Notes |
|--------|---------------|-------|
| Todos per session | 1-100 | In-memory, no persistence |
| Title length | 10-100 chars | Typical usage |
| Description length | 0-300 chars | Often empty |
| Session duration | Minutes to hours | Single run |
