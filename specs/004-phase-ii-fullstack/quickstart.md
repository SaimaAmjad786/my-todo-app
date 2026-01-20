# Quickstart: Phase II Full-Stack Todo Application

**Date**: 2025-12-31
**Branch**: `004-phase-ii-fullstack`
**Purpose**: Step-by-step guide to run the application locally

## Prerequisites

Ensure you have the following installed:

- **Python 3.13+**: Backend runtime
- **Node.js 20+**: Frontend runtime
- **UV**: Python package manager (`pip install uv` or `pipx install uv`)
- **pnpm**: Node package manager (`npm install -g pnpm`)
- **Git**: Version control
- **PostgreSQL client** (optional): For database inspection

## Environment Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd todo-app
git checkout 004-phase-ii-fullstack
```

### 2. Neon Database Setup

1. Create a free account at [neon.tech](https://neon.tech)
2. Create a new project named "todo-app"
3. Copy the connection string from the dashboard
4. It should look like: `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Copy environment template
cp .env.example .env

# Edit .env and add your Neon connection string:
# DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
# BETTER_AUTH_SECRET=<generate-a-random-secret>
# CORS_ORIGINS=http://localhost:3000

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API should now be running at `http://localhost:8000`

### 4. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Copy environment template
cp .env.local.example .env.local

# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
# BETTER_AUTH_URL=http://localhost:8000

# Start the development server
pnpm dev
```

The frontend should now be running at `http://localhost:3000`

## Verification Checklist

After setup, verify the following:

### Backend Verification

- [ ] API docs accessible at `http://localhost:8000/docs`
- [ ] Health check returns 200: `curl http://localhost:8000/health`
- [ ] Database connection successful (no errors in console)

### Frontend Verification

- [ ] Homepage loads at `http://localhost:3000`
- [ ] Signup page accessible at `http://localhost:3000/signup`
- [ ] Signin page accessible at `http://localhost:3000/signin`
- [ ] No console errors in browser developer tools

### Full Flow Verification

1. [ ] Create a new account via signup form
2. [ ] Verify redirect to dashboard after signup
3. [ ] Create a new todo
4. [ ] View todo in list
5. [ ] Mark todo as complete
6. [ ] Delete the todo
7. [ ] Sign out
8. [ ] Sign back in with same credentials

## Common Issues

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Ensure you're in the `backend/` directory and virtual environment is activated

**Issue**: `asyncpg.exceptions.InvalidPasswordError`
**Solution**: Check DATABASE_URL in .env matches Neon dashboard connection string

**Issue**: `Connection refused` when connecting to database
**Solution**: Ensure Neon project is active (not paused due to inactivity)

### Frontend Issues

**Issue**: `CORS error` in browser console
**Solution**: Verify CORS_ORIGINS in backend .env includes `http://localhost:3000`

**Issue**: `fetch failed` or `NetworkError`
**Solution**: Ensure backend is running on port 8000

**Issue**: `TypeError: Failed to fetch` on auth
**Solution**: Check BETTER_AUTH_URL in frontend .env.local

### Database Issues

**Issue**: `relation "users" does not exist`
**Solution**: Run `alembic upgrade head` in backend directory

**Issue**: Migration fails with existing tables
**Solution**: For fresh start: drop all tables in Neon console, then re-run migrations

## Development Workflow

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
pnpm test
```

### Code Formatting

```bash
# Backend (Python)
cd backend
ruff format .
ruff check . --fix

# Frontend (TypeScript)
cd frontend
pnpm lint
pnpm format
```

### Database Migrations

```bash
cd backend

# Create a new migration after model changes
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | Neon PostgreSQL connection string |
| BETTER_AUTH_SECRET | Yes | Secret key for session encryption |
| CORS_ORIGINS | Yes | Comma-separated allowed origins |
| DEBUG | No | Enable debug mode (default: false) |

### Frontend (.env.local)

| Variable | Required | Description |
|----------|----------|-------------|
| NEXT_PUBLIC_API_URL | Yes | Backend API base URL |
| BETTER_AUTH_URL | Yes | Better Auth server URL |

## Next Steps

After successful setup:

1. Review [spec.md](./spec.md) for feature requirements
2. Review [data-model.md](./data-model.md) for database schema
3. Review [contracts/openapi.yaml](./contracts/openapi.yaml) for API specification
4. Run `/sp.tasks` to generate implementation tasks
