# Implementation Plan: Todo App Intermediate Level Enhancements

**Branch**: `002-intermediate-enhancements` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-intermediate-enhancements/spec.md`

## Summary

This plan implements Phase II (Intermediate Level) enhancements for the Todo CLI application: task priorities, categories, search, filter, and sort functionality.

**Key Finding**: The backend (model and service layer) already implements all required features. This plan focuses on exposing these features through the CLI menu.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: colorama (CLI colors)
**Storage**: JSON file persistence (todos.json)
**Testing**: Manual CLI verification
**Target Platform**: Windows/Linux/macOS CLI
**Project Type**: Single project
**Performance Goals**: Instant response for all operations
**Constraints**: CLI-only interface, maintain existing architecture
**Scale/Scope**: Personal task management (hundreds of tasks)

## Constitution Check

*GATE: Must pass before implementation.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Spec defines all Phase II features |
| II. Clean Architecture | PASS | Existing layers: Domain (models) → Service → CLI |
| III. Correctness Over Optimization | PASS | Simple, readable implementation |
| IV. Graceful CLI Behavior | PASS | Existing patterns for menus and messages |
| V. Code Quality | PASS | Following PEP 8, existing code style |
| VI. Manual Verification | PASS | All features testable via CLI |

**Gate Result**: PASS - No violations

## Project Structure

### Documentation (this feature)

```text
specs/002-intermediate-enhancements/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # How to test the feature
└── checklists/
    └── requirements.md  # Validation checklist
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # Entry point
├── models/
│   ├── __init__.py
│   └── todo.py          # Todo entity (ALREADY HAS priority, category)
├── services/
│   ├── __init__.py
│   └── todo_service.py  # Business logic (ALREADY HAS search, filter, sort)
└── cli/
    ├── __init__.py
    └── menu.py          # CLI interface (NEEDS MENU UPDATES)
```

**Structure Decision**: Single project with Domain → Service → CLI layers

## Architecture Overview

### Current State Analysis

**Already Implemented (Backend)**:
1. **Todo Model** (`src/models/todo.py`):
   - `priority`: str (high/medium/low)
   - `category`: str (work/personal/shopping/health/general)

2. **TodoService** (`src/services/todo_service.py`):
   - `search(query)`: Search by keyword
   - `filter_by_status(completed)`: Filter pending/completed
   - `filter_by_category(category)`: Filter by category
   - `filter_by_priority(priority)`: Filter by priority
   - `sort_by_priority()`: Sort High → Medium → Low
   - `sort_by_due_date()`: Sort by due date

3. **CLI Handlers** (`src/cli/menu.py`):
   - `handle_search()`: Search handler exists
   - `handle_filter()`: Filter handler exists
   - `handle_sort()`: Sort handler exists

**NOT Implemented (CLI Menu)**:
- Main menu only shows options 1-6 (Add, View, Update, Delete, Mark, Exit)
- Search, Filter, Sort handlers exist but are NOT in the menu

### What Needs to Change

**Menu Update Required** (`src/cli/menu.py`):
1. Add menu option [6] Search
2. Add menu option [7] Filter
3. Add menu option [8] Sort
4. Move Exit to option [9]
5. Update `run_cli()` to route choices 6, 7, 8, 9

## Feature Decomposition

### 1. Priorities & Categories (P1)

**Status**: ALREADY IMPLEMENTED

**Data Representation**:
- Priority: String enum ("high", "medium", "low"), default "medium"
- Category: String enum (work/personal/shopping/health/general), default "general"

**CLI Input/Output**:
- `get_priority_input()`: Shows numbered menu for priority selection
- `get_category_input()`: Shows numbered menu for category selection
- `format_todo()`: Displays priority with color-coded symbols (!!!, !!, !)
- `format_todo()`: Displays category with color-coded icons ([W], [P], etc.)

**Update Integration**:
- `handle_update_todo()`: Allows priority/category change via shorthand (h/m/l, w/p/s/h/g)

### 2. Search & Filter (P2)

**Search Strategy**:
- Case-insensitive substring matching
- Searches both title and description
- Empty query returns all tasks
- Returns new list, does NOT modify stored data

**Filter Logic**:
- Filter by status: pending (completed=False), completed (completed=True), all
- Filter by category: matches exact category string
- Filter by priority: matches exact priority string
- All filters return new lists, non-destructive

**Result Presentation**:
- Uses existing `display_todos()` function
- Shows progress bar and task cards
- Custom header for each result type

### 3. Sort Tasks (P3)

**Sorting Rules**:
- By Priority: High (0) → Medium (1) → Low (2)
- By Due Date: Earliest first, no-date tasks last
- By ID: Default ascending order

**Non-Mutating Implementation**:
- All sort methods return new sorted lists
- Original `_todos` dictionary is never reordered
- Sort is a view operation only

## User Flow Mapping

### Flow 1: Search by Keyword

```
User Input           → Validation           → Processing         → Output
--------------------------------------------------------------------------------
Select [6] Search    → Valid menu choice    → Show search prompt → "Enter search term:"
Enter "groceries"    → Non-empty string     → service.search()   → Matching todos list
                     → Strip whitespace     → Filter by keyword  → "SEARCH RESULTS: 'groceries'"
```

### Flow 2: Filter by Priority

```
User Input           → Validation           → Processing         → Output
--------------------------------------------------------------------------------
Select [7] Filter    → Valid menu choice    → Show filter menu   → Filter type options
Select [3] Priority  → Valid sub-choice     → Show priority opts → Priority options (H/M/L)
Select [1] High      → Valid priority       → filter_by_priority → "HIGH PRIORITY TODOS"
                     → Map "1" → "high"     → Return new list    → Display filtered todos
```

### Flow 3: Sort Task List

```
User Input           → Validation           → Processing         → Output
--------------------------------------------------------------------------------
Select [8] Sort      → Valid menu choice    → Show sort menu     → Sort options
Select [1] Priority  → Valid sort choice    → sort_by_priority() → "SORTED BY PRIORITY"
                     → Map to sort method   → Return sorted list → High→Medium→Low order
```

## Key Decisions & Trade-offs

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Priority storage | String "high/medium/low" | Simple, readable, extensible | Integer (less readable) |
| Category approach | Single category per task | Simpler UX, spec requirement | Multiple tags (complex) |
| Search matching | Case-insensitive substring | User-friendly, expected behavior | Exact match (too strict) |
| Filter behavior | Non-destructive | Spec requirement FR-017 | In-place modification |
| Sort behavior | Returns new list | Spec requirement FR-020 | Modifies stored order |

## Complexity Tracking

> No violations - implementation follows constitution constraints

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| Menu expansion | Low | Adding 3 menu items |
| Backend changes | None | Already implemented |
| New dependencies | None | Using existing colorama |

## Implementation Sequence

### Phase 1: CLI Menu Updates (ONLY CHANGE NEEDED)

1. **Update `display_menu()`** in `menu.py`:
   - Add option [6] Search Todos
   - Add option [7] Filter Todos
   - Add option [8] Sort Todos
   - Add option [9] Exit (moved from [6])

2. **Update `run_cli()`** in `menu.py`:
   - Add `elif choice == "6": handle_search(service)`
   - Add `elif choice == "7": handle_filter(service)`
   - Add `elif choice == "8": handle_sort(service)`
   - Change exit from `choice == "6"` to `choice == "9"`
   - Update prompt: "Enter choice (1-9)"
   - Update error message range

### Verification

All features can be manually tested:
1. Add tasks with different priorities/categories
2. Use Search to find by keyword
3. Use Filter to show subsets
4. Use Sort to reorder display
5. Verify original data unchanged after filter/sort
