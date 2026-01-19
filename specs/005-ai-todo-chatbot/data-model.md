# Data Model: AI Todo Chatbot (Phase III)

**Feature**: 005-ai-todo-chatbot
**Date**: 2026-01-18

## Entity Overview

Phase III introduces two new entities to support chat functionality:

```
┌─────────┐       ┌──────────────┐       ┌─────────┐
│  User   │──1:N──│ Conversation │──1:N──│ Message │
└─────────┘       └──────────────┘       └─────────┘
     │
     │ 1:N
     ▼
┌─────────┐
│  Task   │
└─────────┘
```

## Entities

### Task (Existing - Phase II)

Represents a todo item belonging to a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| user_id | UUID | FK → User.id, NOT NULL | Owner of the task |
| title | String | NOT NULL, max 255 chars | Task title |
| description | String | NULL allowed, max 2000 chars | Optional details |
| completed | Boolean | NOT NULL, default: false | Completion status |
| created_at | DateTime | NOT NULL, auto-generated | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto-updated | Last modification timestamp |

**Indexes**:
- `idx_task_user_id` on (user_id)
- `idx_task_user_completed` on (user_id, completed)

### Conversation (New - Phase III)

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| user_id | UUID | FK → User.id, NOT NULL | Owner of conversation |
| title | String | NULL allowed, max 100 chars | Optional conversation title |
| created_at | DateTime | NOT NULL, auto-generated | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto-updated | Updated on new message |

**Indexes**:
- `idx_conversation_user_id` on (user_id)
- `idx_conversation_updated` on (user_id, updated_at DESC)

**Relationships**:
- One User has many Conversations
- One Conversation has many Messages
- Cascade delete: Deleting Conversation deletes all its Messages

### Message (New - Phase III)

Represents a single message in a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| conversation_id | UUID | FK → Conversation.id, NOT NULL | Parent conversation |
| user_id | UUID | FK → User.id, NOT NULL | Message owner (for security) |
| role | Enum | NOT NULL | 'user', 'assistant', or 'system' |
| content | Text | NOT NULL | Message text content |
| tool_calls | JSON | NULL allowed | Tools invoked by assistant |
| tool_results | JSON | NULL allowed | Results from tool execution |
| created_at | DateTime | NOT NULL, auto-generated | Creation timestamp |

**Indexes**:
- `idx_message_conversation_id` on (conversation_id)
- `idx_message_conversation_created` on (conversation_id, created_at ASC)

**Relationships**:
- One Conversation has many Messages
- Messages ordered by created_at within conversation

## Enums

### MessageRole

```python
class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
```

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

### Message Model

```python
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Enum as SAEnum, JSON
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Any
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    role: MessageRole = Field(sa_column=Column(SAEnum(MessageRole), nullable=False))
    content: str = Field(nullable=False)
    tool_calls: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    tool_results: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

## Database Migration

### Migration: Create Conversations Table

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversation_user_id ON conversations(user_id);
CREATE INDEX idx_conversation_updated ON conversations(user_id, updated_at DESC);
```

### Migration: Create Messages Table

```sql
CREATE TYPE message_role AS ENUM ('user', 'assistant', 'system');

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    role message_role NOT NULL,
    content TEXT NOT NULL,
    tool_calls JSONB,
    tool_results JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_message_conversation_id ON messages(conversation_id);
CREATE INDEX idx_message_conversation_created ON messages(conversation_id, created_at ASC);
```

## Data Access Patterns

### Common Queries

1. **Get user's conversations** (sorted by recent activity):
   ```sql
   SELECT * FROM conversations
   WHERE user_id = :user_id
   ORDER BY updated_at DESC;
   ```

2. **Get conversation with messages**:
   ```sql
   SELECT c.*, m.* FROM conversations c
   LEFT JOIN messages m ON m.conversation_id = c.id
   WHERE c.id = :conversation_id AND c.user_id = :user_id
   ORDER BY m.created_at ASC;
   ```

3. **Add message to conversation**:
   ```sql
   INSERT INTO messages (conversation_id, user_id, role, content, tool_calls, tool_results)
   VALUES (:conversation_id, :user_id, :role, :content, :tool_calls, :tool_results);

   UPDATE conversations SET updated_at = NOW() WHERE id = :conversation_id;
   ```

## Validation Rules

### Conversation

- `user_id` must exist in users table
- `title` max 100 characters (if provided)

### Message

- `conversation_id` must exist and belong to same user
- `content` cannot be empty
- `role` must be valid enum value
- `tool_calls` must be valid JSON if provided
- `tool_results` must be valid JSON if provided

## Security Considerations

1. **User Scoping**: All queries must filter by user_id
2. **Ownership Validation**: Before accessing conversation, verify user_id matches
3. **No Cross-User Access**: Messages include user_id for additional security layer
4. **Cascade Deletes**: When user deleted, all conversations and messages deleted
