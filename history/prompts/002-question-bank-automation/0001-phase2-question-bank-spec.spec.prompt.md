---
id: 0001
title: phase2-question-bank-spec
stage: spec
date: 2026-01-19
surface: claude-code
model: claude-opus-4-5
feature: phase-2-question-bank
branch: 002-question-bank-automation
user: human
command: /sp.specify
labels: [phase2, question-bank, automation, skills]
links:
  spec: specs/phase-2-question-bank/SPEC.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/phase-2-question-bank/SPEC.md
  - specs/phase-2-question-bank/skills/past-paper-scraper/SKILL.md
  - specs/phase-2-question-bank/skills/question-extractor/SKILL.md
  - specs/phase-2-question-bank/skills/question-validator/SKILL.md
  - specs/phase-2-question-bank/skills/question-bank-manager/SKILL.md
  - specs/phase-2-question-bank/checklists/requirements.md
tests:
  - type: manual
    description: Spec validation checklist complete
---

## Prompt

Create SPEC.md for Exam Tutor Phase 2: Question Bank Automation

## Context
Reference: /specs/MASTER_PLAN.md, /specs/CONSTITUTION.md
Depends on: /specs/phase-1-foundation/ (must be complete)
Timeline: 6-8 hours
Goal: Automate past paper collection and question bank expansion

## Location
/specs/phase-2-question-bank/SPEC.md

## Scope - Phase 2 Only

### Must Build

1. Past Paper Sources
   - Identify official sources: SPSC (spsc.gov.pk), PPSC (ppsc.gop.pk), KPPSC (kppsc.gov.pk)
   - Secondary sources: past paper websites, PDF repositories
   - Document source reliability rating

2. Past Paper Scraper Skill
   - Input: exam_type, year_range, subjects
   - Output: raw questions extracted
   - Handle: PDF parsing, HTML scraping
   - Store raw data in /Raw-Papers/{Exam}/{Year}/

3. Question Extractor Skill
   - Input: raw paper file
   - Output: structured questions (JSON)
   - Extract: question, options, correct_answer
   - Flag: questions needing manual review

4. Question Validator Skill
   - Input: extracted question
   - Output: validated question or rejection reason
   - Check: complete options, valid answer, no duplicates
   - Auto-add: difficulty, topics

5. Question Bank Manager Skill
   - Input: validated questions
   - Output: organized question bank
   - Actions: add, update, deduplicate, tag
   - Maintain: question count per exam/subject/topic

6. Expanded Question Bank
   - Target: 500+ questions per exam (1500+ total)
   - Coverage: all major subjects
   - Metadata: source, year, difficulty, topic tags

## Response snapshot

Created comprehensive SPEC.md for Phase 2 with:
- 4 prioritized user stories with acceptance scenarios
- 29 functional requirements (FR-001 through FR-029)
- 10 measurable success criteria
- 6 edge cases with handling strategies
- Extended question schema with source tracking
- New folder structure additions (Raw-Papers, Needs-Review, Question-Bank-Index)

Created 4 skills with complete SKILL.md definitions:
- past-paper-scraper: Downloads papers from PSC sources with rate limiting
- question-extractor: Parses PDFs/HTML into structured questions
- question-validator: Validates quality, uniqueness, auto-assigns difficulty/topics
- question-bank-manager: Organizes bank with unique IDs and statistics

Updated MASTER_PLAN.md Phase Documentation Links to show Phase 2 status as "Spec Ready".

## Outcome

- Impact: Phase 2 specification complete, ready for planning
- Tests: Spec quality checklist passed (16/16 items)
- Files: 6 files created in specs/phase-2-question-bank/
- Next prompts: /sp.clarify or /sp.plan for Phase 2
- Reflection: Clear scope boundaries help avoid feature creep

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual checklist - PASS
- Prompt variant (if applicable): Standard sp.specify workflow
- Next experiment (smallest change to try): N/A - spec complete
