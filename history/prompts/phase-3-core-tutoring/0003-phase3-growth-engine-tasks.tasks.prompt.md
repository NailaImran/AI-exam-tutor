---
id: "0003"
title: "phase3-growth-engine-tasks"
stage: tasks
date: 2026-01-30
surface: cli
model: claude-opus-4-5-20251101
feature: phase-3-core-tutoring
branch: 003-growth-engine
user: human
command: /sp.tasks
labels: [tasks, phase-3, whatsapp, linkedin, skills, subagents]
links:
  spec: specs/phase-3-core-tutoring/spec.md
  plan: specs/phase-3-core-tutoring/plan.md
  tasks: specs/phase-3-core-tutoring/tasks.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - specs/phase-3-core-tutoring/tasks.md
tests:
  - Manual validation via quickstart.md checklist
---

## Prompt

Execute /sp.tasks to generate implementation tasks for Phase 3 Growth Engine based on spec.md, plan.md, and data-model.md.

## Response snapshot

Generated comprehensive tasks.md with:

**Task Summary**:
- Total tasks: 118
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 13 tasks
- Phase 3 (US1 - WhatsApp Daily): 14 tasks
- Phase 4 (US2 - Study Plans): 16 tasks
- Phase 5 (US3 - Progress Reports): 17 tasks
- Phase 6 (US4 - ERI Badges): 12 tasks
- Phase 7 (US5 - LinkedIn Posts): 15 tasks
- Phase 8 (US6 - WhatsApp Tests): 13 tasks
- Phase 9 (Polish): 11 tasks

**User Story Organization**:
| Story | Priority | Tasks | Can Start After |
|-------|----------|-------|-----------------|
| US1 | P1 (MVP) | T021-T034 | Phase 2 |
| US2 | P2 | T035-T050 | Phase 2 |
| US3 | P2 | T051-T067 | US1 complete |
| US4 | P3 | T068-T079 | Phase 2 |
| US5 | P3 | T080-T094 | Phase 2 |
| US6 | P4 | T095-T107 | US1 complete |

**Parallel Opportunities**:
- Phase 2: 6 schema tasks can run in parallel (T011-T016)
- After Phase 2: US1, US2, US4, US5 can start in parallel
- US3 and US6 depend on US1 (whatsapp-message-sender)

**MVP Scope**: User Story 1 only (T001-T034) - daily WhatsApp question delivery

**Skills to Create** (8 new):
- study-plan-generator
- progress-report-generator
- whatsapp-message-sender
- social-post-generator
- eri-badge-generator
- daily-question-selector
- scheduled-task-runner
- approval-workflow

**Subagents to Create** (3 new):
- study-strategy-planner
- progress-reporting-coordinator
- social-media-coordinator

## Outcome

- ✅ Impact: Complete task list ready for implementation
- 🧪 Tests: Manual validation via quickstart.md
- 📁 Files: 1 file created (tasks.md)
- 🔁 Next prompts: /sp.implement or manual task execution
- 🧠 Reflection: Clear dependency graph enables parallel work on US1, US2, US4, US5

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tasks have correct format [ID] [P?] [Story] Description
- Prompt variant (if applicable): Standard /sp.tasks
- Next experiment: Track actual parallel execution efficiency
