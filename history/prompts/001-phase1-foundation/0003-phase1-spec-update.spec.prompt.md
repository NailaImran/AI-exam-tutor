---
id: 0003
title: phase1-spec-update
stage: spec
date: 2026-01-18
surface: claude-code
model: claude-opus-4-5-20251101
feature: 001-phase1-foundation
branch: 001-phase1-foundation
user: system
command: /sp.specify
labels: [spec, phase1, foundation, exam-tutor]
links:
  spec: specs/001-phase1-foundation/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - specs/001-phase1-foundation/spec.md
  - specs/001-phase1-foundation/checklists/requirements.md
tests:
  - N/A
---

## Prompt

Update SPEC.md for Exam Tutor Phase 1: Foundation (Bronze Tier) with detailed requirements including:
- File system watcher for /Inbox monitoring
- 150+ questions (50 per exam type)
- Student profile system with profile.json, history.json, topic-stats.json, eri.json
- 5 core skills: student-profile-loader, question-bank-querier, answer-evaluator, eri-calculator, performance-tracker
- ERI calculation formula and bands
- Vault folder structure
- Acceptance criteria with 5-second watcher detection

## Response snapshot

Updated spec.md with comprehensive Phase 1 requirements:

**Key Updates**:
- 5 User Stories (P1-P5) covering complete workflow
- 31 Functional Requirements organized by category:
  - Vault Structure (FR-001 to FR-003)
  - File Watcher (FR-004 to FR-009)
  - Question Bank (FR-010 to FR-014)
  - Student Profile System (FR-015 to FR-020)
  - Core Skills (FR-021 to FR-025)
  - ERI Calculation (FR-026 to FR-031)
- 10 Measurable Success Criteria
- 7 Edge Cases with handling behavior
- 9 Documented Assumptions
- 4 Appendices (ERI Details, Vault Structure, Test Request Format, Skills Summary)

**Validation**: All 16 checklist items PASS

## Outcome

- ✅ Impact: Complete spec ready for implementation planning
- 🧪 Tests: N/A (specification document)
- 📁 Files: 2 files updated (spec.md, requirements.md)
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Spec now covers file watcher, 150 questions, eri.json, and 5 skills as requested

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All 16 checklist items PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
