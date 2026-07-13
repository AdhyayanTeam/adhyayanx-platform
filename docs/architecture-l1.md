# ADX Platform — Architecture Report

---

## 1. Executive Summary

**Current project stage:** Working prototype with complete authentication system, organization management, production email integration, and a functional frontend for auth flows. No domain-specific vertical solutions exist.

**Overall completion estimate:** ~40–45% toward a functional MVP; ~15–20% toward production.

**Major implemented capabilities:**
- Full authentication lifecycle: signup (with org+role+membership+subscription creation), login, logout, token refresh, email verification, forgot/reset password
- Organization CRUD with event publication
- User management (CRUD, deactivate, reactivate)
- JWT (RS256) access/refresh token system with Argon2 password hashing
- Resend email integration with HTML templates (verify-email, reset-password)
- Transactional outbox pattern (write side)
- Custom DI container with auto-wiring
- Exception hierarchy (DomainError, InfrastructureError, ApplicationError subtrees) and global error handling
- Structured logging middleware
- PostgreSQL schema with Alembic migrations (2 migrations — 8 tables total)
- Kubernetes-style health probes (`/health/live`, `/health/ready`)
- Password policy enforcement (complexity rules, common password blocking)
- Navigation service for landing URL resolution by blueprint code
- Frontend (Next.js 16): auth flows (login, signup, forgot/reset password, email verification), console pages (dashboard, profile, organization, settings), auth context with silent refresh
- Integration test suite covering auth flows and org lifecycle
- In-memory rate limiter (defined but not wired)

**Major missing capabilities:**
- Authorization / RBAC enforcement (all admin routes are unprotected)
- Event outbox dispatcher (events written but never dispatched)
- Redis, background queues, rate limiting wired
- Frontend console CRUD operations (profile/org editing, settings management)
- Server-side route protection for `/console` routes
- Blueprint implementations (academy, clinic, gym, salon are empty)
- DHARA compute plane integration
- Workspace module
- Concrete domain aggregates (no typed domain objects, everything is `dict[str, Any]`)
- Password brute-force protection / account lockout
- Refresh token rotation
- API documentation (OpenAPI/Swagger)

**Technical debt:**
- `Lifecycle` class created but never integrated into FastAPI lifespan
- Container `_resolve_annotation` has a bug with Union type resolution
- Event handlers discovered but never wired to the EventBus
- `structlog` configured but unused (all code uses stdlib `logging`)
- Email service manually wired outside the DI container
- `BusinessObject` aggregate root is never subclassed
- Generic `Repository` ABC is unused by all concrete repos
- `Capability`, `Policy`, `Workflow` contracts have zero implementations
- `SolutionBlueprint` enum is orphaned (never imported)
- Three commands (`ForgotPasswordCommand`, `RefreshTokenCommand`, `LogoutCommand`) are defined but unused
- `.env.example` contains real credentials (Neon DB URL, Resend API key) — should use placeholders
- Frontend console routes protected only client-side (no server-side auth guard)
- Frontend signup hardcodes `blueprint_code: "academy"`

**Biggest architectural risks:**
1. **Security:** All `/users` and `/organizations` endpoints are completely unprotected — anyone can create, deactivate, or reactivate users and organizations.
2. **Event delivery:** The outbox pattern is half-built — events are written to the DB but never dispatched to handlers. This is a silent failure.
3. **No typed domain model:** The entire codebase operates on `dict[str, Any]` instead of typed aggregate roots. This defeats the purpose of DDD contracts and makes the codebase fragile.
4. **DI wiring bypass:** Services lazily import concrete Postgres repositories instead of using port interfaces, undermining the hexagonal architecture.
5. **Client-side-only auth:** Frontend `/console` routes are protected only by React context checks, not server-side middleware. A direct URL access bypasses the guard.

---

## 2. Repository Structure

```
adhyayanx-platform/
├── .github/workflows/backend.yml          # CI: lint, typecheck, test
├── docs/
│   ├── aps/runtime-spec.md                # Architectural constitution
│   ├── architecture-l1.md                 # This document
│   └── frontend/architecture.md           # Frontend architecture spec
├── docker-compose.yml                     # PostgreSQL 16 only
├── frontend/                              # Next.js 16 App Router
│   ├── package.json                       # React 19, Tailwind v4, shadcn/ui
│   ├── next.config.ts
│   ├── tsconfig.json
│   ├── components.json                    # shadcn/ui config (base-nova style)
│   ├── public/                            # Static assets
│   └── src/
│       ├── app/
│       │   ├── layout.tsx                 # Root layout (Geist fonts, Providers)
│       │   ├── page.tsx                   # Redirects to /login
│       │   ├── providers.tsx              # Client-side AuthProvider
│       │   ├── globals.css                # Tailwind + theme CSS variables
│       │   ├── (public)/                  # Guest-only route group
│       │   │   ├── layout.tsx             # Passthrough layout
│       │   │   ├── login/page.tsx
│       │   │   ├── signup/page.tsx
│       │   │   ├── forgot-password/page.tsx
│       │   │   ├── reset-password/page.tsx
│       │   │   └── verify-email/page.tsx
│       │   └── (console)/                 # Authenticated route group
│       │       ├── layout.tsx             # Auth guard + sidebar
│       │       └── console/
│       │           ├── page.tsx           # Dashboard home
│       │           ├── profile/page.tsx
│       │           ├── organization/page.tsx
│       │           └── settings/page.tsx
│       ├── features/auth/                 # Auth feature module
│       │   ├── index.ts                   # Barrel export
│       │   ├── types.ts                   # TS types for API responses
│       │   ├── api.ts                     # Auth API client methods
│       │   ├── schemas.ts                 # Zod validation schemas
│       │   ├── auth-context.tsx           # AuthProvider + useAuth hook
│       │   └── ui/                        # Auth form components
│       │       ├── login-form.tsx
│       │       ├── signup-form.tsx
│       │       ├── forgot-password-form.tsx
│       │       ├── reset-password-form.tsx
│       │       ├── verify-email-client.tsx
│       │       └── console-sidebar.tsx
│       ├── shared/
│       │   ├── lib/
│       │   │   ├── api-client.ts          # api(), apiAuth(), apiAuthRetry()
│       │   │   └── utils.ts               # cn() class merging
│       │   ├── types/api.ts               # ApiError, ApiResult<T>
│       │   └── ui/                        # shadcn/ui components (13)
│       │       ├── alert.tsx, avatar.tsx, button.tsx, card.tsx
│       │       ├── dropdown-menu.tsx, input.tsx, label.tsx
│       │       ├── loading-spinner.tsx, separator.tsx, sheet.tsx
│       └── middleware.ts                  # Guest-route redirect middleware
├── scripts/                               # .gitkeep — empty
├── docker/                                # .gitkeep — empty
├── README.md                              # Minimal project description
├── .env.example                           # Environment template
└── backend/
    ├── pyproject.toml                     # Python deps, ruff, mypy, pytest config
    ├── uv.lock                            # Locked deps
    ├── alembic.ini                        # Alembic config
    ├── Dockerfile                         # Python 3.12-slim + uv
    ├── .dockerignore                      # Docker build exclusions
    ├── README.md                          # Backend dev guide
    ├── STATUS.md                          # Status checklist
    ├── keys/dev-private.pem               # JWT RSA private key
    ├── keys/dev-public.pem                # JWT RSA public key
    ├── app/
    │   ├── api/                           # HTTP layer
    │   │   ├── main.py                    # App factory, middleware, bootstrap
    │   │   ├── routers/                   # Router registration + health
    │   │   │   ├── __init__.py            # Router registration
    │   │   │   └── health.py              # /health/live + /health/ready
    │   │   ├── middleware/                 # Error handler + logging
    │   │   └── dependencies/              # FastAPI DI bridge
    │   ├── kernel/                        # App bootstrap core
    │   │   ├── bootstrap.py               # Wiring orchestrator
    │   │   ├── container.py               # Custom DI container
    │   │   ├── discovery.py               # Blueprint/handler scanner
    │   │   ├── lifecycle.py               # Startup/shutdown hooks
    │   │   └── config/loader.py           # Pydantic Settings
    │   ├── foundation/                    # Cross-cutting
    │   │   ├── types.py                   # EntityId, Timestamp, Version
    │   │   ├── exceptions/base.py         # Exception hierarchy (3 subtrees)
    │   │   └── security/                  # Placeholder
    │   ├── infrastructure/                # Adapters
    │   │   ├── postgres/                  # Database, ORM, repos, migrations
    │   │   │   ├── database.py            # Engine, session factory
    │   │   │   ├── tables.py              # ORM models (8 tables)
    │   │   │   ├── identity_repository.py
    │   │   │   ├── organization_repository.py
    │   │   │   ├── organization_role_repository.py
    │   │   │   ├── organization_subscription_repository.py
    │   │   │   ├── membership_repository.py
    │   │   │   ├── session_repository.py
    │   │   │   ├── verification_token_repository.py
    │   │   │   ├── outbox_repository.py
    │   │   │   └── migrations/versions/    # 2 migrations
    │   │   ├── redis/                     # Placeholder
    │   │   ├── queues/                    # Placeholder
    │   │   └── rate_limiter.py            # In-memory sliding window
    │   ├── modules/platform/              # Domain modules
    │   │   ├── contracts/                 # Base abstractions (ABC)
    │   │   ├── events/                    # EventBus, Publisher, Outbox
    │   │   ├── identity/                  # Auth + user management (complete)
    │   │   │   ├── auth_service.py        # Auth orchestrator (~730 lines)
    │   │   │   ├── auth_router.py         # Auth HTTP endpoints (8 routes)
    │   │   │   ├── service.py             # User management CRUD
    │   │   │   ├── router.py              # User HTTP endpoints
    │   │   │   ├── token_service.py       # JWT RS256 operations
    │   │   │   ├── password_policy.py     # Argon2 + complexity rules
    │   │   │   ├── navigation_service.py  # Landing URL resolver
    │   │   │   ├── solution_blueprint.py  # Blueprint enum
    │   │   │   ├── commands.py            # 10 command definitions
    │   │   │   ├── events.py              # 12 domain events
    │   │   │   ├── schemas.py             # Pydantic request/response schemas
    │   │   │   ├── handlers.py            # Event handlers (logging stubs)
    │   │   │   └── ports/                 # 6 repository port ABCs
    │   │   ├── organizations/             # Org CRUD
    │   │   ├── notifications/             # Email service (complete)
    │   │   │   ├── email_service.py       # Protocol + EmailMessage
    │   │   │   ├── console_provider.py    # Dev fallback
    │   │   │   ├── resend_provider.py     # Production Resend API
    │   │   │   └── emails/               # HTML email templates
    │   │   │       ├── verify_email.py
    │   │   │       └── reset_password.py
    │   │   ├── workspaces/                # Placeholder
    │   │   └── dhara/                     # Placeholder
    │   ├── modules/blueprints/            # Vertical solutions
    │   │   └── academy/                   # Placeholder
    │   └── shared/                        # Placeholder
    └── tests/
        ├── integration/auth/              # 10 auth tests + conftest
        ├── integration/test_organization_lifecycle.py
        └── unit/notifications/            # 1 email contract test
```

**Top-level folder responsibilities:**

| Folder | Responsibility |
|---|---|
| `frontend/src/app` | Next.js App Router pages with route groups for public/console isolation |
| `frontend/src/features/auth` | Self-contained auth feature: types, API calls, schemas, context, UI components |
| `frontend/src/shared` | Shared utilities (`api-client.ts`, `utils.ts`), types, and shadcn/ui component library |
| `frontend/src/middleware.ts` | Edge middleware: redirects logged-in users away from guest routes |
| `backend/app/api` | FastAPI app factory, HTTP routers, middleware, DI bridge to FastAPI |
| `backend/app/kernel` | Application bootstrap, DI container, lifecycle, settings |
| `backend/app/foundation` | Shared type aliases, exception hierarchy (3 subtrees), security utilities |
| `backend/app/infrastructure` | Database engine, ORM tables (8), 8 repository implementations, migrations (2), rate limiter |
| `backend/app/modules/platform/contracts` | DDD building blocks: aggregate root, command, event, repository, policy, workflow base classes |
| `backend/app/modules/platform/events` | Event bus (in-process), outbox publisher, outbox dispatcher (stub) |
| `backend/app/modules/platform/identity` | Complete auth lifecycle: signup, login, logout, refresh, email verification, password reset, user CRUD |
| `backend/app/modules/platform/organizations` | Organization CRUD with event publication |
| `backend/app/modules/platform/notifications` | Email service with Resend API integration, console fallback, HTML templates |
| `backend/app/modules/platform/workspaces` | Empty placeholder |
| `backend/app/modules/platform/dhara` | Empty placeholder for AI compute plane |
| `backend/app/modules/blueprints` | Empty placeholder for vertical solutions |
| `docs/aps` | Architecture specification document |
| `docs/frontend` | Frontend architecture specification |

---

## 3. Architecture

**Overall architecture:** Monolithic FastAPI backend + Next.js frontend. Backend follows Ports & Adapters (Hexagonal Architecture) with CQRS-inspired command/event separation and a transactional outbox pattern. Frontend follows feature-based module structure with route group isolation.

### Backend Architecture

**Layers (top to bottom, dependency direction flows inward):**

```
API Layer (routers, middleware)
    ↓ depends on
Domain Layer (services, commands, events, ports)
    ↓ depends on
Infrastructure Layer (repositories, database, email providers)
    ↓ depends on
Foundation Layer (types, exceptions)
```

**Key architectural boundaries:**
- **Domain modules** (`modules/platform/`) depend on **ports** (abstract interfaces in each module's `ports/` directory)
- **Infrastructure** (`infrastructure/postgres/`) provides adapter implementations of those ports
- **API layer** (`api/`) depends only on domain services via the DI container
- **Foundation** is shared by all layers

**Module boundaries:** Each domain module (identity, organizations, notifications) is self-contained with its own:
- Port interfaces (`ports/`)
- Domain service
- Commands and events
- HTTP router
- Schemas

**Domain boundaries:**
- **Identity:** Users, authentication, sessions, verification tokens, passwords, roles, memberships, subscriptions, navigation
- **Organizations:** Organization CRUD, slug management, lifecycle
- **Events:** Cross-cutting event infrastructure (bus, outbox)
- **Notifications:** Email delivery abstraction with Resend API and console providers, HTML email templates
- **Workspaces:** Not implemented
- **DHARA:** Not implemented

**Event system:** Two parallel systems exist:
1. **In-process EventBus** (`events/bus.py`) — in-memory dict of handlers, synchronous dispatch within the process
2. **Transactional Outbox** (`events/publisher.py` + `OutboxTable`) — writes events to PostgreSQL within the same transaction

These two systems are **disconnected** — events written to the outbox are never dispatched to the in-process EventBus.

**Request lifecycle:**
1. HTTP request arrives at FastAPI
2. `LoggingMiddleware` logs the request
3. Router receives the request, resolves service from DI container via `Depends(resolve(ServiceClass))`
4. Router constructs a Command object from the request body
5. Service method executes business logic using a database session
6. Service calls repository methods (via port interfaces, but currently via concrete imports)
7. Service calls `Publisher.publish(event, session)` to write events to the outbox table
8. Database session auto-commits on context manager exit
9. Router returns the response
10. Global error handler catches `ADXError` subtypes and maps to HTTP status codes

**Startup lifecycle:**
1. `create_app()` in `main.py` is called
2. `structlog` is configured
3. `FastAPI` instance created with CORS and logging middleware
4. Error handlers and routers registered (health, auth, users, organizations)
5. `Bootstrap.configure()` runs:
   - Settings registered in DI container
   - `Database` created and registered
   - Domain services registered (IdentityService, OrganizationService, AuthService, TokenService, NavigationService, PasswordPolicy)
   - `EventBus` and `Publisher` registered
   - Blueprints discovered (currently none with `register()` function)
   - Event handlers discovered (but not wired to the bus)
6. Email service selected based on `EMAIL_PROVIDER` setting:
   - `"resend"` → `ResendEmailProvider` (production, uses Resend API)
   - `"console"` (default) → `ConsoleEmailProvider` (dev, logs to stdout)
7. Email service manually wired into AuthService via setter
8. App returned

**Critical gap:** The `Lifecycle` object created in `Bootstrap` is never connected to the FastAPI lifespan, so no shutdown hooks run (Database.close() is never called).

### Frontend Architecture

**Framework:** Next.js 16 (App Router) with React 19, TypeScript, Tailwind CSS v4, shadcn/ui (base-nova style).

**Key patterns:**
- **Route groups:** `(public)` for guest-only pages, `(console)` for authenticated pages — same URL structure, different layouts
- **Feature modules:** `features/auth/` is self-contained with types, API calls, schemas, context, and UI components
- **Auth flow:** Access token in React state only, refresh token in HttpOnly cookie. Session restored on mount via `/refresh` + `/me`. 401s trigger automatic retry after silent refresh.
- **API client:** Centralized `api-client.ts` with `api()`, `apiAuth()`, `apiAuthRetry()` wrappers returning `ApiResult<T>` discriminated unions
- **Client-side auth guard:** Console layout checks `useAuth()` and redirects to `/login` if unauthenticated

**Frontend request lifecycle:**
1. User navigates to a route (e.g., `/login`)
2. Route group layout renders (passthrough for public, auth-guarded for console)
3. Page component renders form/UI
4. Form submission calls `authApi.*()` method
5. `authApi` uses `api()` or `apiAuth()` wrapper (prepends `NEXT_PUBLIC_API_URL`, handles errors)
6. On success: auth context updated, navigation occurs
7. On 401: `apiAuthRetry()` attempts silent refresh, then retries once

---

## 4. Module Inventory

### 4.1 `contracts` (Platform Contracts)

**Purpose:** Defines the foundational building blocks for DDD: aggregate root, command, event, repository, capability, policy, and workflow base classes.

**Public API:** `BusinessObject`, `Command`, `DomainEvent`, `Repository`, `Capability`, `Policy`, `PolicyResult`, `WorkflowDefinition`, `WorkflowInstance`, `WorkflowStep`, `StepResult`, `WorkflowContext`, `StateDefinition`

**Dependencies:** Pydantic, ABC

**Database tables:** None

**Events emitted:** None

**Events consumed:** None

**Implementation status:** Base classes defined. `BusinessObject` and `Repository` are never subclassed by actual domain code. `Capability`, `Policy`, and `Workflow` have zero implementations.

**Missing work:** Concrete aggregate roots for Organization and User. Concrete policies for authorization. Any workflow implementation. `Repository` base is unused.

### 4.2 `events` (Event System)

**Purpose:** Provides in-process event bus, outbox publisher, outbox dispatcher, subscriber registry.

**Public API:** `EventBus.publish()`, `EventBus.subscribe()`, `Publisher.publish()`, `OutboxDispatcher.start()/stop()`

**Dependencies:** SQLAlchemy (for `OutboxTable`), contracts

**Database tables:** `event_outbox`, `processed_events`

**Events emitted:** None directly (services emit via Publisher)

**Events consumed:** None (handlers are stubs, never wired)

**Implementation status:** `EventBus` and `Publisher` are functional. `OutboxDispatcher._dispatch_batch()` is a no-op. Handlers are discovered but not connected to the bus.

**Missing work:** Wire handlers to EventBus. Implement `_dispatch_batch()`. Implement `PostgresOutboxRepository` adapter (the port exists, the Postgres adapter exists, but they are not connected). Add background polling task. Implement `processed_events` deduplication.

### 4.3 `identity` (Identity & Authentication)

**Purpose:** Complete authentication lifecycle: signup, login, logout, token refresh, email verification, password reset, user CRUD.

**Public API:** `IdentityService` (create, get, deactivate, reactivate, list), `AuthService` (signup, login, logout, refresh, verify_email, forgot_password, reset_password, get_current_user), `TokenService` (create_access_token, create_refresh_token_pair, decode_access_token, hash_refresh_token), `NavigationService` (resolve_landing), `PasswordPolicy` (validate, hash, verify)

**Dependencies:** Database, Publisher, TokenService, NavigationService, PasswordPolicy, Settings, EmailService

**Database tables:** `users`, `sessions`, `email_verification_tokens`, `organization_roles`, `memberships`, `organization_subscriptions`

**Events emitted:** `UserCreated`, `UserDeactivated`, `UserReactivated`, `OrganizationCreated`, `MembershipCreated`, `OrganizationSubscriptionCreated`, `EmailVerificationTokenCreated`, `EmailVerified`, `PasswordReset`, `UserLoggedIn`, `UserLoggedOut`, `SessionRefreshed`

**Events consumed:** `on_user_created`, `on_user_deactivated`, `on_user_reactivated` (all logging-only stubs)

**Implementation status:** Complete. The auth lifecycle is fully functional including signup with organization+role+membership+subscription creation, login with session management, token refresh, email verification, and password reset with session revocation. Repository ports and Postgres implementations are complete for all 6 sub-domains (identity, membership, organization_role, organization_subscription, session, verification_token). Password policy enforces complexity rules and blocks common passwords. Navigation service resolves landing URLs by blueprint code.

**Missing work:** Authorization middleware on admin routes, rate limiting, brute-force protection, refresh token rotation, typed domain objects (currently dict-based), handler implementations for 9 of 12 events.

### 4.4 `organizations` (Organization Management)

**Purpose:** CRUD operations for organizations with event publication.

**Public API:** `OrganizationService.create()`, `.get()`, `.update()`, `.delete()`, `.list()`

**Dependencies:** Database, Publisher, OrganizationRepository

**Database tables:** `organizations`

**Events emitted:** `OrganizationCreated`, `OrganizationUpdated`, `OrganizationDeleted`

**Events consumed:** `on_organization_created`, `on_organization_updated`, `on_organization_deleted` (all logging-only stubs)

**Implementation status:** High. Full CRUD with slug uniqueness validation, optimistic versioning, and event publication.

**Missing work:** Slug update uniqueness check, authorization, typed aggregate root, handler implementations.

### 4.5 `notifications` (Email Service)

**Purpose:** Email delivery abstraction with pluggable providers and HTML email templates.

**Public API:** `EmailService` (Protocol), `EmailMessage` (dataclass), `ConsoleEmailProvider`, `ResendEmailProvider`, `render_verify_email()`, `render_reset_password()`

**Dependencies:** Resend API (production), stdlib logging (console)

**Database tables:** None

**Events emitted:** None

**Events consumed:** None

**Implementation status:** High. `EmailService` Protocol defined. `ConsoleEmailProvider` works for dev (logs to stdout). `ResendEmailProvider` is fully implemented using `resend.Emails().send()` via `asyncio.to_thread()`. Two HTML email templates implemented as Python functions returning `(subject, html)` tuples: `verify_email.py` (inline-styled verification email with CTA button) and `reset_password.py` (inline-styled password reset email with 24-hour expiry warning). Template rendering uses a `_TEMPLATE_MAP` dictionary mapping template names to renderer functions. Email service is wired into `AuthService` via manual setter injection.

**Missing work:** Additional email templates (welcome, organization invite, etc.), wire `EmailService` into DI container instead of manual setter, add template versioning.

### 4.6 `workspaces`

**Purpose:** Placeholder for workspace module.

**Implementation status:** Empty. `__init__.py` only.

### 4.7 `dhara`

**Purpose:** Placeholder for AI compute plane client.

**Implementation status:** Empty. `__init__.py` and `client/__init__.py` only.

### 4.8 `blueprints/academy`

**Purpose:** Academy vertical solution.

**Implementation status:** Empty. No `register()` function, so blueprint discovery silently skips it.

---

## 5. Identity Module Deep Dive

### Authentication

Implemented in `auth_service.py` (~730 lines — the largest file in the codebase).

**Signup flow:**
1. Validate password via `PasswordPolicy` (Argon2 validation + complexity rules + common password check + context check)
2. Create organization with auto-generated slug (retries up to 3 times on slug collision, with random suffix on retry)
3. Create "owner" role for the organization
4. Create user with Argon2-hashed password
5. Create membership linking user to organization with owner role
6. Create organization subscription with blueprint code
7. Create email verification token (SHA-256 hashed)
8. Send verification email via `EmailService` (Resend or Console provider, failures logged but don't block signup)
9. Publish 5 domain events to outbox

**Login flow:**
1. Load user by email
2. Verify password via Argon2
3. Check user is verified and active
4. Load organization, roles, subscriptions
5. Resolve landing URL from blueprint codes
6. Create session with refresh token (SHA-256 hashed)
7. Create access token (JWT)
8. Publish `UserLoggedIn` event

### Authorization

**Not implemented.** All endpoints are publicly accessible. The `Policy` contract exists in `contracts/policy.py` but has zero implementations. No middleware checks authentication or authorization on any route except the manually-implemented `GET /auth/me`.

### Sessions

Stored in the `sessions` table. Each login creates a session with:
- `refresh_token_hash` (SHA-256)
- `ip_address`, `user_agent`, `device_name`
- `expires_at` (30 days by default)
- `revoked_at` (soft delete)

Sessions are revoked on logout, password reset, or explicit revocation.

### JWT

- **Algorithm:** RS256 (asymmetric RSA)
- **Private key:** `keys/dev-private.pem` (used for signing)
- **Public key:** `keys/dev-public.pem` (used for verification)
- **Access token expiry:** 15 minutes
- **Refresh token expiry:** 30 days (enforced via session `expires_at`)
- **Claims:** `sub` (user ID), `org` (organization ID), `roles` (list), `iat`, `exp`, `type` ("access")
- **No JTI claim** — tokens cannot be individually revoked at the JWT level
- **No key rotation support** — keys loaded once at startup

### Refresh Tokens

- Generated via `secrets.token_urlsafe(48)` (~64 char base64 string)
- Stored as SHA-256 hashes in the `sessions` table
- Sent to client as an HttpOnly, Secure (in production), SameSite=Lax cookie
- **No rotation** — the same refresh token remains valid until expiry or revocation
- **No JTI linkage** — the access token does not reference the session

### Password Reset

1. `forgot_password(email)` creates a token with 1-hour expiry and `purpose=RESET_PASSWORD`
2. Token is SHA-256 hashed before storage
3. Reset email sent via email service
4. `reset_password(token, new_password)` validates token, hashes new password, revokes ALL sessions for the user

### Email Verification

1. During signup, a verification token is created with 24-hour expiry and `purpose=VERIFY_EMAIL`
2. Token is SHA-256 hashed before storage
3. User cannot login until email is verified
4. `verify_email(token)` validates and marks user as verified

### Organization Membership

Created during signup. Links a user to an organization with a role. The `memberships` table has FK constraints to `users`, `organizations`, and `organization_roles`.

### Roles

Created during signup as an "owner" role. Stored in `organization_roles` with a JSON `permissions` field. Roles are included in JWT access tokens.

### Permissions

The `permissions` field on `organization_roles` is a JSON column with no structured schema. The `Capability` and `Policy` contracts exist but are not implemented. **No permission checks are performed anywhere.**

### Middleware

- `LoggingMiddleware` — logs all requests (no auth check)
- `error_handler` — maps ADXError to HTTP status codes (DomainError → 4xx, InfrastructureError → 5xx)
- **No authentication middleware** — the only auth check is manual token parsing in `GET /auth/me`

### Security Considerations

| Concern | Status |
|---|---|
| Password hashing (Argon2) | Implemented |
| JWT signing (RS256) | Implemented |
| Refresh token hashing (SHA-256) | Implemented |
| Verification token hashing | Implemented |
| Cookie security (HttpOnly, Secure, SameSite) | Implemented |
| Rate limiting on login | **Not implemented** |
| Rate limiting on signup | **Not implemented** |
| Rate limiting on forgot-password | **Not implemented** |
| Brute-force protection | **Not implemented** |
| Refresh token rotation | **Not implemented** |
| Admin route protection | **Not implemented** |
| CORS wildcard with credentials | **Invalid config** (browsers reject `*` with credentials) |
| Verification URL in signup response | Information leak risk |
| Email enumeration prevention | Partial (forgot_password nondeterministic, but get_by_email leaks) |

---

## 6. Database

### Table: `organizations`
- **Purpose:** Tenant/organization root entity
- **Relationships:** Parent of users, roles, memberships, subscriptions
- **Constraints:** PK (UUID), UNIQUE (slug), NOT NULL on all fields
- **Indexes:** slug (unique)
- **Current usage:** Organization CRUD, slug-based lookup
- **Unused columns:** None
- **Future concerns:** No soft-delete; hard delete cascades are not configured

### Table: `users`
- **Purpose:** User identity and authentication
- **Relationships:** Belongs to organization (FK missing at DB level), parent of sessions, verification tokens, memberships
- **Constraints:** PK (UUID), UNIQUE (email), NOT NULL
- **Indexes:** email (unique), organization_id
- **Current usage:** Full auth lifecycle
- **Unused columns:** `auth_provider`, `auth_provider_id` (OAuth not implemented)
- **Future concerns:** `organization_id` has no FK constraint — allows orphaned users. Only one organization per user is enforced by the application, not the DB.

### Table: `organization_roles`
- **Purpose:** Role definitions per organization
- **Relationships:** Belongs to organization, parent of memberships
- **Constraints:** PK (UUID), FK to organizations.id, NOT NULL
- **Indexes:** organization_id
- **Current usage:** Created during signup as "owner"
- **Unused columns:** `permissions` (JSON field, never read or checked)
- **Future concerns:** No unique constraint on (name, organization_id) — duplicates possible

### Table: `memberships`
- **Purpose:** Many-to-many user-organization relationships with roles
- **Relationships:** FK to users.id, organizations.id, organization_roles.id
- **Constraints:** PK (UUID), three FKs, NOT NULL
- **Indexes:** user_id, organization_id
- **Current usage:** Created during signup, read during login to load roles
- **Unused columns:** None
- **Future concerns:** No unique constraint on (user_id, organization_id) — duplicate memberships possible. No `list_for_org` query.

### Table: `sessions`
- **Purpose:** Refresh token sessions
- **Relationships:** FK to users.id
- **Constraints:** PK (UUID), FK to users.id, NOT NULL
- **Indexes:** user_id
- **Current usage:** Login, refresh, logout, password reset
- **Unused columns:** `device_name` (stored but never returned to client)
- **Future concerns:** No cleanup job for expired sessions. No index on `refresh_token_hash` (used for lookups).

### Table: `email_verification_tokens`
- **Purpose:** Email verification and password reset tokens
- **Relationships:** FK to users.id
- **Constraints:** PK (UUID), FK to users.id, NOT NULL
- **Indexes:** user_id
- **Current usage:** Email verification, password reset
- **Unused columns:** None
- **Future concerns:** No cleanup job for expired tokens. No index on `token_hash` (used for lookups).

### Table: `organization_subscriptions`
- **Purpose:** Tracks which blueprint solutions an organization has subscribed to
- **Relationships:** FK to organizations.id
- **Constraints:** PK (UUID), FK to organizations.id, NOT NULL
- **Indexes:** organization_id
- **Current usage:** Created during signup, read during login to resolve landing URL
- **Unused columns:** `ends_at` (never checked for expiry), `status` (always "active", never transitioned)
- **Future concerns:** No subscription lifecycle management (cancel, renew, upgrade)

### Table: `event_outbox`
- **Purpose:** Transactional outbox for reliable event publishing
- **Constraints:** PK (UUID), NOT NULL
- **Indexes:** status
- **Current usage:** Events written by Publisher, never dispatched
- **Unused columns:** `retry_count`, `max_retries`, `last_error`, `next_retry_at`, `processed_at` (dispatcher is a no-op)
- **Future concerns:** No cleanup job for processed events. No index on `aggregate_type + aggregate_id`. No index on `next_retry_at`.

### Table: `processed_events`
- **Purpose:** Event deduplication
- **Constraints:** PK (event_id), NOT NULL
- **Indexes:** event_id (PK)
- **Current usage:** Never written to or read from
- **Unused columns:** Entire table is unused
- **Future concerns:** No TTL/cleanup mechanism

---

## 7. API Inventory

### Health Endpoints

| Route | Method | Auth | Status |
|---|---|---|---|
| `/health/live` | GET | None | Implemented |
| `/health/ready` | GET | None | Implemented |

### Auth Endpoints

| Route | Method | Request | Response | Auth | Status |
|---|---|---|---|---|---|
| `/api/v1/auth/signup` | POST | `SignupRequest` (org_name, blueprint, name, email, password) | `SignupResponse` (org, user, verified, message) | None | Complete |
| `/api/v1/auth/login` | POST | `LoginRequest` (email, password, device_name) | `LoginResponse` (access_token, user, org, landing_url) + Set-Cookie | None | Complete |
| `/api/v1/auth/refresh` | POST | Cookie (refresh_token) | `TokenRefreshResponse` (access_token, token_type) | Refresh cookie | Complete |
| `/api/v1/auth/logout` | POST | Cookie (refresh_token) | 204 No Content + Clear-Cookie | Refresh cookie | Complete |
| `/api/v1/auth/verify-email` | POST | `VerifyEmailRequest` (token) | `{"verified": true}` | None | Complete |
| `/api/v1/auth/forgot-password` | POST | `ForgotPasswordRequest` (email) | `{"email_sent": true}` | None | Complete |
| `/api/v1/auth/reset-password` | POST | `ResetPasswordRequest` (token, new_password) | `{"reset": true}` | None | Complete |
| `/api/v1/auth/me` | GET | Bearer token in header | `MeResponse` (user, org, subscriptions, roles) | Bearer token | Complete |

### User Management Endpoints (UNPROTECTED)

| Route | Method | Request | Response | Auth | Status |
|---|---|---|---|---|---|
| `/api/v1/users` | POST | `CreateUserRequest` (email, name) | `UserResponse` | **None** | Functional, unprotected |
| `/api/v1/users/{user_id}` | GET | Path param | `UserResponse` | **None** | Functional, unprotected |
| `/api/v1/users/by-email/{email}` | GET | Path param | `UserResponse` | **None** | Functional, unprotected |
| `/api/v1/users/{user_id}/deactivate` | POST | Path param | `UserResponse` | **None** | Functional, hardcoded org_id=0 |
| `/api/v1/users/{user_id}/reactivate` | POST | Path param | `UserResponse` | **None** | Functional, hardcoded org_id=0 |
| `/api/v1/users` | GET | Query params (skip, limit, organization_id) | `UserListResponse` | **None** | Functional, incorrect pagination total |

### Organization Endpoints (UNPROTECTED)

| Route | Method | Request | Response | Auth | Status |
|---|---|---|---|---|---|
| `/api/v1/organizations` | POST | `OrganizationCreateRequest` (name, slug) | `OrganizationResponse` | **None** | Complete |
| `/api/v1/organizations/{org_id}` | GET | Path param | `OrganizationResponse` | **None** | Complete |
| `/api/v1/organizations/{org_id}` | PATCH | `OrganizationUpdateRequest` (name, slug) | `OrganizationResponse` | **None** | Complete |
| `/api/v1/organizations/{org_id}` | DELETE | Path param | 204 | **None** | Complete |
| `/api/v1/organizations` | GET | Query params (skip, limit) | `OrganizationListResponse` | **None** | Complete, incorrect pagination total |

---

## 8. Event System

### All Events

| Event Type | Module | Emitted By | Consumed By | Handler Status |
|---|---|---|---|---|
| `user.created.v1` | identity | `IdentityService.create_user()` | `identity/handlers.py` | Logging stub |
| `user.deactivated.v1` | identity | `IdentityService.deactivate()` | `identity/handlers.py` | Logging stub |
| `user.reactivated.v1` | identity | `IdentityService.reactivate()` | `identity/handlers.py` | Logging stub |
| `organization.created.v1` | identity (signup) | `AuthService._attempt_signup()` | `organizations/handlers.py` | Logging stub |
| `membership.created.v1` | identity | `AuthService._attempt_signup()` | None | **Unhandled** |
| `organization_subscription.created.v1` | identity | `AuthService._attempt_signup()` | None | **Unhandled** |
| `email_verification_token.created.v1` | identity | `AuthService._attempt_signup()` | None | **Unhandled** |
| `email.verified.v1` | identity | `AuthService.verify_email()` | None | **Unhandled** |
| `password.reset.v1` | identity | `AuthService.reset_password()` | None | **Unhandled** |
| `user.logged_in.v1` | identity | `AuthService.login()` | None | **Unhandled** |
| `user.logged_out.v1` | identity | `AuthService.logout()` | None | **Unhandled** |
| `session.refreshed.v1` | identity | `AuthService.refresh()` | None | **Unhandled** |
| `organization.created.v1` | organizations | `OrganizationService.create()` | `organizations/handlers.py` | Logging stub |
| `organization.updated.v1` | organizations | `OrganizationService.update()` | `organizations/handlers.py` | Logging stub |
| `organization.deleted.v1` | organizations | `OrganizationService.delete()` | `organizations/handlers.py` | Logging stub |

### Event Bus Implementation

- **In-process EventBus** (`events/bus.py`): Dict-backed, async handlers, error swallowing with logging. No persistence.
- **Transactional Outbox** (`events/publisher.py`): Writes events to `event_outbox` table within the same DB transaction. Uses `OutboxTable` ORM model directly.
- **Outbox Dispatcher** (`events/outbox.py`): Skeleton with `start()`/`stop()` lifecycle, but `_dispatch_batch()` is a no-op.
- **Subscriber Registry** (`events/subscriber.py`): Separate dict-backed registry that is never used by the EventBus.

### Future Scalability Concerns

1. **Events are never dispatched** — the entire event-driven architecture is aspirational, not operational
2. **In-process bus** — events are lost on process restart
3. **No event schema versioning** — `v1` is hardcoded with no migration strategy
4. **No idempotency** — `processed_events` table exists but is never used
5. **No ordering guarantees** across partitions
6. **Duplicate `OutboxEntry` definitions** — one in `events/outbox.py` (dataclass), one in `events/ports/outbox_repository.py` (dataclass)

---

## 9. Configuration

### Settings (`kernel/config/loader.py`)

All configuration is managed via Pydantic Settings loading from environment variables and `.env` files:

| Setting | Default | Used |
|---|---|---|
| `app_name` | "adx-platform" | Yes (FastAPI title) |
| `debug` | False | Yes (DB echo) |
| `api_host` / `api_port` | 0.0.0.0 / 8000 | **Defined but not used** (hardcoded in uvicorn.run) |
| `api_prefix` | "/api/v1" | Yes |
| `database_url` | postgresql+asyncpg://... | Yes |
| `redis_url` | redis://... | **Defined but not used** |
| `log_level` | "info" | Yes |
| `jwt_private_key_path` | "keys/dev-private.pem" | Yes |
| `jwt_public_key_path` | "keys/dev-public.pem" | Yes |
| `jwt_algorithm` | "RS256" | Yes |
| `jwt_access_token_expire_minutes` | 15 | Yes |
| `jwt_refresh_token_expire_days` | 30 | Yes |
| `rate_limit_enabled` / requests / window | True / 10 / 60 | **Defined but not wired** |
| `password_min_length` | 8 | Yes |
| `password_max_length` | 128 | Yes |
| `password_require_upper/lower/digit/special` | True/True/True/False | Yes |
| `email_provider` | "console" | Yes (selects Console or Resend provider) |
| `resend_api_key` | "" | Yes (used when `email_provider=resend`) |
| `email_from_address` | "ADX <noreply@adhyayanx.in>" | Yes |

### Feature Flags

None. No feature flag system exists.

### Startup Configuration

Single configuration path via `Settings()`. No profiles (dev/staging/production). No conditional feature enabling.

### Dependency Injection

Custom hand-rolled container (`kernel/container.py`):
- `register(interface, implementation)` — type-to-type mapping (lazy build)
- `register_instance(interface, instance)` — type-to-instance mapping (singleton)
- `resolve(interface)` — auto-wire by inspecting `__init__` type annotations
- **Bug:** Union type resolution fails (line 71 compares against `annotation` instead of `part`)
- **Singleton-only** — no transient or request-scoped lifetimes

---

## 10. Infrastructure

### Database

PostgreSQL 16 via async SQLAlchemy (`asyncpg` driver). Connection pool: `pool_size=5`, `max_overflow=10`, `pool_pre_ping=True`, `pool_recycle=1800s`. SQL statement counter per request via `ContextVar`.

### Repositories

8 Postgres repository implementations:
- `PostgresOrganizationRepository` — full CRUD + slug lookup
- `PostgresOrganizationRoleRepository` — load, create, lookup by name+org, list for org
- `PostgresOrganizationSubscriptionRepository` — create, load active by org
- `PostgresIdentityRepository` — full CRUD + auth ops
- `PostgresMembershipRepository` — create, lookup by user+org, list for user
- `PostgresSessionRepository` — create, lookup by hash, revoke, revoke all, update last seen
- `PostgresVerificationTokenRepository` — create, lookup by hash, mark used
- `PostgresOutboxRepository` — append, fetch next batch (FOR UPDATE SKIP LOCKED), mark processed, increment retry, dead letter

All repositories operate on `dict[str, Any]`, not typed domain objects.

### Email

- `ConsoleEmailProvider` — prints to stdout (dev)
- `ResendEmailProvider` — fully implemented using `resend.Emails().send()` via `asyncio.to_thread()`
- `EmailService` — Protocol interface
- HTML email templates: `verify_email.py`, `reset_password.py` (Python functions returning `(subject, html)`)
- Template rendering via `_TEMPLATE_MAP` dictionary in `ResendEmailProvider`
- Wired via manual setter, not through DI container

### Logging

- `structlog` configured in `main.py` but **all code uses stdlib `logging.getLogger()`**
- `LoggingMiddleware` logs request method, path, status, duration

### Background Tasks

- `Lifecycle.create_task()` exists but is never called
- `OutboxDispatcher` has start/stop lifecycle but is never instantiated
- No background workers, no cron jobs

### Storage

Not implemented. No file storage, S3, or blob storage integration.

### External Integrations

- Resend email API (fully implemented, used for transactional emails)
- DHARA compute plane (empty placeholder)
- No other external integrations

---

## 11. Testing

### Test Structure

```
tests/
├── integration/
│   ├── auth/
│   │   ├── conftest.py          # 332 lines — in-memory repos, mock DB, test app factory
│   │   ├── test_signup.py       # 4 tests
│   │   ├── test_login.py        # 4 tests
│   │   ├── test_logout.py       # 2 tests
│   │   ├── test_refresh.py      # 4 tests
│   │   ├── test_me.py           # 2 tests
│   │   ├── test_verify_email.py # 4 tests
│   │   ├── test_forgot_password.py  # 2 tests
│   │   ├── test_reset_password.py   # 4 tests
│   │   └── test_identity_lifecycle.py  # 1 E2E test
│   └── test_organization_lifecycle.py  # 1 CRUD + events test
└── unit/
    └── notifications/
        └── test_email_provider_contract.py  # 1 smoke test
```

### Coverage

No coverage reporting is configured despite `pytest-cov` being a dev dependency. CI runs `pytest -v` without `--cov`.

### What Is Tested

- Complete auth lifecycle (signup → verify → login → me → refresh → logout → stale refresh fails)
- Organization CRUD lifecycle with event verification
- All major auth failure modes (wrong password, unverified, deactivated, expired token, used token, invalid token)
- Anti-email-enumeration on forgot-password
- Session revocation on password reset
- Slug uniqueness on signup

### What Is Missing

- No tests for user management endpoints (deactivate, reactivate, list)
- No tests for organization authorization (currently unprotected)
- No tests for the EventBus, Publisher, or Outbox
- No unit tests for TokenService, PasswordPolicy, NavigationService
- No tests for error handling middleware
- No tests for the DI container
- No tests for rate limiter
- No tests for database repositories (all tests use in-memory mocks)
- No tests for weak password on reset
- No tests for wrong-purpose tokens
- No coverage reporting

### Quality Assessment

The integration test suite is well-built for what it covers. The test doubles faithfully implement the hexarchical architecture. The conftest is a model of test infrastructure design. However, coverage is narrow — only auth and org CRUD are tested. The unit test directory is almost entirely empty scaffolding.

---

## 12. Frontend

**Framework:** Next.js 16 (App Router) with React 19, TypeScript, Tailwind CSS v4, shadcn/ui (base-nova style).

**Current status:** Functional auth flows and read-only console pages. The frontend implements login, signup, forgot-password, reset-password, and email verification. Console pages show user profile, organization details, and settings (logout only). Auth context manages session state with silent refresh on mount.

**Architecture:** Feature-based module structure (`features/auth/`) with route group layout isolation (`(public)` vs `(console)`). API calls go through centralized `api-client.ts` with `ApiResult<T>` discriminated unions. Client-side auth guard via React context. Edge middleware redirects logged-in users from guest routes.

**Implemented pages:**
- `/login` — Email + password form with Zod validation
- `/signup` — Organization name, owner name, email, password form (hardcodes `blueprint_code: "academy"`)
- `/forgot-password` — Email-only form
- `/reset-password` — Password + confirm password form (reads `?token=` from URL)
- `/verify-email` — Auto-fires verification on mount (reads `?token=` from URL)
- `/console` — Dashboard with user name, profile card, org card
- `/console/profile` — User details (name, email, verified, auth provider, state)
- `/console/organization` — Org details (name, slug, status, created date)
- `/console/settings` — Account settings (logout button only)

**UI components:** 13 shadcn/ui components (alert, avatar, button, card, dropdown-menu, input, label, loading-spinner, separator, sheet) built on `@base-ui/react` primitives.

**Missing work:** Console CRUD operations (edit profile, edit org), server-side route protection for `/console`, additional form validation, error boundary improvements, API error display in forms, loading states for data fetching, responsive design polish.

---

## 13. Docker / Deployment

### Docker

- `backend/Dockerfile`: Python 3.12-slim + uv, exposes port 8000, runs `python -m app.api.main`
- `backend/.dockerignore`: Excludes `.venv`, `.git`, `__pycache__`, `*.pyc`, caches, `.env`
- No multi-stage build (includes build tools in final image)
- No non-root user
- No health check in Dockerfile

### docker-compose.yml

- PostgreSQL 16 Alpine with health check and persistent volume
- No application service defined
- No Redis service
- No network configuration
- Hardcoded credentials (postgres/postgres)

### Health Checks

- `/health/live` and `/health/ready` endpoints exist
- Docker compose has PostgreSQL health check (`pg_isready`)

### CI

GitHub Actions on every push/PR:
1. Install uv + Python 3.12
2. `ruff check .`
3. `ruff format --check .`
4. `mypy .`
5. `pytest -v`

Missing: coverage reporting, test artifact upload, dependency caching, matrix testing.

### Deployment Readiness

Not deployment-ready. Missing:
- Production Docker Compose or Kubernetes manifests
- Environment-specific configuration
- Secret management
- Database migration automation in deploy pipeline
- Proper health checks (liveness vs readiness)
- Graceful shutdown (Lifecycle not wired)
- Structured logging to stdout for container aggregation
- Non-root Docker user

### Production Blockers

1. CORS allows `*` with credentials (invalid, browsers reject)
2. No HTTPS enforcement
3. No rate limiting
4. Admin routes completely unprotected
5. Database credentials hardcoded in docker-compose
6. JWT dev keys in repository
7. No graceful shutdown
8. Events never dispatched

---

## 14. Code Quality Review

### Dead Code

| File | Issue |
|---|---|
| `contracts/repository.py` | Generic `Repository` ABC — never subclassed |
| `contracts/capability.py` | `Capability` ABC — zero implementations |
| `contracts/policy.py` | `Policy` ABC — zero implementations |
| `contracts/workflow.py` | Entire workflow system — zero implementations |
| `events/subscriber.py` | `SubscriberRegistry` — never used by EventBus |
| `events/handlers.py` | `log_all_events` — never registered |
| `identity/commands.py` | `ForgotPasswordCommand`, `RefreshTokenCommand`, `LogoutCommand` — defined but unused |
| `identity/solution_blueprint.py` | `SolutionBlueprint` enum — never imported |
| `identity/schemas.py` | `TokenRefreshRequest`, `ErrorResponse` — defined but unused |
| `infrastructure/rate_limiter.py` | Entire rate limiter — implemented but never wired |
| `kernel/lifecycle.py` | `Lifecycle` — created but never integrated |

### Duplicate Code

| Files | Issue |
|---|---|
| `events/outbox.py` vs `events/ports/outbox_repository.py` | Two `OutboxEntry` dataclass definitions |
| `events/subscriber.py` vs `events/ports/event_bus.py` | Two `EventHandler` type aliases (sync vs async) |
| `tests/integration/auth/conftest.py` vs `test_organization_lifecycle.py` | `DictOrganizationRepository`, `MockAsyncSession`, `MockDatabase`, `RecordingPublisher` duplicated |
| `foundation/types.py` vs `kernel/container.py` vs `api/dependencies/container.py` | Three `T = TypeVar("T")` definitions |
| `identity/service.py` and `organizations/service.py` | Both lazily import concrete Postgres repositories inside every method |

### Unused Abstractions

- `BusinessObject` — never subclassed
- `Repository` — never extended
- `Capability` — never implemented
- `Policy` — never implemented
- `WorkflowDefinition` / `WorkflowInstance` / `WorkflowStep` — never used
- `SubscriberRegistry` — never used
- `SolutionBlueprint` enum — never referenced

### Large Files

| File | Lines | Concern |
|---|---|---|
| `identity/auth_service.py` | ~730 | Too many responsibilities; should be decomposed |
| `tests/integration/auth/conftest.py` | ~332 | Large but justified for test infrastructure |
| `docs/aps/runtime-spec.md` | ~655 | Documentation, not a concern |

### Architecture Violations

1. **Domain services import concrete infrastructure** — `identity/service.py` and `organizations/service.py` import `PostgresIdentityRepository` and `PostgresOrganizationRepository` directly inside methods, bypassing the port abstraction
2. **Email service wired outside DI** — `main.py` calls `auth_service.set_email_service()` after construction, breaking the container's encapsulation
3. **No request-scoped DI** — all services are singletons, which could accumulate state across requests

### DDD Violations

1. **No typed aggregates** — everything operates on `dict[str, Any]` instead of domain objects
2. **`BusinessObject` is never used** — the aggregate root pattern is designed but not implemented
3. **No invariant validation** — `validate_invariants()` is abstract but never implemented
4. **No domain events raised by aggregates** — events are created manually in service methods, not by aggregates applying state changes
5. **No value objects** — email, slug, and other conceptually immutable values are plain strings

### Clean Architecture Violations

1. **Domain layer depends on infrastructure** — lazy imports of `Postgres*Repository` inside service methods
2. **API layer contains business logic** — `auth_router.py` has cookie management helpers that could be in a middleware
3. **No use case layer** — services directly orchestrate without a clear use-case/application-service boundary

### Tight Coupling

1. **`auth_service.py` depends on 7 concrete repository classes** — even though ports exist
2. **`main.py` manually wires email service into AuthService** — tight coupling between app factory and service internals
3. **`_SOLUTION_DOMAINS` in navigation_service.py is hardcoded** — coupled to specific subdomain names

### Premature Abstractions

1. `Capability` ABC — over-engineered before any capabilities exist
2. `Workflow` system — full saga infrastructure with zero consumers
3. `SubscriberRegistry` — parallel to EventBus for unknown reasons
4. Generic `Repository` ABC — designed for a typed domain model that was never built

### Code Smells

1. **Magic UUID(0)** — `identity/router.py` hardcodes `organization_id=UUID(int=0)` for deactivate/reactivate
2. **`len(items)` as total** — both routers compute pagination total from fetched items, defeating the purpose of skip/limit
3. **`structlog` configured but unused** — configuration has no effect
4. **`api_host`/`api_port` settings ignored** — hardcoded in uvicorn.run
5. **Verification URL in signup response** — raw token leaked in API response
6. **Frontend hardcodes `blueprint_code: "academy"`** — signup form doesn't let users choose a blueprint
7. **`.env.example` contains real credentials** — Neon DB URL and Resend API key are committed; should use placeholders
8. **Client-side-only route protection** — `/console` routes protected only by React context, not server-side middleware

---

## 15. Technical Debt

Ranked by severity:

| Rank | Debt | Severity | Impact |
|---|---|---|---|
| 1 | All admin routes (users, orgs) have zero authentication/authorization | **Critical** | Anyone can create, modify, deactivate users and organizations |
| 2 | Outbox dispatcher is a no-op — events written but never dispatched | **Critical** | Event-driven architecture is non-functional |
| 3 | Domain services import concrete Postgres repositories, bypassing ports | **High** | Undermines hexagonal architecture, makes testing harder |
| 4 | `Lifecycle` not integrated into FastAPI lifespan | **High** | No graceful shutdown, DB connection leak |
| 5 | Container `_resolve_annotation` bug with Union types | **High** | Will cause runtime failures for optional dependencies |
| 6 | No typed domain model — everything is `dict[str, Any]` | **High** | Fragile, no compile-time safety, defeats DDD |
| 7 | `.env.example` contains real credentials (Neon DB, Resend API key) | **High** | Security risk — secrets in version control |
| 8 | `BusinessObject` aggregate root never subclassed | **Medium** | No invariant validation, no optimistic locking at domain level |
| 9 | 10+ dead code files (Capability, Policy, Workflow, etc.) | **Medium** | Confusing for new developers, increases cognitive load |
| 10 | `structlog` configured but unused | **Low** | Misleading configuration |
| 11 | Email service wired outside DI | **Medium** | Hidden dependency, testability concern |
| 12 | No rate limiting anywhere | **High** | Vulnerable to abuse |
| 13 | Duplicate `OutboxEntry`, `EventHandler`, `TypeVar("T")` | **Low** | Code confusion |
| 14 | `api_host`/`api_port` settings ignored | **Low** | Configuration drift |
| 15 | Incorrect pagination total in list endpoints | **Low** | Minor functional bug |
| 16 | Three unused commands (ForgotPassword, RefreshToken, Logout) | **Low** | Dead code |
| 17 | Frontend `/console` routes protected only client-side | **Medium** | No server-side auth guard on protected routes |
| 18 | Frontend signup hardcodes `blueprint_code: "academy"` | **Low** | Users cannot choose their blueprint |

---

## 16. Immediate Roadmap

Based solely on the current repository state:

### Milestone 1: Authorization & Security (Complexity: High)
**Why:** The application is completely open. Every `/users` and `/organizations` endpoint is unprotected. This must be fixed before anything else.
**Tasks:** Implement `get_current_user` FastAPI dependency, protect all admin routes, add role-based access checks, fix CORS configuration, add server-side route protection for frontend `/console` routes.
**Dependencies:** None
**Risks:** Changing all endpoint signatures; potential breaking changes to existing tests.

### Milestone 2: Event System Wiring (Complexity: Medium)
**Why:** The outbox pattern is half-built. Events are written but never delivered. This is silent data loss.
**Tasks:** Wire discovered handlers to EventBus, implement `_dispatch_batch()` in OutboxDispatcher, connect dispatcher to lifecycle, implement event handler idempotency via `processed_events`.
**Dependencies:** Milestone 1 (for lifecycle integration)
**Risks:** Background task management, idempotency bugs.

### Milestone 3: Typed Domain Model (Complexity: High)
**Why:** The `dict[str, Any]` pattern undermines the entire DDD foundation. No invariant validation, no type safety.
**Tasks:** Create concrete `Organization`, `User`, `Membership` aggregate roots extending `BusinessObject`. Refactor repositories to return typed objects. Implement `validate_invariants()`.
**Dependencies:** None (can run parallel with Milestone 1)
**Risks:** Large-scale refactoring across services and repositories.

### Milestone 4: Rate Limiting & Brute-Force Protection (Complexity: Medium)
**Why:** The in-memory rate limiter exists but is unwired. Login, signup, and forgot-password are vulnerable to abuse.
**Tasks:** Wire rate limiter as FastAPI middleware/dependency, add failed-login tracking, implement account lockout, add rate limiting to forgot-password.
**Dependencies:** Milestone 1
**Risks:** Redis needed for distributed rate limiting (currently in-memory only).

### Milestone 5: Refresh Token Rotation (Complexity: Low)
**Why:** The same refresh token remains valid indefinitely until expiry. This is a security risk.
**Tasks:** On refresh, issue a new refresh token and invalidate the old one. Update session records accordingly.
**Dependencies:** Milestone 1
**Risks:** Must handle race conditions (concurrent refresh requests).

### Milestone 6: Frontend Enhancements (Complexity: Medium)
**Why:** Console pages are read-only. No CRUD operations for profile or organization.
**Tasks:** Add profile editing form, organization settings form, proper error handling in forms, loading states, responsive design. Add server-side route protection via Next.js middleware.
**Dependencies:** Milestone 1 (for auth endpoints to be stable)
**Risks:** Frontend-backend contract changes.

### Milestone 7: Lifecycle Integration & Graceful Shutdown (Complexity: Low)
**Why:** Database connections are never properly closed. Background tasks are never cancelled.
**Tasks:** Integrate `Lifecycle.lifespan()` into FastAPI app, register `Database.close()` as shutdown hook.
**Dependencies:** None
**Risks:** Minimal.

### Milestone 8: Fix Container Union Resolution Bug (Complexity: Low)
**Why:** The `_resolve_annotation` method in the DI container has a bug that prevents Union type annotations from resolving.
**Tasks:** Fix line 71 to compare `t.__name__ == part` instead of `t.__name__ == annotation`.
**Dependencies:** None
**Risks:** Minimal.

### Milestone 9: Remove Dead Code (Complexity: Low)
**Why:** 10+ files of dead abstractions confuse new developers.
**Tasks:** Remove or archive `Capability`, `Policy`, `Workflow`, `SubscriberRegistry`, unused commands, `SolutionBlueprint`.
**Dependencies:** None
**Risks:** Low, but need to verify no import side effects.

### Milestone 10: Security Hygiene (Complexity: Low)
**Why:** `.env.example` contains real credentials. JWT dev keys are in the repository.
**Tasks:** Replace `.env.example` credentials with placeholders, rotate exposed keys, add `.env` to `.gitignore` (verify), add pre-commit hook for secret detection.
**Dependencies:** None
**Risks:** Must ensure existing deployments are not affected by key rotation.

---

## 17. Production Readiness Score

| Category | Score | Justification |
|---|---|---|
| **Architecture** | 7/10 | Sound design (DDD, hexagonal, outbox), but large gap between design and implementation. Contracts exist but are unused. |
| **Maintainability** | 6/10 | Clean module boundaries, good separation. Dragged down by dict-based data, dead code, and 730-line auth_service. |
| **Security** | 4/10 | Password hashing, JWT, and Resend email are solid. But all admin routes unprotected, no rate limiting, no brute-force protection, CORS misconfigured, `.env.example` leaks credentials. |
| **Testing** | 5/10 | Excellent integration tests for auth (30+ tests). But no unit tests, no coverage reporting, no repository tests, no event system tests, no frontend tests. |
| **Scalability** | 3/10 | Single-process in-memory event bus. No Redis. In-memory rate limiter. No background worker infrastructure. |
| **Developer Experience** | 6/10 | Good CI, clean structure, helpful READMEs. Dragged down by dead code, misleading configurations, and sparse docs. |
| **Deployment** | 2.5/10 | Dockerfile exists with .dockerignore but is insecure (root user, no multi-stage). No production compose/K8s. No secret management. No migration automation. |
| **Documentation** | 7.5/10 | Excellent runtime spec. Good frontend architecture doc. Good STATUS.md and READMEs. Dragged down by stale STATUS.md and no API docs. |
| **Overall** | **5.1/10** | Working prototype with authentication, email integration, and frontend scaffolding. Solid architectural foundations but significant gaps in security, deployment, and operational readiness. |

---

## 18. File-Level Summary

### Core Application

| File | Purpose | Complete? | Refactor? |
|---|---|---|---|
| `api/main.py` | App factory, wiring | Yes | Minor: fix CORS, use settings for host/port, register email service in DI |
| `api/routers/__init__.py` | Router registration | Yes | No |
| `api/routers/health.py` | Health endpoints | Yes | No |
| `api/middleware/error_handler.py` | Global error mapping | Partial | Add AuthenticationError mapping (401), fix type(subclass) handling |
| `api/middleware/logging.py` | Request logging | Yes | Minor: use perf_counter, add request ID |
| `api/dependencies/container.py` | DI bridge to FastAPI | Yes | No |
| `kernel/bootstrap.py` | Startup orchestrator | Yes | Fix: integrate Lifecycle into app |
| `kernel/container.py` | DI container | Partial | Fix Union resolution bug |
| `kernel/discovery.py` | Blueprint/handler discovery | Partial | Handlers discovered but not wired |
| `kernel/lifecycle.py` | Startup/shutdown hooks | Yes (but unused) | Wire into FastAPI lifespan |
| `kernel/config/loader.py` | Settings | Yes | Add validation, use api_host/api_port |
| `foundation/exceptions/base.py` | Exception hierarchy | Yes | No |
| `foundation/types.py` | Type aliases | Yes | Minor: deduplicate TypeVar |
| `foundation/security/__init__.py` | Security utils | Empty | Implement or remove |

### Infrastructure

| File | Purpose | Complete? | Refactor? |
|---|---|---|---|
| `infrastructure/postgres/database.py` | DB engine, sessions | Yes | Minor: add pool metrics |
| `infrastructure/postgres/tables.py` | ORM models | Yes | Add missing composite unique constraints |
| `infrastructure/postgres/unit_of_work.py` | Transaction boundary | Partial | Outbox entries never auto-persisted, no async context manager |
| `infrastructure/postgres/organization_repository.py` | Org persistence | Yes | No |
| `infrastructure/postgres/identity_repository.py` | User persistence | Yes | No |
| `infrastructure/postgres/membership_repository.py` | Membership persistence | Partial | Missing delete, update, list-for-org |
| `infrastructure/postgres/session_repository.py` | Session persistence | Yes | Missing cleanup job |
| `infrastructure/postgres/verification_token_repository.py` | Token persistence | Partial | mark_used typed as Any |
| `infrastructure/postgres/outbox_repository.py` | Outbox persistence | Yes | Not connected to outbox dispatcher |
| `infrastructure/postgres/organization_role_repository.py` | Role persistence | Partial | Missing update, delete |
| `infrastructure/postgres/organization_subscription_repository.py` | Subscription persistence | Partial | Missing update, cancel, expiry check |
| `infrastructure/rate_limiter.py` | Rate limiter | Partial | In-memory only, memory leak, not wired |
| `infrastructure/postgres/migrations/env.py` | Alembic runner | Yes | No |
| `infrastructure/postgres/migrations/versions/*.py` | Schema migrations | Yes | No |

### Domain Modules

| File | Purpose | Complete? | Refactor? |
|---|---|---|---|
| `platform/contracts/business_object.py` | Aggregate root base | Yes (as design) | Never used — consider removing or implementing |
| `platform/contracts/command.py` | Command base | Yes | No |
| `platform/contracts/event.py` | Event base | Yes | No |
| `platform/contracts/repository.py` | Repository base | Yes (as design) | Unused — remove or align repos |
| `platform/contracts/capability.py` | Capability base | Yes (as design) | Unused — remove |
| `platform/contracts/policy.py` | Policy base | Yes (as design) | Unused — remove or implement |
| `platform/contracts/workflow.py` | Workflow base | Yes (as design) | Unused — remove or implement |
| `platform/events/bus.py` | In-process event bus | Yes | Wire handlers |
| `platform/events/publisher.py` | Outbox publisher | Yes | Minor: data field double-stores |
| `platform/events/subscriber.py` | Subscriber registry | Yes | Unused — remove |
| `platform/events/handlers.py` | Core event handlers | Stub | Register with bus |
| `platform/events/outbox.py` | Outbox dispatcher | Stub | Implement _dispatch_batch, wire to lifecycle |
| `platform/events/ports/event_bus.py` | EventBus interface | Yes | No |
| `platform/events/ports/outbox_repository.py` | Outbox port | Yes | No |
| `platform/identity/service.py` | User management | Yes | Fix: use port instead of concrete import |
| `platform/identity/auth_service.py` | Auth orchestrator | Yes | Decompose (730 lines), add rate limiting |
| `platform/identity/auth_router.py` | Auth HTTP routes | Yes | Add shared get_current_user dependency |
| `platform/identity/router.py` | User HTTP routes | Partial | Fix: add auth, fix hardcoded UUID(0) |
| `platform/identity/token_service.py` | JWT operations | Yes | Add JTI, key rotation |
| `platform/identity/navigation_service.py` | Landing URL resolver | Yes | Make configurable |
| `platform/identity/password_policy.py` | Password rules | Yes | Expand common passwords list |
| `platform/identity/commands.py` | Identity commands | Partial | Remove 3 unused commands |
| `platform/identity/events.py` | Identity events | Yes | No |
| `platform/identity/handlers.py` | Event handlers | Stub | Implement real handlers for 9 unhandled events |
| `platform/identity/schemas.py` | Pydantic schemas | Yes | Remove 2 unused schemas |
| `platform/identity/solution_blueprint.py` | Blueprint enum | Yes | Use it or remove it |
| `platform/identity/ports/*.py` | Repository ports | Yes | No |
| `platform/organizations/service.py` | Org CRUD | Yes | Fix: use port instead of concrete import |
| `platform/organizations/router.py` | Org HTTP routes | Yes | Add auth |
| `platform/organizations/commands.py` | Org commands | Yes | No |
| `platform/organizations/events.py` | Org events | Yes | No |
| `platform/organizations/handlers.py` | Org event handlers | Stub | Implement real handlers |
| `platform/organizations/schemas.py` | Org schemas | Yes | No |
| `platform/organizations/ports/*.py` | Org repository port | Yes | No |
| `platform/notifications/email_service.py` | Email protocol | Yes | No |
| `platform/notifications/console_provider.py` | Console email | Yes | No |
| `platform/notifications/resend_provider.py` | Resend email | Yes | Minor: add retry logic, template versioning |
| `platform/notifications/emails/__init__.py` | Email templates package | Yes | No |
| `platform/notifications/emails/verify_email.py` | Verify email template | Yes | No |
| `platform/notifications/emails/reset_password.py` | Reset password template | Yes | No |

### Tests

| File | Purpose | Complete? | Refactor? |
|---|---|---|---|
| `tests/integration/auth/conftest.py` | Test fixtures | Yes | Extract shared fixtures to reduce duplication |
| `tests/integration/auth/test_signup.py` | Signup tests | Yes | Add edge case tests |
| `tests/integration/auth/test_login.py` | Login tests | Yes | Add session side-effect tests |
| `tests/integration/auth/test_logout.py` | Logout tests | Partial | Near-duplicate tests, add cookie-clearing test |
| `tests/integration/auth/test_refresh.py` | Refresh tests | Yes | Add rotation test |
| `tests/integration/auth/test_me.py` | /me tests | Yes | Add token-validation tests |
| `tests/integration/auth/test_verify_email.py` | Verification tests | Yes | Add purpose-mismatch test |
| `tests/integration/auth/test_forgot_password.py` | Forgot password tests | Partial | Only 2 tests — needs more |
| `tests/integration/auth/test_reset_password.py` | Reset password tests | Yes | Add weak-password test |
| `tests/integration/auth/test_identity_lifecycle.py` | E2E lifecycle | Yes | Good smoke test |
| `tests/integration/test_organization_lifecycle.py` | Org lifecycle | Yes | Remove fixture duplication |
| `tests/unit/notifications/test_email_provider_contract.py` | Email contract | Minimal | Needs real assertions |

---

## 19. Git State

| Item | Value |
|---|---|
| **Current branch** | `main` |
| **Remote** | `origin/main` (up to date) |
| **Tags** | `v0.1.0`, `v0.1.0-identity` |
| **Working tree** | Clean — no uncommitted changes |
| **Branches** | Single branch (`main`) — no feature branches |

**Latest commits (most recent first):**
1. `370c2dc` — feat: enhance email verification and resend functionality with organization support and integrate Resend API
2. `6a2b417` — feat: update environment configuration and enhance email notification templates
3. `1d2b54e` — feat: add signup form and email verification components
4. `c246648` — feat: enhance signup process with unique slug generation and error handling for email conflicts
5. `fda23f2` — feat: optimize database event handling and improve session flush timings in AuthService
6. `6aa8d65` — feat: implement create methods in identity and organization repositories; update health check and database session management
7. `f2cc934` — feat(platform): implement Identity v1
8. `9022363` — feat: implement identity management repositories and services
9. `ac23c8a` — feat: update backend workflow and structure; add .dockerignore and initial README

**Unfinished work:** None in progress. Working tree is clean.

---

## 20. Final Assessment

### What kind of software is this today?

A **full-stack prototype** demonstrating DDD/CQRS/Outbox architectural patterns with a working authentication system, organization management, production email integration (Resend), and a functional frontend for auth flows. The backend is a technical foundation with working auth; the frontend provides login/signup/password-reset flows and read-only console pages. No domain-specific functionality exists yet.

### How far is it from an MVP?

A functional MVP would require at minimum:
1. Authorization on all endpoints
2. Frontend console CRUD operations (profile editing, organization management)
3. At least one blueprint implementation (e.g., academy)
4. Working event dispatch
5. Rate limiting
6. Production Docker/deployment setup
7. Server-side route protection for frontend

**Estimated effort:** 3–5 weeks of focused engineering for one senior developer, assuming the architectural decisions are locked. (Reduced from 4–6 weeks due to auth and frontend progress.)

### How far is it from production?

**6–10 weeks** for a small team (2–3 engineers). The gaps are smaller than before: auth middleware is still needed, but email integration and frontend auth flows are done. Remaining gaps: no auth middleware, no event dispatch, no deployment pipeline, no monitoring, no backup strategy, no load testing, no security audit.

### If a senior backend engineer joined tomorrow, what would they need to know first?

1. Read `docs/aps/runtime-spec.md` — this is the architectural constitution
2. Read `docs/frontend/architecture.md` — frontend architecture and API contracts
3. Understand the Ports & Adapters pattern used here — each module has `ports/` (interfaces) and `infrastructure/postgres/` (implementations)
4. Know that the DI container is custom, not a library — resolve via `container.resolve(ServiceClass)`
5. The `auth_service.py` (~730 lines) is the most critical and complex file — read it thoroughly
6. Events go to the outbox but are never dispatched — this is a known gap, not a bug
7. All data flows as `dict[str, Any]` — typed domain objects are designed but not built
8. Tests use in-memory repositories, not a real database
9. Frontend uses Next.js 16 App Router with feature modules — auth is in `features/auth/`
10. Email is wired outside the DI container via manual setter — this is a known shortcut

### Prioritized Next 20 Engineering Tasks

| Priority | Task | Complexity |
|---|---|---|
| 1 | Implement `get_current_user` FastAPI dependency + protect all `/users` and `/organizations` endpoints | High |
| 2 | Fix CORS: explicit origins instead of `*` with credentials | Low |
| 3 | Add server-side route protection for frontend `/console` routes (Next.js middleware) | Medium |
| 4 | Wire `Lifecycle.lifespan()` into FastAPI app for graceful shutdown | Low |
| 5 | Fix container `_resolve_annotation` Union type bug | Low |
| 6 | Wire discovered event handlers to EventBus + implement `OutboxDispatcher._dispatch_batch()` | Medium |
| 7 | Add rate limiting middleware (login, signup, forgot-password) | Medium |
| 8 | Implement refresh token rotation (issue new token on each refresh) | Medium |
| 9 | Add JTI claim to JWT for token-level revocation | Medium |
| 10 | Remove dead code: Capability, Policy, Workflow, SubscriberRegistry, unused commands/schemas | Low |
| 11 | Register `EmailService` in DI container instead of manual setter | Low |
| 12 | Fix `identity/router.py` hardcoded `UUID(int=0)` for org_id | Low |
| 13 | Add composite unique constraints on (membership.user_id, org_id) and (role.name, org_id) | Low |
| 14 | Add database indexes on `sessions.refresh_token_hash` and `email_verification_tokens.token_hash` | Low |
| 15 | Refactor `auth_service.py` into smaller services (signup, login, password-reset) | High |
| 16 | Create typed domain aggregates (Organization, User) extending BusinessObject | High |
| 17 | Add failed-login tracking and account lockout | Medium |
| 18 | Implement real event handlers (welcome email on signup, audit trail on login) | Medium |
| 19 | Replace `.env.example` credentials with placeholders + rotate exposed keys | Low |
| 20 | Add background cleanup jobs for expired sessions and tokens | Medium |
