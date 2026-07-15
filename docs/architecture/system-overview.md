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

ADX provides the common capabilities that every business application
needs — identity, organizations, permissions, notifications, automation,
and events. Business solutions such as Academy, Clinic, and Salon build
on those capabilities instead of reimplementing them.

```
                        ADX

                  Shared Platform
      Identity • Organizations • Events
      Permissions • Notifications • Files

            │                │
            │                │
     ┌──────┴──────┬─────────┴─────────┐
     │             │                   │

 Academy      Clinic (future)    Salon (future)

     │             │                   │

 academy.     clinic.            salon.
 adhyayanx.in adhyayanx.in       adhyayanx.in
```

---

## Frontends

Each subdomain serves a specific purpose:

```
adhyayanx.in              Marketing website
app.adhyayanx.in          Platform home (signup, login, profile, settings)
academy.adhyayanx.in      Academy solution
clinic.adhyayanx.in       Clinic solution (future)
console.adhyayanx.in      Internal operations
```

**adhyayanx.in** — The public face. Explains what ADX is. Drives signups.

**app.adhyayanx.in** — The user's platform home. Signup, login,
email verification, password reset, profile, organization switcher,
and personal settings. After login, the user is redirected
to the appropriate solution.

**academy.adhyayanx.in** — The Academy solution. Student management,
attendance, fees, exams, communication. This is what institute owners
and staff use daily.

**clinic.adhyayanx.in** — The Clinic solution. Future solution.
Same platform, different business logic.

**console.adhyayanx.in** — Internal operations. Platform administrators
manage organizations, users, and subscriptions. Customers never use
the console. It exists only for ADX employees to operate the platform.

---

## Who uses what?

| User               | Uses                                          |
| ------------------ | --------------------------------------------- |
| Visitor            | `adhyayanx.in`                                |
| Organization owner | `app.adhyayanx.in` → redirected to solution   |
| Staff              | Solution (`academy`, `clinic`, etc.)          |
| ADX employee       | `console.adhyayanx.in`                        |

---

## Backend

All frontends communicate with the same shared platform backend.
The backend exposes platform capabilities through APIs. Each frontend
uses only the capabilities it needs, while business-specific features
are implemented by the corresponding solution.

```
adhyayanx.in  ─┐
               │
app.adhyayanx.in  ─┤
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
Identity portal (app.adhyayanx.in)
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

- Users authenticate through a shared identity system. After
  authentication, they are redirected only to the solutions they are
  authorized to access.
- One notification system serves all customers
- One permission model secures everything
- One event system connects all modules
- One billing system manages all subscriptions

Building this once is hard. Building it five times is impossible.

---

## Solutions

A solution is a business application built on the ADX platform.

```
Platform (shared)
├── Identity
├── Organizations
├── Permissions
├── Notifications
├── Events
│
├── Academy Solution
│   ├── Students
│   ├── Attendance
│   ├── Fees
│   ├── Exams
│   └── Communication
│
├── Clinic Solution (future)
│   ├── Patients
│   ├── Appointments
│   ├── Prescriptions
│   └── Billing
│
└── Salon Solution (future)
    ├── Clients
    ├── Bookings
    ├── Services
    └── Payments
```

Each solution defines its own domain model. The platform provides
the foundation. New solutions can be added without changing the platform.

---

## What this document is not

This document explains the structure of the ADX platform.

It does not describe:

- Database schema
- Deployment infrastructure
- API endpoints
- Internal implementation details

Those are covered by the architecture and runtime documentation.

---

## Design Philosophy

ADX helps businesses make better operational decisions by organizing
the information they already have.

Every blueprint follows this philosophy.

The software does not replace professional judgment.
It provides the right information, in the right context,
at the right time.

Whether the user is admitting a student,
treating a patient,
collecting a payment,
or reviewing the day's operations,
the goal is always the same:

Help people understand what is happening,
why it matters,
and what they should do next.

Good software is measured not by how many features it has,
but by how confidently people can make decisions using it.

---

## Further reading

- [Engineering Principles](principles.md) — How we make decisions
- [System Architecture](../architecture-l1.md) — Detailed backend structure
- [Runtime Specification](../aps/runtime-spec.md) — Transaction and event semantics
- [Academy Blueprint](../blueprints/academy/) — Domain model for Academy
