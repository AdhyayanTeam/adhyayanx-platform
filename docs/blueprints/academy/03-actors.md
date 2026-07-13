# 03 — Actors: Roles, Responsibilities, Ownership

> **Scope:** Every role that interacts with the system, what they do, what
> they own, and how they relate to each other. This is about people, not
> permissions (permissions come in Sprint 3).

---

## 1. The Actor Map

```
┌─────────────────────────────────────────────────────────────────┐
│                         INSTITUTE                                │
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │  Owner   │   │ Manager  │   │Counsellor│   │ Teacher  │     │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘     │
│       │              │              │              │             │
│       │         ┌────┴─────┐        │              │             │
│       │         │Accountant│        │              │             │
│       │         └────┬─────┘        │              │             │
│       │              │              │              │             │
│  ┌────┴──────────────┴──────────────┴──────────────┴────┐       │
│  │                    SYSTEM                             │       │
│  └────┬──────────────┬──────────────┬──────────────┬────┘       │
│       │              │              │              │             │
│  ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐     │
│  │  Parent  │   │ Student  │   │Reception.│   │  Admin   │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Primary Actors (Internal — Institute Staff)

### 2.1 Owner

**Who they are:** The person who founded or owns the institute. Often a
former teacher who built the business from 1-room tuition to a multi-branch
operation.

**What they care about:** Revenue, growth, reputation, student outcomes.

**Responsibilities:**
- Strategic decisions (pricing, expansion, new offerings)
- Financial oversight (daily collection, monthly P&L, cash flow)
- Marketing and lead generation strategy (which channels, what budget)
- Key parent relationships (high-value or complaint-handling)
- Staff hiring and retention
- Brand direction

**What they need from the system:**
- Daily numbers on their phone (enrollments, collections, attendance)
- Monthly revenue and enrollment trends
- Marketing attribution (CAC per channel, conversion rate per source)
- Staff performance visibility
- Ability to approve exceptions (fee waivers, discounts, batch transfers)

**Interaction pattern:** Low frequency, high impact. Checks the system
2-3 times a day, primarily on mobile. Wants a 10-second glance at
today's numbers.

---

### 2.2 Branch Manager

**Who they are:** The person who runs day-to-day operations at a branch.
Often the second-in-command, or the owner themselves for single-branch
institutes.

**What they care about:** Operations running smoothly, staff productivity,
parent satisfaction.

**Responsibilities:**
- Daily operations (room scheduling, teacher coordination, staff attendance)
- Batch management (creation, allocation, transfers)
- Conflict resolution (parent complaints, student issues)
- Supervising counsellors and teachers
- Local marketing execution (walk-in management, school visits, events)
- Reporting to the owner

**What they need from the system:**
- Today's schedule overview (which batches, which teachers, which rooms)
- Staff attendance and availability
- Batch capacity and waitlists
- Pending issues (unresolved complaints, pending fee reminders)
- Ability to approve batch transfers and schedule changes

**Interaction pattern:** Medium frequency, medium impact. Uses the system
throughout the day, often on desktop during office hours, mobile otherwise.

---

### 2.3 Counsellor (Admissions Counsellor)

**Who they are:** The person who converts inquiries into enrolled students.
They are the sales team. They are the most relationship-driven role.

**What they care about:** Conversion rate, follow-up speed, their pipeline.

**Responsibilities:**
- Follow up with every lead within 24 hours (ideally within 2 hours)
- Conduct demo classes and counselling sessions
- Handle objections (fees, timing, competition)
- Process enrollments (documents, fee challan generation)
- Nurture dormant leads (periodic check-ins, re-engagement)
- Maintain the lead pipeline (status updates, lost reasons, dormant tracking)
- Build relationships with parents (WhatsApp, phone, in-person)

**What they need from the system:**
- Real-time lead list with contact details, source, and lifecycle status
- Follow-up reminders ("Call Mrs. Sharma — she asked about NEET batch")
- Dormant lead alerts ("This lead hasn't been contacted in 30 days")
- Quick access to offering/fee information for quoting
- Enrollment workflow (select student, select offering variant, select batch,
  generate fee challan)
- Personal conversion metrics (how many calls, how many enrollments, pipeline
  value)

**Interaction pattern:** High frequency, high urgency. Uses the system
constantly throughout the day. Needs mobile-first experience. Cannot
afford to be behind a desk.

---

### 2.4 Teacher / Faculty

**Who they are:** The people who teach. They are the reason students come.
They are the most important differentiator for the institute.

**What they care about:** Teaching quality, student understanding, their
subject, being respected.

**Responsibilities:**
- Deliver lectures according to the schedule
- Create and review homework
- Conduct and evaluate tests
- Track student progress in their curriculum unit
- Communicate with branch manager about student issues
- Prepare study material

**What they need from the system:**
- Their teaching schedule (today, this week)
- Student list for each batch
- Attendance marking (quick, < 30 seconds)
- Test score entry (quick, bulk-friendly)
- Student performance trends in their curriculum unit

**Interaction pattern:** Low frequency, time-constrained. The teacher's
primary job is teaching, not using software. The system must be invisible
— take 30 seconds for attendance, 2 minutes for test scores. If it takes
longer, teachers will revert to paper.

---

### 2.5 Accountant

**Who they are:** The person who manages money. In small institutes, this
might be the owner or a part-time bookkeeper. In larger institutes, a
dedicated role.

**What they care about:** Accuracy, reconciliation, cash flow, compliance.

**Responsibilities:**
- Collect fees (cash, UPI, card, transfer)
- Generate receipts and invoices
- Track installment schedules and due dates
- Send payment reminders
- Maintain the fee ledger
- Handle refunds
- Prepare bank deposits
- Generate GST-compliant invoices

**What they need from the system:**
- Student fee status (what's paid, what's due, what's overdue)
- One-click receipt generation
- UPI QR code generation for payment
- Installment schedule management
- Daily collection summary
- Outstanding payment reports

**Interaction pattern:** High frequency during collection hours. Needs
speed and accuracy. Cannot afford double-entry or manual reconciliation.

---

### 2.6 Receptionist / Front Desk

**Who they are:** The first person visitors see. In small institutes, this
role may be combined with the counsellor.

**What they care about:** Making a good impression, not letting anyone slip
through, keeping things organized.

**Responsibilities:**
- Greet visitors and students
- Answer phone calls
- Log walk-in inquiries
- Direct parents to the right person
- Manage the visitor log
- Handle basic queries (batch timings, fees, directions)

**What they need from the system:**
- Quick inquiry entry (name, phone, course of interest, source)
- Student check-in (arrival tracking)
- Staff directory (who is in which room, who is available)
- Basic information to share (batch timings, fee ranges)

**Interaction pattern:** High frequency, low depth. Needs a very simple
interface — a form with 4 fields, not a complex dashboard.

---

## 3. External Actors (Outside the Institute)

### 3.1 Parent / Guardian

**Who they are:** The person paying fees and making enrollment decisions.
In 90% of cases, this is the parent (mother or father). For adult learners,
the student is the parent.

**What they care about:** Their child's outcome, return on investment,
being informed, being heard.

**What they do:**
- Inquire about offerings (phone, walk-in, website)
- Attend counselling sessions
- Pay fees (sometimes in installments)
- Check attendance (calls or visits the institute)
- Receive exam results
- Discuss concerns with teacher or manager
- Refer other parents (word of mouth is the #1 marketing channel)

**Relationship to the system:**
- Minimal direct system interaction (maybe a parent portal or WhatsApp)
- Receives communications (SMS, WhatsApp, calls)
- May receive a fee receipt via WhatsApp

**Interaction pattern:** Low frequency, high emotional stakes. A parent
who calls is often anxious or upset. The institute's response speed and
quality determines whether they stay or leave.

---

### 3.2 Student

**Who they are:** The person learning. The end user of the educational
service. Ages range from 8 (foundation courses) to 25+ (competitive exam
aspirants).

The same human changes business identity over time:

```
Lead → Prospect → Applicant → Student
```

A **Lead** is anyone who has expressed interest. A **Prospect** has been
qualified (interested + ability + timing). An **Applicant** has started
the enrollment process. A **Student** is enrolled, fee-paid, batch-assigned.

**What they care about:** Learning, scores, social belonging, not being
bored, not being humiliated.

**What they do:**
- Attend classes
- Submit homework
- Take tests
- Ask questions
- Interact with peers
- Sometimes pay fees (adult learners)

**Relationship to the system:**
- Minimal direct interaction (attends class, takes tests)
- May use a student app for homework, test results, study material
- May receive notifications (class reminders, test schedules)

**Interaction pattern:** The student is the least active system user but
the most important beneficiary. The system serves them through the other
actors (teacher marks their attendance, counsellor manages their enrollment,
parent sees their progress).

---

### 3.3 Referral Source

**Who they are:** An existing student or parent who refers a new inquiry.
Word of mouth is the #1 enrollment channel for coaching institutes.

**What they do:**
- Mention the institute to friends, family, colleagues
- Sometimes bring the new parent to the institute
- Expect recognition (thank you, discount, or just gratitude)

**Relationship to the system:**
- The inquiry form should capture "referred by" (which student/parent)
- The system should track referral conversions (did the referred inquiry enroll?)
- The system should support referral rewards (discount on next installment)

---

## 4. Role Overlap (Small vs. Large Institutes)

A critical design consideration: **the same person may wear multiple hats.**

| Institute Size | Owner | Manager | Counsellor | Teacher | Accountant | Receptionist |
|---|---|---|---|---|---|---|
| **1-room tuition** (1 teacher, 20 students) | = Teacher | = Teacher | = Teacher | = Owner | = Owner | = Nobody |
| **Small centre** (2-3 teachers, 80 students) | Owner | = Owner | = Owner | Teacher | = Owner | = Counsellor |
| **Mid-size** (5-8 teachers, 200 students) | Owner | Dedicated | 1-2 dedicated | Teacher | Dedicated | Dedicated |
| **Large centre** (15+ teachers, 500+ students) | Owner (rarely present) | 1 per branch | 3-5 team | Teacher | Team | 1 per branch |

**Implication for Academy:** The system must support role consolidation.
A single user should be able to have multiple roles. A teacher who also
does counselling should see both views. An owner who also manages the
branch should have both permissions.

---

## 5. Who Owns What

| Domain | Primary Owner | Secondary (can view/edit) | Read-only |
|---|---|---|---|
| **Leads** | Counsellor | Manager, Owner | — |
| **Enrollments** | Counsellor (creates), Manager (approves) | Owner | — |
| **Batches** | Manager | Owner | Teacher (their batches) |
| **Attendance** | Teacher (marks), Manager (reviews) | Owner | Parent (their child) |
| **Fees** | Accountant | Manager, Owner | Parent (their child) |
| **Tests/Marks** | Teacher (enters) | Manager, Owner | Parent (their child) |
| **Communication Policies** | Owner (sets), Manager (executes) | Counsellor (sends) | — |
| **Insights & Metrics** | Owner, Manager | Counsellor (own metrics) | Teacher (own batches), Parent (own child) |
| **System Settings** | Owner | Manager | — |

---

## 6. Open Questions

1. Should **students** have direct system access (student app/portal), or
   should all student-facing interactions go through the parent?
2. For **adult learners** (e.g., CAT/GMAT prep where the student is 22+),
   is the student the same as the parent? How does the model change?
3. Should a **teacher** be able to see student fee status (to know if
   a student is at risk of dropping due to non-payment)?
4. Can a **counsellor** also be a **teacher**, or are these always separate?
5. Should Academy support **external trainers** (guest faculty who teach
   one batch but are not institute employees)?
6. How does Academy handle **staff turnover** — when a counsellor leaves,
   how are their pending leads reassigned?
7. How do temporal structures (academic year, admission window, renewal
   cycle) affect each role's daily workflow?

---

*This document describes the people involved, not the system design. The
ownership model informs access control in Sprint 3.*
