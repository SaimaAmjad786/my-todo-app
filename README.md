# Todo App - Phase II Full-Stack Application

A full-stack todo application with user authentication, priorities, tags, due dates, recurring tasks, and browser notifications.

## Features

- User authentication (signup/signin/signout)
- Create, read, update, delete todos
- Priority levels (high/medium/low)
- Tags for organization
- Due dates with overdue indicators
- Recurring tasks (daily/weekly/monthly)
- Browser notification reminders
- Search and filter todos
- Sort by various criteria
- Responsive, animated UI

## Tech Stack

### Backend
- **Python 3.13+** with FastAPI
- **SQLModel** for ORM
- **Neon PostgreSQL** for database
- **Alembic** for migrations
- **JWT** for authentication

### Frontend
- **Next.js 14** with App Router
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Query** for data fetching
- **React Hook Form** with Zod validation

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 20+
- UV (Python package manager)
- pnpm (Node package manager)
- Neon PostgreSQL account

### Backend Setup

```bash
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Copy and configure environment
cp .env.example .env
# Edit .env with your Neon connection string

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Copy and configure environment
cp .env.local.example .env.local

# Start the development server
pnpm dev
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Project Structure

```
todo-app/
├── backend/
│   ├── src/
│   │   ├── api/           # FastAPI routes and middleware
│   │   ├── core/          # Configuration and database
│   │   ├── models/        # SQLModel entities
│   │   └── services/      # Business logic
│   ├── alembic/           # Database migrations
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── lib/           # Utilities
│   │   └── types/         # TypeScript types
│   └── package.json
└── specs/                 # Design documents
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/signup | Register new user |
| POST | /auth/signin | Authenticate user |
| POST | /auth/signout | End session |
| GET | /auth/me | Get current user |
| GET | /todos | List todos (with filters) |
| POST | /todos | Create todo |
| GET | /todos/{id} | Get todo |
| PATCH | /todos/{id} | Update todo |
| DELETE | /todos/{id} | Delete todo |
| POST | /todos/{id}/complete | Mark complete |
| POST | /todos/{id}/incomplete | Mark incomplete |
| GET | /tags | List tags |
| POST | /tags | Create tag |
| DELETE | /tags/{id} | Delete tag |

## License

MIT
