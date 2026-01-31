---
id: 0004
title: phase2-task-generation
stage: tasks
date: 2026-01-20
surface: cli
model: claude-sonnet-4-5
feature: 002-question-bank-automation
branch: 002-question-bank-automation
user: system
command: /sp.tasks
labels: [tasks, phase-2, question-bank, automation, user-stories]
links:
  spec: /specs/phase-2-question-bank/SPEC.md
  plan: /specs/phase-2-question-bank/PLAN.md
  tasks: /specs/phase-2-question-bank/tasks.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: /specs/phase-2-question-bank/tasks.md
    status: created
    lines: 500+
tests:
  - name: N/A (task definition phase)
    status: N/A
---

## Prompt

User requested task generation for Phase 2: Question Bank Automation using `/sp.tasks` command.

User input: "now create tasks for phase 2"

## Response snapshot

Generated comprehensive task breakdown (tasks.md) for Phase 2 implementation with 86 tasks organized by user story:

**Task Organization by User Story**:
- Phase 1: Setup & Infrastructure (9 tasks) - Vault structure, index files
- Phase 2: Foundational (5 tasks) - Skill definitions for 4 automation skills
- Phase 3: US1 - Bulk Import Past Papers [P1] (35 tasks) - Core pipeline implementation
- Phase 4: US2 - Validate and Fix (8 tasks) - Review workflow for flagged questions
- Phase 5: US3 - Deduplicate Across Exams [P3] (8 tasks) - Cross-exam linking
- Phase 6: US4 - Track Statistics [P4] (11 tasks) - Question bank health metrics
- Phase 7: Polish & Cross-Cutting (10 tasks) - Documentation, validation, final report

**Independent Test Criteria**: Each user story includes specific test scenarios that validate the feature works independently.

**Parallel Execution**: 22 tasks marked with [P] can run in parallel (different files, no dependencies).

**MVP Definition**: User Story 1 complete (T001-T049) delivers full automation pipeline + 1500+ questions.

**Task Format**: All tasks follow strict checklist format:
- `- [ ] T001 Create folder...` (Setup)
- `- [ ] T010 [P] Create skill...` (Parallelizable)
- `- [ ] T015 [US1] Implement scraper...` (User Story 1)

**Dependencies Documented**: Clear dependency graph showing US1 must complete before US2-US4.

## Outcome

- ✅ Impact: Complete implementation roadmap for Phase 2 with 86 actionable tasks organized by user story
- 🧪 Tests: Manual validation via skill invocation (agent skills project, no traditional tests)
- 📁 Files: 1 file created (tasks.md with 500+ lines)
- 🔁 Next prompts: Start implementation with T001 (Create Raw-Papers folder structure) or run `/sp.implement` to begin automated implementation
- 🧠 Reflection: Tasks organized by user story enable independent implementation and testing. MVP scope (US1) provides maximum value. Parallel opportunities identified for efficiency.

## Evaluation notes (flywheel)

- Failure modes observed: None. PHR initially created in wrong directory (phase-2-question-bank vs 002-question-bank-automation) but corrected.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): Standard /sp.tasks workflow with user story organization
- Next experiment (smallest change to try): N/A
