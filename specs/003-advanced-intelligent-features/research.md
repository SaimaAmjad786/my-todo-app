# Research: Todo App Advanced Level (Intelligent Features)

**Feature**: 003-advanced-intelligent-features
**Date**: 2025-12-27
**Purpose**: Resolve technical decisions and document best practices

## Research Questions

### 1. Date/Time Representation Strategy

**Question**: How should due date and time be stored in the Todo model?

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| Combined datetime string | Single field, easy sorting | Complex parsing, validation overhead |
| Separate date + time fields | Clear validation, existing pattern | Two fields to manage |
| Python datetime object | Native operations | JSON serialization complexity |

**Decision**: Separate `due_date` (str) and `due_time` (str) fields

**Rationale**:
- Existing code already uses `due_date` as string (YYYY-MM-DD)
- Consistent with existing patterns (priority, category are strings)
- Simple JSON serialization (no conversion needed)
- Clear validation rules for each field
- Time is optional and only valid when date is set

### 2. Monthly Recurrence Edge Cases

**Question**: How to handle monthly recurrence when day doesn't exist in target month?

**Options Considered**:

| Option | Behavior | Example |
|--------|----------|---------|
| Skip to next valid month | Jan 31 -> Mar 31 | Misses February entirely |
| Use last day of month | Jan 31 -> Feb 28/29 | Consistent monthly cadence |
| Error/warning | Alert user | Disrupts workflow |

**Decision**: Use last day of target month

**Rationale**:
- Spec assumption: "Monthly recurrence on day 29-31 adjusts to the last valid day"
- User expectation: monthly task should occur once per month
- Python's `calendar.monthrange()` provides month length reliably

**Implementation**:
```python
from datetime import datetime, timedelta
from calendar import monthrange

def calculate_monthly_next(current_date: str) -> str:
    dt = datetime.strptime(current_date, "%Y-%m-%d")
    year, month = dt.year, dt.month + 1
    if month > 12:
        month = 1
        year += 1
    max_day = monthrange(year, month)[1]
    target_day = min(dt.day, max_day)
    return f"{year:04d}-{month:02d}-{target_day:02d}"
```

### 3. Reminder Triggering Strategy

**Question**: When should reminders be displayed?

**Options Considered**:

| Option | Frequency | User Impact |
|--------|-----------|-------------|
| On every action | After each menu selection | Annoying, repetitive |
| Before menu display only | Once per menu cycle | Balanced, non-intrusive |
| Only on startup | Once per session | Might miss real-time due |

**Decision**: Before main menu display (includes startup)

**Rationale**:
- Spec requirement FR-015: "check on application startup"
- Spec requirement FR-016: "check before each main menu display"
- Single implementation point (`run_cli()` loop)
- Non-blocking per FR-019
- Catches tasks that become due during session

### 4. Recurrence on Completion Return Value

**Question**: What should `set_completed()` return when creating a recurring task?

**Options Considered**:

| Option | Return Value | Caller Impact |
|--------|--------------|---------------|
| Original task only | `Todo` | Caller unaware of new task |
| Tuple (original, new) | `tuple[Todo, Todo|None]` | Type change, breaking |
| Dict with both | `dict` | Flexible but inconsistent |
| New task ID in response | `Todo` with metadata | Complex |

**Decision**: Return tuple `(completed_task, new_task_or_none)`

**Rationale**:
- CLI needs to inform user about new task
- Type hint clearly shows possibility of new task
- None when not recurring (backward compatible logic)
- Clean separation: service creates, CLI displays

**Implementation Note**:
```python
def set_completed(self, todo_id: int, completed: bool) -> tuple[Todo | None, Todo | None]:
    """Returns (completed_task, new_recurring_task_or_none)"""
```

### 5. Time Validation Format

**Question**: How strict should time format validation be?

**Options Considered**:

| Format | Accepted | Rejected |
|--------|----------|----------|
| Strict HH:MM | "09:00", "23:59" | "9:00", "9:0", "24:00" |
| Lenient | "9:00", "09:00" | "9", "900" |
| Very lenient | "9", "9:0", "09:00" | Nothing |

**Decision**: Strict HH:MM format (24-hour)

**Rationale**:
- Spec says HH:MM 24-hour format
- Clear and unambiguous
- Easy to validate with regex: `^([01]?\d|2[0-3]):[0-5]\d$`
- User-friendly error message guides correct input

**Validation Regex**:
```python
import re
TIME_PATTERN = re.compile(r'^([01]?\d|2[0-3]):[0-5]\d$')

def is_valid_time(time_str: str) -> bool:
    return bool(TIME_PATTERN.match(time_str))
```

### 6. Overdue Detection Logic

**Question**: How to determine if a task is overdue?

**Decision**: Compare full datetime when time is set, date only otherwise

**Logic**:
```python
from datetime import datetime

def is_overdue(todo: Todo) -> bool:
    if not todo.due_date:
        return False

    now = datetime.now()
    due_date = datetime.strptime(todo.due_date, "%Y-%m-%d")

    if todo.due_time:
        due_datetime = datetime.strptime(
            f"{todo.due_date} {todo.due_time}",
            "%Y-%m-%d %H:%M"
        )
        return now > due_datetime
    else:
        # No time: overdue if date has passed (not today)
        return due_date.date() < now.date()
```

## Findings Summary

| Topic | Decision | Key Rationale |
|-------|----------|---------------|
| Date/time storage | Separate string fields | Existing pattern, simple serialization |
| Monthly edge case | Use last day of month | Consistent monthly cadence |
| Reminder timing | Before menu display | Spec requirements FR-015/016 |
| Completion return | Tuple (task, new_or_none) | CLI needs new task info |
| Time validation | Strict HH:MM | Clear format per spec |
| Overdue logic | Datetime comparison | Accurate to the minute when time set |

## Dependencies

No new external dependencies required. Using only:
- `datetime` (standard library)
- `calendar` (standard library)
- `re` (standard library, for time validation)
- `colorama` (already installed)

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Backward compatibility | Old todos missing new fields | Default values in `_load()` |
| Time parsing errors | App crash | Try/except with user message |
| Month boundary bugs | Wrong next date | Use `calendar.monthrange()` |
| Reminder spam | Poor UX | Only show before menu, not after actions |
