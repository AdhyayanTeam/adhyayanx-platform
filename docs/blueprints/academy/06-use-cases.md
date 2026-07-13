# 06 — Use Cases

> **Scope:** Specific business actions the academy performs. Each use case
> belongs to exactly one capability. These are not features — they are
> things the business does, with or without software.
>
> **Rule:** Every document in Sprint 2 must be understandable by a coaching
> institute owner with no software background.

---

## 1. Admissions

The journey from first inquiry to enrolled learner.

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| A1 | Capture lead | Record a new inquiry with name, phone, source, and interest | Workflow 1, Step 2 |
| A2 | Attribute lead | Link lead to marketing source (ad, referral, walk-in, website) | Workflow 1, Step 3 |
| A3 | Route lead | Assign lead to a counsellor based on offering, source quality, capacity | Workflow 1, Step 4 |
| A4 | Follow up | First contact within 24 hours (phone call, WhatsApp, in-person) | Workflow 2, Step 1 |
| A5 | Qualify lead | Assess interest, ability, and timing to determine if lead is viable | Workflow 2, Step 2 |
| A6 | Schedule counselling | Book a demo class or counselling session for the learner and parent | Workflow 2, Step 3 |
| A7 | Conduct demo | Deliver a trial class. Counsellor meets parent after. | Workflow 2, Step 3 |
| A8 | Nurture dormant lead | Keep disengaged leads warm with periodic check-ins and announcements | Workflow 2, Step 6 |
| A9 | Re-engage dormant lead | Bring back a dormant lead when timing changes (new batch, boards ending) | Workflow 2, Step 6 |
| A10 | Record lost lead | Archive a lead that will not convert, with reason (competitor, price, timing) | Workflow 2, Step 2 |
| A11 | Process enrollment | Collect documents, select offering variant, generate fee challan | Workflow 2, Step 5 |
| A12 | Reserve seat | Reserve a seat in a preferred batch (pending academic confirmation) | Workflow 4, Step 2 |

---

## 2. Learner Management

Managing the relationship after admission.

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| L1 | Create learner profile | Establish the learner record with personal details, guardian, enrollment | Workflow 9 |
| L2 | Track lifecycle state | Monitor where the learner is: Active, At Risk, Renewed, Dropped, Suspended | Workflow 9 |
| L3 | Detect at-risk learner | Flag learners with low attendance, declining marks, or overdue fees | Workflow 9 |
| L4 | Trigger intervention | Alert counsellor or manager when a learner is at risk | Workflow 9 |
| L5 | Handle renewal | Process learner's decision to continue for the next term or year | Workflow 9 |
| L6 | Process exit | Handle learner departure — course completed, dropped, or transferred | Workflow 9 |
| L7 | Record referral | Track which existing family referred a new lead | Workflow 9 |

---

## 3. Academic Operations

Delivering the educational product.

### 3.1 Attendance

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| AA1 | Mark attendance | Record present/absent/late for each learner in a class session | Workflow 5, Step 2 |
| AA2 | Detect absence | Flag a learner as absent and trigger notification | Workflow 5, Step 3 |
| AA3 | Flag chronic absence | Escalate when a learner has 3+ consecutive or 75%+ absence rate | Workflow 5, Step 4 |
| AA4 | Review weekly attendance | Manager reviews attendance report for all batches, flags issues | Workflow 5, Step 4 |

### 3.2 Batch Placement

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| AA5 | Confirm placement | Confirm learner placement in a batch based on capacity, teacher, schedule | Workflow 4, Step 2 |
| AA6 | Assign batch | Formally assign learner to a confirmed batch | Workflow 4, Step 2 |
| AA7 | Transfer batch | Move a learner from one batch to another (timing, difficulty, schedule) | Workflow 4, Step 3 |
| AA8 | Waitlist learner | Place learner on waitlist when preferred batch is full | Workflow 4, Step 2 |
| AA9 | Manage batch capacity | Monitor batch sizes, merge underfilled batches, split overcrowded ones | Workflow 4, Step 4 |

### 3.2 Curriculum

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| AC1 | Define curriculum structure | Set up the hierarchy (Subject/Module/Level/Paper) for an offering | Research doc |
| AC2 | Map syllabus to structure | Assign topics/chapters to curriculum units for a batch | Research doc |
| AC3 | Track syllabus progress | Record how much of the planned syllabus has been covered | Workflow 6 |

### 3.3 Assessments

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| AT1 | Plan test | Define test name, syllabus, date, duration, marks | Workflow 6, Step 1 |
| AT2 | Conduct test | Administer the test, collect answer sheets | Workflow 6, Step 2 |
| AT3 | Enter marks | Record marks per learner. Optionally add remarks. | Workflow 6, Step 3 |
| AT4 | Compile results | Calculate batch average, rank, trends, improvement/decline | Workflow 6, Step 4 |
| AT5 | Share results | Send results to parents via the Communication capability | Workflow 6, Step 5 |
| AT6 | Track performance | Review batch performance trends, identify weak and strong learners | Workflow 6, Step 6 |

### 3.4 Teaching Support

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| AS1 | Share study material | Distribute notes, question banks, practice sets to learners | Workflow 6 |
| AS2 | Assign homework | Give practice work to learners between sessions | Workflow 6 |

---

## 4. Financial Management

The financial relationship between institute and family.

### 4.1 Fee Structure

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| FS1 | Create fee plan | Define total fee, installment count, due dates for an offering | Workflow 3, Step 1 |
| FS2 | Apply discount | Offer loyalty, referral, or hardship discount (within policy limits) | Workflow 3 |
| FS3 | Apply scholarship | Reduce fee based on merit or financial need | Workflow 3 |
| FS4 | Define payment plan | Set up installment schedule (full, 2-part, 3-part, 4-part) | Workflow 3, Step 1 |

### 4.2 Collection

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| FC1 | Generate invoice | Create a fee invoice or challan for the learner | Workflow 3, Step 3 |
| FC2 | Collect payment | Receive payment via cash, UPI, card, or bank transfer | Workflow 3, Step 3 |
| FC3 | Generate receipt | Produce an auto-numbered, GST-compliant receipt | Workflow 3, Step 3 |
| FC4 | Send payment reminder | Notify family 3 days before installment due date | Workflow 3, Step 2 |

### 4.3 Outstanding Management

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| FO1 | Track outstanding | Monitor unpaid installments across all learners | Workflow 3 |
| FO2 | Escalate overdue | Escalate through stages: remind → call → suspend → write off | Workflow 3, Step 4 |
| FO3 | Process refund | Handle early dropout — full, pro-rata, or no refund per policy | Workflow 3 |
| FO4 | Generate collection summary | Daily/monthly collection totals for the owner | Workflow 3 |

---

## 5. Communication

Maintaining trust through the right message at the right time.

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| C1 | Send absence alert | Notify parent when learner is marked absent (within 1 hour) | Workflow 7 |
| C2 | Send test result | Share marks, batch average, and rank with parent | Workflow 7 |
| C3 | Send fee reminder | Notify family of upcoming installment due date | Workflow 7 |
| C4 | Announce schedule change | Inform affected batch of timing or room changes | Workflow 7 |
| C5 | Send monthly summary | Deliver attendance + performance report to parents | Workflow 7 |
| C6 | Escalate to manager | Route complaints or sensitive issues to the branch manager | Workflow 7 |
| C7 | Set communication policy | Define what triggers what message to whom (delivery handled by Platform) | Workflow 7 |
| C8 | Manage opt-outs | Allow parents to choose which notifications they receive | Workflow 7 |

---

## 6. Decision Support

Decision-ready information for every stakeholder.

| # | Use Case | Description | Sprint 1 Workflow |
|---|---|---|---|
| I1 | Track enrollment metrics | Leads per channel, conversion rate, CAC per channel | Workflow 8 |
| I2 | Track fee metrics | Revenue collected, outstanding, collection efficiency | Workflow 8 |
| I3 | Track attendance metrics | Batch attendance rates, chronic absentees, trends | Workflow 8 |
| I4 | Track academic performance | Batch averages, toppers, struggling learners, improvement trends | Workflow 8 |
| I5 | Track conversion metrics | Counsellor pipeline, follow-up speed, demo-to-enrollment rate | Workflow 8 |
| I6 | Generate daily summary | Today's enrollments, collections, attendance for the owner/manager | Workflow 8 |
| I7 | Generate monthly report | Revenue trend, enrollment trend, retention rate, staff performance | Workflow 8 |

---

## 7. Use Case Count

| Capability | Use Cases |
|---|---|
| Admissions | 12 |
| Learner Management | 7 |
| Academic Operations | 19 |
| Financial Management | 11 |
| Communication | 8 |
| Decision Support | 7 |
| **Total** | **64** |

---

## 8. Open Questions

1. Should **trial classes** (attending one class before enrolling) be a
   separate use case under Admissions, or is it part of "Conduct demo" (A7)?
2. Should **homework tracking** (checking completion) be a use case, or
   is "Assign homework" (AS2) sufficient?
3. How do institutes handle **course changes** (learner switches from JEE
   to NEET mid-way)? Is this a new enrollment or a transfer?
4. Should **referral tracking** be under Admissions (capture referral source)
   or Learner Management (track referral conversions)?
5. Is **fee plan creation** a one-time event at enrollment, or can it be
   modified mid-course?

---

*Sprint 2 — Use Cases*
