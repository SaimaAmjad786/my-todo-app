# Implementation Plan: Todo App Advanced Level (Intelligent Features)

**Branch**: `003-advanced-intelligent-features` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-advanced-intelligent-features/spec.md`

## Summary

This plan implements Phase III (Advanced Level) enhancements for the Todo CLI application: recurring tasks, due time support, and automated reminders. The implementation extends the existing model and service layer while adding reminder checks to the CLI loop.

**Key Finding**: The existing codebase already has `due_date` field. This plan adds `due_time` and `recurrence` fields, plus reminder and auto-regeneration logic.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: colorama (CLI colors), datetime (standard library)
**Storage**: JSON file persistence (todos.json)
**Testing**: Manual CLI verification
**Target Platform**: Windows/Linux/macOS CLI
**Project Type**: Single project
**Performance Goals**: Instant response for all operations (<2 seconds)
**Constraints**: CLI-only, no background threads, no external notifications, no timezone handling
**Scale/Scope**: Personal task management (hundreds of tasks)

## Constitution Check

*GATE: Must pass before implementation.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Spec defines all Phase III features |
| II. Clean Architecture | PASS | Maintains Domain -> Service -> CLI layers |
| III. Correctness Over Optimization | PASS | Simple, readable date/time logic |
| IV. Graceful CLI Behavior | PASS | Non-blocking reminders, clear prompts |
| V. Code Quality | PASS | Following PEP 8, small functions |
| VI. Manual Verification | PASS | All features testable via CLI |

**Gate Result**: PASS - No violations

## Project Structure

### Documentation (this feature)

```text
specs/003-advanced-intelligent-features/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # How to test the feature
├── checklists/
│   └── requirements.md  # Validation checklist
└── tasks.md             # Phase 2 output (from /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # Entry point
├── models/
│   ├── __init__.py
│   └── todo.py          # Todo entity (ADD: due_time, recurrence)
├── services/
│   ├── __init__.py
│   └── todo_service.py  # Business logic (ADD: reminder, recurrence methods)
└── cli/
    ├── __init__.py
    └── menu.py          # CLI interface (ADD: reminder display, recurrence input)
```

**Structure Decision**: Single project with Domain -> Service -> CLI layers (unchanged from Basic/Intermediate)

## Architecture Overview

### Current State Analysis

**Already Implemented**:
1. **Todo Model** (`src/models/todo.py`):
   - `id`, `title`, `description`, `completed`
   - `priority`: str (high/medium/low)
   - `category`: str (work/personal/shopping/health/general)
   - `due_date`: str (YYYY-MM-DD) - ALREADY EXISTS

2. **TodoService** (`src/services/todo_service.py`):
   - CRUD operations
   - Search, filter, sort methods
   - `get_stats()` already calculates overdue count

3. **CLI** (`src/cli/menu.py`):
   - Menu with 9 options
   - Date input already in `get_due_date_input()`
   - Date display already in `get_due_date_display()`

### What Needs to Change

**Model Extension** (`src/models/todo.py`):
- ADD `due_time: str = ""` - Optional time (HH:MM)
- ADD `recurrence: str = "none"` - Recurrence pattern

**Service Extension** (`src/services/todo_service.py`):
- ADD `get_overdue_todos()` - Get tasks past due datetime
- ADD `get_due_today_todos()` - Get tasks due today
- ADD `get_upcoming_todos()` - Get tasks due in next 7 days
- ADD `create_next_occurrence(todo)` - Generate next recurring task
- MODIFY `set_completed()` - Trigger recurrence on completion
- ADD `filter_by_due_status(status)` - Filter by overdue/today/upcoming

**CLI Extension** (`src/cli/menu.py`):
- ADD `get_due_time_input()` - Time input prompt
- ADD `get_recurrence_input()` - Recurrence selection prompt
- ADD `display_reminders(service)` - Show overdue/due tasks
- MODIFY `handle_add_todo()` - Add time and recurrence prompts
- MODIFY `handle_update_todo()` - Add time and recurrence update
- MODIFY `run_cli()` - Call `display_reminders()` before menu
- MODIFY `handle_filter()` - Add due date status filter option

## Feature Decomposition

### 1. Due Time Support (P1)

**Data Representation**:
- `due_time`: String "HH:MM" (24-hour format) or empty string
- Stored separately from `due_date` for clarity
- Only valid if `due_date` is also set

**CLI Input/Output**:
- `get_due_time_input()`: Prompt for HH:MM, validate format
- `get_due_date_display()`: Show both date and time if available
- `format_todo()`: Display time alongside date

**Validation Rules**:
- Time format: HH:MM where HH is 00-23, MM is 00-59
- Time requires date to be set first
- Invalid format shows error, prompts again

### 2. Recurring Tasks (P1)

**Data Representation**:
- `recurrence`: String enum ("none", "daily", "weekly", "monthly")
- Default: "none"

**Recurrence Calculation Logic**:
```
calculate_next_due_date(original_date, recurrence):
  if recurrence == "daily":
    return original_date + 1 day
  if recurrence == "weekly":
    return original_date + 7 days
  if recurrence == "monthly":
    return same day next month (adjusted for month length)
```

**Auto-Regeneration on Completion**:
- When `set_completed(id, True)` is called on a recurring task:
  1. Mark original task complete (don't modify further)
  2. Create new task with:
     - New unique ID
     - Same title, description, priority, category, recurrence
     - Calculated next due date (and same due time if set)
     - completed = False
  3. Return both original (completed) and new task info

### 3. Reminders (P2)

**Reminder Strategy**:
- Check timing: Before main menu display (FR-016)
- Check on startup (FR-015) - same location works

**Implementation**:
```
display_reminders(service):
  overdue = service.get_overdue_todos()
  due_now = service.get_due_now_todos()  # due today, time passed or no time

  if overdue or due_now:
    print reminder banner
    for each task:
      print title, due date/time, overdue duration
    print separator
```

**Non-Blocking Behavior**:
- Reminders are print statements only
- No input required to dismiss
- User proceeds directly to menu

### 4. Due Date Status Filters (P3)

**Filter Options**:
- Overdue: `due_date < today` OR (`due_date == today` AND `due_time < now`)
- Due Today: `due_date == today`
- Upcoming: `due_date` within next 7 days (inclusive)

**Integration**:
- Add to existing `handle_filter()` as option [4] Due Date Status
- Sub-menu: [1] Overdue, [2] Due Today, [3] Upcoming

## User Flow Mapping

### Flow 1: Create Recurring Task

```
User Input           -> Validation           -> Processing         -> Output
--------------------------------------------------------------------------------
Select [1] Add       -> Valid menu choice    -> Show add prompts   -> Title prompt
Enter "Daily standup"-> Non-empty string     -> Store title        -> Description prompt
Enter ""             -> Optional, accepted   -> Store empty        -> Priority prompt
Select [2] Medium    -> Valid choice         -> Store medium       -> Category prompt
Select [1] Work      -> Valid choice         -> Store work         -> Due date prompt
Enter "2025-12-28"   -> Valid YYYY-MM-DD     -> Store date         -> Due time prompt
Enter "09:00"        -> Valid HH:MM          -> Store time         -> Recurrence prompt
Select [1] Daily     -> Valid choice         -> Store daily        -> Create todo
                     ->                      -> service.add()      -> Success message
```

### Flow 2: Complete Recurring Task

```
User Input           -> Validation           -> Processing         -> Output
--------------------------------------------------------------------------------
Select [5] Mark      -> Valid menu choice    -> Show mark prompt   -> ID prompt
Enter "1"            -> Valid ID             -> Get todo           -> Show current status
Select (c)omplete    -> Valid choice         -> Check recurrence   -> If recurring...
                     -> task.recurrence!=none-> Create new task    -> Show celebration
                     ->                      -> Calculate next date -> "Next occurrence created"
                     ->                      -> service.add()      -> Show new task ID
```

### Flow 3: View Reminders on Startup

```
Startup              -> Check               -> Processing          -> Output
--------------------------------------------------------------------------------
App starts           -> Check overdue       -> get_overdue_todos() -> If any exist...
                     -> Check due now       -> get_due_now()       -> Print banner
                     ->                     -> Format each         -> "REMINDERS"
                     ->                     ->                     -> Task list
                     ->                     ->                     -> Separator
                     -> Continue            ->                     -> Display menu
```

## Key Decisions & Trade-offs

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Time storage | Separate `due_time` field | Simpler validation, clearer display | Combined datetime (parsing complexity) |
| Recurrence storage | String enum | Matches existing patterns (priority) | Integer codes (less readable) |
| Reminder timing | Before menu display | Spec requirement FR-016, non-blocking | After each action (too frequent) |
| Next date calculation | datetime utilities | Reliable month handling | Manual arithmetic (edge case bugs) |
| Overdue threshold | datetime.now() | Local time per spec assumption | UTC (complexity, not needed) |

## Complexity Tracking

> No violations - implementation follows constitution constraints

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| Model extension | Low | Adding 2 string fields |
| Recurrence logic | Medium | Date arithmetic with month edge cases |
| Reminder display | Low | Simple print before menu |
| Filter extension | Low | 3 new filter methods |

## Implementation Sequence

### Phase 1: Model Extension

1. **Add fields to Todo model** (`src/models/todo.py`):
   - `due_time: str = ""`
   - `recurrence: str = "none"`

2. **Update TodoService load/save** for backward compatibility:
   - Handle old todos without `due_time`/`recurrence` fields

### Phase 2: Service Layer

3. **Add recurrence calculation** (`src/services/todo_service.py`):
   - `calculate_next_due_date(due_date, recurrence)` helper
   - Handle monthly edge cases (29th, 30th, 31st)

4. **Modify `set_completed()`** to handle recurrence:
   - If recurring and marking complete, create next occurrence
   - Return both completed task and new task (if created)

5. **Add reminder query methods**:
   - `get_overdue_todos()` - past due datetime
   - `get_due_today_todos()` - due date is today
   - `get_upcoming_todos(days=7)` - due within N days

6. **Add due status filter** (`filter_by_due_status(status)`):
   - status: "overdue", "today", "upcoming"

### Phase 3: CLI Updates

7. **Add input helpers** (`src/cli/menu.py`):
   - `get_due_time_input()` - validate HH:MM format
   - `get_recurrence_input()` - selection menu

8. **Update display functions**:
   - `format_todo()` - show time and recurrence
   - `get_due_date_display()` - include time if present

9. **Add `display_reminders(service)`**:
   - Called before `display_menu()` in `run_cli()`
   - Shows overdue and due-now tasks

10. **Update handlers**:
    - `handle_add_todo()` - add time and recurrence prompts
    - `handle_update_todo()` - add time and recurrence update
    - `handle_mark_todo()` - show next occurrence message

11. **Update `handle_filter()`**:
    - Add option [4] Due Date Status
    - Sub-menu for overdue/today/upcoming

### Phase 4: Integration & Testing

12. **Update `run_cli()` loop**:
    - Call `display_reminders(service)` before each menu display

13. **Manual testing**:
    - Create tasks with various due dates/times/recurrences
    - Verify reminder display on startup and menu refresh
    - Complete recurring tasks, verify next occurrence
    - Test all filter options

## Verification Checklist

All features can be manually tested:
1. Add task with due date, due time, and recurrence pattern
2. View task list - verify date/time/recurrence display
3. Update task - change time and recurrence
4. Start app with overdue tasks - verify reminders appear
5. Complete recurring task - verify new task created
6. Verify daily recurrence adds 1 day
7. Verify weekly recurrence adds 7 days
8. Verify monthly recurrence handles edge cases
9. Filter by overdue/today/upcoming
10. Verify Basic and Intermediate features still work
