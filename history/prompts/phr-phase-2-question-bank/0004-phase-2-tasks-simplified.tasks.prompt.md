---
id: 0004
title: phase-2-tasks-simplified
stage: tasks
date: 2026-01-20
surface: CLI
model: claude-sonnet-4-5
feature: phase-2-question-bank
branch: 002-question-bank-automation
user: system
command: /sp.tasks
labels: [tasks, simplified, phase-2, question-bank-automation, 46-tasks]
links:
  spec: /specs/phase-2-question-bank/SPEC.md
  ticket: none
  adr: none
  pr: none
files:
  - path: /specs/phase-2-question-bank/TASKS.md
    status: replaced
    lines: 283
  - path: /specs/phase-2-question-bank/TASKS-OLD.md
    status: archived
    lines: 344
tests:
  - none
---

## Prompt

Create simplified TASKS.md for Exam Tutor Phase 2: Question Bank Automation

User requested a simplified 46-task format organized by skill categories instead of the comprehensive 117-task user-story-based format.

## Format Requirements
- 46 tasks total
- Organized by skill categories (Setup, Scraper, Extractor, Validator, Manager, Pipeline, Processing, Validation)
- Simple checkbox format with time estimates
- Progress tracker table
- Phase gate checklist
- Dependencies diagram
- Implementation strategy section

## Response snapshot

Successfully replaced TASKS.md with simplified 46-task format:

**Task Organization**:
1. **Setup & Research** (10 tasks, 2.5h): Source documentation, folder creation, MCP configuration
2. **past-paper-scraper** (5 tasks, 2h): Skill specification and implementation
3. **question-extractor** (5 tasks, 2.5h): PDF/HTML parsing logic
4. **question-validator** (6 tasks, 2h): Validation and duplicate detection
5. **question-bank-manager** (5 tasks, 1.5h): Question organization and indexing
6. **Batch Pipeline** (5 tasks, 2h): End-to-end workflow orchestration
7. **Mass Processing** (4 tasks, 2h): Process all exam sources
8. **Validation** (6 tasks, 1.5h): Verify completion criteria

**Key Features**:
- Clear checkpoints after each skill category
- Detailed sub-bullets for implementation logic
- Progress tracker table (8 categories, 46 total tasks)
- Phase gate checklist (14 items to verify before completion)
- Dependencies diagram showing critical path and parallel opportunities
- Two implementation strategies: Sequential (4 days) and Parallel (team approach)

**Format Differences from Original**:
- Original: 117 tasks organized by user stories (US1-US4) with strict checklist format
- New: 46 tasks organized by skills/categories with time estimates
- Original: User story phases with independent testing
- New: Skill-based phases with checkpoints

**Total Time Estimate**: 8 hours (consistent with 6-8h timeline)

## Outcome

- ✅ Impact: Simplified task list focusing on incremental skill-by-skill implementation
- 🧪 Tests: Manual validation checkpoints after each skill category
- 📁 Files: Replaced TASKS.md (283 lines), archived old version as TASKS-OLD.md (344 lines)
- 🔁 Next prompts: Begin implementation with P2-001 (SPSC source research)
- 🧠 Reflection: Simplified format easier to follow for sequential implementation, loses user-story independence but gains skill-focused clarity

## Evaluation notes (flywheel)

- Failure modes observed: None - simplified task generation successful
- Graders run and results (PASS/FAIL): Manual review PASS - all 46 tasks have clear descriptions and time estimates
- Prompt variant (if applicable): User-requested simplified format instead of standard user-story organization
- Next experiment (smallest change to try): Execute P2-001 to begin Phase 2 implementation
