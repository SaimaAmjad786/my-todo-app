---
id: 003
title: Implementation Tasks Generated
stage: tasks
date: 2025-12-27
surface: agent
model: claude-opus-4-5-20251101
feature: 002-intermediate-enhancements
branch: 002-intermediate-enhancements
user: hp
command: /sp.tasks
labels: ["tasks", "phase-2", "menu-update", "minimal-changes"]
links:
  spec: specs/002-intermediate-enhancements/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-intermediate-enhancements/tasks.md
tests:
  - Manual CLI verification (T016-T022)
---

## Prompt

Project: Todo App — Intermediate Level (CLI)

Input:
Use the approved Constitution, /sp.specify, and /sp.plan outputs.

Objective:
Break the Intermediate Level implementation into small, executable, testable
development tasks with clear completion criteria.

Tasks to Define:
1. Task Data Model Extension
2. Priority & Tags Input Handling
3. Task Display Enhancements
4. Search Functionality
5. Filter Functionality
6. Sorting Functionality
7. CLI Command Integration
8. Validation & Error Handling
9. Regression Verification
10. Final Cleanup

## Response snapshot

**Key Finding**: Backend is ALREADY 100% complete!
- Todo model has priority + category fields
- TodoService has search(), filter_by_*(), sort_by_*() methods
- CLI handlers (handle_search, handle_filter, handle_sort) exist

**Only Change Needed**: Update menu.py to expose existing functionality

**Tasks Generated**: 22 total

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T005 | Verification (confirm backend) |
| Phase 2 | T006-T015 | Menu update (add options 6-9) |
| Phase 3 | T016-T022 | Validation (manual testing) |

**User Stories Mapped**:
- US1+US2 (P1): Already implemented - no tasks needed
- US3 (P2): T006-T007 (Search menu)
- US4 (P2): T008-T009 (Filter menu)
- US5 (P3): T010-T011 (Sort menu)

**Parallel Opportunities**: T002-T005 (verification), US3/US4/US5 tasks

**Estimated Time**: 25 minutes total

## Outcome

- Impact: Minimal implementation - only menu.py changes needed
- Tests: Manual CLI verification (7 test tasks)
- Files: 1 created (tasks.md)
- Next prompts: Execute tasks or run `/sp.implement`
- Reflection: Backend already complete; scope reduced to menu wiring

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Task format validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
