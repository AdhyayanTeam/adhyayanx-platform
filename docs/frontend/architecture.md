# ADX Platform - Frontend Architecture

## Stack
- Next.js 16 (App Router, TypeScript)
- Tailwind CSS v4 + shadcn/ui (base-nova style)
- React Hook Form + Zod validation
- Plain fetch() via `api()` / `apiAuth()` wrappers
- React Context (AuthProvider) for auth state only

## Folder Structure
```
frontend/src/
├── app/
│   ├── layout.tsx              # Root layout (fonts, Providers)
│   ├── providers.tsx           # AuthProvider wrapper
│   ├── page.tsx                # Redirects to /login
│   ├── globals.css             # Tailwind + shadcn theme
│   ├── (public)/               # Guest-only pages
│   │   ├── layout.tsx          # Passthrough (AuthProvider at root)
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   ├── reset-password/page.tsx
│   │   ├── verify-email/page.tsx
│   │   ├── loading.tsx
│   │   └── error.tsx
│   └── (console)/              # Protected pages
│       ├── layout.tsx          # Auth guard + sidebar
│       ├── loading.tsx
│       ├── error.tsx
│       └── console/
│           ├── page.tsx        # Home
│           ├── profile/page.tsx
│           ├── organization/page.tsx
│           └── settings/page.tsx
├── features/
│   └── auth/
│       ├── types.ts            # User, Organization, API response types
│       ├── schemas.ts          # Zod schemas + form data types
│       ├── api.ts              # authApi object (login, signup, logout, etc.)
│       ├── auth-context.tsx    # AuthProvider + useAuth hook
│       ├── index.ts            # Barrel export
│       └── ui/
│           ├── login-form.tsx
│           ├── signup-form.tsx
│           ├── forgot-password-form.tsx
│           ├── reset-password-form.tsx
│           ├── verify-email-client.tsx
│           └── console-sidebar.tsx
├── shared/
│   ├── lib/
│   │   ├── utils.ts            # cn() helper
│   │   └── api-client.ts       # api(), apiAuth(), apiAuthRetry()
│   ├── types/
│   │   └── api.ts              # ApiError, ApiResult, extractError, errorMessage
│   └── ui/                     # shadcn components (generated + manual)
│       ├── button.tsx, input.tsx, label.tsx, card.tsx, etc.
│       └── loading-spinner.tsx
└── middleware.ts                # UX-only: guest redirect if refresh_token exists
```

## Auth Flow
1. **Login**: POST `/api/v1/auth/login` → access_token in memory + refresh_token in HttpOnly cookie
2. **Signup**: POST `/api/v1/auth/signup` → shows "check email" message
3. **Verify email**: POST `/api/v1/auth/verify-email` with token from URL query
4. **Session restore**: On mount, AuthProvider calls POST `/api/v1/auth/refresh` (reads cookie), then GET `/api/v1/auth/me` with the new access_token
5. **401 retry**: `apiAuthRetry()` calls `retryCallback` (which calls `silentRefresh()`), then retries the original request
6. **Logout**: POST `/api/v1/auth/logout` → clears cookie, resets state

## API Client
- `api<T>(path, init?)` — public, no auth header
- `apiAuth<T>(path, token, init?)` — adds `Authorization: Bearer {token}`
- `apiAuthRetry<T>(path, token, retryCallback, init?)` — retries on 401 after refresh
- All return `ApiResult<T>` = `{ data: T; error: null } | { data: null; error: ApiError }`
- Base URL from `NEXT_PUBLIC_API_URL` env var (defaults to `http://localhost:8000`)

## Middleware (UX-only)
- Checks `refresh_token` cookie on `/login` and `/signup`
- If cookie exists → redirects to `/console`
- NOT a security layer — AuthProvider verifies on mount via `/me`

## Backend API Contracts
- `POST /api/v1/auth/signup` — `{ organization_name, blueprint_code, owner_name, email, password }`
- `POST /api/v1/auth/login` — `{ email, password }` → `{ access_token, user, organization, landing_url }`
- `POST /api/v1/auth/refresh` — reads `refresh_token` cookie → `{ access_token }`
- `POST /api/v1/auth/logout` — clears cookie, 204
- `POST /api/v1/auth/verify-email` — `{ token }`
- `POST /api/v1/auth/forgot-password` — `{ email }`
- `POST /api/v1/auth/reset-password` — `{ token, new_password }`
- `GET /api/v1/auth/me` — requires `Authorization: Bearer` → `{ user, organization, subscriptions, roles }`
- Error shapes: `{ error: { code, message } }` (error_handler) or `{ detail: string }` (HTTPException)

## Email Templates (Backend)
- `backend/app/modules/platform/notifications/emails/verify_email.py` — renders HTML for verification
- `backend/app/modules/platform/notifications/emails/reset_password.py` — renders HTML for password reset
- `resend_provider.py` — maps template names to render functions, sends via Resend API

## Environment Variables (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Build Verification
- `npm run lint` — 0 errors, 0 warnings
- `npm run build` — compiles and generates all pages
- `npx tsc --noEmit` — no type errors
