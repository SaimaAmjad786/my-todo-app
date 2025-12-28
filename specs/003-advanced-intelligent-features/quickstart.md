# Quickstart: Testing Advanced Level Features

**Feature**: 003-advanced-intelligent-features
**Date**: 2025-12-27
**Purpose**: Manual validation scenarios for implementation testing

## Prerequisites

1. Python 3.13+ installed
2. Virtual environment activated
3. Application running: `python -m src.main`

## Test Scenarios

### Scenario 1: Create Task with Due Time

**Goal**: Verify due time can be set during task creation

**Steps**:
1. Select [1] Add Todo
2. Enter title: "Team meeting"
3. Enter description: "Weekly sync"
4. Select priority: [2] Medium
5. Select category: [1] Work
6. Enter due date: `2025-12-28`
7. Enter due time: `14:30`
8. Select recurrence: [4] None

**Expected Result**:
- Task created successfully
- View task list shows: "Due: 2025-12-28 14:30"

---

### Scenario 2: Create Daily Recurring Task

**Goal**: Verify daily recurrence works

**Steps**:
1. Select [1] Add Todo
2. Enter title: "Morning standup"
3. Enter description: ""
4. Select priority: [1] High
5. Select category: [1] Work
6. Enter due date: `2025-12-27`
7. Enter due time: `09:00`
8. Select recurrence: [1] Daily

**Expected Result**:
- Task created with recurrence icon/indicator
- Task shows "Recurs: Daily"

---

### Scenario 3: Complete Recurring Task - Auto-Regeneration

**Goal**: Verify new task is created when recurring task is completed

**Prerequisites**: Scenario 2 completed (daily recurring task exists)

**Steps**:
1. Select [5] Mark Complete/Incomplete
2. Enter ID of the recurring task
3. Select (c)omplete

**Expected Result**:
- Original task marked complete
- Message: "Next occurrence created"
- New task created with:
  - Same title, priority, category
  - Due date: tomorrow (2025-12-28)
  - Same due time (09:00)
  - Recurrence: daily

---

### Scenario 4: Weekly Recurrence

**Goal**: Verify weekly recurrence adds 7 days

**Steps**:
1. Create task with:
   - Title: "Weekly report"
   - Due date: `2025-12-27` (Saturday)
   - Recurrence: [2] Weekly
2. Mark task complete

**Expected Result**:
- New task due date: `2026-01-03` (next Saturday, +7 days)

---

### Scenario 5: Monthly Recurrence - Normal Case

**Goal**: Verify monthly recurrence for normal dates

**Steps**:
1. Create task with:
   - Title: "Monthly review"
   - Due date: `2025-12-15`
   - Recurrence: [3] Monthly
2. Mark task complete

**Expected Result**:
- New task due date: `2026-01-15`

---

### Scenario 6: Monthly Recurrence - Edge Case (31st)

**Goal**: Verify monthly recurrence handles month-end edge cases

**Steps**:
1. Create task with:
   - Title: "Month-end close"
   - Due date: `2025-01-31`
   - Recurrence: [3] Monthly
2. Mark task complete

**Expected Result**:
- New task due date: `2025-02-28` (last day of February)

---

### Scenario 7: Reminders on Startup - Overdue Task

**Goal**: Verify overdue reminders appear on app start

**Setup**:
1. Create task with past due date (e.g., yesterday)
2. Exit the application
3. Restart the application

**Expected Result**:
- Before menu displays, see reminder banner:
  ```
  REMINDERS
  ---------
  [OVERDUE] Task: "Your task title"
  Due: 2025-12-26 - 1 day overdue
  ```

---

### Scenario 8: Reminders Before Menu

**Goal**: Verify reminders appear before each menu display

**Setup**:
1. Have an overdue task in the system
2. Perform any menu action (e.g., View All)

**Expected Result**:
- After action completes, before next menu displays
- Reminder banner appears again

---

### Scenario 9: Filter by Due Date Status - Overdue

**Goal**: Verify overdue filter works

**Steps**:
1. Have tasks with various due dates (past, today, future)
2. Select [7] Filter Todos
3. Select [4] Due Date Status
4. Select [1] Overdue

**Expected Result**:
- Only tasks with due date in the past are shown
- Tasks due today (with passed time) included

---

### Scenario 10: Filter by Due Date Status - Due Today

**Goal**: Verify today filter works

**Steps**:
1. Have tasks with various due dates
2. Select [7] Filter Todos
3. Select [4] Due Date Status
4. Select [2] Due Today

**Expected Result**:
- Only tasks with today's date are shown

---

### Scenario 11: Filter by Due Date Status - Upcoming

**Goal**: Verify upcoming filter works

**Steps**:
1. Have tasks with various due dates (next 7 days, beyond 7 days)
2. Select [7] Filter Todos
3. Select [4] Due Date Status
4. Select [3] Upcoming (7 days)

**Expected Result**:
- Tasks due within next 7 days (inclusive of today)
- Tasks due beyond 7 days NOT shown

---

### Scenario 12: Update Task - Add Recurrence

**Goal**: Verify recurrence can be added to existing task

**Steps**:
1. Create a one-time task (recurrence: none)
2. Select [3] Update Todo
3. Enter task ID
4. Skip title, description, priority, category, date, time changes
5. Select new recurrence: [1] Daily

**Expected Result**:
- Task now shows recurrence: daily
- Completing it will create next occurrence

---

### Scenario 13: Update Task - Remove Recurrence

**Goal**: Verify recurrence can be removed

**Steps**:
1. Have a recurring task
2. Select [3] Update Todo
3. Enter task ID
4. Set recurrence to: [4] None

**Expected Result**:
- Task shows no recurrence indicator
- Completing it will NOT create new task

---

### Scenario 14: Invalid Time Format

**Goal**: Verify time validation error handling

**Steps**:
1. Select [1] Add Todo
2. Complete title, description, priority, category, date
3. Enter invalid time: `25:00`

**Expected Result**:
- Error message: "Invalid time format!"
- Prompted to enter again

---

### Scenario 15: Time Without Date

**Goal**: Verify time requires date

**Steps**:
1. Select [1] Add Todo
2. Complete title, description, priority, category
3. Skip due date (press Enter)
4. Try to enter time

**Expected Result**:
- Time prompt is skipped if no date provided
- OR message: "Due time requires due date"

---

## Regression Tests

Verify these Basic and Intermediate features still work:

### Basic Level
- [ ] Add task (title, description)
- [ ] View all tasks
- [ ] Update task (title, description)
- [ ] Delete task
- [ ] Mark complete/incomplete

### Intermediate Level
- [ ] Set/update priority (high/medium/low)
- [ ] Set/update category
- [ ] Search by keyword
- [ ] Filter by status (pending/completed)
- [ ] Filter by priority
- [ ] Filter by category
- [ ] Sort by priority
- [ ] Sort by due date

## Checklist Summary

| Feature | Test Scenario | Status |
|---------|--------------|--------|
| Due time input | 1 | [ ] |
| Due time display | 1 | [ ] |
| Daily recurrence create | 2 | [ ] |
| Weekly recurrence | 4 | [ ] |
| Monthly recurrence | 5, 6 | [ ] |
| Auto-regeneration | 3 | [ ] |
| Reminders on startup | 7 | [ ] |
| Reminders before menu | 8 | [ ] |
| Filter: Overdue | 9 | [ ] |
| Filter: Due Today | 10 | [ ] |
| Filter: Upcoming | 11 | [ ] |
| Update: Add recurrence | 12 | [ ] |
| Update: Remove recurrence | 13 | [ ] |
| Time validation | 14 | [ ] |
| Time requires date | 15 | [ ] |
| Basic regression | Checklist | [ ] |
| Intermediate regression | Checklist | [ ] |
