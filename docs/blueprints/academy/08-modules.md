# 08 — Modules

> **Scope:** How the software groups business responsibilities. Each module
> owns one capability's responsibilities. Modules are not features — they
> are the software boundaries that align with business ownership.
>
> **Rule:** Every document in Sprint 2 must be understandable by a coaching
> institute owner with no software background.

---

## 1. From Capabilities to Modules

The previous document (`07-responsibilities.md`) defined what each
capability owns. This document defines how the software groups those
responsibilities.

The mapping is simple: **one capability → one module.**

This is not a coincidence. It is deliberate. When the software boundaries
match the business boundaries, the system is easier to understand,
easier to change, and harder to break.

---

## 2. The Module Map

```
┌─────────────────────────────────────────────────────────────┐
│                      ACADEMY SOFTWARE                        │
│                                                              │
│  ┌──────────┐  ┌───────────┐  ┌────────────────────┐        │
│  │Admissions│  │  Learners │  │    Academics       │        │
│  └──────────┘  └───────────┘  └────────────────────┘        │
│                                                              │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────┐       │
│  │     Finance      │  │Communication │  │Decision  │       │
│  │                  │  │              │  │ Support  │       │
│  └──────────────────┘  └──────────────┘  └──────────┘       │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │              Platform Services                      │     │
│  │  (Scheduling, Identity, Notifications, Documents,  │     │
│  │   Media, Search, Audit)                             │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Module Descriptions

### 3.1 Admissions Module

**Responsibility:** The prospect-to-enrollment journey.

**Owns:**
- Lead capture, qualification, routing, follow-up
- Counselling and demo scheduling
- Nurture pipeline for dormant leads
- Offering selection and seat reservation
- Enrollment processing (documents, fee challan)

**Does NOT own:**
- Learner profile (once enrolled, Learners module owns it)
- Fees (Finance module owns all financial matters)
- Curriculum (Academics module owns this)
- Batch confirmation or assignment (Academics module owns this)

**Software boundary:** Everything from "inquiry enters the system" to
"learner is enrolled and seat is reserved." Batch confirmation crosses
into the Academics module.

---

### 3.2 Learners Module

**Responsibility:** The learner lifecycle after admission.

**Owns:**
- Learner profile (personal details, guardian, contact)
- Lifecycle states (Active, At Risk, Renewed, Dropped, Suspended)
- At-risk detection and intervention triggers
- Renewals and re-enrollment
- Exits and withdrawal processing
- Referral tracking

**Does NOT own:**
- Lead pipeline (Admissions module owns this)
- Fees or payments (Finance module owns this)
- Curriculum or teaching (Academics module owns this)
- Communication policies (Communication module owns this)

**Software boundary:** Everything about the learner's relationship with
the academy after enrollment. The learner record is the central concept
here — other modules reference it but do not own it.

---

### 3.3 Academics Module

**Responsibility:** Delivering the educational product.

**Owns:**
- Batch placement, confirmation, and transfer
- Batch capacity management
- Curriculum structure (Subject/Module/Level/Paper — configurable)
- Attendance (recording, absence detection, chronic absence)
- Tests, evaluations, marks
- Performance tracking and trends
- Study material distribution
- Syllabus progress tracking

**Does NOT own:**
- Learner profile (Learners module owns this)
- Fees or money (Finance module owns this)
- Lead pipeline (Admissions module owns this)
- Offering selection (Admissions module owns this)
- Communication policies (Communication module owns this)

**Software boundary:** Everything related to teaching and learning —
from batch placement through curriculum delivery. The batch is the
scheduling context; the curriculum is the content structure. Both live
here.

**Open question:** This module may naturally divide into two sub-modules
in Sprint 3:
- **Academic Planning** — Curriculum, Batches, Timetable
- **Academic Delivery** — Attendance, Teaching, Assessments, Results

Validate in Sprint 3.

---

### 3.4 Finance Module

**Responsibility:** The financial relationship between institute and family.

**Owns:**
- Fee structures (plans, installments, due dates)
- Scholarships and discounts
- Payment collection and receipts
- Outstanding tracking and escalation
- Refunds
- Revenue reporting and collection summaries
- GST compliance

**Does NOT own:**
- Learner profile (Learners module owns this)
- Curriculum or teaching (Academics module owns this)
- Lead pipeline (Admissions module owns this)
- Attendance or assessments (Academics module owns this)
- Communication policies (Communication module owns this)

**Software boundary:** Everything related to money. When a fee is
overdue, Finance sends a signal to Communication for reminders. When
a refund is processed, Finance notifies Learners of status change.
Finance owns the financial truth.

---

### 3.5 Communication Module

**Responsibility:** Institutional communication policy and trigger logic.

**Owns:**
- Communication policies (what triggers what message to whom)
- Trigger logic (event → policy → trigger)
- Audience rules and segmentation
- Escalation routing logic
- Opt-out management

**Does NOT own:**
- Channel delivery infrastructure (Platform Notification Service owns this)
- The actual data being communicated (other modules own their data)
- Learner profile (Learners module owns this)
- Fees or money (Finance module owns this)
- Curriculum or teaching (Academics module owns this)
- Lead pipeline (Admissions module owns this)

**Software boundary:** Communication defines policies and triggers
notifications. The Platform Notification Service handles delivery
(WhatsApp, SMS, email, in-app). Academy never knows how WhatsApp works.

---

### 3.6 Decision Support Module

**Responsibility:** Decision-ready information for every stakeholder.

**Owns:**
- Metrics definitions (what to measure)
- Dashboards and summaries
- Trend analysis and comparisons
- Export functionality (Excel, PDF)

**Does NOT own:**
- Any write operations (Decision Support is a Read Model)
- Any business behavior (Decision Support does not make decisions)
- Any learner data (it reads from Learners)
- Any financial data (it reads from Finance)

**Software boundary:** Decision Support reads from all modules. It does not
write to any. It assembles the picture. It does not generate the data.

---

## 4. Module Dependencies

Dependencies are fine. Duplicate ownership is not.

```
Admissions ──────► Learners        (enrollment hands off to learner record)
Admissions ──────► Academics       (seat reservation requires batch confirmation)
Learners ────────► Finance         (checks fee status for at-risk detection)
Learners ────────► Academics       (checks attendance for at-risk detection)
Academics ───────► Communication   (triggers test results, absence alerts)
Finance ─────────► Communication   (triggers fee reminders)
Communication ───► Platform Notification Service (delivers via channels)
Decision Support ── (reads from all modules — no outbound dependencies)
```

---

## 5. Open Questions

1. **Fee plan creation:** Currently in Finance. Should it be in Admissions
   (since it happens at enrollment time)?
2. **Referral tracking:** Currently in Learners. Should it be in Admissions
   (since referrals generate leads)?
3. **Should Decision Support be a module at all?** It is a Read Model with
   no write operations. It could be a cross-cutting layer instead of a
   module. The current decision is to include it as a module for simplicity.

---

*Sprint 2 — Modules*
