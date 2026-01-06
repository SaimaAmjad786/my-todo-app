 # Phase 2: Frontend & Backend Documentation

  Phase 2 implements a full-stack web application with a **Next.js Frontend** and **RESTful Backend API**. The application provides user authentication and a complete todo management system.

  ---

  ## Table of Contents

  1. [Frontend Architecture](#frontend-architecture)
  2. [Backend API](#backend-api)
  3. [Authentication System](#authentication-system)
  4. [Todo Management](#todo-management)
  5. [API Endpoints](#api-endpoints)
  6. [Data Models](#data-models)
  7. [Setup & Installation](#setup--installation)

  ---

  ## Frontend Architecture

  ### Tech Stack

  | Technology | Version | Purpose |
  |------------|---------|---------|
  | Next.js | 14.x | React Framework with App Router |
  | TypeScript | 5.6+ | Type Safety |
  | React | 18.3+ | UI Library |
  | Tailwind CSS | 3.4+ | Styling |
  | Framer Motion | 12.x | Animations |
  | React Query | 5.60+ | Server State Management |
  | React Hook Form | 7.53+ | Form Handling |
  | Zod | 3.23+ | Schema Validation |
  | Lucide React | 0.460+ | Icons |

  ### Project Structure

  frontend/
  ├── src/
  │   ├── app/                    # Next.js App Router
  │   │   ├── (auth)/             # Auth Route Group
  │   │   │   ├── layout.tsx      # Auth Layout
  │   │   │   ├── signin/         # Sign In Page
  │   │   │   │   └── page.tsx
  │   │   │   └── signup/         # Sign Up Page
  │   │   │       └── page.tsx
  │   │   ├── dashboard/          # Dashboard (Protected)
  │   │   │   └── page.tsx
  │   │   ├── layout.tsx          # Root Layout
  │   │   └── page.tsx            # Landing Page
  │   │
  │   ├── components/
  │   │   ├── layout/             # Layout Components
  │   │   │   ├── Header.tsx
  │   │   │   ├── MobileNav.tsx
  │   │   │   ├── RootLayout.tsx
  │   │   │   └── ErrorBoundary.tsx
  │   │   │
  │   │   ├── todo/               # Todo Components
  │   │   │   ├── TodoList.tsx        # Main List Container
  │   │   │   ├── TodoItem.tsx        # Individual Todo Card
  │   │   │   ├── TodoForm.tsx        # Create/Edit Form
  │   │   │   ├── TodoListSkeleton.tsx
  │   │   │   ├── EmptyState.tsx
  │   │   │   ├── SearchInput.tsx
  │   │   │   ├── FilterBar.tsx
  │   │   │   ├── SortSelector.tsx
  │   │   │   ├── PrioritySelector.tsx
  │   │   │   ├── PriorityBadge.tsx
  │   │   │   ├── DueDateSelector.tsx
  │   │   │   ├── DueDateBadge.tsx
  │   │   │   ├── RecurrenceSelector.tsx
  │   │   │   ├── RecurrenceBadge.tsx
  │   │   │   ├── TagSelector.tsx
  │   │   │   └── DeleteConfirmDialog.tsx
  │   │   │
  │   │   └── ui/                 # Reusable UI Components
  │   │       ├── button.tsx
  │   │       ├── input.tsx
  │   │       ├── textarea.tsx
  │   │       ├── label.tsx
  │   │       ├── card.tsx
  │   │       ├── badge.tsx
  │   │       ├── checkbox.tsx
  │   │       ├── dialog.tsx
  │   │       ├── alert-dialog.tsx
  │   │       ├── select.tsx
  │   │       ├── LoadingSpinner.tsx
  │   │       └── ErrorMessage.tsx
  │   │
  │   ├── hooks/                  # Custom React Hooks
  │   │   ├── useTodos.ts         # Todo CRUD Operations
  │   │   ├── useTags.ts          # Tag Management
  │   │   └── useReminders.ts     # Notification Reminders
  │   │
  │   ├── lib/                    # Utilities
  │   │   ├── api-client.ts       # API Fetch Wrapper
  │   │   ├── auth-context.tsx    # Auth State Provider
  │   │   ├── providers.tsx       # React Query Provider
  │   │   ├── notifications.ts    # Browser Notifications
  │   │   ├── toast.tsx           # Toast Notifications
  │   │   └── utils.ts            # Helper Functions
  │   │
  │   └── types/
  │       └── api.ts              # TypeScript Interfaces
  │
  ├── public/                     # Static Assets
  ├── package.json
  ├── tailwind.config.ts
  ├── tsconfig.json
  └── next.config.js

  ---

  ## Authentication System

  ### Features
  - User Registration (Sign Up)
  - User Login (Sign In)
  - JWT Token-based Authentication
  - Protected Routes
  - Automatic Token Refresh
  - Secure Logout

  ### Auth Flow

  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │   Sign Up   │────▶│   Backend   │────▶│  Dashboard  │
  │   Sign In   │     │  (JWT Gen)  │     │ (Protected) │
  └─────────────┘     └─────────────┘     └─────────────┘
                             │
                      ┌──────▼──────┐
                      │ localStorage │
                      │ access_token │
                      └─────────────┘

  ### Auth Context API

  ```typescript
  interface AuthContextType {
    user: User | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    signup: (email: string, password: string, name?: string) => Promise<void>;
    signin: (email: string, password: string) => Promise<void>;
    signout: () => Promise<void>;
  }

  Usage

  import { useAuth } from "@/lib/auth-context";

  function Component() {
    const { user, isAuthenticated, signin, signout } = useAuth();

    if (!isAuthenticated) {
      return <LoginForm />;
    }

    return <Dashboard user={user} />;
  }

  ---
  Todo Management

  Features

  - ✅ Create, Read, Update, Delete Todos
  - ✅ Mark Complete/Incomplete
  - ✅ Priority Levels (High, Medium, Low)
  - ✅ Due Dates with Reminders
  - ✅ Recurring Tasks (Daily, Weekly, Monthly)
  - ✅ Tags/Categories
  - ✅ Search & Filter
  - ✅ Sort Options
  - ✅ Pagination

  Todo Hooks

  // Fetch all todos with filters
  const { data, isLoading, error } = useTodos(filters);

  // Create new todo
  const createTodo = useCreateTodo();
  await createTodo.mutateAsync({ title: "New Task", priority: "high" });

  // Update todo
  const updateTodo = useUpdateTodo();
  await updateTodo.mutateAsync({ todoId: "123", data: { title: "Updated" }});

  // Delete todo
  const deleteTodo = useDeleteTodo();
  await deleteTodo.mutateAsync("123");

  // Mark complete/incomplete
  const completeTodo = useCompleteTodo();
  const incompleteTodo = useIncompleteTodo();

  ---
  API Endpoints

  Base URL

  http://localhost:8000/api/v1

  Authentication Endpoints

  | Method | Endpoint      | Description       | Body                       |
  |--------|---------------|-------------------|----------------------------|
  | POST   | /auth/signup  | Register new user | { email, password, name? } |
  | POST   | /auth/signin  | Login user        | { email, password }        |
  | POST   | /auth/signout | Logout user       | -                          |
  | GET    | /auth/me      | Get current user  | -                          |

  Todo Endpoints

  | Method | Endpoint              | Description     | Auth |
  |--------|-----------------------|-----------------|------|
  | GET    | /todos                | List all todos  | Yes  |
  | POST   | /todos                | Create todo     | Yes  |
  | GET    | /todos/:id            | Get single todo | Yes  |
  | PATCH  | /todos/:id            | Update todo     | Yes  |
  | DELETE | /todos/:id            | Delete todo     | Yes  |
  | POST   | /todos/:id/complete   | Mark complete   | Yes  |
  | POST   | /todos/:id/incomplete | Mark incomplete | Yes  |

  Query Parameters for GET /todos

  | Parameter | Type    | Description                              |
  |-----------|---------|------------------------------------------|
  | completed | boolean | Filter by status                         |
  | priority  | string  | Filter by priority (high/medium/low)     |
  | tag       | string  | Filter by tag ID                         |
  | search    | string  | Search in title/description              |
  | sort      | string  | Sort field (e.g., -created_at, priority) |
  | page      | number  | Page number (default: 1)                 |
  | page_size | number  | Items per page (default: 20)             |

  Tag Endpoints

  | Method | Endpoint  | Description   | Auth |
  |--------|-----------|---------------|------|
  | GET    | /tags     | List all tags | Yes  |
  | POST   | /tags     | Create tag    | Yes  |
  | DELETE | /tags/:id | Delete tag    | Yes  |

  ---
  Data Models

  User

  interface User {
    id: string;
    email: string;
    name: string | null;
    created_at: string;
  }

  Todo

  interface Todo {
    id: string;
    user_id: string;
    title: string;
    description: string | null;
    completed: boolean;
    priority: "high" | "medium" | "low";
    due_date: string | null;
    reminder_time: string | null;
    recurrence: "none" | "daily" | "weekly" | "monthly";
    parent_id: string | null;
    tags: Tag[];
    created_at: string;
    updated_at: string;
  }

  Tag
  interface Tag {
    id: string;
    name: string;
    created_at: string;
  }

  API Response (Paginated)

  interface TodoListResponse {
    items: Todo[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }

  Error Response

  interface ErrorResponse {
    error: {
      code: string;
      message: string;
      details?: Array<{ field: string; message: string }>;
    };
  }

  ---
  Setup & Installation

  Prerequisites

  - Node.js 18+
  - npm or yarn
  - Backend API running on port 8000

  Installation

  # Navigate to frontend directory
  cd frontend

  # Install dependencies
  npm install

  # Create environment file
  cp .env.example .env.local

  Environment Variables

  # .env.local
  NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

  Development

  # Start development server
  npm run dev

  # Open browser
  # http://localhost:3000

  Production Build

  # Build for production
  npm run build

  # Start production server
  npm start

  Other Commands

  # Lint code
  npm run lint

  # Format code
  npm run format

  ---
  Component Examples

  TodoForm Usage

  <TodoForm
    todo={existingTodo}      // Optional: for editing
    onSuccess={() => {}}      // Called after save
    onCancel={() => {}}       // Called on cancel
  />

  TodoList Usage

  <TodoList />  // Self-contained component with all functionality

  FilterBar Usage

  <FilterBar
    filters={currentFilters}
    onFilterChange={(newFilters) => setFilters(newFilters)}
  />

  ---
  API Client

  The api-client.ts provides a fetch wrapper with:
  - Automatic JWT token injection
  - Error handling with custom ApiError class
  - Query parameter serialization
  - JSON response parsing

  import { apiGet, apiPost, apiPatch, apiDelete, ApiError } from "@/lib/api-client";

  // GET request
  const todos = await apiGet<TodoListResponse>("/todos");

  // POST request
  const newTodo = await apiPost<Todo>("/todos", { title: "New Task" });

  // PATCH request
  const updated = await apiPatch<Todo>("/todos/123", { title: "Updated" });

  // DELETE request
  await apiDelete("/todos/123");

  // Error handling
  try {
    await apiPost("/todos", data);
  } catch (err) {
    if (err instanceof ApiError) {
      console.log(err.status, err.code, err.message);
    }
  }

  ---
  Deployment

  Vercel Configuration

  // vercel.json
  {
    "framework": "nextjs",
    "rootDirectory": "frontend"
  }

  Deploy Steps

  1. Push code to GitHub
  2. Connect repository to Vercel
  3. Set root directory to frontend
  4. Add environment variables
  5. Deploy!
