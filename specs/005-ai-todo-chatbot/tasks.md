# Tasks: AI Todo Chatbot (Phase III)

**Input**: Design documents from `/specs/005-ai-todo-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat-api.yaml

**Tests**: Included as requested in user input (testing scenarios required)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for source, `backend/tests/` for tests
- **Frontend**: `frontend/src/` for source, `frontend/tests/` for tests

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and environment configuration

- [ ] T001 Add OpenAI Agents SDK to backend requirements in backend/requirements.txt
- [ ] T002 Add MCP SDK to backend requirements in backend/requirements.txt
- [ ] T003 [P] Add ChatKit dependency to frontend in frontend/package.json
- [ ] T004 [P] Add OPENAI_API_KEY to environment configuration in backend/.env.example
- [ ] T005 [P] Configure CORS for ChatKit frontend in backend/app/main.py

**Output**: All dependencies installed, environment configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models and migrations that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [ ] T006 Create MessageRole enum in backend/app/models/enums.py
- [ ] T007 Create Conversation model with user_id FK in backend/app/models/conversation.py
- [ ] T008 Create Message model with conversation_id FK in backend/app/models/message.py
- [ ] T009 Register new models in backend/app/models/__init__.py
- [ ] T010 Create Alembic migration for conversations table in backend/alembic/versions/
- [ ] T011 Create Alembic migration for messages table in backend/alembic/versions/
- [ ] T012 Run migrations and verify tables created

### MCP Server Foundation

- [ ] T013 Create MCP server initialization in backend/app/mcp/server.py
- [ ] T014 Create MCP tool response schemas in backend/app/mcp/schemas.py

### API Schemas

- [ ] T015 [P] Create ChatRequest schema in backend/app/api/schemas/chat.py
- [ ] T016 [P] Create ChatResponse schema in backend/app/api/schemas/chat.py
- [ ] T017 [P] Create ToolCall schema in backend/app/api/schemas/chat.py

**Checkpoint**: Foundation ready - database, MCP server, and schemas in place

---

## Phase 3: User Story 1 - Send Chat Message and Get AI Response (Priority: P1)

**Goal**: User can send a message and receive AI response with task creation

**Independent Test**: Send POST /api/{user_id}/chat with message, verify response contains conversation_id and AI response

### Tests for User Story 1

- [ ] T018 [P] [US1] Unit test for add_task MCP tool in backend/tests/unit/test_mcp_tools.py
- [ ] T019 [P] [US1] Integration test for chat endpoint new conversation in backend/tests/integration/test_chat_flow.py

### MCP Tools for User Story 1

- [ ] T020 [US1] Implement add_task MCP tool in backend/app/mcp/tools.py
- [ ] T021 [US1] Add tool registration to MCP server in backend/app/mcp/server.py

### Agent Setup for User Story 1

- [ ] T022 [US1] Create agent configuration with system prompt in backend/app/agent/todo_agent.py
- [ ] T023 [US1] Bind add_task tool to agent function definitions in backend/app/agent/todo_agent.py
- [ ] T024 [US1] Implement agent run function with tool calling in backend/app/agent/todo_agent.py

### Chat Service for User Story 1

- [ ] T025 [US1] Create ChatService class in backend/app/services/chat_service.py
- [ ] T026 [US1] Implement create_conversation method in backend/app/services/chat_service.py
- [ ] T027 [US1] Implement save_message method in backend/app/services/chat_service.py
- [ ] T028 [US1] Implement process_chat method (stateless flow) in backend/app/services/chat_service.py

### API Endpoint for User Story 1

- [ ] T029 [US1] Create POST /api/{user_id}/chat endpoint in backend/app/api/routes/chat.py
- [ ] T030 [US1] Add JWT authentication to chat endpoint in backend/app/api/routes/chat.py
- [ ] T031 [US1] Handle new conversation creation when conversation_id not provided
- [ ] T032 [US1] Return 400 for empty message validation in backend/app/api/routes/chat.py
- [ ] T033 [US1] Register chat router in backend/app/main.py

**Checkpoint**: User can send message "Add a task to buy milk" and receive AI confirmation with task created

---

## Phase 4: User Story 2 - Resume Previous Conversation (Priority: P2)

**Goal**: User can continue conversation with existing conversation_id, AI maintains context

**Independent Test**: Create conversation, restart server, send message with same conversation_id, verify context maintained

### Tests for User Story 2

- [ ] T034 [P] [US2] Integration test for conversation resumption in backend/tests/integration/test_chat_flow.py
- [ ] T035 [P] [US2] Integration test for context awareness in backend/tests/integration/test_chat_flow.py

### Implementation for User Story 2

- [ ] T036 [US2] Implement load_conversation_history method in backend/app/services/chat_service.py
- [ ] T037 [US2] Implement get_conversation_by_id method in backend/app/services/chat_service.py
- [ ] T038 [US2] Add conversation ownership validation in backend/app/services/chat_service.py
- [ ] T039 [US2] Pass conversation history to agent for context in backend/app/agent/todo_agent.py
- [ ] T040 [US2] Return 404 for invalid conversation_id in backend/app/api/routes/chat.py
- [ ] T041 [US2] Update conversation updated_at on new message in backend/app/services/chat_service.py

**Checkpoint**: User can reference "that task" from earlier in conversation and AI understands

---

## Phase 5: User Story 3 - Manage Tasks via Natural Language (Priority: P3)

**Goal**: User can list, complete, update, and delete tasks through chat

**Independent Test**: Create tasks, then use chat to list/complete/update/delete, verify each operation

### Tests for User Story 3

- [ ] T042 [P] [US3] Unit test for list_tasks MCP tool in backend/tests/unit/test_mcp_tools.py
- [ ] T043 [P] [US3] Unit test for complete_task MCP tool in backend/tests/unit/test_mcp_tools.py
- [ ] T044 [P] [US3] Unit test for update_task MCP tool in backend/tests/unit/test_mcp_tools.py
- [ ] T045 [P] [US3] Unit test for delete_task MCP tool in backend/tests/unit/test_mcp_tools.py
- [ ] T046 [P] [US3] Integration test for task operations via chat in backend/tests/integration/test_chat_flow.py

### MCP Tools for User Story 3

- [ ] T047 [US3] Implement list_tasks MCP tool with status filter in backend/app/mcp/tools.py
- [ ] T048 [US3] Implement complete_task MCP tool in backend/app/mcp/tools.py
- [ ] T049 [US3] Implement update_task MCP tool in backend/app/mcp/tools.py
- [ ] T050 [US3] Implement delete_task MCP tool in backend/app/mcp/tools.py
- [ ] T051 [US3] Add ownership validation to all tools in backend/app/mcp/tools.py
- [ ] T052 [US3] Register all tools with MCP server in backend/app/mcp/server.py
- [ ] T053 [US3] Bind all tools to agent function definitions in backend/app/agent/todo_agent.py

**Checkpoint**: User can manage full task lifecycle through natural language

---

## Phase 6: User Story 4 - Error Handling and Confirmation (Priority: P4)

**Goal**: AI handles errors gracefully, confirms destructive actions

**Independent Test**: Trigger error conditions, verify friendly messages; request deletion, verify confirmation flow

### Tests for User Story 4

- [ ] T054 [P] [US4] Integration test for error handling in backend/tests/integration/test_chat_flow.py
- [ ] T055 [P] [US4] Integration test for delete confirmation flow in backend/tests/integration/test_chat_flow.py

### Implementation for User Story 4

- [ ] T056 [US4] Add confirmation prompt to agent system prompt for delete in backend/app/agent/todo_agent.py
- [ ] T057 [US4] Implement tool error handling with user-friendly messages in backend/app/mcp/tools.py
- [ ] T058 [US4] Add task disambiguation when multiple matches in backend/app/mcp/tools.py
- [ ] T059 [US4] Implement API error responses (400, 401, 403, 404, 503) in backend/app/api/routes/chat.py
- [ ] T060 [US4] Add service unavailable handling for OpenAI API errors in backend/app/services/chat_service.py

**Checkpoint**: Errors are user-friendly, delete always asks confirmation first

---

## Phase 7: Frontend - ChatKit Integration

**Goal**: Chat UI using OpenAI ChatKit connected to backend API

### Frontend Components

- [ ] T061 [P] Create chatApi service in frontend/src/services/chatApi.ts
- [ ] T062 Create ChatInterface component wrapping ChatKit in frontend/src/components/chat/ChatInterface.tsx
- [ ] T063 Create MessageList component in frontend/src/components/chat/MessageList.tsx
- [ ] T064 Create chat page in frontend/src/pages/chat.tsx
- [ ] T065 Add chat button/link to navigation in frontend/src/components/
- [ ] T066 Implement conversation persistence (store conversation_id in localStorage) in frontend/src/services/chatApi.ts
- [ ] T067 Add loading state during AI processing in frontend/src/components/chat/ChatInterface.tsx
- [ ] T068 Display errors inline in conversation in frontend/src/components/chat/ChatInterface.tsx
- [ ] T069 Style ChatKit to match existing application theme in frontend/src/styles/

**Checkpoint**: User can access chat from frontend, send messages, see responses

---

## Phase 8: Deployment & Production

**Goal**: Production-ready configuration

- [ ] T070 Add OPENAI_API_KEY to production environment variables
- [ ] T071 Configure ChatKit allowed domains for production in frontend/next.config.js
- [ ] T072 Update CORS settings for production frontend URL in backend/app/main.py
- [ ] T073 [P] Add rate limiting for chat endpoint in backend/app/api/routes/chat.py
- [ ] T074 [P] Add logging for chat operations in backend/app/services/chat_service.py
- [ ] T075 Document deployment steps in specs/005-ai-todo-chatbot/quickstart.md
- [ ] T076 Test end-to-end flow in staging environment

**Checkpoint**: Application deployed and functional in production

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [ ] T077 [P] Verify stateless behavior (restart server, resume conversation)
- [ ] T078 [P] Run all unit tests and verify passing
- [ ] T079 [P] Run all integration tests and verify passing
- [ ] T080 Code cleanup and remove debug statements
- [ ] T081 Update quickstart.md with final verification steps

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ─── BLOCKS ALL USER STORIES
    │
    ├──────────────────────────────────┐
    ▼                                  │
Phase 3 (US1 - Chat & Add Task)        │
    │                                  │
    ▼                                  │
Phase 4 (US2 - Resume Conversation)    │
    │                                  │
    ▼                                  │
Phase 5 (US3 - Full Task Management)   │
    │                                  │
    ▼                                  │
Phase 6 (US4 - Error Handling)         │
    │                                  │
    ├──────────────────────────────────┤
    ▼                                  ▼
Phase 7 (Frontend)              Phase 8 (Deployment)
    │                                  │
    └──────────────┬───────────────────┘
                   ▼
           Phase 9 (Polish)
```

### User Story Dependencies

- **US1 (P1)**: Requires Foundational phase - establishes core chat loop
- **US2 (P2)**: Requires US1 - extends conversation handling
- **US3 (P3)**: Requires US1 - adds more MCP tools
- **US4 (P4)**: Requires US1, US3 - adds error handling to existing tools

### Parallel Opportunities

**Within Phase 1:**
```bash
# Can run in parallel:
T003 (ChatKit) | T004 (env) | T005 (CORS)
```

**Within Phase 2:**
```bash
# Can run in parallel:
T015 | T016 | T017 (all schemas)
```

**Within Phase 3 Tests:**
```bash
# Can run in parallel:
T018 | T019 (test files)
```

**Within Phase 5 Tests:**
```bash
# Can run in parallel:
T042 | T043 | T044 | T045 | T046 (all tests)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test "Add a task to buy milk" works end-to-end
5. Deploy MVP if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Test → Deploy (MVP - can add tasks via chat!)
3. Add US2 → Test → Deploy (can resume conversations)
4. Add US3 → Test → Deploy (full CRUD via chat)
5. Add US4 → Test → Deploy (polished error handling)
6. Add Frontend → Test → Deploy (complete chat UI)
7. Polish → Final Deploy

---

## Task Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Setup | 5 | 3 |
| Foundational | 12 | 3 |
| US1 (P1) | 16 | 2 |
| US2 (P2) | 8 | 2 |
| US3 (P3) | 12 | 5 |
| US4 (P4) | 7 | 2 |
| Frontend | 9 | 1 |
| Deployment | 7 | 2 |
| Polish | 5 | 3 |
| **TOTAL** | **81** | **23** |

---

## Notes

- [P] tasks = different files, no dependencies within same phase
- [US#] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MCP tools must validate user ownership before any operation
- All state in database - no in-memory state between requests
