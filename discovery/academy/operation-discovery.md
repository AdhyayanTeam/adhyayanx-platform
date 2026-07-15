# Academy — Operation Discovery

> This document is exploratory.
>
> Nothing in this document is considered part of the Academy model
> until it has been validated and promoted into the documentation.
>
> The purpose of this document is to discover, not to decide.

Discovery documents capture evidence.

Documentation captures understanding.

Software captures implementation.

---

## Source

All observations come from `docs/blueprints/academy/02-a-day-at-the-academy.md`.

---

## Goal

The goal is to discover the smallest set of business operations that explain the observed work.

Each operation transforms something. Before it runs, something is one way. After it runs, something is another way. If nothing changes, it's not an operation.

---

## Classification

Every observation from the observation document, classified.

| Observation | Classification | Evidence |
|-------------|---------------|----------|
| Shutters roll up / office unlocked | Activity | OBS-OPEN-001 |
| Owner checks yesterday's collection | Activity | OBS-OPEN-002 |
| Owner reviews pending payments | Activity | OBS-OPEN-003 |
| Three parents promised to pay, none did | Exception | OBS-OPEN-004 |
| Faculty member called in sick | Trigger | OBS-OPEN-005 |
| No replacement was arranged | Exception | OBS-OPEN-006 |
| Batch has44 students, started with40 | Exception | OBS-OPEN-007 |
| AC repair person didn't come | Exception | OBS-OPEN-008 |
| Owner reads handwritten register | Activity | OBS-OPEN-009 |
| Register not up to date | Information state | OBS-OPEN-010 |
| Staff reports AC not working | Activity | OBS-OPEN-011 |
| Phone rings | Trigger | OBS-ENQ-001 |
| Receptionist answers questions from memory | Activity | OBS-ENQ-002 |
| Receptionist records enquiry in ledger | Activity | OBS-ENQ-003 |
| Parent asks about scholarships | Activity | OBS-ENQ-004 |
| Receptionist can't answer | Exception | OBS-ENQ-005 |
| Receptionist writes sticky note for follow-up | Activity | OBS-ENQ-006 |
| Sticky note will be buried by lunchtime | Exception | OBS-ENQ-007 |
| Parent walks in with child | Trigger | OBS-ADM-001 |
| Counsellor asks for documents | Activity | OBS-ADM-002 |
| Parent forgot Aadhaar | Exception | OBS-ADM-003 |
| Counsellor asks owner for permission | Activity | OBS-ADM-004 |
| Owner approves with condition | Decision | OBS-ADM-005 |
| Counsellor writes "Aadhaar pending" | Activity | OBS-ADM-006 |
| Counsellor fills admission form | Activity | OBS-ADM-007 |
| Parent asks about fees | Activity | OBS-ADM-008 |
| Counsellor explains fee structure | Activity | OBS-ADM-009 |
| They wait for accountant | Exception | OBS-ADM-010 |
| Accountant takes cash | Activity | OBS-ADM-011 |
| Accountant writes receipt | Activity | OBS-ADM-012 |
| Counsellor checks whiteboard for batch capacity | Activity | OBS-ADM-013 |
| Whiteboard says38, owner said44 | Exception | OBS-ADM-014 |
| Counsellor writes name on board | Activity | OBS-ADM-015 |
| Admission complete after45 minutes | Information | OBS-ADM-016 |
| Aadhaar still missing, no one tracking | Exception | OBS-ADM-017 |
| Batch begins | Trigger | OBS-CLS-001 |
| Teacher opens attendance register | Activity | OBS-CLS-002 |
| Teacher calls name, student absent | Activity | OBS-CLS-003 |
| Teacher marks absent | Activity | OBS-CLS-004 |
| No one calls parent | Exception | OBS-CLS-005 |
| Student claims he was present | Trigger | OBS-CLS-006 |
| Teacher checks register | Activity | OBS-CLS-007 |
| No way to verify | Exception | OBS-CLS-008 |
| Teacher says "I'll fix it next time" | Exception | OBS-CLS-009 |
| Student frustrated | Exception | OBS-CLS-010 |
| Teacher begins lesson | Activity | OBS-CLS-011 |
| Student asks about homework | Activity | OBS-CLS-012 |
| Teacher forgot to check homework | Exception | OBS-CLS-013 |
| Teacher writes note to self | Activity | OBS-CLS-014 |
| Teacher reviews test papers | Activity | OBS-CLS-015 |
| Three students scored below50% | Information | OBS-CLS-016 |
| Teacher writes names on sticky note | Activity | OBS-CLS-017 |
| Sticky note will fall off | Exception | OBS-CLS-018 |
| Accountant sits with day's collection | Activity | OBS-FEE-001 |
| Four parents paid today | Information | OBS-FEE-002 |
| Accountant opens ledger | Activity | OBS-FEE-003 |
| Accountant writes in ledger | Activity | OBS-FEE-004 |
| Accountant calculates balance by hand | Activity | OBS-FEE-005 |
| Student's installment was due last week | Trigger | OBS-FEE-006 |
| Accountant calls parent | Activity | OBS-FEE-007 |
| No answer | Exception | OBS-FEE-008 |
| Accountant sends WhatsApp message | Activity | OBS-FEE-009 |
| Parent asks to pay next month | Trigger | OBS-FEE-010 |
| Accountant doesn't know policy | Exception | OBS-FEE-011 |
| Receptionist hands cash to accountant | Activity | OBS-FEE-012 |
| Accountant counts cash | Activity | OBS-FEE-013 |
| Cash is500 short | Exception | OBS-FEE-014 |
| Receptionist checks records | Activity | OBS-FEE-015 |
| Missing piece of paper | Exception | OBS-FEE-016 |
| Accountant notes discrepancy | Activity | OBS-FEE-017 |
| Last batch leaves | Trigger | OBS-CLOSE-001 |
| Owner asks "How many admissions?" | Activity | OBS-CLOSE-002 |
| Receptionist flips through papers | Activity | OBS-CLOSE-003 |
| Receptionist says "I think" | Exception | OBS-CLOSE-004 |
| Owner asks "How much did we collect?" | Activity | OBS-CLOSE-005 |
| Owner asks about absences | Activity | OBS-CLOSE-006 |
| Owner writes tomorrow's priorities | Activity | OBS-CLOSE-007 |
| Owner locks office | Activity | OBS-CLOSE-008 |

**Totals:**
- Activities: 42
- Triggers: 7
- Decisions: 1
- Exceptions: 17
- Information: 5

---

## Clustering

Activities were grouped using two tests:

1. **If this disappeared tomorrow, would the academy stop functioning?**
2. **What is different after this finishes?**

The second test is stronger. It forces every operation to transform something.

---

## Business operations — current hypothesis

| # | Operation | Before | After |
|---|-----------|--------|-------|
| 1 | Acquire Student | Interested person | Active student |
| 2 | Manage Fees | Money owed | Money collected |
| 3 | Conduct Class | Scheduled class | Completed class |
| 4 | Assess Learning | Unknown understanding | Known understanding |

**Count: 4**

Each operation transforms something. If nothing changes, it's not an operation — it's an activity or a decision.

---

## Per-operation analysis

### 1 — Acquire Student

**Purpose**

Convert interest into a student attending their first class.

**Trigger**

Someone shows interest — phone call, walk-in, referral, website enquiry.

**Participants**

- Parent
- Student
- Receptionist
- Counsellor
- Accountant
- Owner (when exceptions require approval)

**Inputs**

- Parent name and phone number
- Student name, age, current class
- Course of interest
- How they heard about the academy (sometimes)
- Previous academic records (sometimes)
- First installment payment (sometimes partial)
- Batch availability (may be inaccurate)

**Completed when**

The student is enrolled in a batch, has paid the first installment, and can attend the next class.

**Common exceptions**

- Required documents are missing
- Batch is full or overfull
- Parent wants to negotiate fees
- Accountant is unavailable
- Batch capacity information is inaccurate
- Parent changes mind mid-process
- Counsellor can't answer a question
- Follow-up is forgotten

---

### 2 — Manage Fees

**Purpose**

Ensure the academy receives money owed. This includes defining what students owe, collecting payments, chasing overdue amounts, and handling exceptions.

**Trigger**

Payment due date arrives, or parent walks in to pay, or a fee plan needs to be created.

**Participants**

- Accountant
- Receptionist (when collecting cash)
- Parent
- Owner (for discounts, refunds, policy decisions)

**Inputs**

- Student name and enrollment status
- Fee plan (total amount, installments, due dates)
- Amount paid so far
- Outstanding balance
- Payment mode (cash, UPI, bank transfer)

**Completed when**

Payment is received, receipt is issued, and the ledger is updated. Or: fee plan is created and communicated to the parent.

**Common exceptions**

- Parent doesn't have the full amount
- Parent asks for extension
- Cash doesn't match receipts
- Payment mode is unavailable
- Parent disputes the amount
- Accountant doesn't know the policy on extensions
- Refund is requested
- Discount is requested

---

### 3 — Conduct Class

**Purpose**

Deliver learning to students. A class session is one unit of this: teacher arrives, attendance is taken, lesson is delivered, homework is assigned, class ends.

**Trigger**

Batch start time arrives.

**Participants**

- Teacher
- Students
- Branch manager (when issues arise)

**Inputs**

- Batch schedule and roster
- Lesson plan (sometimes)
- Homework from previous class (sometimes)
- Room allocation

**Completed when**

The class session ends, attendance is recorded, and the lesson is delivered.

**Common exceptions**

- Teacher is absent and no substitute is arranged
- Room is unavailable
- Fewer students than expected attend
- Teacher forgot to prepare lesson plan
- Homework from previous class wasn't checked
- Student disputes attendance record
- Student is absent without notification

---

### 4 — Assess Learning

**Purpose**

Measure what students have learned. Identify who is struggling. Inform parents. This is different from teaching — teaching asks "did we teach?", assessment asks "did they learn?"

**Trigger**

Test date arrives, or teacher decides to assess progress, or a student is flagged for review.

**Participants**

- Teacher
- Students
- Branch manager (for review)
- Parent (for communication)

**Inputs**

- Test papers or assignments
- Answer key or evaluation criteria
- Previous test scores (sometimes)
- Attendance record (sometimes)

**Completed when**

All submissions are evaluated, results are available for review, and struggling students are flagged.

**Common exceptions**

- Students don't submit
- Teacher doesn't evaluate on time
- Results are not communicated to parents
- Low-performing students are flagged but no action is taken
- Results are recorded on sticky notes that get lost
- Parent disagrees with the assessment

---

## Observation hierarchy

Inside each operation, work happens at three levels:

```
Operational Engine
    ↓
Decision
    ↓
Activity
```

Example:

```
Manage Fees
    ↓
Allow installment? (decision)
    ↓
Update fee plan (activity)
```

Example:

```
Conduct Class
    ↓
Should class continue? (decision)
    ↓
Mark attendance (activity)
```

Operational engines transform something. Decisions determine how. Activities carry out the work.

This hierarchy is a hypothesis. It will be validated or broken by future observations.

---

## What survived

4 business operations emerged from 42 observations.

### Operations

1. Acquire Student
2. Manage Fees
3. Conduct Class
4. Assess Learning

### Not operations

- "Review day" — decision support, consumes outputs from all operations
- "Run Academy" — decision context, not a transformation
- "Manage faculty availability" — exception workflow inside Conduct Class
- "Record attendance" — activity inside Conduct Class

---

## Current Understanding

### Validated by observation

- Students make enquiries.
- Counselling happens before admission.
- First payment is collected during enrollment.
- Attendance is recorded during class.
- Tests are conducted and scored.
- Fees follow an installment plan.
- The owner reviews the day.

### Observed but uncertain

- Batch capacity overrides.
- Scholarship approval.
- Payment extensions.
- Attendance dispute resolution.
- Faculty substitution process.
- Cash discrepancy handling.

### Not yet observed

- Dropouts.
- Re-admissions.
- Referrals as a business process.
- Alumni.
- Certificate issuance.
- Course completion.
- Renewals.
- Multi-branch operations.
- Online/hybrid teaching.

---

## Assumptions

### Structural assumptions

- One academy = one branch.
- Every enrollment belongs to one batch.
- The academy operates from a physical location.
- A batch is led by one primary faculty member.

### Workflow assumptions

- Fee collection happens after admission.
- Attendance is recorded once per class.
- Every student has at least one parent or guardian.
- The owner is the final authority on policy decisions.

### Operation scope assumptions

- Acquire Student covers first enquiry to first class only.
- Whether retention, re-admissions, referrals, and alumni belong here remains an open question.

These are not facts. They are assumptions waiting to be validated.

---

## Open Questions

- Is acquiring and retaining students one business operation or two?
- Do referrals belong to acquisition or a separate growth process?
- Is re-admission the same workflow as first admission?
- What happens when a student stops attending classes?
- Under what circumstances does a former student return?
- What purpose does the academy have for tracking alumni, if any?

---

## Next observations

The current understanding is based on one ordinary working day.

To validate or refine this model, observe:

- Admission season
- Examination season
- Course completion
- Student dropout
- Fee default
- New batch creation
- Parent meeting
- Faculty resignation
