# Data Model: Todo App Intermediate Level

**Branch**: `002-intermediate-enhancements` | **Date**: 2025-12-27

## Entities

### Todo (Extended)

The core task entity with Phase II extensions.

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| id | int | Yes | Auto-increment | Unique, positive |
| title | str | Yes | - | Non-empty, trimmed |
| description | str | No | "" | Trimmed |
| completed | bool | No | False | - |
| priority | str | No | "medium" | One of: high, medium, low |
| category | str | No | "general" | One of: work, personal, shopping, health, general |
| due_date | str | No | "" | Format: YYYY-MM-DD or empty |

### Priority (Value Object)

Enumeration of task urgency levels.

| Value | Display | Color | Symbol |
|-------|---------|-------|--------|
| high | HIGH | Red | !!! |
| medium | MEDIUM | Yellow | !! |
| low | LOW | Green | ! |

### Category (Value Object)

Predefined groupings for task organization.

| Value | Display | Color | Icon |
|-------|---------|-------|------|
| work | Work | Blue | [W] |
| personal | Personal | Magenta | [P] |
| shopping | Shopping | Green | [S] |
| health | Health | Red | [H] |
| general | General | Cyan | [G] |

## Data Flow

```
User Input → CLI Layer → Service Layer → Model Layer → JSON Storage
              ↓                ↓              ↓
         Validation      Business Logic   Data Structure
```

## Storage Format (JSON)

```json
{
  "todos": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, bread, eggs",
      "completed": false,
      "priority": "high",
      "due_date": "",
      "category": "shopping"
    }
  ],
  "next_id": 2
}
```

## Relationships

- Todo has exactly ONE priority (required, defaults to "medium")
- Todo has exactly ONE category (required, defaults to "general")
- No relationships between todos (flat structure)
