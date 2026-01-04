# Research: Phase II Full-Stack Todo Application

**Date**: 2025-12-31
**Branch**: `004-phase-ii-fullstack`
**Purpose**: Resolve technology decisions and establish best practices for Phase II implementation

## Technology Stack Decisions

### 1. Backend Framework: FastAPI

**Decision**: Use FastAPI as the Python REST framework

**Rationale**:
- Constitution specifies "FastAPI or similar REST framework" for Phase II
- Native async support for database operations with Neon PostgreSQL
- Built-in OpenAPI/Swagger documentation generation
- Pydantic integration aligns with SQLModel (both use Pydantic)
- Type hints and validation out of the box
- Excellent performance for Python web frameworks

**Alternatives Considered**:
- Flask: Simpler but lacks native async, manual OpenAPI setup
- Django REST: Heavier, includes ORM (conflicts with SQLModel choice)

### 2. Database ORM: SQLModel

**Decision**: Use SQLModel for database operations

**Rationale**:
- Constitution explicitly specifies SQLModel
- Combines SQLAlchemy ORM with Pydantic models
- Single model definition for both database and API validation
- Async support via SQLAlchemy 2.0 async engine
- Simpler than raw SQLAlchemy for educational purposes

**Configuration**:
- Async engine with `create_async_engine` from sqlalchemy.ext.asyncio
- Connection pooling configured for serverless (Neon)
- Alembic for migrations with async support

### 3. Authentication: Better Auth

**Decision**: Use Better Auth for user authentication

**Rationale**:
- Constitution explicitly specifies Better Auth
- Handles password hashing, session management, token generation
- Supports email/password authentication flow
- Works with PostgreSQL for session storage
- Provides both backend integration and frontend components

**Integration Pattern**:
- Backend: Better Auth server SDK for Python/FastAPI
- Frontend: Better Auth React hooks and components
- Session tokens stored in secure HTTP-only cookies
- CSRF protection enabled

### 4. Frontend Framework: Next.js 14+ with App Router

**Decision**: Use Next.js with the App Router (not Pages Router)

**Rationale**:
- Constitution specifies Next.js with React and TypeScript
- App Router is the recommended approach for new Next.js projects
- Server Components for initial page loads (faster)
- Client Components for interactive todo features
- Built-in routing, layouts, and loading states

**Alternatives Considered**:
- Pages Router: Legacy approach, less optimized
- Vite + React Router: More manual setup, no SSR benefits

### 5. Styling: Tailwind CSS

**Decision**: Use Tailwind CSS for styling

**Rationale**:
- Constitution recommends Tailwind
- Utility-first approach enables rapid UI development
- Excellent responsive design utilities
- Built-in animation utilities for hover/transition states
- Consistent design system without writing custom CSS

**UI Component Library**:
- Consider shadcn/ui for accessible, unstyled components
- Radix UI primitives for complex interactions (modals, dropdowns)

### 6. Database: Neon Serverless PostgreSQL

**Decision**: Use Neon Serverless PostgreSQL

**Rationale**:
- Constitution explicitly specifies Neon
- Serverless scaling with automatic sleep/wake
- PostgreSQL compatibility (full SQL support)
- Connection pooling via Neon Proxy (handles serverless cold starts)
- Free tier available for development

**Connection Configuration**:
- Use `@neondatabase/serverless` driver for optimal performance
- Connection string via environment variable
- SSL required for production

### 7. API Versioning Strategy

**Decision**: URL path versioning with `/api/v1/` prefix

**Rationale**:
- Constitution requires API versioning strategy before implementation
- Simple, explicit, widely understood pattern
- Easy to maintain multiple versions if needed
- Clear separation between API versions

**Implementation**:
- All endpoints under `/api/v1/`
- Future versions would use `/api/v2/`, etc.

### 8. Error Response Format

**Decision**: Consistent JSON error format with error code and message

**Rationale**:
- Constitution requires "meaningful error codes and messages"
- Standardized format enables consistent frontend error handling

**Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error message",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ]
  }
}
```

### 9. Browser Notifications (Reminders)

**Decision**: Use Web Notifications API with client-side scheduling

**Rationale**:
- Spec requires browser notifications for reminders
- No background jobs allowed (constitution constraint)
- Service Workers not required for basic notifications

**Implementation Approach**:
- Request notification permission on first reminder creation
- Store reminder times in database
- Frontend polls or calculates next reminder on page load
- Use `setTimeout` for scheduling during active session
- Graceful degradation if permission denied

### 10. Recurring Task Generation

**Decision**: Generate next occurrence on task completion (client-triggered)

**Rationale**:
- No background jobs allowed
- Simpler than scheduled job approach
- Immediate feedback to user

**Implementation Approach**:
- When recurring task marked complete, API generates next occurrence
- New task created with incremented due date based on recurrence pattern
- Original task remains completed (audit trail)
- Frontend shows both completed instance and next occurrence

## Best Practices

### Backend Best Practices

1. **Dependency Injection**: Use FastAPI's `Depends()` for database sessions and auth
2. **Service Layer**: Business logic in services, not route handlers
3. **Repository Pattern**: Optional - SQLModel already provides good abstraction
4. **Async All The Way**: Use async/await for database operations
5. **Environment Configuration**: Use pydantic-settings for config validation

### Frontend Best Practices

1. **Server Components Default**: Use Client Components only when needed
2. **Data Fetching**: Use React Query or SWR for client-side caching
3. **Form Handling**: Use react-hook-form with zod validation
4. **State Management**: React Context for auth state, local state for UI
5. **Error Boundaries**: Wrap pages in error boundaries for graceful failures

### Security Best Practices

1. **CORS**: Configure for frontend origin only
2. **HTTPS**: Required in production (enforced by deployment)
3. **Input Validation**: Pydantic models validate all input
4. **SQL Injection**: SQLModel/SQLAlchemy parameterized queries
5. **XSS Prevention**: React's default escaping + CSP headers

## Open Questions (Resolved)

| Question | Resolution |
|----------|------------|
| Which UI component library? | shadcn/ui with Radix primitives |
| How to handle recurring tasks without background jobs? | Generate on completion |
| Session storage mechanism? | HTTP-only cookies via Better Auth |
| API versioning approach? | URL path versioning /api/v1/ |
| How to implement reminders? | Client-side scheduling with Web Notifications API |

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Better Auth Documentation](https://better-auth.com/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [Neon Documentation](https://neon.tech/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)
