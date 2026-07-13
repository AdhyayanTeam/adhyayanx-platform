# 07 — Responsibilities

> **Scope:** What each capability owns and what it never owns. This prevents
> messy boundaries later — capabilities that own too much become dumping
> grounds, and capabilities that own too little become hollow wrappers.
>
> **Rule:** Every document in Sprint 2 must be understandable by a coaching
> institute owner with no software background.

---

## 1. Why This Matters

When capabilities have unclear boundaries, two things go wrong:

1. **Duplicate ownership.** Two capabilities both think they own the same
   thing. Fees get managed in both Admissions and Finance. The learner
   profile gets updated in both Learner Management and Academic Operations.
   Nobody knows which one is the source of truth.

2. ** Responsibility gaps.** Nobody owns something. The fee plan gets
   created but nobody is responsible for tracking whether installments
   are paid. The learner is at risk but nobody is responsible for
   intervening.

Clear responsibilities prevent both problems.

---

## 2. Responsibility Matrix

### 2.1 Admissions

**Primary Responsibility:** The prospect-to-enrollment journey.

| Owns | Never Owns |
|---|---|
| Lead lifecycle (capture, qualify, route, follow up) | Learner profile (once enrolled, Learner Management owns it) |
| Counselling and demo | Money (Finance owns all financial matters) |
| Conversion decisions (nurture, enroll, archive) | Curriculum or syllabus (Academic Operations owns these) |
| Offering selection and seat reservation | Batch confirmation or assignment (Academic Operations owns these) |
| Enrollment processing (documents, fee challan) | Communication policies (Communication owns these) |

**Handoff point:** When a lead converts, Admissions creates the enrollment
and reserves a seat. Academic Operations confirms the batch placement.
Admissions retains the lead history (source, counsellor, conversion path)
for attribution and analytics.

---

### 2.2 Learner Management

**Primary Responsibility:** The learner lifecycle after admission.

| Owns | Never Owns |
|---|---|
| Learner profile (personal details, guardian, contact) | Leads (Admissions owns the lead lifecycle) |
| Lifecycle states (Active, At Risk, Renewed, Dropped, Suspended) | Fees or payments (Finance owns all financial matters) |
| At-risk detection and intervention triggers | Curriculum or teaching (Academic Operations owns these) |
| Renewals and re-enrollment | Communication policies (Communication owns these) |
| Exits and withdrawal processing | Marketing attribution (Admissions owns this) |
| Referral tracking (who referred whom) | |

**Handoff point:** When a learner is at risk due to attendance, Learner
Management triggers Academic Operations to provide attendance data. When
at risk due to fees, Learner Management triggers Finance to provide
outstanding data. Learner Management orchestrates — it does not own the
underlying data.

---

### 2.3 Academic Operations

**Primary Responsibility:** Delivering the educational product.

| Owns | Never Owns |
|---|---|
| Batch placement, confirmation, and transfer | Learner profile or lifecycle (Learner Management owns this) |
| Batch capacity management | Fees or money (Finance owns this) |
| Curriculum structure (Subject/Module/Level/Paper) | Lead pipeline or conversion (Admissions owns this) |
| Attendance (recording, absence detection, chronic absence) | Offering selection (Admissions owns this) |
| Tests, evaluations, marks | Communication policies (Communication owns this) |
| Performance tracking and trends | |
| Study material distribution | |
| Syllabus progress tracking | |

**Handoff point:** When Academic Operations detects chronic absence, it
sends a signal to Learner Management to trigger intervention. When test
results are ready, Academic Operations hands them to Communication for
parent delivery. Academic Operations does not decide what gets communicated
— Communication does.

---

### 2.4 Financial Management

**Primary Responsibility:** The financial relationship between institute
and family.

| Owns | Never Owns |
|---|---|
| Fee structures (plans, installments, due dates) | Learner profile or lifecycle (Learner Management owns this) |
| Scholarships and discounts | Curriculum or teaching (Academic Operations owns this) |
| Payment collection and receipts | Lead pipeline or conversion (Admissions owns this) |
| Outstanding tracking and escalation | Attendance or assessments (Academic Operations owns this) |
| Refunds | Communication policies (Communication owns this) |
| Revenue reporting and collection summaries | |
| GST compliance | |

**Handoff point:** When a fee is overdue, Finance sends a signal to
Communication to send reminders. When a refund is processed, Finance
updates the learner's financial status and notifies Learner Management
of any status change. Finance does not decide whether to suspend a
learner — that is a Learner Management decision based on financial data.

---

### 2.5 Communication

**Primary Responsibility:** Institutional communication policy and
trigger logic.

| Owns | Never Owns |
|---|---|
| Communication policies (what triggers what message to whom) | Channel delivery infrastructure (Platform Notification Service owns this) |
| Trigger logic (event → policy → trigger) | Learner profile or lifecycle (Learner Management owns this) |
| Audience rules and segmentation | Fees or money (Finance owns this) |
| Opt-out management | Curriculum or teaching (Academic Operations owns this) |
| Escalation routing logic | Lead pipeline (Admissions owns this) |
| | The actual content of what is communicated (other capabilities own their data) |

**Handoff point:** Communication defines the policy and triggers the
notification. The Platform Notification Service handles channel delivery
(WhatsApp, SMS, email, in-app). Academy never knows how WhatsApp works.
When Academic Operations has test results, it triggers Communication.
Communication decides who gets notified and when. Platform delivers.

---

### 2.6 Decision Support

**Primary Responsibility:** Decision-ready information for every stakeholder.

| Owns | Never Owns |
|---|---|
| Metrics definitions (what to measure) | Any write operations (Decision Support is a Read Model) |
| Dashboards and summaries | Any business behavior (Decision Support does not make decisions) |
| Trend analysis and comparisons | Any learner data (it reads from other capabilities) |
| Export functionality (Excel, PDF) | Any financial data (it reads from Finance) |

**Handoff point:** Decision Support reads from all capabilities. It does not
write to any. When the owner looks at a dashboard, Decision Support retrieves
data from Admissions (conversion rates), Finance (collection summary),
Academic Operations (attendance rates, test scores), and Learner
Management (retention rates). It assembles the picture. It does not
generate the data.

---

## 3. Ownership Summary

| Capability | Owns | Never Owns |
|---|---|---|
| **Admissions** | Lead lifecycle, counselling, enrollment, offering selection | Learner profile, money, curriculum, batch confirmation, communication |
| **Learner Management** | Learner profile, lifecycle states, renewals, exits | Leads, fees, curriculum, communication policies |
| **Academic Operations** | Batch placement, curriculum, attendance, tests, results, performance | Learner profile, money, leads, offering selection, communication policies |
| **Financial Management** | Fees, payments, receipts, refunds, revenue reports | Learner profile, academic outcomes, leads |
| **Communication** | Policies, triggers, opt-out | Learner data, fee data, academic data, lead data, channel delivery |
| **Decision Support** | Metrics, dashboards, trends | Any write operations or business behavior |

---

## 4. How to Validate Boundaries

When a new use case appears in Sprint 3, ask:

1. **Which capability owns it?** If two capabilities both claim ownership,
   the boundary is wrong.
2. **What data does it need?** If it needs data from another capability,
   that is a dependency, not ownership. Dependencies are fine. Duplicate
   ownership is not.
3. **What does it never own?** If the use case touches learner profile
   data, it should not own that data — Learner Management does.

---

## 5. Open Questions

1. **Batch transfers:** Is this an Admissions decision (which batch?) or
   a Learner Management event (lifecycle state change)? Currently modeled
   as Admissions use case A13. May need to be a joint responsibility.
2. **Fee plan creation:** Is this a one-time event at enrollment (Admissions
   owns it) or an ongoing financial relationship (Finance owns it)?
   Currently modeled as Financial Management use case FS1.
3. **Referral tracking:** Is this Admissions (capture referral source at
   lead creation) or Learner Management (track referral conversions over
   time)? Currently split: A1 captures the source, L7 tracks conversions.

---

*Sprint 2 — Responsibilities*
