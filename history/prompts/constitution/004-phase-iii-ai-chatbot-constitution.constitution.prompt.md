---
id: 004
title: Phase III AI Chatbot Constitution Amendment
stage: constitution
date: 2026-01-18
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: temp_main
user: user
command: /sp.constitution
labels: ["phase-iii", "ai-chatbot", "mcp", "openai-agents-sdk", "constitution"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

You are designing Phase III of a Fullstack Todo AI Chatbot.

Goal:
Build an AI-powered conversational Todo chatbot using MCP (Model Context Protocol) with OpenAI Agents SDK.

System Must:
- Use FastAPI backend
- Use OpenAI ChatKit frontend
- Use OpenAI Agents SDK for AI logic
- Use Official MCP SDK for tools
- Be fully stateless
- Store all state in Neon PostgreSQL using SQLModel
- Support authentication with Better Auth

Core Idea:
Users interact in natural language and the AI will:
- Add, list, update, delete, and complete todos
- Use MCP tools for all task actions
- Store conversations and messages in the database
- Resume chats after server restart

Architecture:
Frontend: OpenAI ChatKit
Backend: FastAPI
AI: OpenAI Agents SDK
Tools: MCP Server (Official SDK)
DB: Neon PostgreSQL

Rules:
- Follow spec-driven development strictly
- No guessing or extra features
- Only what the spec allows

## Response snapshot

Updated constitution from v3.1.0 to v4.0.0 (MAJOR version bump) with:

**Key Changes:**
- Phase II marked as "Completed", Phase III marked as "Current"
- Added Phase III architecture layers (MCP Tools Layer, AI Agent Layer, ChatKit Frontend)
- Added new principle IX: Stateless AI Architecture
- Added Technical Stack for Phase III (OpenAI Agents SDK, MCP SDK, ChatKit)
- Added Conversation and Message entities to domain model
- Defined 7 MCP tools (add_todo, list_todos, get_todo, update_todo, delete_todo, complete_todo, uncomplete_todo)
- Added Phase III Success Criteria
- Extended Authentication & Security principle for Phase III

**Architecture Defined:**
- Frontend: OpenAI ChatKit
- Backend: FastAPI (extended)
- AI: OpenAI Agents SDK
- Tools: Official MCP SDK
- Database: Neon PostgreSQL (extended schema)
- Auth: JWT (continued from Phase II)

## Outcome

- ✅ Impact: Constitution v4.0.0 defines complete Phase III scope for AI chatbot
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: /sp.specify, /sp.plan, /sp.tasks for Phase III implementation
- 🧠 Reflection: Major constitution amendment establishes clear boundaries for AI chatbot feature

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with spec creation for Phase III
