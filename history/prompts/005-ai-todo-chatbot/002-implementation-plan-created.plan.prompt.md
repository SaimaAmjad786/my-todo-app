---
id: 002
title: AI Chatbot Implementation Plan Created
stage: plan
date: 2026-01-18
surface: agent
model: claude-opus-4-5-20251101
feature: 005-ai-todo-chatbot
branch: 005-ai-todo-chatbot
user: user
command: /sp.plan
labels: ["phase-iii", "ai-chatbot", "mcp", "openai-agents-sdk", "implementation-plan"]
links:
  spec: specs/005-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-ai-todo-chatbot/plan.md
  - specs/005-ai-todo-chatbot/research.md
  - specs/005-ai-todo-chatbot/data-model.md
  - specs/005-ai-todo-chatbot/quickstart.md
  - specs/005-ai-todo-chatbot/contracts/chat-api.yaml
tests:
  - N/A
---

## Prompt

Create a step-by-step development plan for Phase III.

Plan Must Cover:

1) Database setup with SQLModel and Neon
2) FastAPI backend structure
3) MCP server with tools
4) OpenAI Agents SDK integration
5) Stateless chat flow
6) ChatKit frontend integration
7) Authentication with Better Auth
8) Deployment steps
9) Domain allowlist for ChatKit
10) Testing scenarios

Plan in logical phases:
- Setup phase
- Backend phase
- MCP phase
- Agent phase
- Frontend phase
- Deployment phase

Each phase must define clear goals and outputs.

## Response snapshot

Created comprehensive implementation plan for Phase III AI Todo Chatbot:

**Plan File**: `specs/005-ai-todo-chatbot/plan.md`

**8 Implementation Phases**:
1. Setup Phase - Dependencies, migrations, environment
2. Backend Phase - Conversation & Message models
3. MCP Phase - 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
4. Agent Phase - OpenAI Agents SDK integration
5. API Phase - POST /api/{user_id}/chat endpoint
6. Frontend Phase - ChatKit integration
7. Deployment Phase - Production configuration
8. Testing Phase - Unit and integration tests

**Supporting Documents Created**:
- `research.md` - Technology decisions and rationale
- `data-model.md` - Conversation and Message entity definitions
- `contracts/chat-api.yaml` - OpenAPI specification
- `quickstart.md` - Development setup guide

**Constitution Check**: ALL 9 PRINCIPLES PASS

**Key Architecture Decisions**:
- In-process MCP server within FastAPI
- Full conversation reload from DB per request (stateless)
- OpenAI Agents SDK with function calling
- ChatKit wrapped in custom component

## Outcome

- ✅ Impact: Complete Phase III implementation plan ready for task generation
- 🧪 Tests: N/A (planning document)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.yaml
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan covers all 10 requested areas with clear phases and dependencies

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check PASS (9/9 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with /sp.tasks
