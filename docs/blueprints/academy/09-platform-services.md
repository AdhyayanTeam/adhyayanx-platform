# 09 — Platform Services

> **Scope:** Platform infrastructure that business capabilities consume.
> This document covers two layers: **Platform Domains** (shared business
> data owned by the platform) and **Platform Services** (reusable technical
> behavior). Many of these will be shared across future ADX blueprints
> (Clinic, Salon, Gym, etc.).
>
> **Rule:** Every document in Sprint 2 must be understandable by a coaching
> institute owner with no software background.

---

## 1. Platform Architecture

The ADX Platform has two distinct layers above blueprints:

```
Platform Domains (own shared business data)
├── Identity
├── Organizations
├── Users
├── Workspaces
├── Reference Data
└── Subscriptions (future)

Platform Services (execute reusable technical behavior)
├── Identity Services: Authentication, Authorization
├── Communication Services: Notifications
├── Content Services: Documents, Media
└── Foundation Services: Scheduling, Workflow & Automation, Search, Audit

══════════════════════════════════════════════════════════════════

Academy Blueprint
├── Business Capabilities (what the business does)
│   ├── Admissions
│   ├── Learner Management
│   ├── Academic Operations
│   ├── Financial Management
│   ├── Communication
│   └── Decision Support
│
└── Consumes Platform Domains and Services
```

**Platform Domains** own persistent business data. They answer "who" and
"what" — who is the organization, what are the branches, who are the users.

**Platform Services** execute logic. They answer "how" — how do we
authenticate, how do we send a notification, how do we detect scheduling
conflicts.

The distinction matters because:
- **Domains** are data ownership boundaries. Academy references Platform
  Domains but never owns them.
- **Services** are behavior providers. They know nothing about coaching
  institutes, learners, or fees. They know about time, identity, and
  delivery.
- Both are **shared** across ADX blueprints. Clinic, Gym, and Salon
  consume the same Platform Domains and Services.

---

## 2. Platform Domains

Platform Domains own shared business data used across all blueprints.

### 2.1 Identity

**What it owns:** Authentication credentials, login sessions, password
management, multi-factor authentication.

**Academy consumes:** Yes. Every user must be identified.

**Already exists in codebase:** Yes — `backend/app/modules/platform/identity/`

### 2.2 Organizations

**What it owns:** Organization profile (name, logo, timezone, locale),
branches, subscription, owner relationship.

**Academy consumes:** Yes. Every academy is an Organization. Branches
are Organization data, not Academy data.

**Already exists in codebase:** Partially.

### 2.3 Users

**What it owns:** User profiles, role assignments, staff directory.

**Academy consumes:** Yes. Owner, Manager, Counsellor, Teacher,
Accountant, Receptionist are all Users within an Organization.

**Already exists in codebase:** Partially.

### 2.4 Workspaces

**What it owns:** Workspace boundaries within an Organization. Each
blueprint runs in its own workspace.

**Academy consumes:** Yes. Academy is a workspace within an Organization.

**Already exists in codebase:** No.

### 2.5 Reference Data

Reference Data provides shared truth across all blueprints. Not
Academy-specific, not Clinic-specific — universally needed.

```
Reference Data

Geography
├── Countries
├── States
├── Cities
└── Timezones

Localization
├── Languages
└── Currencies

Calendars
├── Academic Calendar
├── Business Calendar
├── Fiscal Calendar
└── Holiday Calendar

Classification
├── Categories
├── Tags
├── Status Lists
└── Enumerations

Standards
├── Gender
├── Blood Groups
└── Nationality
```

**Why Calendars, not "Academic Years":** Clinic doesn't have Academic
Years. Gym doesn't. Salon doesn't. But they all have calendars. The
Academy blueprint defines its Academic Calendar on top of platform
calendar primitives.

**Academy consumes:** Yes — Academic Calendar, Holidays, Currencies,
Geography.

**Already exists in codebase:** No.

### 2.6 Subscriptions (Future)

**What it owns:** ADX platform subscription management — which
organization has which plan, billing, limits.

**Academy consumes:** Indirectly. The Organization's subscription
determines which features are available.

**Already exists in codebase:** No.

---

## 3. Platform Services

Platform Services provide reusable technical behavior. They execute
logic. They know nothing about coaching institutes — they know about
time, identity, delivery, and automation.

### 3.1 Identity Services

#### Authentication

**What it does:** Verifies who someone is. Login, logout, session
management, password reset, multi-factor authentication.

**Why it exists:** Every user of the system must be identified.

**Already exists in codebase:** Yes.

#### Authorization

**What it does:** Determines what an authenticated user is allowed to do.
Role-based access control.

**Why it exists:** Different roles have different permissions.

**Already exists in codebase:** Partially.

### 3.2 Communication Services

#### Notifications

**What it does:** Delivers messages to users via the appropriate channel.
The Communication business capability decides **what** gets sent and
**to whom.** The Notification Service decides **how** it gets delivered.

**Why it exists:** Separating policy from delivery means new channels
(voice call, push notification) can be added without changing business
logic. Academy never knows how WhatsApp works.

**Already exists in codebase:** Partially.

### 3.3 Content Services

#### Documents

**What it does:** Generates PDF and other document formats. Handles
templating, numbering, and storage. Used for fee receipts, invoices,
report cards, enrollment forms.

**Already exists in codebase:** No.

#### Media

**What it does:** Stores and serves files — images, videos, study
material. Handles upload, download, thumbnails, access control.

**Already exists in codebase:** No.

### 3.4 Foundation Services

#### Scheduling

**What it does:** Manages time slots, availability, conflict detection,
and recurrence. Answers: "Is this teacher free at 10 AM on Monday?"
"Are there scheduling conflicts for this batch?"

**Why it exists:** Many capabilities need scheduling — Admissions
(batch creation), Academics (timetable, attendance, exams), Learners
(batch transfer). It is cross-cutting, not business-specific.

**Already exists in codebase:** No.

#### Workflow & Automation

**What it does:** Orchestrates approvals, timers, reminders, escalations,
retries, waiting, and automation. Answers: "What happens when a fee is
overdue for 15 days?" "Who approves a batch transfer?" "Send a reminder
every Monday at 9 AM."

**Why it exists:** Every blueprint will need workflow and automation.
Clinic needs appointment reminders. Gym needs class notifications.
Academy needs fee escalation chains. This is platform infrastructure,
not Academy-specific.

**Already exists in codebase:** No.

#### Search

**What it does:** Provides fast, full-text search across data. Answers:
"Find all leads from last month's exhibition." "Find all learners with
overdue fees."

**Already exists in codebase:** Partially.

#### Audit

**What it does:** Records who did what and when. Tracks changes to
important data — fee modifications, enrollment changes, grade updates.
Provides an audit trail for accountability.

**Already exists in codebase:** No.

---

## 4. Platform Capabilities Summary

### Platform Domains

| Domain | What it owns | Academy consumes? | Exists today? |
|---|---|---|---|
| **Identity** | Authentication credentials, sessions | Yes | Yes |
| **Organizations** | Organization profile, branches, owner | Yes | Partially |
| **Users** | User profiles, role assignments, staff | Yes | Partially |
| **Workspaces** | Workspace boundaries per blueprint | Yes | No |
| **Reference Data** | Geography, Calendars, Classifications, Standards | Yes | No |
| **Subscriptions** | Platform subscription management | Indirectly | No |

### Platform Services

| Category | Service | What it provides | Exists today? |
|---|---|---|---|
| **Identity** | Authentication | Who is this user? | Yes |
| **Identity** | Authorization | What can they do? | Partially |
| **Communication** | Notifications | Deliver messages via channels | Partially |
| **Content** | Documents | Generate PDFs, receipts, reports | No |
| **Content** | Media | Store and serve files | No |
| **Foundation** | Scheduling | Time slots, availability, conflicts | No |
| **Foundation** | Workflow & Automation | Approvals, timers, escalations, automation | No |
| **Foundation** | Search | Fast full-text search | Partially |
| **Foundation** | Audit | Change tracking, accountability | No |

---

## 5. Open Questions

1. Should **Scheduling** support recurring events (weekly timetable) or
   only one-time slots? Most institute batches follow a weekly recurring
   pattern.
2. Should **Notifications** support WhatsApp Business API from day one,
   or start with SMS + in-app and add WhatsApp later?
3. Should **Documents** generate GST-compliant invoices, or is that a
   Finance module concern?
4. Should **Audit** track every data change, or only changes to critical
   data (fees, grades, enrollment status)?
5. Should **Workflow & Automation** be built as a rule engine, or as
   hardcoded business logic per blueprint?
6. Are there other platform capabilities we are missing? For example:
   - **Payment Gateway** integration (UPI, card processing)
   - **Calendar** integration (Google Calendar, Outlook)
   - **WhatsApp** as a first-class platform service (not just a notification
     channel)

---

*Sprint 2 — Platform Domains & Services*
