---
id: 0002
title: phase2-question-bank-plan
stage: plan
date: 2026-01-19
surface: claude-code
model: claude-opus-4-5
feature: phase-2-question-bank
branch: 002-question-bank-automation
user: human
command: /sp.plan
labels: [phase2, question-bank, automation, planning]
links:
  spec: specs/phase-2-question-bank/SPEC.md
  plan: specs/phase-2-question-bank/PLAN.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/phase-2-question-bank/PLAN.md
  - specs/phase-2-question-bank/research.md
  - specs/phase-2-question-bank/data-model.md
  - specs/phase-2-question-bank/contracts/past-paper-scraper.contract.md
  - specs/phase-2-question-bank/contracts/question-extractor.contract.md
  - specs/phase-2-question-bank/contracts/question-validator.contract.md
  - specs/phase-2-question-bank/contracts/question-bank-manager.contract.md
tests:
  - type: manual
    description: Constitution check passed, all research questions resolved
---

## Prompt

Create PLAN.md for Exam Tutor Phase 2: Question Bank Automation

Context:
- Reference: /specs/phase-2-question-bank/SPEC.md
- Depends on: Phase 1 complete
- Timeline: 6-8 hours
- Approach: Spec-driven development with Claude Code

Location: /specs/phase-2-question-bank/PLAN.md

Tasks:
1. Source Research - Document PSC URLs, identify secondary sources
2. Folder Structure - Create /Raw-Papers/, /Needs-Review/, /Question-Bank-Index/
3. past-paper-scraper skill - Downloads papers from official sources
4. question-extractor skill - Parses PDFs into structured JSON
5. question-validator skill - Validates completeness and duplicates
6. question-bank-manager skill - Adds to bank, generates IDs
7. Batch Processing - Full pipeline workflow
8. Testing - Verify 1500+ questions

## Response snapshot

Created comprehensive PLAN.md with:
- Technical context matching Phase 1 architecture (MCP filesystem, Agent Skills)
- Constitution check passing all 6 principles
- 26 tasks organized in 5 phases (Setup, Core Skills, Integration, Expansion, Validation)
- Clear acceptance criteria for each task

Generated supporting artifacts:
- research.md: 7 research decisions (sources, PDF parsing, duplicate detection, rate limiting, IDs, storage, validation)
- data-model.md: 7 entity schemas with relationships
- 4 skill contracts defining input/output specifications

Updated MASTER_PLAN.md Phase 2 status to "Plan Ready" with link to PLAN.md.

## Outcome

- Impact: Phase 2 planning complete, ready for task generation
- Tests: Constitution check passed (6/6 principles)
- Files: 7 files created (PLAN.md, research.md, data-model.md, 4 contracts)
- Next prompts: /sp.tasks to generate BUILD.md
- Reflection: Multi-level validation design balances automation with accuracy

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check - PASS
- Prompt variant (if applicable): Standard sp.plan workflow
- Next experiment (smallest change to try): N/A - plan complete
