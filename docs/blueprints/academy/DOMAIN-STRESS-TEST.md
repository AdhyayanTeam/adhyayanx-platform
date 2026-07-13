# Academy Domain Stress Test

> **Purpose:** Validate the Sprint 1 domain model against edge cases.
> Every future change should be validated against these scenarios.
>
> **Format:** Scenario → Current Model → Pass/Partial/Fail → Required Change

---

## Scenario 1: Single-Teacher Tuition

**Scenario:**
Owner runs a 1-room tuition center. They are the teacher, counsellor,
accountant, and receptionist. 20 students. No staff.

**Current Model:**
Owner, Teacher, Counsellor, Accountant, Receptionist are separate actors
with distinct responsibilities and ownership.

**Result:** PASS

**Reason:**
Roles collapse into one person. Responsibilities remain unchanged — the
owner still performs all functions, just as one person. The role overlap
table in `03-actors.md` already handles this (row: "1-room tuition").

**Required Change:** None.

---

## Scenario 2: One-to-One Coaching

**Scenario:**
A CAT/GMAT tutor teaches exclusively 1-on-1. Each student has their own
schedule. No batches. No group classes.

**Current Model:**
Batch is a core concept. Attendance is per session per batch. A session
belongs to a batch.

**Result:** PARTIAL

**Reason:**
The Batch abstraction becomes weak. A "batch of 1" is technically valid
but feels forced. The stronger question is: can a Session exist without
a Batch? In 1-on-1 coaching, the student's schedule IS the batch.

**Required Change:**
Sprint 2 should investigate whether Session can exist without Batch, or
whether "batch of 1" is an acceptable configuration.

---

## Scenario 3: Monthly Subscription Pricing

**Scenario:**
An English speaking institute charges ₹2,000/month. No course duration.
Student stays as long as they want. No installment plan — recurring
monthly payment.

**Current Model:**
Fee Plan is tied to an enrollment with installments. Course duration
defines the fee schedule. Renewal is annual.

**Result:** PARTIAL

**Reason:**
The installment model assumes a defined course duration with N payments.
A subscription model has no defined end date and no installment count.
The fee collection workflow assumes "installment due on date X" — in
subscription mode, every month is the same installment.

**Required Change:**
Sprint 2 should investigate whether Fee Plan supports both
"installment-based" and "subscription-based" models, or whether these
are fundamentally different payment structures.

---

## Scenario 4: Online-Only Institute

**Scenario:**
An institute runs entirely online. No physical rooms. Teachers teach
from home. Students attend from home. No walk-ins. All leads come from
website/social media.

**Current Model:**
Walk-in is a lead source. Room is part of batch creation. Physical
location is assumed in many workflows.

**Result:** PASS

**Reason:**
Walk-in is one source among many — online leads are already modeled
(room is optional in batch creation). The communication model
(WhatsApp/SMS) works regardless of physical location. The absence of
walk-ins is a configuration (receptionist role becomes minimal), not
a structural change.

**Required Change:** None. Room assignment should be optional in batch
creation (it may already be).

---

## Scenario 5: Student Joins Mid-Term

**Scenario:**
A JEE batch started in April. A new student enrolls in July — joining
an existing batch that has already covered 3 months of syllabus.

**Current Model:**
Enrollment triggers batch allocation. The student joins the batch as-is.

**Result:** PASS

**Reason:**
The model doesn't assume all students in a batch started at the same
time. A student enrolling mid-term joins the current batch and catches
up on missed material (or receives separate catch-up sessions). This
is a common real-world scenario that the current model handles naturally.

**Required Change:** None. However, Sprint 2 should consider whether
the system tracks "batch start date" vs "student start date" — they
may differ.

---

## Scenario 6: No Exams (Skill-Based Learning)

**Scenario:**
A music institute teaches guitar. No exams. No marks. No test scores.
Progress is assessed by the teacher's judgment, not by marks.

**Current Model:**
Test → Result → Communication is a full workflow. Marks are entered.
Performance is tracked by test scores.

**Result:** PARTIAL

**Reason:**
The Test workflow assumes tests exist. In skill-based learning, there
are no formal tests — progress is qualitative (teacher notes, skill
milestones). The system shouldn't require tests to exist.

**Required Change:**
Sprint 2 should ensure the Test workflow is optional, not mandatory.
The system should support "teacher observation notes" as an alternative
to formal test scores.

---

## Scenario 7: Working Professionals (No Parent)

**Scenario:**
A GMAT prep institute teaches working professionals (age 25-30). The
student is the customer. They pay their own fees. No parent involvement.

**Current Model:**
Parent is the customer. Parent pays fees. Parent receives communication.
The parent-student-institute triangle is central.

**Result:** PARTIAL

**Reason:**
The model assumes parent involvement in payment, communication, and
decision-making. For adult learners, the student IS the parent. The
Guardian concept exists but the communication model assumes parent
notifications. Adult students don't want their "parent" notified —
they want the communication themselves.

**Required Change:**
Sprint 2 should ensure the communication model supports "Student" as
the communication recipient, not just "Parent/Guardian." The Guardian
concept should be optional, not required.

---

## Scenario 8: Multi-Branch with Shared Teachers

**Scenario:**
An institute has 3 branches. Physics teacher teaches at Branch A on
Monday and Branch B on Wednesday. Same teacher, different locations.

**Current Model:**
Batch belongs to a branch. Teacher is assigned to a batch. Branch
Manager manages operations at one branch.

**Result:** PARTIAL

**Reason:**
The model assumes a teacher belongs to a branch (managed by that
branch's manager). In reality, a teacher may belong to the institute
and teach across branches. The branch is a scheduling context, not
an ownership context for teachers.

**Required Change:**
Sprint 2 should investigate whether Teacher is owned by the Institute
(not the Branch) and Branch is a scheduling/location context. The
Branch Manager's supervision of teachers across branches needs clarity.

---

## Summary

| # | Scenario | Result | Key Finding |
|---|---|---|---|
| 1 | Single-teacher tuition | PASS | Role consolidation already handled |
| 2 | One-to-one coaching | PARTIAL | Can Session exist without Batch? |
| 3 | Monthly subscription | PARTIAL | Fee Plan needs subscription model |
| 4 | Online-only institute | PASS | Room should be optional |
| 5 | Student joins mid-term | PASS | Track batch start vs student start |
| 6 | No exams | PARTIAL | Test workflow should be optional |
| 7 | Working professionals | PARTIAL | Guardian should be optional |
| 8 | Multi-branch shared teachers | PARTIAL | Teacher belongs to institute, not branch |

**Overall: 3 PASS, 5 PARTIAL, 0 FAIL**

The Sprint 1 domain model is **structurally sound**. The PARTIAL results
indicate configuration needs, not structural breaks. Sprint 2 should
address these as it refines the model.

---

*Every future change to the Academy domain should be validated against
these scenarios. If a change breaks a PASS scenario into a FAIL, the
change is wrong. If it reveals a new edge case, add it here.*

*Sprint 1 — COMPLETE*
