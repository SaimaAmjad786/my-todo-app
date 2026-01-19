# Quickstart: AI Todo Chatbot (Phase III)

**Feature**: 005-ai-todo-chatbot
**Date**: 2026-01-18

## Prerequisites

Before starting Phase III development:

1. **Phase II must be complete and stable**
   - Backend running with FastAPI
   - Frontend running with Next.js
   - Database connected to Neon PostgreSQL
   - Authentication working with JWT

2. **Required accounts/keys**
   - OpenAI API key (with access to GPT-4 or later)
   - Existing Neon PostgreSQL database

## Environment Setup

### 1. Add Environment Variables

Add to your `.env` file:

```env
# Existing Phase II variables...

# Phase III - AI Chatbot
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4  # or gpt-4-turbo, gpt-3.5-turbo
```

### 2. Install Backend Dependencies

```bash
cd backend

# Add new dependencies
pip install openai>=1.0.0
pip install mcp>=1.0.0

# Or with UV
uv add openai>=1.0.0 mcp>=1.0.0
```

### 3. Install Frontend Dependencies

```bash
cd frontend

# Add ChatKit
npm install @openai/chatkit
# or
pnpm add @openai/chatkit
```

### 4. Run Database Migrations

```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "Add conversation and message tables"

# Apply migration
alembic upgrade head
```

## Development Workflow

### 1. Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 2. Start Frontend Server

```bash
cd frontend
npm run dev
# or
pnpm dev
```

### 3. Test Chat Endpoint

```bash
# Get a JWT token first (login)
TOKEN="your-jwt-token"

# Start a new conversation
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'

# Continue conversation
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "uuid-from-response", "message": "Show me all my tasks"}'
```

## File Structure After Setup

```
backend/
├── app/
│   ├── models/
│   │   ├── conversation.py   # NEW
│   │   └── message.py        # NEW
│   ├── services/
│   │   └── chat_service.py   # NEW
│   ├── mcp/
│   │   ├── server.py         # NEW
│   │   └── tools.py          # NEW
│   ├── agent/
│   │   └── todo_agent.py     # NEW
│   └── api/routes/
│       └── chat.py           # NEW

frontend/
├── src/
│   ├── components/chat/
│   │   ├── ChatInterface.tsx # NEW
│   │   └── MessageList.tsx   # NEW
│   ├── pages/
│   │   └── chat.tsx          # NEW
│   └── services/
│       └── chatApi.ts        # NEW
```

## Testing Checklist

### Backend Tests

```bash
cd backend

# Run MCP tool tests
pytest tests/unit/test_mcp_tools.py -v

# Run chat integration tests
pytest tests/integration/test_chat_flow.py -v
```

### Manual Testing Scenarios

1. **New Conversation**
   - Send message without conversation_id
   - Verify new conversation_id returned

2. **Add Task**
   - Message: "Add a task called 'Test task'"
   - Verify task created in database

3. **List Tasks**
   - Message: "Show me all my tasks"
   - Verify tasks listed correctly

4. **Complete Task**
   - Message: "Mark 'Test task' as complete"
   - Verify task.completed = true

5. **Delete Task (with confirmation)**
   - Message: "Delete 'Test task'"
   - Verify AI asks for confirmation
   - Confirm deletion
   - Verify task deleted

6. **Resume Conversation**
   - Restart backend server
   - Send message with existing conversation_id
   - Verify context maintained

## Troubleshooting

### OpenAI API Errors

```python
# Check API key
import openai
openai.api_key = "your-key"
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Database Connection Issues

```bash
# Test Neon connection
psql "postgresql://user:pass@host/db?sslmode=require"

# Check migrations
alembic current
alembic history
```

### CORS Issues

Ensure backend CORS settings include frontend URL:

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment Notes

### Production Environment Variables

```env
OPENAI_API_KEY=sk-production-key
OPENAI_MODEL=gpt-4
CHATKIT_ALLOWED_DOMAINS=https://yourdomain.com
```

### ChatKit Domain Allowlist

Configure allowed domains in your ChatKit settings to prevent unauthorized usage:

```javascript
// frontend/next.config.js
module.exports = {
  env: {
    CHATKIT_ALLOWED_DOMAINS: process.env.CHATKIT_ALLOWED_DOMAINS,
  },
};
```

## Next Steps

After completing setup:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement Phase 1 (Setup) tasks
3. Implement Phase 2 (Database Models) tasks
4. Continue through phases sequentially

Refer to `plan.md` for detailed phase descriptions and task breakdowns.
