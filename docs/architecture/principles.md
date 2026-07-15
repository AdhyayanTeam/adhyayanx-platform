# ADX Engineering Principles

> **This document explains how we make engineering decisions in ADX. It
> intentionally avoids framework- or pattern-specific terminology. If a
> future design conflicts with these principles, the principles win.**

---

## 1. Business services describe business decisions

Business services are responsible for business decisions.

They should not manage database sessions, transactions, framework objects,
or infrastructure details.

They should only:

- Read business data
- Apply business rules
- Request business changes
- Raise business events

---

## 2. Infrastructure supports business logic

Infrastructure is responsible for:

- Starting and finishing work
- Transactions
- Event delivery
- External systems
- Data storage

Business logic should be able to change without infrastructure,
and infrastructure should be able to change without business logic.

---

## 3. Technology should be replaceable

Changing the database, event transport, or framework should not require
changing business rules.

If changing technology requires changing business services, the boundary
is in the wrong place.

---

## 4. Name things by responsibility

Prefer names that describe what something does rather than the
architectural pattern it follows.

---

## 5. Solve today's problem

Introduce abstractions only when they remove an existing problem.

Do not add abstractions for anticipated future needs.

---

## 6. Start with the workflow, not the solution

Before introducing a new abstraction, describe:

- How the work happens today.
- What is difficult or repetitive.
- What the desired workflow should be.

Only then decide whether a new abstraction is needed.

**Patterns are tools, not goals.**

---

## 7. Prefer simple explanations

If a design cannot be explained in plain language,
it is probably too complicated.

Use architectural patterns only when they make the code simpler,
not when they make it sound more sophisticated.

---

## Decision Test

Before introducing a new abstraction, ask:

1. What problem exists today?
2. Can the problem be explained in one paragraph?
3. Will this make the code easier to understand?
4. If we removed this abstraction, what would become harder?

If these questions cannot be answered clearly,
the abstraction probably should not be introduced.
