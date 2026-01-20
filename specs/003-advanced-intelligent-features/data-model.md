# Data Model: Todo App Advanced Level

**Feature**: 003-advanced-intelligent-features
**Date**: 2025-12-27
**Source**: [spec.md](./spec.md) Key Entities section

## Entity: Todo (Extended)

### Current Fields (from Basic + Intermediate)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-generated | Unique identifier, auto-incremented |
| title | str | Yes | - | Task name, non-empty |
| description | str | No | "" | Additional details |
| completed | bool | No | False | Completion status |
| priority | str | No | "medium" | Priority level: high, medium, low |
| due_date | str | No | "" | Due date in YYYY-MM-DD format |
| category | str | No | "general" | Category: work, personal, shopping, health, general |

### New Fields (Advanced Level)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| due_time | str | No | "" | Due time in HH:MM format (24-hour) |
| recurrence | str | No | "none" | Recurrence pattern: none, daily, weekly, monthly |

### Field Constraints

#### due_time
- Format: `HH:MM` (24-hour)
- Valid range: `00:00` to `23:59`
- Requires `due_date` to be set (cannot have time without date)
- Empty string if not specified

#### recurrence
- Allowed values: `none`, `daily`, `weekly`, `monthly`
- Default: `none`
- When not `none`, completing the task triggers auto-regeneration

### Complete Todo Structure

```python
@dataclass
class Todo:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "medium"      # high | medium | low
    due_date: str = ""            # YYYY-MM-DD
    category: str = "general"     # work | personal | shopping | health | general
    due_time: str = ""            # HH:MM (24-hour) - NEW
    recurrence: str = "none"      # none | daily | weekly | monthly - NEW
```

## Enumeration: Recurrence Pattern

| Value | Description | Date Calculation |
|-------|-------------|------------------|
| none | One-time task (default) | N/A |
| daily | Repeats every day | +1 day |
| weekly | Repeats every 7 days | +7 days |
| monthly | Repeats same day each month | Same day next month (adjusted for month length) |

### Monthly Edge Cases

| Original Date | Next Month Has | Result |
|---------------|----------------|--------|
| Jan 31 | 28 days (Feb) | Feb 28 |
| Jan 31 | 29 days (Feb leap) | Feb 29 |
| Mar 31 | 30 days (Apr) | Apr 30 |
| Aug 31 | 30 days (Sep) | Sep 30 |

## JSON Serialization Format

```json
{
  "todos": [
    {
      "id": 1,
      "title": "Daily standup",
      "description": "Team sync meeting",
      "completed": false,
      "priority": "medium",
      "due_date": "2025-12-28",
      "category": "work",
      "due_time": "09:00",
      "recurrence": "daily"
    }
  ],
  "next_id": 2
}
```

## Backward Compatibility

Old todos without `due_time` and `recurrence` fields must be handled:

```python
def _load(self) -> None:
    # ... existing load logic ...
    for todo_data in data.get("todos", []):
        # Handle old todos without new fields
        if "due_time" not in todo_data:
            todo_data["due_time"] = ""
        if "recurrence" not in todo_data:
            todo_data["recurrence"] = "none"
        # ... rest of load logic ...
```

## Validation Rules

### Date Validation
- Format: `YYYY-MM-DD`
- Must be a valid calendar date
- Regex: `^\d{4}-\d{2}-\d{2}$` (basic format check)
- Full validation: `datetime.strptime(date, "%Y-%m-%d")`

### Time Validation
- Format: `HH:MM` (24-hour)
- Hours: 00-23
- Minutes: 00-59
- Regex: `^([01]?\d|2[0-3]):[0-5]\d$`
- Time requires date to be set first

### Recurrence Validation
- Must be one of: `none`, `daily`, `weekly`, `monthly`
- Default to `none` if invalid value provided

## State Transitions

### Task Lifecycle with Recurrence

```
[Created] --> [Pending] --> [Completed]
                               |
                               v (if recurrence != "none")
                        [New Task Created]
                               |
                               v
                          [Pending]
```

### Recurrence on Completion

When a recurring task is marked complete:
1. Original task: `completed = True` (no other changes)
2. New task created with:
   - New unique ID
   - `completed = False`
   - Same: title, description, priority, category, due_time, recurrence
   - New `due_date` calculated from recurrence pattern

## Relationships

```
Todo (1) -----> (0..1) Due DateTime
     |
     +--------> (1) Priority (enum)
     |
     +--------> (1) Category (enum)
     |
     +--------> (1) Recurrence Pattern (enum)
```

- No foreign keys (single entity model)
- All relationships are attribute-based
- No cascading deletes or updates needed
