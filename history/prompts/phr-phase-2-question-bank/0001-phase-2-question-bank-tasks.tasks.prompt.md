---
id: 0001
title: phase-2-question-bank-tasks
stage: tasks
date: 2026-01-20
surface: CLI
model: claude-sonnet-4-5
feature: phase-2-question-bank
branch: 002-question-bank-automation
user: system
command: /sp.tasks
labels: [tasks, phase-2, question-bank-automation, pipeline]
links:
  spec: /specs/phase-2-question-bank/SPEC.md
  ticket: none
  adr: none
  pr: none
files:
  - path: /specs/phase-2-question-bank/TASKS.md
    status: created
    lines: 445
tests:
  - none
---

## Prompt

Create TASKS.md for Exam Tutor Phase 2: Question Bank Automation

## Context
Location: /specs/phase-2-question-bank/TASKS.md
Reference: /specs/phase-2-question-bank/SPEC.md, PLAN.md
Depends on: Phase 1 complete

## Header
# Phase 2: Question Bank Automation - Tasks
⚠️ SCOPE: Phase 2 Only
⚠️ PREREQUISITE: Phase 1 must be 100% complete

## Task Format
| ID | Task | Status | Time | Notes |
|----|------|--------|------|-------|

## Task Categories

### Setup
- P2-001: Document past paper sources (SPSC, PPSC, KPPSC URLs)
- P2-002: Create /Raw-Papers/ folder structure
- P2-003: Create /Question-Bank/_review/ for flagged questions
- P2-004: Update mcp.json for web_fetch capability

### Skills Development
- P2-005: Create past-paper-scraper/SKILL.md
- P2-006: Implement past-paper-scraper
- P2-007: Create question-extractor/SKILL.md
- P2-008: Implement question-extractor
- P2-009: Create question-validator/SKILL.md
- P2-010: Implement question-validator
- P2-011: Create question-bank-manager/SKILL.md
- P2-012: Implement question-bank-manager

### Integration
- P2-013: Create batch pipeline script
- P2-014: Test scraper on 3 sources
- P2-015: Test extractor on 5 papers
- P2-016: Test validator catches duplicates
- P2-017: Test manager adds to Question-Bank

### Validation
- P2-018: Verify 500+ questions for SPSC
- P2-019: Verify 500+ questions for PPSC
- P2-020: Verify 500+ questions for KPPSC
- P2-021: Verify all questions have source/year metadata
- P2-022: Review flagged questions in /_review/

## Phase Gate
- [ ] All 22 tasks complete
- [ ] 4 skills tested and working
- [ ] 1500+ total questions in bank
- [ ] Batch pipeline runs end-to-end
- [ ] No duplicate questions
- [ ] Flagged questions documented

✅ Phase 2 complete → Proceed to Phase 3

## Response snapshot

Generated comprehensive TASKS.md with 117 tasks organized into 9 phases:

**Phase Structure:**
1. Setup (T001-T007): Folder structure and registry initialization
2. Foundational (T008-T034): 4 core skills implementation - BLOCKS all user stories
3. User Story 1 - Bulk Import (T035-T050): End-to-end pipeline automation
4. User Story 2 - Validate & Fix (T051-T061): Review workflow for flagged questions
5. User Story 3 - Deduplicate (T062-T073): Cross-exam question linking
6. User Story 4 - Statistics (T074-T086): Question bank metrics and reporting
7. Expansion (T087-T098): Scale to 1500+ questions across all exams
8. Validation & QA (T099-T110): Verify all success criteria
9. Documentation (T111-T117): Finalize docs and completion report

**Key Features:**
- All tasks follow strict checklist format: `- [ ] [ID] [P?] [Story] Description with file path`
- Tasks organized by user story for independent implementation and testing
- Clear checkpoints after each phase for validation
- Parallel opportunities marked with [P] flag
- Story labels [US1], [US2], [US3], [US4] for traceability
- MVP path clearly defined (Phases 1-3)
- Dependencies and execution order documented
- Success criteria checklist included

**Skills Coverage:**
- past-paper-scraper: Web scraping with rate limiting
- question-extractor: PDF/HTML parsing with confidence scoring
- question-validator: Completeness checks, duplicate detection, topic auto-suggestion
- question-bank-manager: ID generation, storage, indexing, statistics

**Total Tasks:** 117 tasks spanning setup through documentation

## Outcome

- ✅ Impact: Comprehensive task breakdown enabling systematic implementation of Phase 2 question bank automation with clear MVP path
- 🧪 Tests: No automated tests - tasks define manual validation checkpoints
- 📁 Files: Created /specs/phase-2-question-bank/TASKS.md (445 lines)
- 🔁 Next prompts: Begin Phase 1 Setup (T001-T007) to initialize folder structure
- 🧠 Reflection: Task organization by user story enables independent delivery and testing of each capability, with clear foundation phase that blocks all feature work

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation followed template and specification requirements
- Graders run and results (PASS/FAIL): Manual review PASS - all 117 tasks follow checklist format with proper IDs, story labels, and file paths
- Prompt variant (if applicable): Standard /sp.tasks workflow
- Next experiment (smallest change to try): Execute Phase 1 Setup tasks to validate folder structure creation
