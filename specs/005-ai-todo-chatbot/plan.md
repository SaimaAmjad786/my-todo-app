# Implementation Plan: AI Todo Chatbot (Phase III)

**Branch**: `005-ai-todo-chatbot` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-ai-todo-chatbot/spec.md`

## Summary

Build an AI-powered conversational Todo chatbot that allows users to manage their tasks through natural language. The system uses OpenAI Agents SDK for AI orchestration, MCP (Model Context Protocol) for tool exposure, and persists all state in Neon PostgreSQL for stateless operation. Frontend uses OpenAI ChatKit for the conversational UI.

## Technical Context

**Language/Version**: Python 3.13+ (Backend), TypeScript (Frontend)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, OpenAI ChatKit
**Storage**: Neon Serverless PostgreSQL (extended from Phase II)
**Testing**: pytest (backend), integration tests for chat flows
**Target Platform**: Web (Linux server deployment)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5s response time for chat, 100 concurrent sessions
**Constraints**: Stateless architecture, all state in database
**Scale/Scope**: Single tenant per user, conversation persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Specification complete with 30 FRs |
| II. Clean Architecture | PASS | Follows Phase III layers (Domain → MCP → Agent → API → Frontend) |
| III. Correctness Over Optimization | PASS | Focus on working implementation first |
| IV. Graceful User Interface | PASS | ChatKit provides professional chat UI |
| V. Code Quality | PASS | PEP 8, type hints, ESLint required |
| VI. Verification & Testing | PASS | MCP tool tests, integration tests planned |
| VII. Web Architecture | PASS | REST API extended with chat endpoints |
| VIII. Authentication & Security | PASS | JWT auth continued from Phase II |
| IX. Stateless AI Architecture | PASS | All state in PostgreSQL |

**Gate Result**: ALL PASS - Proceed to implementation

## Project Structure

### Documentation (this feature)

```text
specs/005-ai-todo-chatbot/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # Development setup guide
├── contracts/           # API contracts
│   └── chat-api.yaml    # OpenAPI spec for chat endpoint
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/
│   │   ├── task.py           # Existing Task model
│   │   ├── user.py           # Existing User model
│   │   ├── conversation.py   # NEW: Conversation model
│   │   └── message.py        # NEW: Message model
│   ├── services/
│   │   ├── task_service.py   # Existing task operations
│   │   └── chat_service.py   # NEW: Chat orchestration
│   ├── mcp/
│   │   ├── server.py         # NEW: MCP server setup
│   │   └── tools.py          # NEW: MCP tool definitions
│   ├── agent/
│   │   └── todo_agent.py     # NEW: OpenAI Agent configuration
│   └── api/
│       ├── routes/
│       │   ├── tasks.py      # Existing task routes
│       │   └── chat.py       # NEW: Chat endpoint
│       └── deps.py           # Dependencies (auth, db)
└── tests/
    ├── unit/
    │   └── test_mcp_tools.py # MCP tool unit tests
    └── integration/
        └── test_chat_flow.py # End-to-end chat tests

frontend/
├── src/
│   ├── components/
│   │   └── chat/
│   │       ├── ChatInterface.tsx  # NEW: ChatKit wrapper
│   │       └── MessageList.tsx    # NEW: Message display
│   ├── pages/
│   │   └── chat.tsx              # NEW: Chat page
│   └── services/
│       └── chatApi.ts            # NEW: Chat API client
└── tests/
```

**Structure Decision**: Web application structure with backend/ and frontend/ directories. Phase III adds new modules (mcp/, agent/) to backend without modifying existing Phase II code.

---

## Phase 0: Research & Technology Decisions

### Decision 1: OpenAI Agents SDK Integration Pattern

**Decision**: Use OpenAI Agents SDK with function calling for MCP tool invocation

**Rationale**:
- OpenAI Agents SDK provides built-in conversation management
- Function calling allows declarative tool definitions
- SDK handles retry logic and error handling

**Alternatives Considered**:
- LangChain: More complex, overkill for this use case
- Direct OpenAI API: Less abstraction, more boilerplate
- Anthropic Claude: Different API, would require separate frontend

### Decision 2: MCP Server Architecture

**Decision**: In-process MCP server running within FastAPI application

**Rationale**:
- Simpler deployment (single process)
- Direct database access without RPC overhead
- Tools can reuse existing service layer

**Alternatives Considered**:
- Separate MCP server process: Added complexity, IPC overhead
- HTTP-based tool calls: Latency, more failure points

### Decision 3: Conversation State Management

**Decision**: Load full conversation history on each request, persist after each response

**Rationale**:
- True stateless architecture
- Survives server restarts
- Simple to implement and debug

**Alternatives Considered**:
- In-memory cache with persistence: Complexity, cache invalidation issues
- Streaming with checkpoints: Overkill for this scale

### Decision 4: ChatKit Integration

**Decision**: Use OpenAI ChatKit with custom styling to match existing UI

**Rationale**:
- Official OpenAI component library
- Built-in streaming support
- Handles message rendering, input, loading states

**Alternatives Considered**:
- Custom chat UI: More work, no streaming support
- Third-party chat libraries: Compatibility concerns with OpenAI API

---

## Phase 1: Setup Phase

**Goal**: Project infrastructure and dependencies

**Outputs**:
- Updated backend dependencies (OpenAI SDK, MCP SDK)
- Updated frontend dependencies (ChatKit)
- Database migrations for Conversation and Message tables
- Environment configuration for OpenAI API key

**Tasks**:
1. Add OpenAI Agents SDK to backend requirements
2. Add MCP SDK to backend requirements
3. Add ChatKit to frontend dependencies
4. Create Alembic migration for Conversation table
5. Create Alembic migration for Message table
6. Add OPENAI_API_KEY to environment configuration
7. Configure CORS for ChatKit frontend

---

## Phase 2: Backend Phase - Database Models

**Goal**: Extend database schema for chat functionality

**Outputs**:
- Conversation SQLModel
- Message SQLModel
- Database relationships configured

**Tasks**:
1. Create Conversation model with user_id foreign key
2. Create Message model with conversation_id foreign key
3. Add role enum (user, assistant, system)
4. Configure cascade delete for messages when conversation deleted
5. Add indexes for efficient conversation retrieval

---

## Phase 3: MCP Phase - Tool Server

**Goal**: Expose todo operations as MCP tools

**Outputs**:
- MCP server configuration
- 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Tool response schemas

**Tasks**:
1. Initialize MCP server with Official SDK
2. Implement add_task tool with user_id context
3. Implement list_tasks tool with status filter
4. Implement complete_task tool with ownership validation
5. Implement delete_task tool with ownership validation
6. Implement update_task tool with partial updates
7. Define JSON response schemas for each tool
8. Add error handling for invalid operations

---

## Phase 4: Agent Phase - AI Integration

**Goal**: Configure OpenAI Agent with MCP tools

**Outputs**:
- Agent configuration with system prompt
- Tool binding to MCP server
- Conversation context loading

**Tasks**:
1. Create agent configuration with todo-focused system prompt
2. Bind MCP tools to agent function definitions
3. Implement conversation history loading from database
4. Implement message saving (user message before agent, assistant after)
5. Add confirmation flow for destructive actions (delete)
6. Handle agent errors gracefully with user-friendly messages

---

## Phase 5: API Phase - Chat Endpoint

**Goal**: REST endpoint for chat interactions

**Outputs**:
- POST /api/{user_id}/chat endpoint
- Request/response schemas
- Authentication integration

**Tasks**:
1. Create ChatRequest schema (conversation_id optional, message required)
2. Create ChatResponse schema (conversation_id, response, tool_calls)
3. Implement chat endpoint with JWT authentication
4. Create new conversation when conversation_id not provided
5. Validate conversation ownership before processing
6. Return 400 for empty messages
7. Return 404 for invalid conversation_id

---

## Phase 6: Frontend Phase - ChatKit Integration

**Goal**: Conversational UI using OpenAI ChatKit

**Outputs**:
- Chat page with ChatKit component
- Message history display
- API integration

**Tasks**:
1. Install and configure ChatKit dependencies
2. Create ChatInterface component wrapping ChatKit
3. Implement chat API client service
4. Add conversation persistence (store conversation_id)
5. Display loading state during AI processing
6. Handle and display errors inline
7. Style to match existing application theme

---

## Phase 7: Deployment Phase

**Goal**: Production deployment configuration

**Outputs**:
- Updated deployment configuration
- Environment variables for production
- Domain allowlist for ChatKit

**Tasks**:
1. Add OPENAI_API_KEY to production environment
2. Configure ChatKit allowed domains
3. Update CORS settings for production frontend URL
4. Test end-to-end flow in staging environment
5. Document deployment steps

---

## Phase 8: Testing Phase

**Goal**: Verify all functionality

**Outputs**:
- MCP tool unit tests
- Chat endpoint integration tests
- End-to-end chat flow tests

**Tasks**:
1. Write unit tests for each MCP tool
2. Write integration test for new conversation creation
3. Write integration test for conversation resumption
4. Write integration test for task operations via chat
5. Write integration test for error handling
6. Verify stateless behavior (restart server, resume conversation)

---

## Dependencies & Execution Order

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Database Models) ──────┐
    │                           │
    ▼                           │
Phase 3 (MCP Tools) ◄───────────┘
    │
    ▼
Phase 4 (Agent)
    │
    ▼
Phase 5 (API Endpoint)
    │
    ├────────────────┐
    ▼                ▼
Phase 6 (Frontend)   Phase 8 (Testing)
    │                │
    ▼                │
Phase 7 (Deployment) ◄─────────┘
```

**Critical Path**: Setup → Models → MCP → Agent → API → Frontend → Deployment

**Parallel Opportunities**:
- Frontend (Phase 6) can start after API (Phase 5) is defined
- Testing (Phase 8) can run in parallel with Frontend development

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API rate limits | Medium | High | Implement retry with backoff, cache common responses |
| MCP SDK compatibility | Low | Medium | Use official SDK, pin versions |
| Conversation context too large | Low | Medium | Implement message truncation for old conversations |
| ChatKit styling conflicts | Low | Low | Use CSS isolation, override styles as needed |

---

## Complexity Tracking

> No constitution violations detected. Implementation follows all principles.

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| New dependencies | Medium | OpenAI SDK, MCP SDK, ChatKit all well-documented |
| Database changes | Low | Two new tables, simple relationships |
| Architecture change | Medium | New layers (MCP, Agent) added cleanly |
| Testing | Medium | Agent responses require pattern validation |
