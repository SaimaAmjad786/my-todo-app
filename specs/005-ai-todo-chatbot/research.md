# Research: AI Todo Chatbot (Phase III)

**Feature**: 005-ai-todo-chatbot
**Date**: 2026-01-18
**Status**: Complete

## Research Questions

### 1. OpenAI Agents SDK vs Direct API

**Question**: Should we use OpenAI Agents SDK or direct OpenAI API calls?

**Decision**: Use OpenAI Agents SDK

**Rationale**:
- Agents SDK provides higher-level abstractions for tool calling
- Built-in conversation management and context handling
- Easier to define and bind tools
- Better error handling and retry logic

**Alternatives Considered**:
| Option | Pros | Cons |
|--------|------|------|
| Agents SDK | High-level API, tool binding, conversation management | Newer, less documentation |
| Direct API | Full control, well-documented | More boilerplate, manual tool handling |
| LangChain | Flexible, many integrations | Complex, overkill for this use case |

### 2. MCP Server Architecture

**Question**: How should the MCP server be structured?

**Decision**: In-process MCP server within FastAPI

**Rationale**:
- Single deployment unit
- Direct database access
- Reuse existing service layer
- No IPC overhead

**Implementation Pattern**:
```python
# MCP tools defined as Python functions
# Registered with OpenAI function calling schema
# Called by agent during conversation processing
```

### 3. Conversation Persistence Strategy

**Question**: How to handle conversation state across requests?

**Decision**: Full reload from database on each request

**Rationale**:
- True stateless architecture
- Survives server restarts
- Simple debugging (all state visible in DB)
- Scales horizontally without session affinity

**Trade-offs**:
- Slightly higher latency (DB read per request)
- Acceptable for expected scale (100 concurrent sessions)

### 4. ChatKit Integration Approach

**Question**: How to integrate OpenAI ChatKit with existing frontend?

**Decision**: Wrap ChatKit in custom component with existing theme

**Rationale**:
- ChatKit handles complex chat UI logic
- Custom wrapper allows styling integration
- API client connects to our backend, not OpenAI directly

**Key Considerations**:
- ChatKit sends messages to our FastAPI backend
- Backend handles OpenAI API calls
- Maintains our authentication layer

### 5. Tool Definition Schema

**Question**: What schema to use for MCP tool definitions?

**Decision**: OpenAI function calling JSON Schema

**Tool Definitions**:
```json
{
  "add_task": {
    "description": "Create a new todo task",
    "parameters": {
      "title": {"type": "string", "required": true},
      "description": {"type": "string", "required": false}
    }
  },
  "list_tasks": {
    "description": "List all tasks with optional filter",
    "parameters": {
      "status": {"type": "string", "enum": ["all", "completed", "pending"]}
    }
  },
  "complete_task": {
    "description": "Mark a task as completed",
    "parameters": {
      "task_id": {"type": "string", "required": true}
    }
  },
  "delete_task": {
    "description": "Delete a task permanently",
    "parameters": {
      "task_id": {"type": "string", "required": true}
    }
  },
  "update_task": {
    "description": "Update a task's title or description",
    "parameters": {
      "task_id": {"type": "string", "required": true},
      "title": {"type": "string"},
      "description": {"type": "string"}
    }
  }
}
```

### 6. Error Handling Strategy

**Question**: How should errors be communicated to users?

**Decision**: AI-friendly error messages returned to agent

**Pattern**:
1. Tool execution fails → Return structured error JSON
2. Agent receives error → Generates user-friendly explanation
3. User sees natural language error message

**Example**:
```json
// Tool returns:
{"success": false, "error": "task_not_found", "message": "No task with ID 123"}

// Agent responds:
"I couldn't find a task with that ID. Would you like me to show you your current tasks?"
```

### 7. Confirmation Flow for Destructive Actions

**Question**: How to implement delete confirmation?

**Decision**: Agent asks for confirmation in conversation

**Flow**:
1. User: "Delete my groceries task"
2. Agent: "Are you sure you want to delete 'Buy groceries'? This cannot be undone."
3. User: "Yes"
4. Agent calls delete_task tool
5. Agent: "Done! I've deleted the 'Buy groceries' task."

**Implementation**: System prompt instructs agent to confirm before delete operations.

## Technology Versions

| Package | Version | Notes |
|---------|---------|-------|
| openai | ^1.0.0 | Agents SDK included |
| mcp | ^1.0.0 | Official MCP SDK |
| @openai/chatkit | ^0.1.0 | React components |
| fastapi | existing | No version change |
| sqlmodel | existing | No version change |

## External Resources

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [OpenAI ChatKit](https://github.com/openai/chatkit)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
