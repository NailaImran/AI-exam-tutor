---
id: 0002
title: phase1-foundation-impl-plan
stage: plan
date: 2026-01-17
surface: claude-code
model: claude-opus-4-5-20251101
feature: 001-phase1-foundation
branch: 001-phase1-foundation
user: developer
command: /sp.plan
labels: [plan, phase1, foundation, implementation]
links:
  spec: specs/001-phase1-foundation/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/001-phase1-foundation/plan.md
  - specs/001-phase1-foundation/research.md
  - specs/001-phase1-foundation/data-model.md
  - specs/001-phase1-foundation/quickstart.md
  - specs/001-phase1-foundation/contracts/student-profile-loader.contract.md
  - specs/001-phase1-foundation/contracts/question-bank-querier.contract.md
  - specs/001-phase1-foundation/contracts/answer-evaluator.contract.md
  - specs/001-phase1-foundation/contracts/exam-readiness-calculator.contract.md
  - specs/001-phase1-foundation/contracts/performance-tracker.contract.md
tests:
---

## Prompt

Create PLAN.md for Exam Tutor Phase 1: Foundation (Bronze Tier)

## Context
Reference: SPEC.md (Phase 1)
Timeline: 8-12 hours
Approach: Spec-driven development with Claude Code

## Planning Requirements

### Task Breakdown
Create detailed tasks for:

1. Project Setup (1 hr)
2. Core Files (1 hr)
3. Question Bank Creation (3-4 hrs)
4. Student Profile System (1-2 hrs)
5. Agent Skills (2-3 hrs)
6. File Watcher (1-2 hrs)
7. Integration & Testing (1 hr)

### Deliverable Format
- Task ID (P1-001, P1-002, etc.)
- Task name
- Estimated time
- Dependencies
- Acceptance criteria
- Files to create/modify

### Constraints
- Each task ≤ 2 hours
- No external APIs (except file system MCP)
- All skills must be testable independently
- Follow existing SKILL.md format

## Response snapshot

Created comprehensive implementation plan for Phase 1 Foundation with:

1. **Technical Context**: Claude Code Skills, MCP Filesystem, JSON/Markdown data formats

2. **Constitution Check**: All 6 principles PASS (file-based, atomic, deterministic, composable, no user interaction, MCP-first)

3. **Research Findings** (4 decisions):
   - R1: Manual question curation (50+ questions)
   - R2: On-demand polling for file watcher
   - R3: Baseline defaults for first-session ERI
   - R4: 20 topics for PPSC Pakistan Studies

4. **Data Model**: 7 entities documented with schemas
   - Student Profile, Session History, Topic Stats, Session Detail
   - Question, Syllabus Structure, Topic Weights

5. **Skill Contracts**: 5 contracts with I/O schemas
   - student-profile-loader
   - question-bank-querier
   - answer-evaluator
   - exam-readiness-calculator
   - performance-tracker

6. **Task Groups**: 8 groups, 9.5 hours estimated
   - Setup (1 hr) → Documentation (1 hr) → Question Bank (3 hrs)
   - Syllabus (0.5 hr) → Student Data (0.5 hr) → Skills (2 hrs)
   - Integration (1 hr) → Validation (0.5 hr)

7. **Quickstart Guide**: 5-minute setup instructions

## Outcome

- ✅ Impact: Complete implementation plan ready for /sp.tasks execution
- 🧪 Tests: N/A - planning document
- 📁 Files: 10 files created (plan, research, data-model, quickstart, 5 contracts, CLAUDE.md updated)
- 🔁 Next prompts: /sp.tasks to generate detailed task breakdown
- 🧠 Reflection: Plan aligns with spec's 20 functional requirements and 8 success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed successfully
- Graders run and results (PASS/FAIL): Constitution check PASS
- Prompt variant (if applicable): Standard /sp.plan flow with research + contracts
- Next experiment (smallest change to try): N/A - proceed to /sp.tasks
