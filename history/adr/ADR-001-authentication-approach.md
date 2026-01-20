# ADR-001: Authentication Approach

> **Scope**: Authentication and authorization strategy for Phase II full-stack application.

- **Status:** Accepted
- **Date:** 2026-01-03
- **Feature:** 004-phase-ii-fullstack
- **Context:** Phase II requires user authentication to scope todos to individual users. The constitution originally specified "Better Auth" but implementation chose custom JWT.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - auth affects all API endpoints
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Better Auth vs custom JWT
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects backend, frontend, and all user data
-->

## Decision

Use custom JWT authentication with python-jose and passlib instead of Better Auth SDK:

- **Token Library**: python-jose for JWT encoding/decoding
- **Password Hashing**: passlib with bcrypt backend
- **Token Storage**: HTTP-only cookies (frontend) or Authorization header
- **Token Expiry**: Access tokens with configurable expiration
- **Middleware**: FastAPI dependency injection for route protection

## Consequences

### Positive

- **Better FastAPI Integration**: Native dependency injection pattern, no SDK abstraction layer
- **Full Control**: Complete visibility into authentication flow, easier debugging
- **No Third-Party Dependency**: Avoids SDK versioning issues and potential breaking changes
- **Simpler Architecture**: Direct JWT handling without additional service complexity
- **Educational Value**: Students learn authentication fundamentals rather than SDK usage

### Negative

- **More Code to Maintain**: Must implement signup, signin, token refresh manually
- **Security Responsibility**: Team must ensure proper implementation of security best practices
- **No Built-in Features**: Features like OAuth, magic links, etc. require additional work if needed

## Alternatives Considered

**Alternative A: Better Auth SDK**
- Third-party SDK handling auth flows
- Pro: Less code, built-in features
- Con: Additional dependency, less control, potential integration complexity with FastAPI async

**Alternative B: Auth0/Firebase Auth**
- External authentication service
- Pro: Enterprise-grade, scalable
- Con: External dependency, cost at scale, overkill for educational project

**Alternative C: FastAPI-Users**
- FastAPI-specific auth library
- Pro: FastAPI-native, well-documented
- Con: Still an abstraction, less educational value

**Why JWT + passlib was chosen**: Better FastAPI integration, full control over auth flow, educational value in understanding authentication fundamentals, and simpler architecture without third-party SDK dependencies.

## References

- Feature Spec: [specs/004-phase-ii-fullstack/spec.md](../../specs/004-phase-ii-fullstack/spec.md)
- Implementation Plan: [specs/004-phase-ii-fullstack/plan.md](../../specs/004-phase-ii-fullstack/plan.md)
- Related ADRs: None (first ADR)
- Constitution Amendment: v3.1.0 (updated Principle VIII to reflect this decision)
