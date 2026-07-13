# 05 — Business Capabilities

> **Scope:** What the academy business must be able to do. Not how it does
> it, not what software supports it — just the capabilities the business
> possesses.
>
> **Rule:** Every document in Sprint 2 must be understandable by a coaching
> institute owner with no software background. If it requires knowledge of
> DDD, software architecture, or programming to understand, it is too
> technical and should be simplified.
>
> **Note:** These are derived from the Sprint 1 operating model
> (`01-business-overview.md`). Each capability traces to one or more
> workflows (`04-business-workflows.md`).
>
> **Platform assumption:** These capabilities assume the existence of
> Platform Domains (Identity, Organizations, Users, Workspaces, Reference
> Data) that already exist above every blueprint. Organization management
> (branches, branding, users, roles, academic year configuration, etc.)
> belongs to the ADX Platform and is intentionally outside the Academy
> blueprint. Academy references Platform domains — it does not own them.

---

## 1. The Capability Map

```
┌─────────────────────────────────────────────────────────────┐
│                     ACADEMY BUSINESS                         │
│                                                              │
│  ┌──────────┐  ┌───────────┐  ┌────────────────────┐        │
│  │Admissions│  │ Learner   │  │   Academic          │        │
│  │          │  │Management │  │   Operations        │        │
│  └──────────┘  └───────────┘  └────────────────────┘        │
│                                                              │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────┐       │
│  │    Financial     │  │Communication │  │ Decision Support │       │
│  │    Management    │  │              │  │          │       │
│  └──────────────────┘  └──────────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

6 capabilities. Each is a thing the business would say it possesses.
Each has a business outcome that justifies its existence.

---

## 2. Admissions

**Business Outcome:** Convert prospects into students.

**What it is:** The journey from first inquiry to enrollment creation.
Includes lead generation, follow-up, counselling, demo, offering
selection, seat reservation, and enrollment processing. This is the
revenue engine — without a steady flow of new students, the business
dies.

**Why it exists:**
- Coaching institutes have natural attrition (students leave after exams,
  or drop out). They must constantly replace them.
- The first 24-48 hours after a lead enters are critical — speed of
  follow-up is the #1 predictor of conversion.
- Conversion is non-linear. Leads go dormant. They come back. The system
  must handle this as a normal state, not an edge case.

**Business pressure:** Conversion rate (8-12% is typical). Every percentage
point improvement directly impacts revenue. Cost per acquisition (CAC) by
channel determines where the institute invests its marketing budget.

**Sprint 1 workflows:** Workflow 1 (Lead Generation & Attribution),
Workflow 2 (Convert — Lead to Enrolled Student), Workflow 4
(Batch Allocation & Transfer — the enrollment and reservation portion)

**Note:** Admissions owns offering selection, seat reservation, and
enrollment creation. Batch confirmation and assignment are academic
decisions — see Academic Operations.

---

## 3. Learner Management

**Business Outcome:** Maintain the learner lifecycle.

**What it is:** The relationship with the learner after admission. Includes
the learner profile, lifecycle state transitions (Active, At Risk, Renewed,
Dropped, Suspended, etc.), re-enrollment, transfers, and exits. This is
not CRUD over a student table — it is managing the ongoing relationship
between the learner and the academy.

**Why it exists:**
- The learner is the central entity that every capability interacts with.
- Lifecycle states drive business decisions: at-risk learners need
  intervention, renewed learners generate revenue, dropped learners
  need exit surveys.
- The same human changes business identity over time:
  Lead → Prospect → Applicant → Learner.

**Business pressure:** Retention rate. "Are learners staying, or are they
leaking out? Where in the lifecycle are we losing them?"

**Sprint 1 workflows:** Workflow 9 (Student Lifecycle — Lead to Exit),
cross-cutting interactions with all workflows

---

## 4. Academic Operations

**Business Outcome:** Deliver learning.

**What it is:** Everything related to the educational product itself.
Includes batch placement, attendance, curriculum structure, teaching
delivery, tests, evaluation, performance tracking, and study material.
This is the actual product — everything else is a support capability.

**Why it exists:**
- The learner came to learn, get better scores, and achieve an outcome.
  This is what they pay for.
- Teacher quality is the #1 differentiator, but from a systems perspective
  the pressure is on visibility — can the owner see how learners are
  performing? Can parents see their child's progress?
- The curriculum hierarchy is configurable (Subject, Module, Level, Paper
  vary by institute type). See `research/curriculum-hierarchy.md`.
- Batch placement is an academic decision — it depends on capacity,
  teacher availability, learner level, and schedule compatibility.
  Admissions reserves the seat; Academics confirms the placement.

**Business pressure:** Learner outcomes (scores, rank improvement). Parent
visibility into their child's progress. Teacher effectiveness.

**Sprint 1 workflows:** Workflow 5 (Daily Attendance), Workflow 6
(Test → Result → Communication — the academic portion), Workflow 4
(Batch Allocation — the placement and capacity portion)

**Open question:** Academic Operations may naturally divide into two
sub-domains in Sprint 3:
- **Academic Planning** — Curriculum, Batches, Timetable
- **Academic Delivery** — Attendance, Teaching, Assessments, Results

If an Academic Head were hired, these would likely be two separate teams.
Do not split now. Validate in Sprint 3.

**Other open questions:**
- Can a Session exist without a Batch? (Scenario 2: 1-on-1 coaching)
- Should the Test workflow be optional? (Scenario 6: skill-based learning
  with no formal exams)

---

## 5. Financial Management

**Business Outcome:** Collect revenue accurately.

**What it is:** The financial relationship between the institute and the
learner family. Not merely transactions — this includes fee structures,
scholarships, discounts, payment plans, liabilities, waivers, refunds,
and compliance. Poor financial management kills institutes faster than
poor teaching.

**Why it exists:**
- Fee collection is not "payments." It is a relationship. The person
  collecting fees is often the same person who counselled the learner.
  Pushing too hard on payment damages the relationship. Being too soft
  damages cash flow.
- Different institutes have different fee models: installment-based,
  subscription-based, upfront, or hybrid.
- GST compliance requires accurate, auto-numbered receipts.

**Business pressure:** Collection efficiency. Cash flow. Outstanding
recovery. "Are we collecting what we're owed, on time?"

**Sprint 1 workflows:** Workflow 3 (Fee Collection — full lifecycle),
the fee portions of Workflow 2 (Enrollment Processing)

**Open questions:**
- Should Fee Plan support both installment-based and subscription-based
  models? (Scenario 3: monthly subscription pricing)
- How do scholarships and discounts interact? Are they cumulative?

---

## 6. Communication

**Business Outcome:** Maintain trust with parents and students.

**What it is:** The trust mechanism between the institute and the
family. Includes communication policies, trigger logic, audience rules,
and opt-out management. In Indian educational services, the parent is
the customer — they need constant reassurance that their child is
attending, performing, and being cared for.

**Why it exists:**
- Too much communication → parents ignore it. Too little → parents
  feel neglected.
- The policy model is: Business Event → Policy → Trigger. This decouples
  the business decision from the delivery mechanism. The Platform
  Notification Service handles channel delivery (WhatsApp, SMS, email,
  in-app) — Academy never knows how WhatsApp works.

**Business pressure:** Parent satisfaction. Retention. "Are parents
hearing from us enough? Are we reaching them on the right channel?"

**Sprint 1 workflows:** Workflow 7 (Communication Lifecycle), the
communication portions of Workflows 5, 6, and 9

**Note:** This is a business capability, not a "notifications" feature.
Communication owns policies and triggers. Channel delivery belongs to
the Platform Notification Service.

---

## 7. Decision Support

**Business Outcome:** Drive decisions with data.

**What it is:** The metrics, dashboards, and decision-ready information
that every stakeholder needs. Owner sees revenue and enrollment trends.
Manager sees daily operations. Teacher sees learner performance. Parent
sees their child's progress. Counsellor sees their conversion pipeline.

**Why it exists:**
- Most institute owners make decisions based on gut feel. Metrics exist
  but are rarely used well. The challenge is presenting data in a way
  that actually drives action.
- This is not "Reports." Reports are outputs. Metrics are what the
  business needs.

**Business pressure:** Decision quality. "Are we making decisions based
on data, or based on gut feel?"

**Sprint 1 workflows:** Workflow 8 (Measure — Insights & Metrics),
cross-cutting reads from all workflows

**Note:** At this stage, Decision Support is a **Read Model** — it
consumes data from other capabilities but does not own business behavior.
It does not have its own write operations. If analytics pipelines, metric
definitions, or scheduled reports emerge later, it may grow into a bounded
context. Today it does not.

---

## 8. Traceability to Sprint 1

| Sprint 1 Workflow | Capability(s) |
|---|---|
| Workflow 1: Lead Generation & Attribution | Admissions |
| Workflow 2: Convert (Lead → Enrolled Student) | Admissions, Learner Management |
| Workflow 3: Fee Collection | Financial Management |
| Workflow 4: Batch Allocation & Transfer | Admissions (reservation), Academic Operations (placement) |
| Workflow 5: Daily Attendance | Academic Operations |
| Workflow 6: Test → Result → Communication | Academic Operations, Communication |
| Workflow 7: Communication Lifecycle | Communication |
| Workflow 8: Measure (Decision Support & Metrics) | Decision Support |
| Workflow 9: Student Lifecycle | Learner Management, Communication |

Every Sprint 1 workflow maps to at least one capability. No capability
exists without a Sprint 1 workflow to justify it.

---

## 9. What These Capabilities Are NOT

- **Not modules.** Modules are a software grouping (see `08-modules.md`).
  Capabilities are a business grouping.
- **Not features.** A capability is not "Attendance Tracking" — it is
  "Academic Operations." Attendance is a use case within it (see
  `06-use-cases.md`).
- **Not bounded contexts.** That is a software architecture concept
  (see `10-context-discovery.md`).
- **Not workflow steps.** "Lead Capture" is a step in a workflow, not
  a capability. "Admissions" is the capability that contains that step.

---

## 10. Open Questions

1. Is **Settings** a capability? The operating model assumes institute-wide
   configuration (fee policies, attendance rules, communication preferences)
   exists. Should it be a 7th capability, or is it an infrastructure concern?
2. Is **Grow** (Renewals & Referrals) a separate capability or part of
   Admissions? The Sprint 1 operating model has Grow as a separate verb,
   but in practice renewals may be a use case within Learner Management
   or Admissions.
3. Does **Learner Management** own transfers (batch transfers, course
   changes), or does Admissions own them? A batch transfer is both an
   admissions decision (which batch?) and a learner lifecycle event.
4. Is **Curriculum Management** part of Academic Operations, or is it
   a cross-cutting concern that multiple capabilities need?

---

*Sprint 2 — Business Capabilities*
