# Tasks: Todo App Advanced Level (Intelligent Features)

**Input**: Design documents from `/specs/003-advanced-intelligent-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- Paths: `src/models/todo.py`, `src/services/todo_service.py`, `src/cli/menu.py`

---

## Phase 1: Setup (Model Extension)

**Purpose**: Extend domain model with new fields for Advanced Level

- [X] T001 Add due_time field to Todo dataclass in src/models/todo.py
- [X] T002 Add recurrence field to Todo dataclass in src/models/todo.py
- [X] T003 Update TodoService._load() for backward compatibility with new fields in src/services/todo_service.py

**Checkpoint**: Model extended, old todos load correctly with default values

---

## Phase 2: Foundational (Validation & Core Logic)

**Purpose**: Validation helpers and recurrence calculation that ALL user stories depend on

- [X] T004 Add RECURRENCE_PATTERNS constant (none, daily, weekly, monthly) in src/services/todo_service.py
- [X] T005 [P] Add is_valid_time() helper function for HH:MM validation in src/cli/menu.py
- [X] T006 [P] Add calculate_next_due_date() helper function in src/services/todo_service.py
- [X] T007 Implement monthly edge case handling (29th, 30th, 31st) in calculate_next_due_date() in src/services/todo_service.py

**Checkpoint**: Validation and calculation logic ready - user story implementation can begin

---

## Phase 3: User Story 1 - Create Recurring Tasks (Priority: P1)

**Goal**: Users can create tasks with recurrence patterns (daily/weekly/monthly) and completing them auto-generates the next occurrence

**Independent Test**: Create a daily recurring task, mark complete, verify new task created with tomorrow's date

### Implementation for US1

- [X] T008 [US1] Add get_recurrence_input() prompt function in src/cli/menu.py
- [X] T009 [US1] Update TodoService.add() to accept recurrence parameter in src/services/todo_service.py
- [X] T010 [US1] Update handle_add_todo() to prompt for recurrence in src/cli/menu.py
- [X] T011 [US1] Add create_next_occurrence() method in src/services/todo_service.py
- [X] T012 [US1] Modify set_completed() to trigger recurrence logic in src/services/todo_service.py
- [X] T013 [US1] Update handle_mark_todo() to display next occurrence message in src/cli/menu.py
- [X] T014 [US1] Add recurrence display to format_todo() in src/cli/menu.py

**Checkpoint**: Recurring tasks work - create, complete, verify auto-regeneration

---

## Phase 4: User Story 2 - Set Due Date and Time (Priority: P1)

**Goal**: Users can set optional due time (HH:MM) in addition to due date

**Independent Test**: Create task with date and time, verify both display correctly

### Implementation for US2

- [X] T015 [US2] Add get_due_time_input() prompt function in src/cli/menu.py
- [X] T016 [US2] Update TodoService.add() to accept due_time parameter in src/services/todo_service.py
- [X] T017 [US2] Update handle_add_todo() to prompt for due time (only if date set) in src/cli/menu.py
- [X] T018 [US2] Update get_due_date_display() to include time if present in src/cli/menu.py
- [X] T019 [US2] Update format_todo() to show due time in src/cli/menu.py

**Checkpoint**: Due time works - create task with time, verify display

---

## Phase 5: User Story 3 - Receive Deadline Reminders (Priority: P2)

**Goal**: Overdue and due-now tasks display reminders before each menu

**Independent Test**: Create overdue task, restart app, verify reminder displays before menu

### Implementation for US3

- [X] T020 [US3] Add get_overdue_todos() method in src/services/todo_service.py
- [X] T021 [US3] Add get_due_now_todos() method in src/services/todo_service.py
- [X] T022 [US3] Add display_reminders() function in src/cli/menu.py
- [X] T023 [US3] Format reminder messages with title, due date/time, overdue duration in src/cli/menu.py
- [X] T024 [US3] Call display_reminders() before display_menu() in run_cli() in src/cli/menu.py

**Checkpoint**: Reminders work - overdue tasks show reminder banner on startup and before each menu

---

## Phase 6: User Story 4 - Manage Recurring Task Settings (Priority: P2)

**Goal**: Users can update recurrence pattern on existing tasks

**Independent Test**: Update a recurring task to change or remove recurrence

### Implementation for US4

- [X] T025 [US4] Update TodoService.update() to accept recurrence parameter in src/services/todo_service.py
- [X] T026 [US4] Update handle_update_todo() to prompt for recurrence change in src/cli/menu.py
- [X] T027 [US4] Add shorthand input for recurrence (d/w/m/n) in handle_update_todo() in src/cli/menu.py

**Checkpoint**: Recurrence update works - change daily to weekly, remove recurrence

---

## Phase 7: User Story 5 - View Tasks by Due Date Status (Priority: P3)

**Goal**: Filter tasks by overdue, due today, or upcoming (next 7 days)

**Independent Test**: Create tasks with various dates, filter by each status, verify correct results

### Implementation for US5

- [X] T028 [US5] Add get_due_today_todos() method in src/services/todo_service.py
- [X] T029 [US5] Add get_upcoming_todos() method in src/services/todo_service.py
- [X] T030 [US5] Add filter_by_due_status() method in src/services/todo_service.py
- [X] T031 [US5] Update handle_filter() to add option [4] Due Date Status in src/cli/menu.py
- [X] T032 [US5] Implement due status sub-menu (Overdue/Today/Upcoming) in handle_filter() in src/cli/menu.py

**Checkpoint**: Due date filters work - filter by overdue, today, upcoming

---

## Phase 8: Polish & Validation

**Purpose**: Final integration, error handling, and regression testing

- [X] T033 Verify time requires date validation in handle_add_todo() in src/cli/menu.py
- [X] T034 Add time update to handle_update_todo() in src/cli/menu.py
- [X] T035 Manual test: Create task with date, time, recurrence - verify all display
- [X] T036 Manual test: Complete recurring task - verify next occurrence created correctly
- [X] T037 Manual test: Verify daily (+1 day), weekly (+7 days), monthly (edge cases)
- [X] T038 Manual test: Reminders appear on startup and before each menu
- [X] T039 Manual test: All due date filters work correctly
- [X] T040 Regression test: Basic Level features (Add, View, Update, Delete, Mark)
- [X] T041 Regression test: Intermediate Level features (Search, Filter, Sort)
- [X] T042 Run quickstart.md validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion
- **Phase 3-7 (User Stories)**: All depend on Phase 2 completion
- **Phase 8 (Polish)**: Depends on all user stories

### User Story Dependencies

- **US1 (Recurring Tasks)**: Depends on Phase 2 only
- **US2 (Due Time)**: Depends on Phase 2 only - independent of US1
- **US3 (Reminders)**: Can use US2 time display but core logic independent
- **US4 (Update Recurrence)**: Depends on US1 (recurrence must exist first)
- **US5 (Due Date Filters)**: Uses methods from US3 but independently testable

### Task Dependencies Within Phases

```
Phase 1: T001 -> T002 -> T003 (sequential, same files)
Phase 2: T004 -> T005 [P] T006 -> T007 (T005 parallel with T006)
Phase 3: T008 -> T009 -> T010 -> T011 -> T012 -> T013 -> T014
Phase 4: T015 -> T016 -> T017 -> T018 -> T019
Phase 5: T020 [P] T021 -> T022 -> T023 -> T024
Phase 6: T025 -> T026 -> T027
Phase 7: T028 [P] T029 -> T030 -> T031 -> T032
Phase 8: All can run sequentially as manual tests
```

### Parallel Opportunities

Phase 2 parallel tasks:
- T005 (time validation) and T006 (date calculation) - different purposes

Phase 5 parallel tasks:
- T020 (overdue) and T021 (due now) - different methods

Phase 7 parallel tasks:
- T028 (today) and T029 (upcoming) - different methods

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T007)
3. Complete Phase 3: US1 - Recurring Tasks (T008-T014)
4. Complete Phase 4: US2 - Due Time (T015-T019)
5. **STOP and VALIDATE**: Test recurring + time features

### Incremental Delivery

1. Setup + Foundational -> Core ready
2. Add US1 (Recurring) -> Test independently
3. Add US2 (Due Time) -> Test independently
4. Add US3 (Reminders) -> Test independently
5. Add US4 (Update Recurrence) -> Test independently
6. Add US5 (Due Date Filters) -> Test independently
7. Polish phase for final validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story is independently testable
- No automated tests - manual CLI verification only
- Commit after each task or logical group
- due_date already exists in model - only adding due_time and recurrence
