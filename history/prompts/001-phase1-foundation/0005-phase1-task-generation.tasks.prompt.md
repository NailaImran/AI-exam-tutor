---
id: 0005
title: phase1-task-generation
stage: tasks
date: 2026-01-18
surface: claude-code
model: claude-opus-4-5-20251101
feature: 001-phase1-foundation
branch: 001-phase1-foundation
user: system
command: /sp.tasks
labels: [tasks, phase1, foundation, exam-tutor]
links:
  spec: specs/001-phase1-foundation/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - specs/001-phase1-foundation/tasks.md
tests:
  - N/A
---

## Prompt

Generate detailed task list for Exam Tutor Phase 1: Foundation (Bronze Tier) based on:
- plan.md (tech stack, structure)
- spec.md (5 user stories with priorities)
- data-model.md (entities)
- contracts/ (5 skill contracts)

Organize tasks by user story for independent implementation.

## Response snapshot

Created comprehensive tasks.md with 67 tasks across 8 phases:

**Task Distribution**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 23 tasks (question bank + syllabus)
- Phase 3 (US3 - Register Student): 6 tasks
- Phase 4 (US1 - Practice Test): 8 tasks
- Phase 5 (US2 - ERI Display): 7 tasks
- Phase 6 (US4 - Company Handbook): 6 tasks
- Phase 7 (US5 - File Watcher): 6 tasks
- Phase 8 (Polish): 5 tasks

**Per User Story**:
- US1: 8 tasks (question-bank-querier, answer-evaluator, performance-tracker skills)
- US2: 7 tasks (exam-readiness-calculator skill, Dashboard.md)
- US3: 6 tasks (profile files, student-profile-loader skill)
- US4: 6 tasks (Company_Handbook.md)
- US5: 6 tasks (inbox-processor, logging)

**Parallel Opportunities**: 15 question file tasks can run in parallel

**MVP Scope**: Phases 1-4 (Setup + Foundational + US3 + US1) = 43 tasks

## Outcome

- ✅ Impact: Complete executable task list ready for implementation
- 🧪 Tests: Manual validation (no automated tests for Phase 1)
- 📁 Files: 1 file created (tasks.md with 67 tasks)
- 🔁 Next prompts: /sp.implement or manual task execution
- 🧠 Reflection: US3 placed before US1 due to profile dependency; all tasks have exact file paths

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tasks follow checklist format (checkbox, ID, labels, file paths)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
