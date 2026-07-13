# 10 — Context Discovery

> **Scope:** Where to draw boundaries around business responsibilities.
> Each context has a clear primary responsibility and does not overlap
> with others. These are not software modules — they are the conceptual
> boundaries that will eventually become the building blocks of the
> software architecture.
>
> **Rule:** Every document in Sprint 2 must be understandable by a coaching
> institute owner with no software background.

---

## 1. Why Boundaries Matter

When the academy business grows, complexity grows with it. Without clear
boundaries, the system becomes a tangled web where changing one thing
breaks three others. Clear boundaries mean:
- **One team can own one context** without coordinating with everyone else
- **Changes in one context don't ripple** into others
- **Each context can evolve independently** as the business discovers
  new needs

The previous documents defined capabilities (what the business does) and
responsibilities (what each capability owns). This document discovers
where the natural boundaries lie.

---

## 2. What Each Context Owns

### Admissions

Admissions owns the prospect-to-enrollment journey.

**Includes:**
- Lead lifecycle (capture, qualify, route, follow up, nurture, re-engage)
- Counselling and demo scheduling
- Offering selection and seat reservation
- Enrollment processing (documents, fee challan)
- Marketing attribution (cost per lead, cost per enrollment per channel)

**Does NOT include:**
- The learner record after enrollment (Learner owns this)
- Batch confirmation or assignment (Academics owns this)
- Fee collection (Finance owns this)
- Curriculum structure (Academics owns this)

---

### Learner

Learner owns the relationship with the enrolled learner.

**Includes:**
- Learner profile (personal details, guardian, contact)
- Lifecycle states (Active, At Risk, Renewed, Dropped, Suspended)
- At-risk detection and intervention triggers
- Renewals and re-enrollment
- Exits and withdrawal processing
- Referral tracking

**Does NOT include:**
- Lead pipeline (Admissions owns this)
- Fees or payments (Finance owns this)
- Curriculum or teaching (Academics owns this)
- Communication policies (Communication owns this)

---

### Academics

Academics owns the delivery of education.

**Includes:**
- Batch placement, confirmation, and transfer
- Batch capacity management
- Curriculum structure (Subject/Module/Level/Paper — configurable)
- Attendance (recording, absence detection, chronic absence)
- Tests, evaluations, marks
- Performance tracking and trends
- Study material distribution
- Syllabus progress tracking

**Does NOT include:**
- Learner profile (Learner owns this)
- Fees or money (Finance owns this)
- Lead pipeline or offering selection (Admissions owns this)
- Communication policies (Communication owns this)

**Open question:** This context may naturally divide into two sub-contexts
in Sprint 3:
- **Academic Planning** — Curriculum, Batches, Timetable
- **Academic Delivery** — Attendance, Teaching, Assessments, Results

Validate in Sprint 3.

---

### Finance

Finance owns the financial relationship between institute and family.

**Includes:**
- Fee structures (plans, installments, due dates)
- Scholarships and discounts
- Payment collection and receipts
- Outstanding tracking and escalation
- Refunds
- Revenue reporting and collection summaries
- GST compliance

**Does NOT include:**
- Learner profile (Learner owns this)
- Curriculum or teaching (Academics owns this)
- Lead pipeline (Admissions owns this)
- Communication policies (Communication owns this)

---

### Communication

Communication owns institutional communication policy and trigger logic.

**Includes:**
- Communication policies (what triggers what message to whom)
- Trigger logic (event → policy → trigger)
- Audience rules and segmentation
- Escalation routing logic
- Opt-out management

**Does NOT include:**
- Channel delivery infrastructure (Platform Notification Service handles this)
- The actual data being communicated (other contexts own their data)
- Learner profile (Learner owns this)
- Fees or money (Finance owns this)
- Curriculum or teaching (Academics owns this)

---

### Decision Support

Decision Support is a Read Model that spans all contexts. It reads data
from each context but does not own any business behavior. It has no write
operations.

**Includes:**
- Metrics definitions (what to measure)
- Dashboards and summaries
- Trend analysis and comparisons
- Export functionality (Excel, PDF)

**Does NOT include:**
- Any write operations
- Any business behavior (Decision Support does not make decisions)
- Any learner data (it reads from Learner)
- Any financial data (it reads from Finance)

If analytics pipelines, metric definitions, or scheduled reports emerge
later, Decision Support may grow into its own context. Today it does not.

---

## 3. Context Summary

| Context | Primary Responsibility |
|---|---|
| **Admissions** | Prospect-to-enrollment journey |
| **Learner** | Learner lifecycle after admission |
| **Academics** | Delivery of education |
| **Finance** | Financial relationship with family |
| **Communication** | Institutional communication policy |
| **Decision Support** | Decision-ready information (Read Model) |

---

## 4. The Central Concept

> Learner appears to be the central business concept connecting Admissions,
> Academics, Finance, Communication, and Decision Support. Every context
> either creates, references, or reads from the Learner. This observation
> will be validated during Sprint 3.

---

## 5. Boundary Validation

When a new requirement appears in Sprint 3, ask:

1. **Which context owns it?** If two contexts both claim ownership,
   the boundary is wrong.
2. **Can this context change independently?** If changing Admissions
   requires changing Finance, the boundaries may be too tight.

---

## 6. Open Questions

1. **Batch transfers:** Now owned by Academics. Does this create friction
   when Admissions needs to reserve a seat that Academics hasn't confirmed
   yet?
2. **Fee plan creation:** Currently in Finance. Should it be in Admissions
   (since it happens at enrollment time)?
3. **Referral tracking:** Currently in Learner. Should it be in Admissions
   (since referrals generate leads)?
4. **Curriculum management:** Is this a cross-cutting concern that multiple
   contexts need, or is it exclusively owned by Academics?
5. **Decision Support:** Should it eventually become its own context, or
   should it remain a Read Model that spans all contexts?

---

## 7. Sprint 2 Traceability

| Sprint 2 Document | This Document |
|---|---|
| `05-capabilities.md` | Each capability maps to a context |
| `06-use-cases.md` | Each use case belongs to exactly one context |
| `07-responsibilities.md` | Context boundaries align with responsibility ownership |
| `08-modules.md` | Each module corresponds to one context |
| `09-platform-services.md` | Platform domains and services are consumed by contexts, not owned by them |

---

*Sprint 2 — Context Discovery*
