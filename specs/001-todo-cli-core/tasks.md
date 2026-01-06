# Tasks: Todo CLI Core (Phase I)

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Manual CLI verification only (no automated tests for Phase I per plan.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root (per plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: src/, src/models/, src/services/, src/cli/
- [x] T002 Create pyproject.toml with Python 3.13+ requirement and UV configuration
- [x] T003 [P] Create src/__init__.py (empty package marker)
- [x] T004 [P] Create src/models/__init__.py (empty package marker)
- [x] T005 [P] Create src/services/__init__.py (empty package marker)
- [x] T006 [P] Create src/cli/__init__.py (empty package marker)
- [x] T007 Create src/main.py with basic entry point that prints startup message

**Checkpoint**: Project runs with `uv run python -m src.main` and displays startup message

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create Todo dataclass in src/models/todo.py with fields: id (int), title (str), description (str=""), completed (bool=False)
- [x] T009 Create TodoService class in src/services/todo_service.py with _todos dict and _next_id counter
- [x] T010 Implement TodoService.get_all() method returning list of all todos ordered by ID
- [x] T011 Create display_menu() function in src/cli/menu.py showing 6 options (Add, View, Update, Delete, Mark, Exit)
- [x] T012 Create run_cli() function in src/cli/menu.py with main loop and menu option dispatch
- [x] T013 Update src/main.py to import and call run_cli() from src/cli/menu.py
- [x] T014 Add graceful exit handling (option 6) in src/cli/menu.py

**Checkpoint**: Application displays menu, accepts option 6 to exit gracefully

---

## Phase 3: User Story 1 - Add New Todo (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new todos with title and optional description

**Independent Test**: Run app, select Add, enter title "Test", verify confirmation shows ID 1

### Implementation for User Story 1

- [x] T015 [US1] Implement TodoService.add(title, description) method in src/services/todo_service.py
- [x] T016 [US1] Add title validation in TodoService.add() - reject empty/whitespace-only titles
- [x] T017 [US1] Create handle_add_todo() function in src/cli/menu.py prompting for title and description
- [x] T018 [US1] Wire menu option 1 to handle_add_todo() in run_cli() loop
- [x] T019 [US1] Display success message with new todo ID after adding in src/cli/menu.py

**Checkpoint**: Can add todos with title only or title+description; empty titles rejected with error message

---

## Phase 4: User Story 2 - View All Todos (Priority: P2)

**Goal**: Display all todos with ID, title, description, and completion status indicators

**Independent Test**: Add 2-3 todos, select View, verify all display with [ ] or [x] indicators

### Implementation for User Story 2

- [x] T020 [US2] Create format_todo(todo) function in src/cli/menu.py returning formatted string with checkbox indicator
- [x] T021 [US2] Create handle_view_todos() function in src/cli/menu.py displaying all todos or "No todos" message
- [x] T022 [US2] Wire menu option 2 to handle_view_todos() in run_cli() loop
- [x] T023 [US2] Display descriptions on separate indented line when present in format_todo()

**Checkpoint**: Empty list shows message; todos display with ID, checkbox status, title, and description if present

---

## Phase 5: User Story 3 - Update Todo (Priority: P3)

**Goal**: Allow updating title and/or description of existing todos

**Independent Test**: Add todo, select Update, change title, View to verify change persisted

### Implementation for User Story 3

- [x] T024 [US3] Implement TodoService.update(id, title, description) method in src/services/todo_service.py
- [x] T025 [US3] Add validation in TodoService.update() - reject empty titles, handle missing ID
- [x] T026 [US3] Create handle_update_todo() function in src/cli/menu.py prompting for ID and new values
- [x] T027 [US3] Add "press Enter to keep current" behavior for optional field updates in handle_update_todo()
- [x] T028 [US3] Wire menu option 3 to handle_update_todo() in run_cli() loop
- [x] T029 [US3] Display success/error messages after update attempt in src/cli/menu.py

**Checkpoint**: Can update title and/or description; missing ID shows error; empty title rejected

---

## Phase 6: User Story 4 - Delete Todo (Priority: P4)

**Goal**: Remove todos permanently by ID

**Independent Test**: Add todo, note ID, delete by ID, View to verify removed

### Implementation for User Story 4

- [x] T030 [US4] Implement TodoService.delete(id) method in src/services/todo_service.py returning bool
- [x] T031 [US4] Create handle_delete_todo() function in src/cli/menu.py prompting for ID
- [x] T032 [US4] Wire menu option 4 to handle_delete_todo() in run_cli() loop
- [x] T033 [US4] Display success/error messages after delete attempt in src/cli/menu.py

**Checkpoint**: Deleted todos no longer appear in view; missing ID shows error; new todos get new IDs (not reused)

---

## Phase 7: User Story 5 - Mark Complete/Incomplete (Priority: P5)

**Goal**: Toggle completion status of todos

**Independent Test**: Add todo, mark complete, View shows [x], mark incomplete, View shows [ ]

### Implementation for User Story 5

- [x] T034 [US5] Implement TodoService.set_completed(id, completed) method in src/services/todo_service.py
- [x] T035 [US5] Create handle_mark_todo() function in src/cli/menu.py prompting for ID and complete/incomplete choice
- [x] T036 [US5] Wire menu option 5 to handle_mark_todo() in run_cli() loop
- [x] T037 [US5] Display success/error messages after mark attempt in src/cli/menu.py

**Checkpoint**: Completion status toggles correctly; View shows updated checkbox indicator

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Error handling improvements and final validation

- [x] T038 Add try/except wrapper in run_cli() for KeyboardInterrupt (Ctrl+C) graceful exit
- [x] T039 Add input validation helper get_integer_input() in src/cli/menu.py for ID inputs
- [x] T040 Ensure all error messages are user-friendly (no stack traces) per FR-013, FR-014
- [x] T041 Validate all menu options handle invalid input gracefully (non-numeric choices)
- [x] T042 Run manual validation against all acceptance scenarios in spec.md
- [x] T043 Verify quickstart.md examples work correctly with implemented application

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - Can proceed sequentially in priority order (P1 → P2 → P3 → P4 → P5)
  - US1 (Add) should complete first as other stories need todos to exist for testing
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Add)**: No dependencies after Foundational - MVP entry point
- **User Story 2 (P2 - View)**: Can use US1 to create test data, but View logic is independent
- **User Story 3 (P3 - Update)**: Needs todos to exist (use US1 for test data)
- **User Story 4 (P4 - Delete)**: Needs todos to exist (use US1 for test data)
- **User Story 5 (P5 - Mark)**: Needs todos to exist (use US1 for test data)

### Within Each User Story

- Service layer before CLI layer
- Core implementation before integration
- Wire to menu after implementation complete

### Parallel Opportunities

- T003, T004, T005, T006 can run in parallel (independent __init__.py files)
- Within each user story, [P] marked tasks can run in parallel

---

## Parallel Example: Phase 1 Setup

```bash
# These can run in parallel:
Task: "Create src/__init__.py"
Task: "Create src/models/__init__.py"
Task: "Create src/services/__init__.py"
Task: "Create src/cli/__init__.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Todo)
4. **STOP and VALIDATE**: Test adding todos works correctly
5. Application is usable for basic todo creation

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Add) → Test independently → MVP!
3. Add User Story 2 (View) → Test independently → Can see added todos
4. Add User Story 3 (Update) → Test independently → Full CRUD minus delete
5. Add User Story 4 (Delete) → Test independently → Full CRUD
6. Add User Story 5 (Mark) → Test independently → Complete feature set
7. Polish phase → Production ready

---

## Validation Checkpoints

| Phase | Validation Criteria |
|-------|---------------------|
| Setup | `uv run python -m src.main` runs without error |
| Foundational | Menu displays, option 6 exits gracefully |
| US1 (Add) | Can add todo, ID assigned, empty title rejected |
| US2 (View) | Empty message shown; todos display with status |
| US3 (Update) | Title/description update works; errors handled |
| US4 (Delete) | Todo removed; view confirms; ID not reused |
| US5 (Mark) | Status toggles; view shows correct checkbox |
| Polish | All spec acceptance scenarios pass |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual testing only for Phase I (no automated tests)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
