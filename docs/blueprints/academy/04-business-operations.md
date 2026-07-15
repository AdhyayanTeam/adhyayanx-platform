# Business Operations

> **Purpose of this document**
>
> This document lists the work an academy performs. Each operation
> represents one complete business outcome, independent of how software
> implements it.

---

## Admissions

```
Receive enquiry
    ↓
Follow up enquiry
    ↓
Schedule counselling
    ↓
Conduct counselling
    ↓
Admit student
    ↓
Collect first payment
    ↓
Assign batch
    ↓
Track pending documents
```

---

### Receive enquiry

**Purpose**

A potential student or parent contacts the academy with questions.

**Trigger**

Phone call, walk-in, website form, or referral.

**People involved**

- Receptionist
- Parent or student

**Information required**

- Name
- Phone number
- Course of interest
- How they heard about the institute

**Success**

Enquiry is recorded with enough detail to follow up.

**Failure**

- Parent doesn't leave contact information
- Receptionist forgets to record the enquiry
- Source of enquiry is not captured

**Business rules**

- Every enquiry must be recorded on the same day.
- The receptionist must capture the source (walk-in, phone, referral,
  website).
- If the receptionist cannot answer a question, a callback must be
  promised within24 hours.

---

### Follow up enquiry

**Purpose**

Re-engage a potential student or parent who has not yet enrolled.

**Trigger**

Follow-up date arrives, or parent calls back.

**People involved**

- Counsellor
- Parent or student

**Information required**

- Previous enquiry details
- Date of last contact
- Reason for follow-up

**Success**

Parent agrees to visit or attend a counselling session.

**Failure**

- Parent doesn't answer
- Parent has already enrolled elsewhere
- Follow-up was never scheduled

**Business rules**

- Every enquiry must be followed up within3 days.
- If the parent doesn't answer after3 attempts, the enquiry is
  marked dormant.
- Dormant enquiries are revisited during seasonal peaks (April–June,
  October–December).

---

### Schedule counselling

**Purpose**

Set a meeting between a counsellor and a potential student/parent.

**Trigger**

Parent agrees to visit after a follow-up.

**People involved**

- Counsellor
- Receptionist
- Parent or student

**Information required**

- Preferred date and time
- Parent and student names
- Course of interest

**Success**

Counselling session is scheduled and confirmed.

**Failure**

- Parent doesn't show up
- Counsellor is unavailable
- Time slot conflicts with batch schedule

**Business rules**

- Counselling must be offered within7 days of the first enquiry.
- If the parent misses the session, a follow-up must be attempted
  within2 days.

---

### Conduct counselling

**Purpose**

Explain courses, fees, schedule, and batch details to a potential
student and parent.

**Trigger**

Parent and student arrive for the scheduled session.

**People involved**

- Counsellor
- Parent
- Student

**Information required**

- Available courses and their fees
- Batch timings and availability
- Faculty credentials
- Past results (if available)

**Success**

Parent agrees to enrol the student.

**Failure**

- Parent decides not to enrol
- Parent wants to think about it
- Course or timing doesn't suit the student

**Business rules**

- The counsellor must explain the full fee structure, including
  installment options.
- The counsellor must show batch availability honestly — do not
  promise a seat in a full batch.
- If the parent asks for a discount, the counsellor must check with
  the owner.

---

### Admit student

**Purpose**

Register a new student in the academy.

**Trigger**

Parent agrees to enrol and provides required documents.

**People involved**

- Counsellor
- Receptionist
- Accountant
- Parent
- Student

**Information required**

- Student name, date of birth, address
- Parent/guardian name, phone number, address
- Previous school and class
- Course and batch
- Documents: previous marksheet, passport-size photos, Aadhaar card
  (or equivalent ID)

**Success**

Student is registered, first fee is collected, student is assigned
to a batch.

**Failure**

- Required documents are missing
- Batch is full
- First payment is not made
- Parent changes their mind mid-process

**Business rules**

- Admission is not complete until the first fee installment is
  collected.
- If documents are missing, the admission can proceed with owner
  approval, but the missing document must be tracked.
- The parent must receive a receipt for the first payment.
- The student must be assigned to a batch before leaving the premises.

---

### Assign batch

**Purpose**

Place a newly admitted student in the correct batch.

**Trigger**

Admission is complete.

**People involved**

- Counsellor
- Receptionist

**Information required**

- Course and subject
- Available batches and their timings
- Current batch capacity
- Student's preferred timing (if any)

**Success**

Student is added to the batch and knows when to attend.

**Failure**

- All batches for the course are full
- Student's preferred timing has no available batch
- Batch capacity is exceeded

**Business rules**

- A batch may not exceed its stated capacity without owner approval.
- If the batch is full, the student must be placed on a waitlist or
  offered an alternative timing.
- The student must be told which batch they are in and when their
  first class is.

---

### Track pending documents

**Purpose**

Ensure all required documents are collected after admission.

**Trigger**

Admission is completed with missing documents.

**People involved**

- Receptionist
- Parent

**Information required**

- List of documents required for the course
- Documents already received
- Documents still pending

**Success**

All required documents are received and filed.

**Failure**

- Parent never delivers the documents
- No one follows up

**Business rules**

- Pending documents must be tracked until received.
- A follow-up reminder must be sent within7 days.
- If documents are not received within30 days, the owner must be
  notified.

---

## Teaching

```
Start class
    ↓
Record attendance
    ↓
Resolve attendance dispute
    ↓
Deliver lesson
    ↓
Assign homework
    ↓
Evaluate homework
    ↓
Record test scores
    ↓
Flag struggling students
```

---

### Start class

**Purpose**

Begin a scheduled teaching session.

**Trigger**

Batch start time arrives.

**People involved**

- Faculty
- Students

**Information required**

- Batch schedule
- Room allocation
- Today's lesson plan

**Success**

Class begins on time with the expected students.

**Failure**

- Faculty is absent and no substitute is arranged
- Room is occupied or unavailable
- Fewer students than expected attend

**Business rules**

- If faculty is absent, the branch manager must be notified
  immediately.
- If a substitute is available, the class must not be cancelled.
- If the class is cancelled, students and parents must be notified.

---

### Record attendance

**Purpose**

Mark which students are present in a class session.

**Trigger**

Class begins.

**People involved**

- Faculty

**Information required**

- Batch roster
- Student names

**Success**

Attendance is recorded for every student in the batch.

**Failure**

- Faculty forgets to take attendance
- Attendance is recorded inaccurately
- Student disputes the record

**Business rules**

- Attendance must be recorded at the start of every class.
- Absent students must be flagged for follow-up.

---

### Resolve attendance dispute

**Purpose**

Address a situation where a student claims the attendance record
is wrong.

**Trigger**

Student or parent raises a dispute.

**People involved**

- Faculty
- Branch manager (if needed)
- Student
- Parent (if needed)

**Information required**

- Attendance record for the disputed date
- Any corroborating evidence (other students, teacher recollection)

**Success**

The dispute is resolved and the record is corrected if necessary.

**Failure**

- Neither party can prove their case
- The record is corrected without verification
- The dispute escalates to the owner

**Business rules**

- Attendance corrections require branch manager approval.
- A correction log must be maintained — who corrected, when, why.
- If the same student disputes attendance more than3 times in a
  term, the owner must be notified.

---

### Assign homework

**Purpose**

Give students practice work to complete outside of class.

**Trigger**

End of a lesson.

**People involved**

- Faculty
- Students

**Information required**

- Today's lesson topic
- Homework content
- Due date

**Success**

Students know what to do and when it's due.

**Failure**

- Faculty forgets to assign homework
- Students don't understand the assignment
- Due date conflicts with a holiday

**Business rules**

- Homework must be relevant to the current lesson.
- Due dates must not fall on holidays.

---

### Evaluate homework

**Purpose**

Check and provide feedback on student homework submissions.

**Trigger**

Due date arrives.

**People involved**

- Faculty

**Information required**

- Homework submissions
- Answer key or evaluation criteria

**Success**

All submissions are evaluated and returned.

**Failure**

- Students don't submit
- Faculty doesn't evaluate on time
- No feedback is given

**Business rules**

- Homework must be evaluated within3 days of submission.
- Students who don't submit must be flagged.

---

### Record test scores

**Purpose**

Enter student marks after a test or examination.

**Trigger**

Test papers are evaluated.

**People involved**

- Faculty
- Branch manager (for review)

**Information required**

- Student names
- Test paper or subject
- Marks obtained
- Maximum marks

**Success**

Scores are recorded and available for review.

**Failure**

- Scores are recorded inaccurately
- Scores are not communicated to parents
- Scores are lost (paper-based)

**Business rules**

- Test scores must be recorded within7 days of the test.
- Parents must be informed of test results within14 days.

---

### Flag struggling students

**Purpose**

Identify students who are performing below expectations and need
intervention.

**Trigger**

Test results, attendance patterns, or faculty observation.

**People involved**

- Faculty
- Branch manager
- Owner (if needed)
- Parent (if needed)

**Information required**

- Test scores over time
- Attendance record
- Faculty observations

**Success**

The student receives additional support (extra classes, parent meeting,
tutor assignment).

**Failure**

- The student is flagged but no action is taken
- The flag is lost (sticky note falls off)
- The parent is not informed

**Business rules**

- A student scoring below50% on2 consecutive tests must be flagged.
- A student missing5 consecutive classes must be flagged.
- Flagged students must be reviewed by the branch manager weekly.

---

## Finance

```
Collect fee
    ↓
Issue receipt
    ↓
Follow up overdue fee
    ↓
Negotiate payment terms
    ↓
Approve discount
    ↓
Process refund
    ↓
Reconcile cash
    ↓
Record discrepancy
```

---

### Collect fee

**Purpose**

Receive payment from a student or parent.

**Trigger**

Payment due date arrives, or parent pays in person.

**People involved**

- Accountant
- Receptionist
- Parent

**Information required**

- Student name
- Fee plan and installment number
- Amount due
- Payment mode (cash, UPI, bank transfer)

**Success**

Payment is received and recorded.

**Failure**

- Parent doesn't have the full amount
- Payment mode is unavailable
- Parent wants to negotiate terms

**Business rules**

- Payment must be recorded on the same day.
- Cash must be counted in the presence of the payer when possible.
- UPI and bank transfer payments must be verified before the receipt
  is issued.

---

### Issue receipt

**Purpose**

Provide proof of payment to the parent.

**Trigger**

Payment is received.

**People involved**

- Accountant
- Parent

**Information required**

- Student name
- Amount paid
- Payment date
- Payment mode
- Receipt number
- Remaining balance

**Success**

Parent receives a receipt with all details.

**Failure**

- Receipt book is empty
- Receipt is filled out incorrectly
- Parent doesn't take the receipt

**Business rules**

- A receipt must be issued for every payment, no exceptions.
- The receipt must show the remaining balance after payment.
- Duplicate copies must be maintained (institute copy and parent copy).

---

### Follow up overdue fee

**Purpose**

Contact parents who have missed a payment deadline.

**Trigger**

Installment due date passes without payment.

**People involved**

- Accountant
- Parent

**Information required**

- Student name
- Installment number
- Amount due
- Due date
- Days overdue

**Success**

Parent commits to a payment date.

**Failure**

- Parent doesn't answer
- Parent asks for more time
- Parent disputes the amount

**Business rules**

- First reminder must be sent on the day after the due date.
- Second reminder must be sent7 days after the due date.
- If no response after14 days, the owner must be notified.
- If no payment after30 days, the student may be suspended from
  classes (owner decides).

---

### Negotiate payment terms

**Purpose**

Handle a situation where a parent asks to change the payment schedule.

**Trigger**

Parent requests a delay, partial payment, or alternate arrangement.

**People involved**

- Accountant
- Owner (for approval)
- Parent

**Information required**

- Current fee plan
- Amount paid so far
- Amount outstanding
- Parent's proposed alternative

**Success**

A new arrangement is agreed upon and documented.

**Failure**

- Owner rejects the proposal
- Parent cannot commit to a new date
- Terms are agreed but not documented

**Business rules**

- The accountant cannot approve term changes without owner approval.
- Every change must be documented in writing (even a WhatsApp message).
- The fee plan must be updated to reflect the new arrangement.

---

### Approve discount

**Purpose**

Grant a fee reduction to a student or parent.

**Trigger**

Parent requests a discount, or owner decides to offer one.

**People involved**

- Owner
- Accountant
- Parent

**Information required**

- Student name
- Original fee amount
- Requested discount amount or percentage
- Reason for discount

**Success**

Discount is approved, fee plan is updated, parent is informed.

**Failure**

- Discount is rejected
- Discount is approved but not recorded
- Fee plan is not updated

**Business rules**

- Discounts above10% require owner approval.
- All discounts must be documented with a reason.
- Discounts must be reflected in the fee plan before the next
  payment is due.

---

### Process refund

**Purpose**

Return money to a student who is leaving mid-course.

**Trigger**

Student drops out or is expelled.

**People involved**

- Accountant
- Owner
- Parent

**Information required**

- Student name
- Fee plan and total paid
- Refund policy
- Reason for leaving

**Success**

Refund is calculated correctly, approved, and paid to the parent.

**Failure**

- Refund amount is disputed
- Refund is delayed
- Fee plan doesn't reflect the refund

**Business rules**

- Refunds must follow the published refund policy.
- Refunds above a threshold require owner approval.
- A refund receipt must be issued.
- The student's enrollment status must be updated.

---

### Reconcile cash

**Purpose**

Verify that physical cash matches recorded receipts.

**Trigger**

End of day, or when cash bundle is handed over.

**People involved**

- Accountant
- Receptionist

**Information required**

- Cash received
- Receipts issued
- Any manual notes about unrecorded payments

**Success**

Cash matches receipts exactly.

**Failure**

- Cash is short
- Cash is over
- Source of discrepancy cannot be identified

**Business rules**

- Cash must be reconciled daily.
- Discrepancies must be reported to the owner on the same day.
- If a discrepancy cannot be resolved, it must be documented with
  all available information.

---

### Record discrepancy

**Purpose**

Document a cash or receipt mismatch when the cause is unknown.

**Trigger**

Cash reconciliation reveals a difference.

**People involved**

- Accountant
- Receptionist (if involved)

**Information required**

- Expected amount
- Actual amount
- Difference
- Possible causes
- Actions taken

**Success**

The discrepancy is documented and the owner is notified.

**Failure**

- The discrepancy is ignored
- No documentation is created
- The same discrepancy recurs without investigation

**Business rules**

- Every discrepancy must be recorded, even if small.
- The owner must be notified on the same day.
- If the same discrepancy recurs3 times, an investigation is
  required.

---

## Operations

```
Arrange faculty substitution
    ↓
Move student to another batch
    ↓
Handle complaint
    ↓
Review daily numbers
    ↓
Close the day
```

---

### Arrange faculty substitution

**Purpose**

Find a replacement when a faculty member is unavailable.

**Trigger**

Faculty member calls in sick or is otherwise unavailable.

**People involved**

- Branch manager
- Owner (if needed)
- Substitute faculty

**Information required**

- Which batches are affected
- Available substitutes
- Time of the class

**Success**

A substitute is found and the class is not cancelled.

**Failure**

- No substitute is available
- The class is cancelled without notifying students
- The substitute is not prepared

**Business rules**

- Substitution must be arranged at least1 hour before the class.
- Students must be notified if a substitute is teaching.
- If no substitute is available, the class must be rescheduled and
  students notified.

---

### Move student to another batch

**Purpose**

Transfer a student from one batch to another.

**Trigger**

Student or parent requests a change, or owner decides to rebalance.

**People involved**

- Branch manager
- Receptionist
- Student
- Parent (if minor)

**Information required**

- Current batch
- Requested batch
- Reason for transfer
- Available seats in the target batch

**Success**

Student is moved, attendance records are updated, student knows their
new schedule.

**Failure**

- Target batch is full
- Schedule conflicts with student's other commitments
- Records are not updated

**Business rules**

- Transfers require branch manager approval.
- The target batch must have available seats (or owner approval to
  exceed capacity).
- Attendance records must reflect the transfer date.
- The student must be told their new batch timing immediately.

---

### Handle complaint

**Purpose**

Address a concern raised by a student, parent, or staff member.

**Trigger**

Complaint is received (in person, phone, WhatsApp, etc.).

**People involved**

- Owner or branch manager
- Complainant
- Relevant staff member

**Information required**

- Nature of the complaint
- Who is involved
- When it happened
- What resolution is expected

**Success**

Complaint is acknowledged, investigated, and resolved.

**Failure**

- Complaint is ignored
- Resolution is not communicated
- Same complaint recurs

**Business rules**

- Every complaint must be acknowledged within24 hours.
- The complainant must be told what action will be taken.
- If the complaint involves staff, the staff member must be informed.
- Recurring complaints must be escalated to the owner.

---

### Review daily numbers

**Purpose**

Assess how the day went based on key metrics.

**Trigger**

End of the working day.

**People involved**

- Owner
- Branch manager
- Accountant

**Information required**

- Number of admissions today
- Total fees collected
- Number of absences
- Pending payments
- Complaints received
- Faculty availability for tomorrow

**Success**

Owner has a clear picture of the day and sets priorities for tomorrow.

**Failure**

- Numbers are approximate or incomplete
- Priorities are not documented
- Priorities are not followed up the next day

**Business rules**

- Daily review must happen before the office closes.
- Tomorrow's priorities must be written down (not just remembered).
- If key numbers are unavailable, the owner must flag the data gap.

---

### Close the day

**Purpose**

End operations and prepare for the next working day.

**Trigger**

Last batch leaves.

**People involved**

- Owner
- Receptionist
- Accountant

**Information required**

- Cash collected and reconciled
- Attendance records completed
- Any pending items for tomorrow

**Success**

Office is secured, cash is stored, pending items are documented.

**Failure**

- Cash is not stored securely
- Pending items are forgotten
- Attendance records are incomplete

**Business rules**

- Cash must be stored in the designated secure location.
- The receptionist must confirm all students have left.
- Pending items for tomorrow must be written down before leaving.

---

## How often each operation happens

### Every day

- Record attendance
- Collect fee
- Issue receipt
- Reconcile cash
- Close the day

### Several times a week

- Receive enquiry
- Follow up enquiry
- Record test scores

### Weekly

- Flag struggling students
- Review daily numbers (aggregate)
- Follow up overdue fees (batch reminders)

### Monthly

- Arrange faculty substitution (aggregate planning)
- Handle complaints (review patterns)
- Process refunds

### Seasonally (April–June, October–December)

- Conduct admissions at scale
- Assign batches (new term)
- Create fee plans
- Launch marketing campaigns
- Negotiate payment terms (bulk)

### Yearly

- Create academic calendar
- Review and update fee structures
- Assess faculty performance
- Plan new courses
