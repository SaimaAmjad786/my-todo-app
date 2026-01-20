# Tasks: Todo App Intermediate Level Enhancements

**Input**: Design documents from `/specs/002-intermediate-enhancements/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Key Finding**: Backend (models + services + handlers) is ALREADY fully implemented. Only CLI menu needs updating.

**Organization**: Tasks grouped by implementation phase, minimal changes required.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- Paths: `src/models/todo.py`, `src/services/todo_service.py`, `src/cli/menu.py`

---

## Phase 1: Verification (Pre-Implementation Check)

**Purpose**: Confirm backend is complete before updating menu

- [X] T001 Verify Todo model has priority and category fields in src/models/todo.py
- [X] T002 [P] Verify TodoService has search() method in src/services/todo_service.py
- [X] T003 [P] Verify TodoService has filter_by_status(), filter_by_category(), filter_by_priority() methods in src/services/todo_service.py
- [X] T004 [P] Verify TodoService has sort_by_priority() method in src/services/todo_service.py
- [X] T005 [P] Verify handle_search(), handle_filter(), handle_sort() functions exist in src/cli/menu.py

**Checkpoint**: All backend components verified - ready for menu update

---

## Phase 2: CLI Menu Update (ONLY CHANGE NEEDED)

**Purpose**: Expose existing functionality through menu options

**Goal**: Add Search, Filter, Sort to main menu

### US1+US2: Priority & Category (P1) - ALREADY IMPLEMENTED ✅

> No tasks needed - priority and category are already in Add/Update workflows

**Verification**: Create a task, observe priority and category prompts

---

### US3: Search Menu Integration (P2)

**Goal**: Add Search option to main menu

**Independent Test**: Select [6] Search, enter keyword, verify matching results shown

- [X] T006 [US3] Add menu option [6] Search Todos to display_menu() in src/cli/menu.py
- [X] T007 [US3] Add choice routing for "6" to call handle_search(service) in run_cli() in src/cli/menu.py

**Checkpoint**: Search accessible from menu and working

---

### US4: Filter Menu Integration (P2)

**Goal**: Add Filter option to main menu

**Independent Test**: Select [7] Filter, choose filter type, verify filtered results shown

- [X] T008 [US4] Add menu option [7] Filter Todos to display_menu() in src/cli/menu.py
- [X] T009 [US4] Add choice routing for "7" to call handle_filter(service) in run_cli() in src/cli/menu.py

**Checkpoint**: Filter accessible from menu and working

---

### US5: Sort Menu Integration (P3)

**Goal**: Add Sort option to main menu

**Independent Test**: Select [8] Sort, choose sort type, verify sorted results shown

- [X] T010 [US5] Add menu option [8] Sort Todos to display_menu() in src/cli/menu.py
- [X] T011 [US5] Add choice routing for "8" to call handle_sort(service) in run_cli() in src/cli/menu.py

**Checkpoint**: Sort accessible from menu and working

---

### Menu Finalization

**Purpose**: Complete menu restructuring

- [X] T012 Move Exit option from [6] to [9] in display_menu() in src/cli/menu.py
- [X] T013 Update choice routing: change "6" exit to "9" in run_cli() in src/cli/menu.py
- [X] T014 Update input prompt from "Enter choice (1-6)" to "Enter choice (1-9)" in run_cli() in src/cli/menu.py
- [X] T015 Update error message from "1 and 6" to "1 and 9" in run_cli() in src/cli/menu.py

**Checkpoint**: Menu shows 9 options, all routing correct

---

## Phase 3: Validation & Polish

**Purpose**: Verify all features work and document completion

- [X] T016 Manual test: Add task with priority and category, verify display in src/cli/menu.py
- [X] T017 Manual test: Search for keyword, verify matching results
- [X] T018 Manual test: Filter by status, priority, category, verify correct filtering
- [X] T019 Manual test: Sort by priority, verify High→Medium→Low order
- [X] T020 Manual test: Verify original data unchanged after filter/sort operations
- [X] T021 Run regression: Verify Basic Level features (Add, View, Update, Delete, Mark) still work
- [X] T022 Run quickstart.md validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Verification)**: No dependencies - start immediately
- **Phase 2 (Menu Update)**: Depends on Phase 1 verification passing
- **Phase 3 (Validation)**: Depends on Phase 2 completion

### Task Dependencies Within Phase 2

```
T006 → T007  (US3: menu option before routing)
T008 → T009  (US4: menu option before routing)
T010 → T011  (US5: menu option before routing)
T012 → T013 → T014 → T015  (Exit move: sequential updates)
```

### Parallel Opportunities

Phase 1 tasks T002, T003, T004, T005 can run in parallel.

Phase 2 User Story tasks can run in parallel:
- US3 tasks (T006-T007)
- US4 tasks (T008-T009)
- US5 tasks (T010-T011)

---

## Implementation Strategy

### Quick Implementation (Recommended)

Since backend is complete, implementation is minimal:

1. **Verify** (5 min): Run Phase 1 checks
2. **Update Menu** (10 min): Complete Phase 2 tasks T006-T015
3. **Test** (10 min): Run Phase 3 validation

**Total estimated time**: 25 minutes

### Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T005 | Verification (backend check) |
| Phase 2 | T006-T015 | Menu update (only changes) |
| Phase 3 | T016-T022 | Validation (testing) |

**Total**: 22 tasks

### MVP Scope

**Minimum Viable**: Complete T006-T015 (menu update only)
- All backend already works
- Just need menu exposure

---

## Notes

- Backend is 100% complete - no model/service changes needed
- Only `src/cli/menu.py` needs modification
- All changes are in `display_menu()` and `run_cli()` functions
- Tests are manual CLI verification (no automated tests requested)
- Constitution compliance: All 6 principles pass
