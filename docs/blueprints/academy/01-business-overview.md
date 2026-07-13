# 01 — The Academy Operating Model

> **Scope:** What an academy IS, the working operating model, and why each
> core capability exists. This is not a spec. This is a product-architect's
> understanding of the domain.
>
> **Note:** This operating model is v1. The verbs may evolve after Sprint 2.
> See `DECISIONS.md` for the reasoning behind terminology choices.

---

## 1. What IS an Academy?

An academy sells **structured learning over time**. The customer pays for a
relationship — not a one-off transaction — and expects a measurable outcome
(exam score, skill acquisition, placement).

The fundamental difference from e-commerce or SaaS:

| Property | E-commerce | SaaS | Academy |
|---|---|---|---|
| Revenue model | Per-transaction | Subscription | Course fees (installments) |
| Delivery | Shipping/digital | Always-on | Scheduled classes + self-study |
| Success metric | GMV, NRR | DAU, churn | Scores, rank improvement |
| Customer relationship | Transactional | Product-led | High-touch (counsellor + teacher) |
| Duration | Seconds | Ongoing | Weeks to months |
| Decision complexity | Low | Medium | High (career impact) |

The high-touch, long-duration nature means the business cannot run without
**people managing people**. Software is an enabler, not the product.

Every future ADX blueprint will have its own operating model. This is the
**Academy Operating Model**. Others will follow: Clinic, Salon, Gym, etc.

---

## 2. Working Operating Model v1 (80% Common)

Every coaching institute, tuition centre, test-prep company, and skill
academy — regardless of subject, audience, or geography — runs the same
fundamental machine:

```
  ┌──────────┐
  │  ACQUIRE  │   Generate leads. Track where they come from.
  └────┬─────┘
       │
  ┌────▼─────┐
  │  CONVERT  │   Turn leads into enrolled students.
  └────┬─────┘       Non-linear. Leads go dormant. They come back.
       │
  ┌────▼─────┐
  │  ONBOARD  │   Collect fees. Assign batch. Welcome the student.
  └────┬─────┘
       │
  ┌────▼─────┐
  │  EDUCATE  │   Teach. Take attendance. Conduct tests.
  └────┬─────┘
       │
  ┌────▼──────┐
  │  MEASURE   │   Track metrics. Generate insights. Drive decisions.
  └────┬──────┘
       │
  ┌────▼─────┐
  │  RETAIN   │   Communicate. Build trust. Prevent dropout.
  └────┬─────┘
       │
  ┌────▼─────┐
  │   GROW    │   Renewals. Referrals. Expansion.
  └──────────┘
```

Each box is a **capability** — a function the business must perform
regardless of whether software exists. The verbs may evolve. The
capabilities will not.

> **Note:** This is Working Operating Model v1. After Sprint 2, verbs may
> change (e.g., Enroll instead of Convert, Deliver instead of Educate).
> The verbs describe the business flow, not the software architecture.

---

## 3. Why Each Capability Exists

### 3.1 Acquire (Lead Generation & Attribution)

**Why it exists:** Without a steady flow of new leads, the business dies.
Coaching institutes have a natural attrition rate (students leave after
cracking an exam, or drop out). They must constantly replace them.

**What it does:**
- Runs ads (Google, Instagram, local newspapers)
- Manages walk-in inquiries at the front desk
- Handles online form submissions (website, JustDial, social media)
- Tracks which source each lead came from (attribution)
- Calculates cost per lead and cost per enrollment per channel
- Manages referral programs (existing parents bring new parents)

**Business pressure:** Cost per acquisition (CAC). "Is the money I'm spending
on ads actually bringing in students?" But more importantly: "Which channels
produce the **best students**, not just the most leads?"

**Key insight:** Lead generation is not "marketing." It is the **pipeline
feeder**. The entire conversion workflow depends on a healthy, measurable
inflow of leads. Attribution determines where the institute invests its
limited marketing budget.

---

### 3.2 Convert (Lead → Enrolled Student)

**Why it exists:** A lead is not a student. Someone must guide the
prospect through interest → evaluation → commitment. This is the most
human-intensive function. And it is **non-linear**.

**The real journey:**

```
Lead
  ├── Qualified (interested + ability + timing)
  │     ├── Demo / Counselling Session
  │     │     ├── Enrolled → Onboard
  │     │     └── Not ready → Nurture
  │     └── Ghosted → Dormant
  │           └── Re-engaged (6 months later, before boards) → Demo
  └── Unqualified (not interested, wrong timing, competitor)
        └── Archived with reason
```

Leads disappear. Parents ghost. Students join a competitor, then come back
after boards. The conversion workflow must handle dormancy and re-engagement
as first-class states, not edge cases.

**What it does:**
- Follows up with leads (phone calls, WhatsApp, in-person meetings)
- Conducts demo classes or counselling sessions
- Handles objections (fee concerns, timing, competition)
- Nurtures dormant leads (periodic check-ins, new batch announcements)
- Processes enrollment paperwork
- Allocates students to the right educational offering and batch

**Business pressure:** Conversion rate (8-12% is typical for coaching).
Every percentage point improvement directly impacts revenue. The first
24-48 hours after a lead enters are critical — speed of follow-up is the
#1 predictor of conversion.

**Key insight:** This is not a "lead management" feature. It is the
**revenue engine**. The entire business depends on this function working
well. And it must handle the reality that conversion is cyclical, not linear.

---

### 3.3 Onboard (Fees + Batch Allocation + Welcome)

**Why it exists:** Once a student enrolls, three things must happen quickly:
1. Fees are collected (or installment plan agreed)
2. Student is placed in the right batch
3. Student feels welcomed and ready to start

These are separate operational tasks but they form a single business
capability: **onboarding**. The student's first experience after saying
"yes" determines their long-term engagement.

**What it does:**
- Generates fee invoices/challans
- Collects payments (cash, UPI, card, bank transfer)
- Tracks installment schedules and due dates
- Sends payment reminders
- Defines batches (name, offering, schedule, teacher, room)
- Allocates students to batches
- Handles batch transfers
- Manages batch capacity
- Sends welcome message and initial orientation

**Business pressure:** Collection efficiency. Batch balance (overcrowded
hurts quality, under-filled wastes teacher time). Speed — a student who
enrolled but hasn't been placed in a batch within 3 days starts to doubt
their decision.

**Key insight:** Fee collection is not "payments." It is a relationship.
The person collecting fees is often the same person who counselled the
student. Pushing too hard on payment damages the relationship. Being too
soft damages cash flow.

---

### 3.4 Educate (Attendance + Academics + Teaching)

**Why it exists:** This is the actual product. Everything else is support
capabilities. The student came to learn, get better scores, and achieve an
outcome.

**Sub-capabilities:**

**Attendance** — Two reasons it matters:
1. **Parental expectation:** Parents are paying ₹30,000+ per year. They
   want to know their child is actually attending classes.
2. **Business intelligence:** Low attendance is the earliest warning sign
   of student dropout. If a student stops attending, they will likely
   stop paying (or demand a refund).

**Academics** — The teaching itself:
- Delivers lectures (in-person, online, or hybrid)
- Assigns homework and practice problems
- Conducts tests (weekly, monthly, chapter-wise)
- Evaluates tests and records marks
- Tracks individual student progress
- Identifies weak areas per student
- Provides study material (notes, question banks)

**Curriculum** — The structure of what gets taught:
- Every institute organizes knowledge differently
- Coaching: Subject → Chapter → Topic
- Computer training: Module → Topic
- Language: Level → Skill → Lesson
- See `research/curriculum-hierarchy.md` for cross-type analysis
- **The hierarchy is unresolved.** Academy must not assume "Course" or
  "Subject" are universal concepts.

**Business pressure:** Teacher quality is the #1 differentiator. But from
a systems perspective, the pressure is on **visibility** — can the owner
see how students are performing across batches? Can parents see their
child's progress? Can the teacher see which students need help?

---

### 3.5 Measure (Insights & Metrics)

**Why it exists:** Every stakeholder needs to see different things:
- **Owner:** Revenue, enrollment trends, staff performance, CAC by channel,
  branch comparison
- **Branch Manager:** Daily operations summary, fee collection, attendance
- **Teacher:** Student performance, attendance in their batches
- **Parent:** Their child's attendance, marks, upcoming schedule
- **Counsellor:** Their conversion rate, follow-up pipeline

**What it does:**
- Tracks KPIs per capability (not just reports — actionable metrics)
- Generates daily/weekly/monthly summaries
- Shows financial summaries (revenue collected, outstanding, forecasts)
- Shows operational metrics (enrollment count, attendance rate, conversion rate)
- Shows academic performance (batch averages, toppers, struggling students)
- Exports data for external analysis (Excel, PDF)

**Business pressure:** Most institute owners make decisions based on gut feel.
Metrics exist but are rarely used well. The challenge is presenting data
in a way that actually drives action.

**Key insight:** This is not "Reports." Reports are outputs. **Metrics**
are what the business needs. The capability should be named for what it
produces (decision-ready information), not the artifact (a report).

---

### 3.6 Retain (Communication & Trust)

**Why it exists:** In Indian educational services, the parent is the customer.
The student is the user. The parent pays, the student learns. The parent
needs constant reassurance that:
- Their child is attending
- Their child is performing
- The institute is doing its job

**The communication model:**

```
Business Event          Communication Policy        Channel
─────────────          ────────────────────        ───────
Student absent    →    Notify parent immediately  → WhatsApp
Fee due in 3 days →    Send reminder              → WhatsApp/SMS
Test result ready →    Share with parent           → WhatsApp/In-app
Schedule changed  →    Announce to affected batch  → WhatsApp/SMS
Monthly summary   →    Send progress report        → Email/In-app
```

The **business event** triggers a **policy**. The policy selects a
**channel**. This separation means new channels (email, SMS, voice call,
in-app) can be added without changing the business event. And the same
event can trigger different policies for different audiences.

**Business pressure:** Too much communication → parents ignore it. Too little
→ parents feel neglected. The channel matters (WhatsApp for quick updates,
formal letters for reports, phone calls for complaints).

**Key insight:** Communication is not "notifications." It is the trust
mechanism. When a parent trusts the institute, they renew. When they
don't, they leave.

---

### 3.7 Grow (Renewals & Referrals)

**Why it exists:** Acquiring a new student is 5-10x more expensive than
retaining an existing one. The business grows through:
- **Renewals:** Existing students continuing for the next term/year
- **Referrals:** Existing parents bringing new parents (word of mouth is
  the #1 enrollment channel)
- **Expansion:** New batches, new courses, new branches

**What it does:**
- Tracks renewal readiness (is the student likely to continue?)
- Manages referral programs (who referred whom, reward tracking)
- Identifies expansion opportunities (which batches have waitlists?)
- Manages the seasonal admission cycle (April–June peak)

**Business pressure:** Renewal rate. Referral rate. "Are we growing from
our existing base, or only from new marketing?"

---

## 4. The Two Customer Relationships

This is the most important structural insight for Academy:

```
┌─────────────────────────────────────────────────────┐
│                    ACADEMY                           │
│                                                     │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│   │ Parent   │◄──►│Counsellor│◄──►│ Teacher  │     │
│   │(pays)    │    │(sells)   │    │(teaches) │     │
│   └────┬─────┘    └──────────┘    └────┬─────┘     │
│        │                               │            │
│        │         ┌──────────┐          │            │
│        └────────►│ Student  │◄─────────┘            │
│                  │(learns)  │                       │
│                  └──────────┘                       │
└─────────────────────────────────────────────────────┘
```

- **Parent** pays money, expects results, needs communication
- **Student** attends classes, does homework, takes tests
- **Counsellor** sells the dream, manages the relationship
- **Teacher** delivers the product, builds trust through competence

The software must serve all four relationships. Most institute software
only serves the teacher-student relationship (LMS) or the admin relationship
(management software). The **missing piece** is the parent-student-institute
triangle.

---

## 5. What Makes Academy Different

Academy is not an LMS. It is not a school management system. It is not a
course marketplace.

**Academy is the operating system for educational service businesses.**

The distinction:
- **LMS** = content delivery + quizzes. Used by the teacher and student.
- **School Management System** = attendance + fees + reports. Used by admin.
- **Academy** = the entire business workflow from lead to outcome.
  Used by every role. Built for the specific needs of coaching institutes
  and tuition centres in India.

The 80% common operating model above is the foundation. The remaining 20%
is where institutes differentiate (their teaching methodology, their brand,
their student experience). Academy must handle the 80% flawlessly so that
the institute can focus on the 20%.

---

## 6. The Temporal Dimension

Businesses run on calendars. Every capability in the operating model is
affected by time:

| Temporal Concept | What it is | Affects |
|---|---|---|
| **Academic Year** | The annual cycle (April–March for school-aligned institutes) | Admissions, renewals, reporting |
| **Admission Window** | Peak period for new enrollments (April–June) | Marketing, conversion, onboarding |
| **Term / Semester** | Subdivision of the academic year (not all institutes have this) | Fees, academics, renewal |
| **Course Duration** | Length of the educational offering (3 months – 2 years) | Fees, batch lifecycle |
| **Exam Window** | Scheduled periods for formal assessments | Academics, communication |
| **Fee Cycle** | Rhythm of fee collection (monthly, quarterly, per installment) | Fees, communication |
| **Renewal Cycle** | Period when students decide to continue or exit | Retain, Grow |

**Key insight:** Different institute types follow different temporal models:
- **School-aligned** (coaching): April–March, seasonal peaks, annual renewal
- **Rolling enrollment** (computer/language): Always open, no fixed year
- **Exam-cycle** (CA/CMA): Tied to external exam body schedule

Academy must support multiple temporal models, not impose one.

---

## 7. The Offering Hypothesis

What the student actually purchases varies by institute type:

| Institute Type | What the student buys |
|---|---|
| Coaching | "JEE Nurture Course" — an entry variant of an offering |
| Computer training | "Full Stack Development" — the offering itself |
| Language | "B1 English" — a proficiency level within an offering |
| CA/CMA | "CA Foundation" — a certification level |

**"Educational Offering"** is the working term for what is advertised to
the market. Whether the student buys the Offering itself, a Variant of it,
or a Level within it — this is an open research question.

See `research/curriculum-hierarchy.md` for the full analysis.

---

## 8. Open Questions

1. Should Academy support **multi-branch** from day one, or start
   single-branch and add multi-branch later?
2. Should Academy include a **student/parent app**, or is a web-based
   parent portal sufficient?
3. Does Academy need to integrate with **WhatsApp Business API** for
   parent communication, or is SMS + in-app notification enough?
4. Should Academy support **online classes** (live + recorded), or only
   manage offline (in-person) operations?
5. How does Academy handle **multi-currency** for potential international
   use, or is it INR-only?
6. What is the **commercial unit of sale** — the Educational Offering, a
   Variant, a Batch, or a Seat? This affects pricing, invoicing, and
   renewals.
7. What is the **curriculum hierarchy**? See `research/curriculum-hierarchy.md`.
8. What is the **smallest unit of learning** the institute manages —
   Session? Topic? Chapter? This affects attendance, homework, timetable,
   syllabus, and exams.

---

*This document describes the domain as it exists in reality, not as we plan
to build it. The operating model is v1 — verbs may change after Sprint 2.
Decisions about what to build and how come in later sprints.*
