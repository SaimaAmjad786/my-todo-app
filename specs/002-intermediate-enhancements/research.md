# Research: Todo App Intermediate Level Enhancements

**Branch**: `002-intermediate-enhancements` | **Date**: 2025-12-27

## Research Summary

This document captures research findings for Phase II (Intermediate Level) features.

## Key Finding: Backend Already Implemented

After analyzing the existing codebase, ALL backend features for Phase II are already implemented:

### Existing Implementation Status

| Feature | Model Layer | Service Layer | CLI Handler | Menu Exposed |
|---------|-------------|---------------|-------------|--------------|
| Priority | `todo.priority` | validation in `add()`, `update()` | `get_priority_input()` | YES (add/update) |
| Category | `todo.category` | `CATEGORIES` list, validation | `get_category_input()` | YES (add/update) |
| Search | N/A | `search(query)` | `handle_search()` | **NO** |
| Filter by Status | N/A | `filter_by_status()` | `handle_filter()` | **NO** |
| Filter by Category | N/A | `filter_by_category()` | `handle_filter()` | **NO** |
| Filter by Priority | N/A | `filter_by_priority()` | `handle_filter()` | **NO** |
| Sort by Priority | N/A | `sort_by_priority()` | `handle_sort()` | **NO** |
| Sort by Due Date | N/A | `sort_by_due_date()` | `handle_sort()` | **NO** |

## Decision 1: Priority Storage Format

**Decision**: Use string enum ("high", "medium", "low")

**Rationale**:
- Already implemented this way in existing code
- Human-readable in JSON storage
- Easy to validate and display
- Consistent with category approach

**Alternatives Considered**:
- Integer (0, 1, 2): Less readable, requires mapping for display
- Python Enum class: Over-engineering for simple CLI app

## Decision 2: Category Structure

**Decision**: Single predefined category per task

**Rationale**:
- Simpler UX for CLI input
- Matches spec requirement (single category, not multiple tags)
- Predefined list prevents typos: work, personal, shopping, health, general

**Alternatives Considered**:
- Multiple tags: More complex input/output, not in spec
- Custom categories: Requires category management feature, out of scope

## Decision 3: Search Implementation

**Decision**: Case-insensitive substring matching on title + description

**Rationale**:
- Already implemented correctly in `TodoService.search()`
- User-friendly: "milk" matches "Buy MILK"
- Non-destructive: Returns new list

**Implementation Details**:
```python
def search(self, query: str) -> list[Todo]:
    query = query.lower().strip()
    if not query:
        return self.get_all()
    return [t for t in self._todos.values()
            if query in t.title.lower() or query in t.description.lower()]
```

## Decision 4: Filter Behavior

**Decision**: All filters are non-destructive view operations

**Rationale**:
- Spec requirement FR-017: "Filters MUST NOT permanently modify stored task data"
- Each filter method returns a new list
- Original `_todos` dictionary unchanged

## Decision 5: Sort Behavior

**Decision**: All sorts are non-destructive view operations

**Rationale**:
- Spec requirement FR-020: "Sort MUST NOT permanently modify stored task order"
- Python's `sorted()` returns new list by default
- Existing implementation already follows this pattern

## Conclusion

No new backend development required. Only CLI menu needs updating to expose existing functionality.
