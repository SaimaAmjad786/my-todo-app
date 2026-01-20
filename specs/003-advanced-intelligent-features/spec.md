# Feature Specification: Todo App Advanced Level (Intelligent Features)

**Feature Branch**: `003-advanced-intelligent-features`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "Todo App Advanced Level - Intelligent Features: Recurring Tasks, Due Dates, Time Reminders"

## Overview

This specification defines the Advanced Level (Phase III) enhancements for the existing Todo CLI application. These features add intelligent, time-based behavior including recurring tasks, precise due date/time tracking, and automated reminders. This builds on the completed Basic and Intermediate levels.

**Prerequisites**: A fully functional Intermediate Level CLI Todo application with:
- Add/Delete/Update/View/Mark Complete (Basic)
- Priority levels (High/Medium/Low)
- Categories/Tags
- Search, Filter, Sort functionality

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Recurring Tasks (Priority: P1)

As a user, I want to create recurring tasks (daily, weekly, monthly) so that routine activities automatically regenerate after completion.

**Why this priority**: Recurring tasks are the core differentiator of the Advanced Level. Without them, users must manually recreate repetitive tasks, which defeats the purpose of a productivity tool.

**Independent Test**: Can be fully tested by creating a recurring task, marking it complete, and verifying a new task is automatically generated with the correct next due date.

**Acceptance Scenarios**:

1. **Given** I am creating a new task, **When** I choose to make it recurring, **Then** I can select from Daily, Weekly, or Monthly recurrence patterns
2. **Given** I have a daily recurring task due today, **When** I mark it complete, **Then** a new task is automatically created with tomorrow's date
3. **Given** I have a weekly recurring task due on Monday, **When** I mark it complete, **Then** a new task is automatically created due next Monday
4. **Given** I have a monthly recurring task due on the 15th, **When** I mark it complete, **Then** a new task is automatically created due on the 15th of next month
5. **Given** I complete a recurring task, **When** the new task is generated, **Then** it inherits title, description, priority, category, and recurrence pattern but gets a new unique ID

---

### User Story 2 - Set Due Date and Time (Priority: P1)

As a user, I want to set specific due dates and times for my tasks so I can track precise deadlines.

**Why this priority**: Due dates are fundamental to task management and are required for the reminder system to function.

**Independent Test**: Can be tested by creating tasks with various due dates/times and verifying they display correctly in the task list.

**Acceptance Scenarios**:

1. **Given** I am creating a new task, **When** I am prompted for due date, **Then** I can enter a date in YYYY-MM-DD format or skip
2. **Given** I am creating a task with a due date, **When** I am prompted for due time, **Then** I can enter a time in HH:MM (24-hour) format or skip
3. **Given** I have an existing task, **When** I choose to update it, **Then** I can modify the due date and time
4. **Given** I view my task list, **When** tasks have due dates/times, **Then** both date and time are clearly displayed

---

### User Story 3 - Receive Deadline Reminders (Priority: P2)

As a user, I want to receive reminders for upcoming and overdue tasks so I don't miss important deadlines.

**Why this priority**: Reminders provide proactive notification but depend on due dates being set first (P1 features).

**Independent Test**: Can be tested by creating tasks with past or imminent due dates/times and verifying reminder messages appear.

**Acceptance Scenarios**:

1. **Given** I start the application, **When** there are overdue tasks, **Then** I see reminder messages listing overdue tasks
2. **Given** I am at the main menu, **When** tasks become due (current time matches or passes due time), **Then** I see reminder messages before the menu displays
3. **Given** there are multiple overdue or due tasks, **When** reminders are shown, **Then** each task is listed with its title, due date/time, and how overdue it is
4. **Given** reminders are displayed, **When** I continue using the app, **Then** reminders do not block my interaction (informational only)

---

### User Story 4 - Manage Recurring Task Settings (Priority: P2)

As a user, I want to update or remove recurrence from existing tasks so I can adjust my routine as needs change.

**Why this priority**: Modification of recurrence is important for usability but secondary to initial creation.

**Independent Test**: Can be tested by updating a recurring task to change or remove its recurrence pattern.

**Acceptance Scenarios**:

1. **Given** I have a recurring task, **When** I choose to update it, **Then** I can change the recurrence pattern (daily/weekly/monthly/none)
2. **Given** I have a recurring task, **When** I set recurrence to none, **Then** the task becomes a one-time task
3. **Given** I have a non-recurring task, **When** I update it, **Then** I can add a recurrence pattern

---

### User Story 5 - View Tasks by Due Date Status (Priority: P3)

As a user, I want to filter or view tasks by their due date status (overdue, due today, upcoming) so I can focus on urgent items.

**Why this priority**: This is a convenience feature that enhances the existing filter functionality.

**Independent Test**: Can be tested by creating tasks with various due dates and using filters to view specific subsets.

**Acceptance Scenarios**:

1. **Given** I have tasks with various due dates, **When** I filter by "Overdue", **Then** only tasks past their due date are shown
2. **Given** I have tasks with various due dates, **When** I filter by "Due Today", **Then** only tasks due today are shown
3. **Given** I have tasks with various due dates, **When** I filter by "Upcoming" (next 7 days), **Then** only tasks due within the next week are shown

---

### Edge Cases

- What happens when a monthly recurring task is due on the 31st and the next month has fewer days? Use the last day of that month (e.g., Feb 28/29)
- What happens when a user enters an invalid date format? Display error message and prompt again
- What happens when a user enters an invalid time format? Display error message and prompt again
- What happens when due time is set but not due date? Require due date if due time is provided
- What happens when a recurring task has no due date? Recurrence calculates from current date when marked complete
- What happens when there are no overdue tasks at startup? Skip reminder display, proceed to menu
- What happens when multiple tasks are overdue? Display all reminders sequentially before menu

## Requirements *(mandatory)*

### Functional Requirements

**Recurring Tasks**:
- **FR-001**: System MUST allow users to mark a task as recurring during creation
- **FR-002**: System MUST support three recurrence patterns: Daily, Weekly, Monthly
- **FR-003**: System MUST default to "None" (non-recurring) if user does not specify
- **FR-004**: When a recurring task is marked complete, system MUST automatically create a new task
- **FR-005**: The new recurring task MUST inherit: title, description, priority, category, recurrence pattern
- **FR-006**: The new recurring task MUST receive a new unique ID
- **FR-007**: The new recurring task MUST have due date calculated based on recurrence pattern:
  - Daily: +1 day from original due date (or current date if no due date)
  - Weekly: +7 days from original due date
  - Monthly: Same day next month (adjusted for month length)
- **FR-008**: System MUST allow users to update recurrence pattern on existing tasks
- **FR-009**: Completing a recurring task MUST NOT modify the original (completed) task record

**Due Date and Time**:
- **FR-010**: System MUST allow users to set an optional due date (YYYY-MM-DD format) during task creation
- **FR-011**: System MUST allow users to set an optional due time (HH:MM, 24-hour format) during task creation
- **FR-012**: Due time MUST only be accepted if due date is also provided
- **FR-013**: System MUST allow users to update due date and time on existing tasks
- **FR-014**: System MUST display due date and time clearly in task views

**Reminders**:
- **FR-015**: System MUST check for overdue and due tasks on application startup
- **FR-016**: System MUST check for overdue and due tasks before each main menu display
- **FR-017**: System MUST display reminder messages for tasks that are overdue or due now
- **FR-018**: Reminder messages MUST include: task title, due date/time, overdue duration (if applicable)
- **FR-019**: Reminders MUST be informational only and NOT block user interaction
- **FR-020**: Multiple reminders MUST be displayed sequentially

**Filtering (Extension)**:
- **FR-021**: System MUST allow filtering by due date status: Overdue, Due Today, Upcoming (next 7 days)
- **FR-022**: Due date filters MUST NOT permanently modify stored task data

### Key Entities

- **Todo (Extended)**: The core task entity with additional attributes:
  - id: Unique identifier (integer)
  - title: Task name (required)
  - description: Additional details (optional)
  - completed: Completion status (boolean)
  - priority: High, Medium, or Low (default: Medium)
  - category: Predefined category (default: general)
  - due_date: Optional date string (YYYY-MM-DD)
  - due_time: Optional time string (HH:MM, 24-hour format)
  - recurrence: Recurrence pattern (none, daily, weekly, monthly) - default: none

- **Recurrence Pattern**: Enumeration defining repetition rules:
  - none: One-time task (default)
  - daily: Repeats every day
  - weekly: Repeats every 7 days
  - monthly: Repeats on the same day each month

## Assumptions

- Local system time is used for all date/time calculations (no timezone handling)
- Reminders are displayed as CLI text messages, not system notifications
- "Overdue" means the current datetime has passed the task's due datetime
- "Due Today" means the due date matches today's date regardless of time
- "Upcoming" means due date is within the next 7 days (inclusive of today)
- When a recurring task without a due date is completed, the new task's due date is calculated from the current date
- Monthly recurrence on day 29-31 adjusts to the last valid day of shorter months

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a recurring task and see automatic regeneration within 2 seconds of marking complete
- **SC-002**: Users can set due date and time during task creation in under 30 seconds additional time
- **SC-003**: Overdue task reminders appear within 1 second of application startup
- **SC-004**: 100% of recurring task completions generate a correctly dated new task
- **SC-005**: All existing Basic and Intermediate features continue to work without regression
- **SC-006**: Reminder messages display without requiring any user action to dismiss (non-blocking)
- **SC-007**: Users can filter tasks by due date status (overdue/today/upcoming) in 2 menu selections
