# Tasks: Phase II Full-Stack Todo Application

**Input**: Design documents from `/specs/004-phase-ii-fullstack/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/openapi.yaml, research.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the specification. Test tasks are omitted per guidelines.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure for both backend and frontend

- [X] T001 [P] Create backend project structure with directories: src/models/, src/services/, src/api/routes/, src/api/middleware/, src/api/deps/, src/core/, tests/contract/, tests/integration/, tests/unit/, alembic/
- [X] T002 [P] Create frontend project structure with directories: src/app/(auth)/, src/app/dashboard/, src/components/ui/, src/components/todo/, src/components/layout/, src/lib/, src/hooks/, src/types/, tests/components/
- [X] T003 [P] Initialize backend Python project with pyproject.toml (FastAPI, SQLModel, uvicorn, alembic, pydantic-settings, asyncpg, python-jose)
- [X] T004 [P] Initialize frontend Next.js project with package.json (next, react, typescript, tailwindcss, @tanstack/react-query, react-hook-form, zod)
- [X] T005 [P] Configure backend linting with ruff in pyproject.toml
- [X] T006 [P] Configure frontend linting with ESLint and Prettier in .eslintrc.js and .prettierrc
- [X] T007 [P] Create backend .env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS
- [X] T008 [P] Create frontend .env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_URL
- [X] T009 [P] Configure Tailwind CSS in frontend/tailwind.config.ts with custom color scheme
- [X] T010 [P] Install and configure shadcn/ui base components in frontend/src/components/ui/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T011 Create database configuration in backend/src/core/database.py with async SQLModel engine for Neon PostgreSQL
- [X] T012 Create application settings in backend/src/core/config.py using pydantic-settings
- [X] T013 Create base SQLModel models in backend/src/models/base.py with UUID primary key and timestamp mixins
- [X] T014 Create FastAPI application entry point in backend/src/main.py with CORS middleware and health check
- [X] T015 Create error response schemas in backend/src/api/schemas/error.py per OpenAPI spec
- [X] T016 Create global exception handlers in backend/src/api/middleware/error_handler.py
- [X] T017 Configure Alembic for async migrations in backend/alembic/env.py
- [X] T018 Create API versioning router in backend/src/api/routes/__init__.py with /api/v1 prefix
- [X] T019 [P] Create TypeScript type definitions in frontend/src/types/api.ts matching OpenAPI schemas
- [X] T020 [P] Create API client utility in frontend/src/lib/api-client.ts with fetch wrapper and error handling
- [X] T021 [P] Create base layout component in frontend/src/components/layout/RootLayout.tsx with Tailwind setup
- [X] T022 Create React Query provider in frontend/src/lib/providers.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1)

**Goal**: Enable users to create accounts, sign in, and maintain authenticated sessions

**Independent Test**: Complete signup flow, sign out, sign back in with same credentials

### Backend Implementation

- [X] T023 [US1] Integrate Better Auth server SDK in backend/src/core/auth.py with session configuration
- [X] T024 [US1] Create User model extending Better Auth in backend/src/models/user.py (id, email, name, timestamps)
- [X] T025 [US1] Create auth schemas in backend/src/api/schemas/auth.py (SignupRequest, SigninRequest, AuthResponse, User)
- [X] T026 [US1] Create auth dependency in backend/src/api/deps/auth.py for extracting current user from session
- [X] T027 [US1] Implement signup endpoint POST /auth/signup in backend/src/api/routes/auth.py
- [X] T028 [US1] Implement signin endpoint POST /auth/signin in backend/src/api/routes/auth.py
- [X] T029 [US1] Implement signout endpoint POST /auth/signout in backend/src/api/routes/auth.py
- [X] T030 [US1] Implement current user endpoint GET /auth/me in backend/src/api/routes/auth.py
- [X] T031 [US1] Create initial database migration 001_initial_schema in backend/alembic/versions/

### Frontend Implementation

- [X] T032 [US1] Create auth context and hooks in frontend/src/lib/auth-context.tsx for session state
- [X] T033 [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx with form validation
- [X] T034 [US1] Create signin page in frontend/src/app/(auth)/signin/page.tsx with form validation
- [X] T035 [US1] Create auth layout in frontend/src/app/(auth)/layout.tsx with centered card design
- [X] T036 [US1] Create protected route middleware in frontend/src/middleware.ts redirecting unauthenticated users
- [X] T037 [US1] Add signout functionality to header in frontend/src/components/layout/Header.tsx

**Checkpoint**: User Story 1 complete - users can register, sign in, and sign out

---

## Phase 4: User Story 2 - Basic Todo Management (Priority: P1)

**Goal**: Enable authenticated users to create, view, update, delete, and complete/incomplete todos

**Independent Test**: Create todo, view in list, update details, mark complete, delete

### Backend Implementation

- [X] T038 [US2] Create Priority and Recurrence enums in backend/src/models/enums.py
- [X] T039 [US2] Create Todo model in backend/src/models/todo.py with all fields per data-model.md
- [X] T040 [US2] Create todo schemas in backend/src/api/schemas/todo.py (CreateTodoRequest, UpdateTodoRequest, Todo, TodoListResponse)
- [X] T041 [US2] Create TodoService in backend/src/services/todo_service.py with CRUD methods (user-scoped)
- [X] T042 [US2] Implement list todos endpoint GET /todos in backend/src/api/routes/todos.py (basic list, no filters yet)
- [X] T043 [US2] Implement create todo endpoint POST /todos in backend/src/api/routes/todos.py
- [X] T044 [US2] Implement get todo endpoint GET /todos/{id} in backend/src/api/routes/todos.py
- [X] T045 [US2] Implement update todo endpoint PATCH /todos/{id} in backend/src/api/routes/todos.py
- [X] T046 [US2] Implement delete todo endpoint DELETE /todos/{id} in backend/src/api/routes/todos.py
- [X] T047 [US2] Implement complete endpoint POST /todos/{id}/complete in backend/src/api/routes/todos.py
- [X] T048 [US2] Implement incomplete endpoint POST /todos/{id}/incomplete in backend/src/api/routes/todos.py
- [X] T049 [US2] Add migration 002_add_todos_table in backend/alembic/versions/

### Frontend Implementation

- [X] T050 [US2] Create todo API hooks in frontend/src/hooks/useTodos.ts using React Query
- [X] T051 [US2] Create TodoList component in frontend/src/components/todo/TodoList.tsx
- [X] T052 [US2] Create TodoItem component in frontend/src/components/todo/TodoItem.tsx with checkbox and actions
- [X] T053 [US2] Create TodoForm component in frontend/src/components/todo/TodoForm.tsx for create/edit
- [X] T054 [US2] Create DeleteConfirmDialog component in frontend/src/components/todo/DeleteConfirmDialog.tsx
- [X] T055 [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx with TodoList
- [X] T056 [US2] Add empty state component in frontend/src/components/todo/EmptyState.tsx with call-to-action

**Checkpoint**: User Story 2 complete - basic CRUD operations functional

---

## Phase 5: User Story 3 - Priority and Organization (Priority: P2)

**Goal**: Allow users to assign priorities and tags to organize todos

**Independent Test**: Create todos with different priorities and tags, verify visual display

### Backend Implementation

- [X] T057 [US3] Create Tag model in backend/src/models/tag.py with user_id foreign key
- [X] T058 [US3] Create TodoTag junction model in backend/src/models/todo_tag.py
- [X] T059 [US3] Update Todo model to include tags relationship in backend/src/models/todo.py
- [X] T060 [US3] Create tag schemas in backend/src/api/schemas/tag.py (Tag, CreateTagRequest)
- [X] T061 [US3] Create TagService in backend/src/services/tag_service.py with CRUD methods
- [X] T062 [US3] Implement list tags endpoint GET /tags in backend/src/api/routes/tags.py
- [X] T063 [US3] Implement create tag endpoint POST /tags in backend/src/api/routes/tags.py
- [X] T064 [US3] Implement delete tag endpoint DELETE /tags/{id} in backend/src/api/routes/tags.py
- [X] T065 [US3] Update create/update todo endpoints to handle tag_ids in backend/src/api/routes/todos.py
- [X] T066 [US3] Add migration 003_add_tags_tables in backend/alembic/versions/

### Frontend Implementation

- [X] T067 [US3] Create PriorityBadge component in frontend/src/components/todo/PriorityBadge.tsx with color coding
- [X] T068 [US3] Create TagChip component in frontend/src/components/todo/TagChip.tsx
- [X] T069 [US3] Create TagSelector component in frontend/src/components/todo/TagSelector.tsx with autocomplete
- [X] T070 [US3] Create PrioritySelector component in frontend/src/components/todo/PrioritySelector.tsx
- [X] T071 [US3] Update TodoItem to display priority badge and tags in frontend/src/components/todo/TodoItem.tsx
- [X] T072 [US3] Update TodoForm to include priority and tag selection in frontend/src/components/todo/TodoForm.tsx
- [X] T073 [US3] Create tag API hooks in frontend/src/hooks/useTags.ts

**Checkpoint**: User Story 3 complete - priority and tags functional

---

## Phase 6: User Story 4 - Search and Filter (Priority: P2)

**Goal**: Enable users to find todos using search and filters

**Independent Test**: Create multiple todos, search by keyword, filter by status/priority/tag

### Backend Implementation

- [X] T074 [US4] Add search parameter to list todos endpoint with ILIKE query in backend/src/services/todo_service.py
- [X] T075 [US4] Add completed filter parameter to list todos in backend/src/services/todo_service.py
- [X] T076 [US4] Add priority filter parameter to list todos in backend/src/services/todo_service.py
- [X] T077 [US4] Add tag filter parameter to list todos with JOIN query in backend/src/services/todo_service.py
- [X] T078 [US4] Update GET /todos endpoint to accept all filter query params in backend/src/api/routes/todos.py

### Frontend Implementation

- [X] T079 [US4] Create SearchInput component in frontend/src/components/todo/SearchInput.tsx with debounce
- [X] T080 [US4] Create FilterBar component in frontend/src/components/todo/FilterBar.tsx
- [X] T081 [US4] Create StatusFilter component in frontend/src/components/todo/StatusFilter.tsx (all/complete/incomplete)
- [X] T082 [US4] Create PriorityFilter component in frontend/src/components/todo/PriorityFilter.tsx
- [X] T083 [US4] Create TagFilter component in frontend/src/components/todo/TagFilter.tsx
- [X] T084 [US4] Update useTodos hook to support filter parameters in frontend/src/hooks/useTodos.ts
- [X] T085 [US4] Update dashboard to include SearchInput and FilterBar in frontend/src/app/dashboard/page.tsx

**Checkpoint**: User Story 4 complete - search and filter functional

---

## Phase 7: User Story 5 - Sorting (Priority: P2)

**Goal**: Allow users to sort todos by various criteria

**Independent Test**: Create todos with different dates/priorities, verify sort order changes

### Backend Implementation

- [X] T086 [US5] Add sort parameter to list todos with ORDER BY in backend/src/services/todo_service.py
- [X] T087 [US5] Support sort options: created_at, -created_at, due_date, -due_date, priority, -priority, title, -title
- [X] T088 [US5] Update GET /todos endpoint to accept sort query param in backend/src/api/routes/todos.py

### Frontend Implementation

- [X] T089 [US5] Create SortSelector component in frontend/src/components/todo/SortSelector.tsx
- [X] T090 [US5] Update useTodos hook to support sort parameter in frontend/src/hooks/useTodos.ts
- [X] T091 [US5] Add SortSelector to FilterBar in frontend/src/components/todo/FilterBar.tsx

**Checkpoint**: User Story 5 complete - sorting functional

---

## Phase 8: User Story 8 - Responsive and Animated UI (Priority: P2)

**Goal**: Ensure professional, responsive, animated interface across devices

**Independent Test**: Access on desktop and mobile, verify layout adapts with smooth animations

- [X] T092 [US8] Add responsive breakpoints to TodoList for mobile/desktop in frontend/src/components/todo/TodoList.tsx
- [X] T093 [US8] Add hover animations to TodoItem in frontend/src/components/todo/TodoItem.tsx
- [X] T094 [US8] Add transition animations for todo state changes in frontend/src/components/todo/TodoItem.tsx
- [X] T095 [US8] Create LoadingSpinner component in frontend/src/components/ui/LoadingSpinner.tsx
- [X] T096 [US8] Create LoadingSkeleton component for todo list in frontend/src/components/todo/TodoListSkeleton.tsx
- [X] T097 [US8] Add loading states to dashboard page in frontend/src/app/dashboard/page.tsx
- [X] T098 [US8] Create ErrorMessage component in frontend/src/components/ui/ErrorMessage.tsx with retry option
- [X] T099 [US8] Add error boundary wrapper in frontend/src/components/layout/ErrorBoundary.tsx
- [X] T100 [US8] Create mobile-friendly navigation in frontend/src/components/layout/MobileNav.tsx
- [X] T101 [US8] Add toast notifications for success/error feedback in frontend/src/lib/toast.tsx

**Checkpoint**: User Story 8 complete - responsive and animated UI implemented

---

## Phase 9: User Story 6 - Due Dates and Reminders (Priority: P3)

**Goal**: Enable due dates with visual indicators and browser notification reminders

**Independent Test**: Create todo with due date and reminder, verify notification appears

### Backend Implementation

- [X] T102 [US6] Add due_date and reminder_time fields to todo responses in backend/src/api/schemas/todo.py
- [X] T103 [US6] Update create/update todo to handle due_date and reminder_time in backend/src/services/todo_service.py
- [X] T104 [US6] Add validation: reminder_time must be <= due_date in backend/src/api/schemas/todo.py

### Frontend Implementation

- [X] T105 [US6] Create DatePicker component in frontend/src/components/ui/DatePicker.tsx
- [X] T106 [US6] Create DueDateSelector component in frontend/src/components/todo/DueDateSelector.tsx
- [X] T107 [US6] Create ReminderSelector component in frontend/src/components/todo/ReminderSelector.tsx
- [X] T108 [US6] Update TodoForm to include due date and reminder fields in frontend/src/components/todo/TodoForm.tsx
- [X] T109 [US6] Create DueDateBadge component with overdue styling in frontend/src/components/todo/DueDateBadge.tsx
- [X] T110 [US6] Update TodoItem to display due date badge in frontend/src/components/todo/TodoItem.tsx
- [X] T111 [US6] Create reminder notification service in frontend/src/lib/notifications.ts using Web Notifications API
- [X] T112 [US6] Create reminder scheduler hook in frontend/src/hooks/useReminders.ts with setTimeout logic
- [X] T113 [US6] Add notification permission request on first reminder set in frontend/src/lib/notifications.ts

**Checkpoint**: User Story 6 complete - due dates and reminders functional

---

## Phase 10: User Story 7 - Recurring Tasks (Priority: P3)

**Goal**: Enable recurring todos that regenerate on completion

**Independent Test**: Create daily recurring task, mark complete, verify new instance created

### Backend Implementation

- [X] T114 [US7] Add recurrence field to todo responses in backend/src/api/schemas/todo.py
- [X] T115 [US7] Create recurrence calculation utility in backend/src/services/recurrence.py (daily/weekly/monthly)
- [X] T116 [US7] Update complete endpoint to generate next occurrence for recurring todos in backend/src/services/todo_service.py
- [X] T117 [US7] Return both completed_todo and next_occurrence in complete response per OpenAPI spec

### Frontend Implementation

- [X] T118 [US7] Create RecurrenceSelector component in frontend/src/components/todo/RecurrenceSelector.tsx
- [X] T119 [US7] Update TodoForm to include recurrence selection in frontend/src/components/todo/TodoForm.tsx
- [X] T120 [US7] Create RecurrenceBadge component in frontend/src/components/todo/RecurrenceBadge.tsx
- [X] T121 [US7] Update TodoItem to display recurrence indicator in frontend/src/components/todo/TodoItem.tsx
- [X] T122 [US7] Handle complete response with next_occurrence in useTodos hook frontend/src/hooks/useTodos.ts

**Checkpoint**: User Story 7 complete - recurring tasks functional

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [X] T123 [P] Add comprehensive input validation messages across all forms
- [X] T124 [P] Add keyboard navigation support to TodoList and forms
- [X] T125 [P] Add aria labels and roles for accessibility in all components
- [X] T126 [P] Optimize React Query caching strategy in frontend/src/lib/providers.tsx
- [X] T127 [P] Add rate limiting to backend API endpoints in backend/src/api/middleware/rate_limit.py
- [X] T128 Run quickstart.md validation checklist to verify all features work end-to-end
- [X] T129 Review and update README.md with Phase II documentation

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup (no dependencies)
    ↓
Phase 2: Foundational (depends on Setup)
    ↓
    ├── Phase 3: US1 - Auth (depends on Foundational)
    │       ↓
    │   Phase 4: US2 - Basic CRUD (depends on US1 for auth)
    │       ↓
    │       ├── Phase 5: US3 - Priority/Tags (depends on US2)
    │       ├── Phase 6: US4 - Search/Filter (depends on US2)
    │       ├── Phase 7: US5 - Sorting (depends on US2)
    │       └── Phase 8: US8 - UI/UX (depends on US2)
    │               ↓
    │           Phase 9: US6 - Due Dates (depends on US3+)
    │           Phase 10: US7 - Recurring (depends on US3+)
    │               ↓
    │           Phase 11: Polish (depends on all stories)
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Auth) | Foundational | Phase 2 complete |
| US2 (Basic CRUD) | US1 | Phase 3 complete |
| US3 (Priority/Tags) | US2 | Phase 4 complete |
| US4 (Search/Filter) | US2 | Phase 4 complete |
| US5 (Sorting) | US2 | Phase 4 complete |
| US6 (Due Dates) | US3 | Phase 5 complete |
| US7 (Recurring) | US3 | Phase 5 complete |
| US8 (UI/UX) | US2 | Phase 4 complete |

### Parallel Opportunities

**Within Phase 1 (Setup)**:
```
T001, T002, T003, T004, T005, T006, T007, T008, T009, T010 - all parallel
```

**Within Phase 2 (Foundational)**:
```
T019, T020, T021 - can run in parallel (frontend tasks)
```

**Phases 5, 6, 7, 8 can run in parallel** (after Phase 4):
- US3 (Priority/Tags)
- US4 (Search/Filter)
- US5 (Sorting)
- US8 (UI/UX)

**Phases 9, 10 can run in parallel** (after Phase 5):
- US6 (Due Dates)
- US7 (Recurring)

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 - Authentication
4. Complete Phase 4: US2 - Basic CRUD
5. **STOP and VALIDATE**: Test signup, signin, create/edit/delete/complete todos
6. Deploy/demo as MVP

### Incremental Delivery

| Increment | Stories Included | Cumulative Value |
|-----------|-----------------|------------------|
| MVP | US1 + US2 | Auth + Basic CRUD |
| +Organization | + US3 | + Priorities, Tags |
| +Discovery | + US4 + US5 | + Search, Filter, Sort |
| +Polish | + US8 | + Responsive, Animated UI |
| +Advanced | + US6 + US7 | + Due Dates, Reminders, Recurring |
| Complete | + Polish | Full Phase II |

### Suggested Commit Points

- After Phase 2: "feat: add project foundation and database setup"
- After Phase 3: "feat: add user authentication (US1)"
- After Phase 4: "feat: add basic todo CRUD operations (US2)"
- After Phase 5: "feat: add priority and tag organization (US3)"
- After Phases 6-8: "feat: add search, filter, sort, and responsive UI (US4, US5, US8)"
- After Phases 9-10: "feat: add due dates, reminders, and recurring tasks (US6, US7)"
- After Phase 11: "chore: polish and finalize Phase II"

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story checkpoint is independently testable
- Commit after each phase or logical group
- Backend and frontend tasks within same story can be parallelized by different developers
