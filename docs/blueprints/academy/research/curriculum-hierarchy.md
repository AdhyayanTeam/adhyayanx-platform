# Research: Curriculum Hierarchy

> **Purpose:** How do different educational businesses organize knowledge?
> Is there a common abstraction, or does each type invent its own?

> **Status:** Research complete. Findings documented. Abstraction proposed
> but not finalized.

---

## 1. Institute Types Studied

### 1.1 Coaching Institutes (JEE/NEET/UPSC)

**Example:** Allen Career Institute, Aakash, Prerna Education

**Hierarchy observed:**

```
JEE 2027 (the thing advertised)
  ├── Physics
  │     ├── Thermodynamics
  │     ├── Mechanics
  │     ├── Optics
  │     └── ...
  ├── Chemistry
  │     ├── Organic
  │     ├── Inorganic
  │     └── Physical
  └── Mathematics
        ├── Algebra
        ├── Calculus
        └── Coordinate Geometry
```

**What they call the layers:**

| Layer | What Allen calls it | What Aakash calls it |
|---|---|---|
| Top | "Course" (Nurture, Enthusiast, Leader) | "Course" (Class 11, Class 12, Dropper) |
| Middle | "Subject" (Physics, Chemistry, Biology) | "Subject" |
| Bottom | Topics within subject | Topics within subject |

**Key insight:** The top layer is NOT the curriculum. It is the **entry point**
or **program variant**. "Nurture" = join after Class 10. "Enthusiast" = join
after Class 11. "Leader" = dropper year. The curriculum (Physics, Chemistry,
Math) is the SAME across all three. Only the pacing and depth differ.

**So the real structure is:**

```
Educational Offering (JEE 2027)
  ├── Entry Variant (Nurture / Enthusiast / Leader)
  │     └── defines: starting point, pacing, duration
  ├── Subject (Physics, Chemistry, Math)
  │     ├── Chapter (Thermodynamics, Mechanics)
  │     │     └── Topic (Heat Transfer, Laws of Thermodynamics)
  │     └── ...
  └── Batch (Morning, Evening)
        └── Session (Today's class on Heat Transfer)
```

**"Course" is NOT a curriculum layer.** It is a commercial label for a
specific entry variant. Allen sells "Nurture Course" and "Enthusiast Course"
— these are different priced products with different durations, not different
curricula.

---

### 1.2 Computer Training Institutes

**Example:** CDMI, NIIT (historically), local coding bootcamps

**Hierarchy observed:**

```
Full Stack Development (the thing advertised)
  ├── HTML/CSS
  ├── JavaScript
  ├── React
  ├── Node.js
  ├── Database
  └── DevOps
```

**What they call the layers:**

| Layer | What they call it |
|---|---|
| Top | "Course" (Full Stack Development) |
| Middle | "Module" (HTML, CSS, JavaScript, React) |
| Bottom | "Topic" or "Lesson" within module |

**Key insight:** The middle layer is called "Module" here, not "Subject."
But structurally it is the same concept — a grouping of related knowledge
units within the broader offering.

**The structure is:**

```
Educational Offering (Full Stack Development)
  ├── Module (HTML/CSS, JavaScript, React, Node)
  │     ├── Topic (Selectors, Flexbox, Grid)
  │     └── ...
  └── Batch (Batch A, Batch B)
        └── Session (Today's class on Flexbox)
```

**There is no "entry variant" like coaching.** Students join at the
beginning and progress linearly. The offering has a fixed start and end.

---

### 1.3 Language Institutes

**Example:** British Council, local English speaking institutes

**Hierarchy observed:**

```
English Speaking Course (the thing advertised)
  ├── Level A1 (Beginner)
  ├── Level A2 (Elementary)
  ├── Level B1 (Intermediate)
  ├── Level B2 (Upper Intermediate)
  ├── Level C1 (Advanced)
  └── Level C2 (Proficient)
```

**Within each level, organized by skill:**

```
Level B1 (Intermediate)
  ├── Listening
  ├── Reading
  ├── Writing
  └── Speaking
```

**What they call the layers:**

| Layer | What British Council calls it |
|---|---|
| Top | "Course" or "Program" |
| Middle | "Level" (A1–C2 per CEFR framework) |
| Sub-layer | "Skill" (Listening, Reading, Writing, Speaking) |
| Bottom | "Lesson" or "Session" |

**Key insight:** The middle layer here is NOT a subject or module — it is a
**proficiency level.** The hierarchy has an EXTRA dimension: Level contains
Skills, and Skills contain Lessons. This is fundamentally different from
coaching or computer training.

**The structure is:**

```
Educational Offering (English Speaking)
  ├── Level (A1, A2, B1, B2, C1, C2)
  │     ├── Skill (Listening, Reading, Writing, Speaking)
  │     │     └── Lesson (Topic: Formal Letter Writing)
  │     └── ...
  └── Batch (Morning Batch, Weekend Batch)
        └── Session (Today's class on Letter Writing)
```

**The "commercial unit" here is the Level.** Students buy "B1 English
Course," not "English Speaking Course." They progress through levels
over months or years.

---

### 1.4 Professional Certification (CA/CMA)

**Example:** JK Shah Classes, Swapnil Patni's Classes, VSI Jaipur

**Hierarchy observed for CA:**

```
Chartered Accountant (the qualification)
  ├── Foundation (Entry level)
  │     ├── Paper 1: Accounting
  │     ├── Paper 2: Business Laws
  │     ├── Paper 3: Quantitative Aptitude
  │     └── Paper 4: Business Economics
  ├── Intermediate (Second level)
  │     ├── Group 1
  │     │     ├── Paper 1: Advanced Accounting
  │     │     ├── Paper 2: Corporate Laws
  │     │     └── Paper 3: Taxation
  │     └── Group 2
  │           ├── Paper 4: Cost & Management Accounting
  │           ├── Paper 5: Auditing
  │           └── Paper 6: Financial Management
  └── Final (Third level)
        ├── Group 1
        │     └── Papers...
        └── Group 2
              └── Papers...
```

**What they call the layers:**

| Layer | What they call it |
|---|---|
| Top | "Course" or "Level" (Foundation, Intermediate, Final) |
| Middle | "Group" (Group 1, Group 2) and "Paper" (Paper 1, Paper 2) |
| Bottom | "Chapter" or "Topic" within paper |

**Key insight:** The hierarchy here has FOUR layers:
Level → Group → Paper → Topic. And students can be at different levels
simultaneously (studying for Inter Group 1 while retaking Inter Group 2).

**The "commercial unit" is the Level.** Students buy "CA Foundation Course"
or "CA Intermediate Course." Each level is a separate product with separate
fees and separate exam eligibility.

---

### 1.5 Skill-Based Institutes (Design, Music, Cooking)

**Example:** NID coaching, music academies, culinary schools

**Hierarchy observed:**

```
NID Entrance Preparation (the thing advertised)
  ├── Design Fundamentals
  │     ├── Visual Composition
  │     ├── Color Theory
  │     └── Perspective
  ├── Drawing & Sketching
  │     ├── Human Figures
  │     ├── Objects
  │     └── Scenes
  └── General Aptitude
        ├── Logical Reasoning
        └── Creative Thinking
```

**The structure is similar to computer training:** Offering → Module → Topic.
The middle layer is called "Module" or "Subject" depending on the institute.

---

## 2. Cross-Type Comparison

| Dimension | Coaching | Computer | Language | CA/CMA | Skill |
|---|---|---|---|---|---|
| **Top layer** | Educational Offering | Course | Course | Level (Foundation/Inter/Final) | Course |
| **Middle layer** | Subject | Module | Level → Skill | Group → Paper | Module |
| **Bottom layer** | Chapter → Topic | Topic | Lesson | Chapter → Topic | Topic |
| **Session** | Class meeting | Class meeting | Class meeting | Class meeting | Class meeting |
| **Entry variant** | Yes (Nurture/Enthusiast/Leader) | No (fixed start) | Yes (by proficiency) | No (sequential levels) | No (fixed start) |
| **Extra dimension** | Entry point affects pacing | None | Proficiency level | Group within level | None |

---

## 3. Is There a Common Abstraction?

**Yes, partially.**

Every institute type has the same structural pattern:

```
Educational Offering
  └── [Something that groups knowledge]
        └── [Something that represents a teaching unit]
              └── Session (the class meeting)
```

The middle layer is ALWAYS there, but it has different names and different
internal structures:

| Institute Type | Middle Layer Name | Contains |
|---|---|---|
| Coaching | Subject | Chapters → Topics |
| Computer | Module | Topics |
| Language | Level → Skill | Lessons |
| CA/CMA | Group → Paper | Chapters → Topics |
| Skill | Module | Topics |

**The common abstraction for the middle layer is:**

> **Curriculum Unit** — a grouping of related knowledge that an institute
> teaches as a coherent block.

"Subject" and "Module" are both Curriculum Units. They are the same concept
with different names. The internal structure of a Curriculum Unit varies
(by chapter, by topic, by skill) but the concept is the same.

---

## 4. What IS the Commercial Unit of Sale?

This is the harder question. The research shows:

| Institute Type | What the student buys |
|---|---|
| Coaching | "JEE Nurture Course" — an entry variant of an educational offering |
| Computer | "Full Stack Development Course" — the educational offering itself |
| Language | "B1 English Course" — a proficiency level within an offering |
| CA/CMA | "CA Foundation Course" — a certification level |
| Skill | "NID Entrance Prep Course" — the educational offering itself |

**There is no single commercial unit.** It varies by institute type:

- Sometimes it's the **Educational Offering** (Full Stack Development)
- Sometimes it's a **variant** of the offering (JEE Nurture vs. Enthusiast)
- Sometimes it's a **level** within the offering (English B1, CA Foundation)

**Implication for Academy:** The system must support multiple commercial
units. It cannot assume that "Program = what the student buys." The student
may buy an Offering, a Variant, or a Level depending on the institute type.

---

## 5. Proposed Abstraction (Working Hypothesis)

```
Educational Offering
  └── Curriculum Unit (Subject / Module / Level / Group)
        └── Topic (Chapter / Lesson / Skill)
              └── Session (the class meeting)
```

With two cross-cutting dimensions:

1. **Entry Variant** — how a student enters the offering (by year, by
   proficiency, by starting point). Not all institute types have this.

2. **Proficiency Level** — where the student is within the offering
   (A1→C2, Foundation→Final). Not all institute types have this.

**What Academy must support:**

- The Educational Offering as the top-level concept
- A configurable Curriculum Unit layer (the institute names it)
- A configurable Topic layer (the institute names it)
- Session as the universal bottom layer
- Optional Entry Variant and Proficiency Level dimensions

**What Academy must NOT assume:**

- That "Course" means the same thing everywhere
- That "Subject" is the only middle layer
- That the hierarchy is always 3 layers deep
- That every institute has entry variants or proficiency levels

---

## 6. Temporal Dimension (Time)

The research also revealed that every institute type has temporal structures:

| Temporal Concept | Coaching | Computer | Language | CA/CMA |
|---|---|---|---|---|
| **Academic Year** | April–March (follows school calendar) | No fixed year (rolling enrollment) | No fixed year (rolling) | Exam cycle (May/Nov) |
| **Admission Window** | Peak April–June (new academic year) | Always open | Always open | Registration deadlines before exams |
| **Term/Semester** | No — continuous coverage of syllabus | No — linear module progression | Levels (A1→B1→B2) take months each | Levels (Foundation→Inter→Final) take years |
| **Course Duration** | 1-2 years (JEE), 1 year (NEET) | 3-6 months (Full Stack) | 2-4 months per level | 4-5 years total (all 3 levels) |
| **Exam Window** | Weekly tests, monthly tests, final mock | Module-end assessments | Level-end assessments (IELTS exam dates) | ICAI exam schedules (May/Nov) |
| **Fee Cycle** | Installments aligned with course duration | Upfront or 2-3 installments | Monthly or per-level | Per-level fees |
| **Renewal Cycle** | Annual (new academic year) | N/A (course ends) | Per-level renewal | Per-level registration |

**Key insight:** Coaching institutes follow the **school calendar**
(April–March). Computer and language institutes follow **rolling enrollment**
(no fixed year). CA/CMA follows the **exam body's calendar** (ICAI schedule).

**Academy must support multiple temporal models:**

1. **School-calendar model** (April–March, annual renewal, seasonal peaks)
2. **Rolling-enrollment model** (always open, no fixed year)
3. **Exam-cycle model** (tied to external exam schedule)

---

## 7. Open Questions

1. Should Academy **force a 3-layer hierarchy** (Offering → Curriculum Unit → Topic),
   or should it allow **2-layer** (Offering → Topic) and **4-layer**
   (Offering → Level → Group → Paper → Topic)?

2. Is "Curriculum Unit" the right name, or should we use something else?

3. How do we handle **cross-listed topics** (a topic that appears in
   multiple Curriculum Units, e.g., "Statistics" in both Math and Physics)?

4. Should the **temporal model** be configurable per institute, or should
   Academy impose one model?

5. What is the relationship between **Entry Variant** and **Proficiency Level**?
   Are they independent dimensions or overlapping?

---

*This research informs Sprint 2 decisions. The hierarchy is not finalized.
The abstraction is a working hypothesis.*
