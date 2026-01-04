# Data Model: Phase II Full-Stack Todo Application

**Date**: 2025-12-31
**Branch**: `004-phase-ii-fullstack`
**Purpose**: Define database entities, relationships, and validation rules

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      User       │       │      Todo       │       │      Tag        │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK, UUID)   │──┐    │ id (PK, UUID)   │    ┌──│ id (PK, UUID)   │
│ email (unique)  │  │    │ user_id (FK)    │────┘  │ name            │
│ name            │  └───▶│ title           │       │ user_id (FK)    │
│ created_at      │       │ description     │       │ created_at      │
│ updated_at      │       │ completed       │       └─────────────────┘
└─────────────────┘       │ priority        │              │
                          │ due_date        │              │
                          │ reminder_time   │              │
                          │ recurrence      │              │
                          │ parent_id (FK)  │──┐           │
                          │ created_at      │  │           │
                          │ updated_at      │  │           │
                          └─────────────────┘  │           │
                                 │             │           │
                                 └─────────────┘           │
                                                           │
                          ┌─────────────────┐              │
                          │   TodoTag       │              │
                          │  (Junction)     │              │
                          ├─────────────────┤              │
                          │ todo_id (FK)    │◀─────────────┤
                          │ tag_id (FK)     │◀─────────────┘
                          └─────────────────┘
```

## Entities

### User

Managed by Better Auth. The following fields are the minimum expected:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| name | VARCHAR(100) | NULLABLE | Optional display name |
| created_at | TIMESTAMP | NOT NULL, default NOW() | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, auto-updated | Last update time |

**Note**: Password hash and session fields managed by Better Auth internally.

### Todo

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| user_id | UUID | FK → User.id, NOT NULL | Owner of the todo |
| title | VARCHAR(255) | NOT NULL, min length 1 | Todo title |
| description | TEXT | NULLABLE | Optional detailed description |
| completed | BOOLEAN | NOT NULL, default FALSE | Completion status |
| priority | ENUM | NOT NULL, default 'medium' | Priority level: high/medium/low |
| due_date | TIMESTAMP | NULLABLE | Optional deadline |
| reminder_time | TIMESTAMP | NULLABLE | Optional reminder notification time |
| recurrence | ENUM | NOT NULL, default 'none' | Recurrence pattern: none/daily/weekly/monthly |
| parent_id | UUID | FK → Todo.id, NULLABLE | Reference to parent recurring todo |
| created_at | TIMESTAMP | NOT NULL, default NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, auto-updated | Last update time |

**Indexes**:
- `idx_todo_user_id` on `user_id` (foreign key lookup)
- `idx_todo_user_completed` on `(user_id, completed)` (filter by status)
- `idx_todo_user_priority` on `(user_id, priority)` (filter by priority)
- `idx_todo_user_due_date` on `(user_id, due_date)` (sort by due date)

### Tag

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| name | VARCHAR(50) | NOT NULL | Tag label |
| user_id | UUID | FK → User.id, NOT NULL | Owner of the tag |
| created_at | TIMESTAMP | NOT NULL, default NOW() | Creation time |

**Constraints**:
- UNIQUE constraint on `(user_id, name)` - tag names unique per user

**Indexes**:
- `idx_tag_user_id` on `user_id` (foreign key lookup)
- `idx_tag_user_name` on `(user_id, name)` (unique constraint index)

### TodoTag (Junction Table)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| todo_id | UUID | FK → Todo.id, NOT NULL | Reference to todo |
| tag_id | UUID | FK → Tag.id, NOT NULL | Reference to tag |

**Constraints**:
- Composite PK on `(todo_id, tag_id)`
- ON DELETE CASCADE for both foreign keys

## Enumerations

### Priority

```sql
CREATE TYPE priority_level AS ENUM ('high', 'medium', 'low');
```

| Value | Display | Sort Order |
|-------|---------|------------|
| high | High | 1 |
| medium | Medium | 2 |
| low | Low | 3 |

### Recurrence

```sql
CREATE TYPE recurrence_pattern AS ENUM ('none', 'daily', 'weekly', 'monthly');
```

| Value | Description |
|-------|-------------|
| none | One-time task (no recurrence) |
| daily | Repeats every day |
| weekly | Repeats every 7 days |
| monthly | Repeats every month (same day of month) |

## Validation Rules

### User Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| email | Valid email format | "Invalid email format" |
| email | Max 255 characters | "Email must be 255 characters or less" |
| name | Max 100 characters | "Name must be 100 characters or less" |

### Todo Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| title | Not empty | "Title is required" |
| title | Max 255 characters | "Title must be 255 characters or less" |
| description | Max 5000 characters | "Description must be 5000 characters or less" |
| due_date | Must be valid ISO date if provided | "Invalid date format" |
| reminder_time | Must be before or equal to due_date | "Reminder must be before or on due date" |
| recurrence | Must be valid enum value | "Invalid recurrence pattern" |
| priority | Must be valid enum value | "Invalid priority level" |

### Tag Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| name | Not empty | "Tag name is required" |
| name | Max 50 characters | "Tag name must be 50 characters or less" |
| name | Alphanumeric + spaces + hyphens only | "Tag name contains invalid characters" |

## State Transitions

### Todo Completion

```
┌───────────────┐     mark_complete()    ┌───────────────┐
│   Incomplete  │ ─────────────────────▶ │   Completed   │
│ completed=F   │                        │ completed=T   │
└───────────────┘                        └───────────────┘
        ▲                                        │
        │                                        │
        └──────── mark_incomplete() ◀────────────┘
```

### Recurring Todo Lifecycle

```
┌───────────────────────────────────────────────────────────────────┐
│                     Recurring Todo Created                         │
│  (recurrence != 'none', due_date set)                             │
└───────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────┐
│                     User Marks Complete                            │
└───────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────┐
│                     System Creates Next Instance                   │
│  - New todo with parent_id = completed todo's id                  │
│  - due_date = calculate_next_due_date(recurrence, old_due_date)   │
│  - completed = FALSE                                               │
│  - reminder_time recalculated if original had reminder            │
└───────────────────────────────────────────────────────────────────┘
```

### Next Due Date Calculation

| Recurrence | Calculation |
|------------|-------------|
| daily | due_date + 1 day |
| weekly | due_date + 7 days |
| monthly | due_date + 1 month (same day, or last day if overflow) |

## Data Access Patterns

### Common Queries

1. **List user's todos** (with filters)
   - Filter by: user_id, completed, priority, tags, search term
   - Sort by: created_at, due_date, priority, title
   - Pagination: offset/limit

2. **Get todo by ID**
   - Verify user ownership (WHERE user_id = ?)

3. **Search todos**
   - Full-text search on title and description
   - Case-insensitive matching

4. **Filter by tag**
   - JOIN through TodoTag junction table

5. **Get user's tags**
   - All tags created by user (for tag picker/autocomplete)

### Query Performance Considerations

- User-scoped queries always include `user_id` in WHERE clause
- Composite indexes support common filter combinations
- Full-text search may use PostgreSQL `ILIKE` for simplicity (or `tsvector` for scale)
- Pagination uses `OFFSET/LIMIT` (acceptable for <10K todos per user)

## Migration Strategy

### Initial Migration (001_initial_schema)

1. Create `priority_level` enum type
2. Create `recurrence_pattern` enum type
3. Create `users` table (Better Auth managed)
4. Create `todos` table with all fields
5. Create `tags` table
6. Create `todo_tags` junction table
7. Create indexes

### Future Migrations

- Add new columns with defaults
- Never delete columns without deprecation period
- Enum additions are safe; removals require data migration
