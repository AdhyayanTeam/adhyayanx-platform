# Academy Domain Decisions

> **Purpose:** Record every important domain decision — what we decided,
> why, and the current status. Six months from now, you'll be able to
> answer *why* a concept exists, not just *what* it is.

> **Format:** Architecture Decision Record (ADR), focused on the domain,
> not the implementation.

---

## Decision #001

**Decision:** Use "Educational Offering" instead of "Program."

**Reason:** "Program" means different things across different institute types.
For coaching institutes, "JEE 2027" is a program. For computer training
institutes, "Full Stack Development" is a program. For language institutes,
"English Speaking Course" is a program. The word "Program" biases toward
formal education and doesn't capture the commercial reality of what is
being sold.

**Status:** Hypothesis

---

## Decision #002

**Decision:** Treat "Offering Variant" as a candidate business concept, not
a finalized one.

**Reason:** Offering Variant (Weekend / Regular / Crash / Online / Offline)
survives three test cases (JEE, IELTS, Full Stack) but breaks for 1:1
personal coaching where there is no variant — the personal coaching itself
is the offering. Need to validate across more institute types before
promoting to core domain.

**Status:** Hypothesis

---

## Decision #003

**Decision:** Model communication as Business Event → Policy → Channel.

**Reason:** Decoupling the trigger (business event) from the delivery
mechanism (channel) allows new channels (email, SMS, voice call) to be
added without changing the business event. Also allows the same event
to trigger different policies for different audiences (parent gets
WhatsApp immediately, teacher gets daily digest).

**Status:** Hypothesis

---

## Decision #004

**Decision:** Rename "Reports" to "Insights & Metrics."

**Reason:** Reports are outputs. Metrics are what the business actually needs.
The function should be named for what it produces (decision-ready information),
not the artifact (a report). This reframes the conversation from "what
reports do we build?" to "what metrics does the business need?"

**Status:** Hypothesis

---

## Decision #005

**Decision:** Operating model verbs (Acquire, Convert, Onboard, etc.) are
not frozen yet.

**Reason:** The current working model is Acquire → Convert → Onboard →
Educate → Measure → Retain → Grow. But after Sprint 2, verbs may change
(e.g., Enroll instead of Convert, Deliver instead of Educate). The verbs
describe the business flow, not the software architecture. They should
be stabilized only after the domain model is validated.

**Status:** Working Draft v1

---

*New decisions are added as they arise. Existing decisions are updated when
status changes. Each decision includes the reasoning so future contributors
understand the "why" behind the "what."*
