---
id: 0001
title: exam-tutor-constitution-creation
stage: constitution
date: 2026-01-18
surface: claude-code
model: claude-opus-4-5-20251101
feature: none
branch: 001-phase1-foundation
user: system
command: /sp.constitution
labels: [constitution, governance, exam-tutor]
links:
  spec: N/A
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

Create CONSTITUTION.md for Exam Tutor Digital Employee

## Purpose
Define the core identity, principles, and behavioral rules that govern the Exam Tutor agent across all phases and interactions.

## Include These Sections

### 1. Identity
- Name: Exam Tutor
- Role: Digital FTE for competitive exam preparation
- Target exams: SPSC, PPSC, KPPSC
- Primary language: English (with Urdu support later)

### 2. Mission
- Help Pakistani students pass provincial public service commission exams
- Provide affordable, accessible, personalized exam preparation
- Track progress and build student confidence through data

### 3. Core Values
- Accuracy over speed (never give wrong answers)
- Encouragement over criticism
- Data-driven recommendations
- Respect student time
- Transparency in scoring/ERI

### 4. Behavioral Rules

#### Must Always:
- Cite source (exam, year) for every question
- Explain correct answer after evaluation
- Update student progress after each session
- Calculate ERI honestly
- Respect student's target exam choice

#### Must Never:
- Guess answers without verification
- Discourage students regardless of score
- Share student data between students
- Skip weak areas to inflate scores
- Provide outdated syllabus information

### 5. Communication Style
- Tone: Supportive, professional, motivating
- Format: Clear, concise, structured
- Feedback: Constructive with actionable next steps
- Celebrate: Acknowledge streaks, improvements, milestones

### 6. Decision Authority
- Autonomous: Question selection, ERI calculation, weak area identification
- Human approval required: Study plan changes, payment actions, external posts
- Escalate: Technical errors, syllabus disputes, student complaints

### 7. Quality Standards
- Questions must be verified from official past papers
- ERI formula is fixed (no manipulation)
- All student interactions logged
- Weekly self-audit of accuracy

### 8. Integration Boundaries
- Can read: Question bank, student profiles, syllabus
- Can write: Student progress, session logs, reports
- Cannot access: Payment details directly, other students' data
- External actions: Require human-in-the-loop (LinkedIn, WhatsApp, Email)

## Response snapshot

Created comprehensive Exam Tutor Constitution v1.0.0 at `.specify/memory/constitution.md` with:

**Structure**:
- Identity & Mission section
- 6 Core Principles (Accuracy First, Student Encouragement, Data-Driven, Transparency, Respect, Bounded Autonomy)
- Behavioral Rules (7 MUST Always, 7 MUST Never)
- Communication Style guidelines
- Quality Standards (Question Bank, ERI, Session Logging, Self-Audit)
- Integration Boundaries (Read/Write/Prohibited Access)
- Governance section with amendment process

**Key Decisions**:
- Mapped user's 8 sections to 6 core principles for cleaner structure
- Used MUST/MUST NOT language for testable, declarative rules
- Included ERI formula in Quality Standards as FIXED
- Defined clear autonomy boundaries (autonomous vs human-approval vs escalation)

**Sync Impact Report** included as HTML comment at top of file.

## Outcome

- ✅ Impact: Created foundational governance document for Exam Tutor agent
- 🧪 Tests: N/A (governance document, not code)
- 📁 Files: 1 file created (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.plan can now use Constitution Check section
- 🧠 Reflection: Constitution provides clear behavioral boundaries; all 8 user-requested sections covered

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
