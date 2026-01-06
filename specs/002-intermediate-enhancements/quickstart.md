# Quickstart: Testing Intermediate Level Features

**Branch**: `002-intermediate-enhancements` | **Date**: 2025-12-27

## Prerequisites

- Python 3.13+
- UV package manager
- Existing todo app running

## Start the Application

```bash
cd E:\Users\hp\Documents\my-task\todo-app
python -m src.main
```

## Test Priority & Category (P1)

### Test 1: Add Task with Priority

1. Select `[1] Add Todo`
2. Enter title: "Urgent meeting"
3. Enter description: "Team standup"
4. Select priority: `[1] High`
5. Select category: `[1] Work`
6. Verify: Todo shows `!!! HIGH` and `[W] Work`

### Test 2: Add Task with Default Values

1. Select `[1] Add Todo`
2. Enter title: "Optional task"
3. Press Enter for description
4. Press Enter for priority (defaults to Medium)
5. Press Enter for category (defaults to General)
6. Verify: Todo shows `!! MEDIUM` and `[G] General`

### Test 3: Update Priority/Category

1. Select `[3] Update Todo`
2. Enter todo ID
3. Press Enter to keep title
4. Press Enter to keep description
5. Enter `h` for high priority
6. Enter `p` for personal category
7. Verify: Changes displayed correctly

## Test Search (P2)

### Test 4: Search by Keyword

1. Create todos with various titles containing "groceries"
2. Select `[6] Search Todos`
3. Enter: "groceries"
4. Verify: Only matching todos shown
5. Verify: Title shows "SEARCH RESULTS: 'groceries'"

### Test 5: Search with No Results

1. Select `[6] Search Todos`
2. Enter: "xyznonexistent"
3. Verify: "No todos found!" message

## Test Filter (P2)

### Test 6: Filter by Status

1. Mark some todos complete
2. Select `[7] Filter Todos`
3. Select `[1] Status`
4. Select `[1] Pending only`
5. Verify: Only pending todos shown

### Test 7: Filter by Priority

1. Create todos with different priorities
2. Select `[7] Filter Todos`
3. Select `[3] Priority`
4. Select `[1] High`
5. Verify: Only high priority todos shown

### Test 8: Filter by Category

1. Create todos in different categories
2. Select `[7] Filter Todos`
3. Select `[2] Category`
4. Select `[1] Work`
5. Verify: Only work category todos shown

## Test Sort (P3)

### Test 9: Sort by Priority

1. Create todos with mixed priorities
2. Select `[8] Sort Todos`
3. Select `[1] Priority`
4. Verify: High priority first, then Medium, then Low

### Test 10: Sort by ID (Default)

1. Select `[8] Sort Todos`
2. Select `[3] ID`
3. Verify: Todos in ID order (1, 2, 3, ...)

## Test Non-Destructive Operations

### Test 11: Verify Data Unchanged After Filter

1. Note current todo order
2. Apply a filter
3. Return to main menu
4. Select `[2] View All Todos`
5. Verify: Original order preserved

### Test 12: Verify Data Unchanged After Sort

1. Note current todo order
2. Apply a sort
3. Return to main menu
4. Select `[2] View All Todos`
5. Verify: Original order preserved (sorted by ID)

## Success Criteria Verification

| Criteria | Test |
|----------|------|
| SC-001: Priority/Category in workflow | Tests 1-3 |
| SC-002: Search under 5 seconds | Test 4 |
| SC-003: Filter in 2 menu selections | Tests 6-8 |
| SC-004: Instant operations | All tests |
| SC-005: Priority/Category displayed | Test 1-2 |
| SC-006: Non-destructive operations | Tests 11-12 |
