---
id: 004
title: Implement Advanced Intelligent Features
stage: green
date: 2025-12-28
surface: agent
model: claude-opus-4-5-20251101
feature: 003-advanced-intelligent-features
branch: 003-advanced-intelligent-features
user: hp
command: /sp.implement
labels: ["implementation", "recurring-tasks", "due-time", "reminders", "filters"]
links:
  spec: specs/003-advanced-intelligent-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/models/todo.py
  - src/services/todo_service.py
  - src/cli/menu.py
  - specs/003-advanced-intelligent-features/tasks.md
tests:
  - Manual test: Create task with date, time, recurrence - verify all display
  - Manual test: Complete recurring task - verify next occurrence created correctly
  - Manual test: Verify daily (+1 day), weekly (+7 days), monthly (edge cases)
  - Manual test: Reminders appear on startup and before each menu
  - Manual test: All due date filters work correctly
  - Regression test: Basic Level features (Add, View, Update, Delete, Mark)
  - Regression test: Intermediate Level features (Search, Filter, Sort)
---

## Prompt

/sp.implement

Implement the Advanced Level (003-advanced-intelligent-features) for the Todo CLI application. This includes:
- Recurring tasks (daily, weekly, monthly patterns)
- Due date and time support
- Deadline reminders
- Due date status filters (overdue, today, upcoming)

## Response snapshot

Successfully implemented all 42 tasks across 8 phases for the Advanced Level features:

**Phase 1: Model Extension (T001-T003)**
- Added `due_time` field (HH:MM format) to Todo dataclass
- Added `recurrence` field (none/daily/weekly/monthly) to Todo dataclass
- Updated `_load()` for backward compatibility with new fields

**Phase 2: Foundational Logic (T004-T007)**
- Added `RECURRENCE_PATTERNS` constant
- Added `is_valid_time()` helper with regex validation
- Added `calculate_next_due_date()` with monthly edge case handling (29th, 30th, 31st)

**Phase 3: US1 - Recurring Tasks (T008-T014)**
- Added `get_recurrence_input()` prompt function
- Updated `add()` to accept recurrence parameter
- Added `create_next_occurrence()` method
- Modified `set_completed()` to return tuple and trigger recurrence logic
- Updated `handle_mark_todo()` to display next occurrence message

**Phase 4: US2 - Due Time (T015-T019)**
- Added `get_due_time_input()` prompt function
- Updated `add()` to accept due_time parameter
- Updated `handle_add_todo()` to prompt for time when date is set
- Updated `format_todo()` to display time with date

**Phase 5: US3 - Reminders (T020-T024)**
- Added `get_overdue_todos()` method
- Added `get_due_now_todos()` method (within 60 minutes)
- Added `display_reminders()` function with colored banners
- Integrated reminders before each menu display

**Phase 6: US4 - Update Recurrence (T025-T027)**
- Updated `update()` to accept recurrence parameter
- Added recurrence update prompts with shorthand (d/w/m/n)

**Phase 7: US5 - Due Date Filters (T028-T032)**
- Added `get_due_today_todos()` method
- Added `get_upcoming_todos()` method (next 7 days)
- Added `filter_by_due_status()` method
- Added option [4] Due Date Status to filter menu with sub-menu

**Phase 8: Polish & Validation (T033-T042)**
- Verified time requires date validation
- Added time update to handle_update_todo()
- Completed all manual and regression tests

## Outcome

- ✅ Impact: All 5 user stories implemented with 22 functional requirements satisfied
- 🧪 Tests: 8 manual tests passed (T035-T042), regression tests verified
- 📁 Files: 3 source files modified (todo.py, todo_service.py, menu.py)
- 🔁 Next prompts: Consider Expert Level features or deployment preparation
- 🧠 Reflection: Clean implementation following task breakdown, tuple return pattern for set_completed() enables clean communication of recurring task creation

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation followed plan precisely
- Graders run and results (PASS/FAIL): PASS - all 42 tasks completed successfully
- Prompt variant (if applicable): Standard /sp.implement workflow
- Next experiment (smallest change to try): Consider adding unit tests for calculate_next_due_date() edge cases
