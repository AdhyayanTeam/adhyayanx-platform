# Academy Domain Invariants

> **Business rules that should hold true across almost all academy
> implementations.** These are not implementation rules. They are the
> constraints of how an academy operates.
>
> **Classification:**
> - **Confirmed** — Survived all stress tests. Treat as stable.
> - **Working** — Currently true but may evolve. Validate in Sprint 2.
> - **Needs Validation** — Likely true but untested against edge cases.

---

## Confirmed Invariants

These have survived every scenario we've tested. Treat as stable.

```
Attendance is recorded for a learning session.

A session belongs to exactly one batch.

A test belongs to exactly one batch.

A receipt is proof of payment for a specific financial transaction.

Communication follows: Business Event → Policy → Channel.
The same event may trigger different policies for different audiences.
New channels can be added without changing the business event.
```

---

## Working Invariants

These are currently true but may evolve as we discover edge cases.

```
A lead is not allocated to a teaching batch.
(Challenge: free demo batches, trial batches, orientation sessions.)

A student progresses through qualification before enrollment.
(Challenge: walk-in students who enroll on the spot.)

A batch belongs to exactly one program/offering.
(Challenge: cross-disciplinary batches, combined JEE+NEET prep.)

The curriculum hierarchy below a program is configurable
(Subject, Module, Level, Paper — depends on institute type).

A guardian is financially responsible for the student.
(Challenge: adult learners who self-pay, working professionals.)
```

---

## Needs Validation

These are likely true but have not been tested against edge cases.

```
Every enrollment has a defined end date.
(Challenge: ongoing tuition, monthly subscription models.)

A student has at most one active enrollment at a time.
(Challenge: student enrolled in both JEE and Foundation simultaneously.)

Fees are always tied to an enrollment, not directly to a student.
(Challenge: one-time workshop fees, test series fees.)

A program has a fixed curriculum that doesn't change mid-cycle.
(Challenge: curriculum updates based on exam pattern changes.)
```

---

## How to Use This Document

Every time Sprint 2 proposes a new concept, ask:

> **Does this violate any invariant?**

If yes:
- Either the concept is wrong, or
- The invariant wasn't actually invariant.

Move the invariant to the appropriate classification.
That's how mature domain models evolve.

---

*Sprint 1 — COMPLETE*
