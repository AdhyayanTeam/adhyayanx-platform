# ADX System Overview

> **ADX is a business platform.**
>
> It provides common capabilities — identity, organizations, permissions,
> notifications, events — and business solutions like Academy are built
> on top of the same platform.

---

## What are we building?

ADX is not a single application. It is a platform that powers multiple
business solutions. Each solution serves a different type of customer,
but they all share the same backend.

Think of it like Shopify.

Shopify provides shared capabilities — merchant identity, product catalog,
payments, notifications. Individual stores are built on top of those
capabilities. Shopify does not rebuild checkout for every store.

ADX does the same thing for educational institutes, clinics, salons,
and gyms.

---

## Frontends

Each subdomain serves a specific purpose:

```
adhyayanx.in              Marketing website
login.adhyayanx.in        Identity portal (signup, login, verify)
academy.adhyayanx.in      Academy solution
clinic.adhyayanx.in       Clinic solution (future)
console.adhyayanx.in      Internal operations
```

**adhyayanx.in** — The public face. Explains what ADX is. Drives signups.

**login.adhyayanx.in** — Where users authenticate. Signup, login,
email verification, password reset. After login, the user is redirected
to the appropriate solution.

**academy.adhyayanx.in** — The Academy solution. Student management,
attendance, fees, exams, communication. This is what institute owners
and staff use daily.

**clinic.adhyayanx.in** — The Clinic solution. Future blueprint.
Same platform, different business logic.

**console.adhyayanx.in** — Internal operations. Platform administrators
manage organizations, users, and subscriptions. Not customer-facing.

---

## Backend

All frontends communicate with the same shared platform backend.

```
adhyayanx.in  ─┐
               │
login.adhyayanx.in  ─┤
               │
academy.adhyayanx.in ─┤──── Platform Backend
               │
clinic.adhyayanx.in  ─┤
               │
console.adhyayanx.in ─┘
```

The backend provides these platform capabilities:

```
Identity          Who users are, how they authenticate
Organizations     Tenants, their settings, their subscriptions
Permissions       What users can do within an organization
Notifications     Email, SMS, push notifications
Automation        Workflows triggered by business events
Events            Domain events that connect modules
Files             Document and media storage
```

Business solutions like Academy build on top of these capabilities.
They add their own domain logic — students, attendance, fees, exams —
but they do not rebuild identity, permissions, or notifications.

---

## Business Flow

```
Marketing site (adhyayanx.in)
    │
    ▼
User signs up
    │
    ▼
Identity portal (login.adhyayanx.in)
    │
    ├── Organization created
    ├── Owner account created
    ├── Email verification sent
    │
    ▼
User verifies email, logs in
    │
    ▼
Redirected to solution (academy.adhyayanx.in)
    │
    ▼
Daily use: students, attendance, fees, exams
    │
    ▼
Business events fire automatically
    │
    ▼
Platform services handle: notifications, automation, reporting
```

Every step in this flow is powered by the same backend. The marketing
site, identity portal, and Academy solution are different frontends
talking to one platform.

---

## Why a shared platform?

Why not build a separate backend for Academy, another for Clinic,
another for Salon?

Because the hard problems are the same across all of them:

```
Identity          Every solution needs user accounts
Organizations     Every solution has tenants
Permissions       Every solution controls access
Notifications     Every solution sends emails
Automation        Every solution has workflows
Billing           Every solution manages subscriptions
```

Only the business logic differs.

Academy has students and attendance.
Clinic has patients and appointments.
Salon has clients and bookings.

The platform handles everything else. This means:

- One login works across all solutions
- One notification system serves all customers
- One permission model secures everything
- One event system connects all modules
- One billing system manages all subscriptions

Building this once is hard. Building it five times is impossible.

---

## The blueprint model

A blueprint is a business solution built on the ADX platform.

```
Platform (shared)
├── Identity
├── Organizations
├── Permissions
├── Notifications
├── Events
│
├── Academy Blueprint
│   ├── Students
│   ├── Attendance
│   ├── Fees
│   ├── Exams
│   └── Communication
│
├── Clinic Blueprint (future)
│   ├── Patients
│   ├── Appointments
│   ├── Prescriptions
│   └── Billing
│
└── Salon Blueprint (future)
    ├── Clients
    ├── Bookings
    ├── Services
    └── Payments
```

Each blueprint defines its own domain model. The platform provides
the foundation. New blueprints can be added without changing the platform.

---

## Further reading

- [Engineering Principles](principles.md) — How we make decisions
- [System Architecture](../architecture-l1.md) — Detailed backend structure
- [Runtime Specification](../aps/runtime-spec.md) — Transaction and event semantics
- [Academy Blueprint](../blueprints/academy/) — Domain model for Academy
