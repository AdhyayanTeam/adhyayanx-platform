# Scenario: Ordinary Working Day

## Purpose

Challenge whether the current operational model explains the work
performed during an ordinary working day.

Current operational model:

1. Enroll Student
2. Manage Fees
3. Conduct Classes
4. Assess Learning

This scenario attempts to find observations that cannot be explained
by the current model.

---

## Timeline

### 8:00 AM

Shutters roll up. Office unlocked.

Owner checks yesterday's collection in the ledger. Three parents
promised to pay, none did. Owner reviews pending payments.

Faculty member called in sick. No replacement arranged.

AC repair person didn't come yesterday. AC still not working.

Owner reads handwritten register. Register not up to date.

Staff reports AC not working to owner.

### 9:00 AM

Phone rings. Parent enrolling child in Class 8. Receptionist answers
from memory. Records enquiry in ledger. Parent asks about scholarships.
Receptionist can't answer. Writes sticky note for follow-up. Sticky
note will be buried by lunchtime.

### 10:00 AM

Parent walks in with child. Counsellor asks for documents. Parent
forgot Aadhaar. Counsellor asks owner for permission. Owner approves
with condition: Aadhaar pending. Counsellor writes "Aadhaar pending."
Fills admission form. Parent asks about fees. Counsellor explains fee
structure. They wait for accountant.

### 10:30 AM

Accountant arrives. Takes cash. Writes receipt. Counsellor checks
whiteboard for batch capacity. Whiteboard says 38, owner said 44.
Counsellor writes name on board. Admission complete after 45 minutes.
Aadhaar still missing, no one tracking.

### 11:00 AM

Batch begins. Teacher opens attendance register. Calls name. Student
absent. Teacher marks absent. No one calls parent.

### 11:15 AM

Student says he was present. Teacher checks register. No way to
verify. Teacher says "I'll fix it next time." Student frustrated.

### 11:30 AM

Teacher begins lesson. Student asks about homework. Teacher forgot to
check homework. Writes note to self.

### 2:00 PM

Teacher reviews test papers. Three students scored below 50%. Teacher
writes names on sticky note. Sticky note will fall off.

### 4:00 PM

Accountant sits with day's collection. Four parents paid today.
Accountant opens ledger. Writes in ledger. Calculates balance by hand.

### 4:30 PM

Student's installment was due last week. Accountant calls parent. No
answer. Sends WhatsApp message. Parent asks to pay next month.
Accountant doesn't know policy.

### 5:00 PM

Receptionist hands cash to accountant. Accountant counts cash. Cash
is 500 short. Receptionist checks records. Missing piece of paper.
Accountant notes discrepancy.

### 5:30 PM

Last batch leaves. Owner asks "How many admissions?" Receptionist
flips through papers. Says "I think." Owner asks "How much did we
collect?" Owner asks about absences. Owner writes tomorrow's
priorities. Owner locks office.

---

## Evidence Analysis

| Observation | Classification | Notes |
|-------------|---------------|-------|
| Shutters roll up | Opening | Not a transformation |
| Owner checks collection | Decision Making | Consumes outputs |
| Owner reviews pending payments | Decision Making | Consumes outputs |
| Faculty sick, no replacement | Conduct Classes | Exception handling |
| AC broken → AC repaired | Outside Model | More evidence required |
| Owner reads register | Decision Making | Consumes outputs |
| Register not up to date | Information Quality | Data exists but is stale |
| Staff reports AC issue | Outside Model | More evidence required |
| Phone enquiry | Enroll Student | Core activity |
| Enquiry recorded in ledger | Enroll Student | Core activity |
| Scholarship question | Enroll Student | Core activity |
| Can't answer | Knowledge Gap | Policy or guidance missing |
| Sticky note for follow-up | Information Gap | Unreliable tracking method |
| Parent walks in | Enroll Student | Core activity |
| Documents requested | Enroll Student | Core activity |
| Aadhaar forgotten | Enroll Student | Exception - missing document |
| Owner approval for exception | Enroll Student | Decision within operation |
| Admission form filled | Enroll Student | Core activity |
| Fee structure explained | Enroll Student | Core activity |
| Waiting for accountant | Enroll Student | Exception - resource unavailable |
| Cash taken | Manage Fees | Core activity |
| Receipt written | Manage Fees | Core activity |
| Batch capacity checked | Enroll Student | Core activity |
| Whiteboard says 38, owner says 44 | Information Quality | Data is inconsistent |
| Name written on board | Enroll Student | Core activity |
| Admission complete | Enroll Student | Core activity |
| Aadhaar still missing | Information Gap | Item not tracked |
| Attendance marked | Conduct Classes | Core activity |
| Student absent | Conduct Classes | Core activity |
| No parent notification | Conduct Classes | Exception - process gap |
| Student disputes attendance | Conduct Classes | Exception - verification gap |
| No verification possible | Information Gap | No audit trail exists |
| Teacher forgets homework check | Conduct Classes | Exception - human error |
| Note written to self | Information Gap | Unreliable tracking method |
| Test papers reviewed | Assess Learning | Core activity |
| Three students below 50% | Assess Learning | Core activity |
| Names on sticky note | Information Gap | Unreliable tracking method |
| Day's collection counted | Manage Fees | Core activity |
| Ledger updated | Manage Fees | Core activity |
| Balance calculated by hand | Manage Fees | Core activity |
| Overdue installment called | Manage Fees | Core activity |
| Parent doesn't answer | Manage Fees | Exception - contact failure |
| WhatsApp sent | Manage Fees | Core activity |
| Parent asks for extension | Manage Fees | Exception - policy question |
| Accountant doesn't know policy | Knowledge Gap | Policy or guidance missing |
| Cash handed to accountant | Manage Fees | Core activity |
| Cash counted | Manage Fees | Core activity |
| Cash is 500 short | Manage Fees | Exception - discrepancy |
| Discrepancy noted | Information Quality | Issue documented but unresolved |
| Owner asks for numbers | Decision Making | Consumes outputs |
| Receptionist flips through papers | Information Gap | Data not accessible |
| Owner writes priorities | Decision Making | Consumes outputs |
| Owner locks office | Closing | Not a transformation |

---

## Patterns observed

### Information problems

Three distinct types emerged:

**Information Gap** — Information doesn't exist or can't be found.

- Sticky note for follow-up (will be buried)
- Aadhaar still missing (no one tracking)
- No way to verify attendance (no audit trail)
- Note written to self (will be forgotten)
- Names on sticky note (will fall off)
- Receptionist flips through papers (data not accessible)

**Knowledge Gap** — The person doesn't know what decision to make
because policy or guidance is missing.

- Can't answer scholarship question
- Accountant doesn't know extension policy

**Information Quality** — Information exists but is stale,
inconsistent, or unreliable.

- Register not up to date
- Whiteboard says 38, owner says 44
- Discrepancy noted but unresolved

### Decision Making

Owner's daily review activities:

- Checking yesterday's collection
- Reviewing pending payments
- Asking "How many admissions?"
- Asking "How much did we collect?"
- Writing tomorrow's priorities

These consume outputs from all operations. They're not
transformations — they're what the owner does to decide what
matters today.

### Outside model

Facility maintenance:

- AC broken → AC repaired

Outside current operational model. More evidence required.

---

## What did not fit?

**Facility maintenance** — AC repair, equipment issues.

Outside current operational model. More evidence required.

**Decision making** — Owner's daily review, checking numbers,
setting priorities.

Outside current operational model. Consumes outputs from operations.

---

## Questions raised

- Should facility maintenance be a separate operation?
  Or is it an activity that happens alongside operations?

- Who handles facility issues when the owner isn't there?
  Is there a process, or does it depend on who happens to be around?

- The owner's daily review consumes information from all operations.
  Is this a cross-cutting concern, or a separate operation?

- When the receptionist hands cash to the accountant, is that
  Manage Fees or a separate cash handling process?

- Why are there so many information problems?
  Is the current tooling (ledger, whiteboard, sticky notes)
  fundamentally insufficient?

- What would the business look like if answers were inexpensive?
  How many of these problems disappear if information is
  always current and accessible?

---

## Verdict

Current operational model explains all business transformations
observed during this scenario.

Several observations fall outside the model, but none currently
require expanding it. These observations will be monitored in
future scenarios.

---

## Evidence

### Evidence Status

Current operational model: Revision 1

Scenarios analysed: 1

Business contexts observed:

- Ordinary working day

Outstanding contexts:

- Admission season
- Examination week
- Student dropout
- Faculty resignation
- Fee default

Model stability: Unknown

---

## Model changes

None.
