# Working Glossary

> **Status:** All definitions are working definitions. They may evolve as
> Sprint 2 progresses. Do not treat as final.

> **Maintained throughout every sprint.** New terms are added as they appear.
> Existing terms are updated when our understanding deepens.

---

## People

| Term | Working Definition | Status |
|---|---|---|
| Lead | Any human who has expressed interest, regardless of source or quality | Candidate |
| Prospect | A lead that has been qualified (interested + ability + timing) | Candidate |
| Applicant | A prospect in the enrollment process — documents submitted, fee pending | Candidate |
| Student | An enrolled, fee-paid, batch-assigned individual | Stable |
| Guardian | Person making financial decisions for the student; may differ from parent | Candidate |
| Owner | Person who founded or owns the institute; strategic decision-maker | Stable |
| Branch | A physical location where the institute operates | Stable |
| Staff | Anyone employed by the institute (manager, counsellor, teacher, accountant, receptionist) | Stable |

---

## Educational Structure

| Term | Working Definition | Status |
|---|---|---|
| Educational Offering | A broad learning experience advertised to the market (e.g., "JEE 2027", "IELTS Prep", "Full Stack Development") | Candidate — replaces "Program" to avoid bias |
| Offering Variant | A delivery format of an educational offering (Weekend / Regular / Crash / Online / Offline) | Candidate — survives 3 test cases, not yet core; may collapse into Educational Offering for some institute types |
| Curriculum | The structured body of knowledge within an offering; the hierarchy between Educational Offering and Batch | Candidate — hierarchy unresolved; see `research/curriculum-hierarchy.md` |
| Batch | A group of learners learning together at a fixed schedule; belongs to a specific Offering Variant | Candidate |
| Session | A single class meeting — one teacher, one topic, one time slot | Candidate |

**Open questions:**
- What is the curriculum hierarchy? (See `research/curriculum-hierarchy.md`)
- What is the smallest unit of learning the institute manages?
- Does "Course" or "Subject" map to a real business concept, or are they implementation words?

---

## Commercial

| Term | Working Definition | Status |
|---|---|---|
| Commercial Unit | What the customer actually purchases; may be Educational Offering, Offering Variant, Batch, Seat, or Subscription | **Open research question** |
| CAC | Cost of acquiring one enrolled student (marketing spend / enrollments) | Stable |
| Attribution | Which channel/source produced the lead | Stable |
| Fee Schedule | The installment plan agreed at enrollment | Candidate |
| Receipt | Proof of payment; GST-compliant; auto-numbered | Stable |

---

## Lifecycle

| Term | Working Definition | Status |
|---|---|---|
| Lead → Prospect → Applicant → Student | The progression of a human through the academy's relationship model | Candidate — lifecycle may have more or fewer states |
| Dormant | A lead or student who has disengaged but not formally exited | Candidate |
| Re-engaged | A dormant lead or student who has returned to active interaction | Candidate |
| Dropped | A student who has left without completing the course; exit reason recorded | Candidate |
| Renewed | A student who has committed to the next course or term | Candidate |

---

## Operations

| Term | Working Definition | Status |
|---|---|---|
| Academic Year | The annual cycle within which the institute operates (e.g., April–March) | Candidate — temporal dimension |
| Admission Window | The period during which new enrollments are actively pursued | Candidate — temporal dimension |
| Term / Semester | A subdivision of the academic year (may not exist in all institute types) | Candidate — temporal dimension |
| Course Duration | The length of a specific educational offering (e.g., 12 months, 6 weeks) | Candidate — temporal dimension |
| Holiday Calendar | Days when the institute is closed; affects scheduling and attendance | Candidate — temporal dimension |
| Exam Window | Scheduled periods for formal assessments | Candidate — temporal dimension |
| Fee Cycle | The rhythm of fee collection (monthly, quarterly, per installment) | Candidate — temporal dimension |
| Renewal Cycle | The period when students decide to continue or exit | Candidate — temporal dimension |

**Open questions:**
- Which of these temporal concepts are universal across institute types?
- Which are specific to certain institute types?
- What is the relationship between Academic Year and Term/Semester in institutes that don't follow a school calendar?

---

## Communication

| Term | Working Definition | Status |
|---|---|---|
| Business Event | Something that happens in the institute that may trigger communication (absence, fee due, test result) | Candidate |
| Communication Policy | The rule that determines what happens when a business event occurs (who gets notified, when, how urgently) | Candidate |
| Channel | The delivery mechanism for a communication (WhatsApp, SMS, Email, Voice Call, In-App) | Candidate |

---

## Terminology Notes

- **"Program"** avoided in favor of **"Educational Offering"** — "Program" means different things across institute types and biases the model toward formal education.
- **"Course"** and **"Subject"** treated as implementation words, not business concepts — see research note.
- **"Offering"** is a working hypothesis — may collapse into Educational Offering or become a first-class concept.
- **"Reports"** renamed to **"Insights & Metrics"** — reports are outputs; metrics are what the business needs.

---

*This glossary is maintained across every sprint. Terms are added as they appear.
Definitions evolve as our understanding deepens.*
