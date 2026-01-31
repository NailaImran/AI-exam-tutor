---
id: 0001
title: phase1-foundation-spec-creation
stage: spec
date: 2026-01-17
surface: claude-code
model: claude-opus-4-5-20251101
feature: 001-phase1-foundation
branch: 001-phase1-foundation
user: developer
command: /sp.specify
labels: [spec, phase1, foundation, bronze-tier]
links:
  spec: specs/001-phase1-foundation/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/001-phase1-foundation/spec.md
  - specs/001-phase1-foundation/checklists/requirements.md
tests:
---

## Prompt

Create SPEC.md for Exam Tutor Phase 1: Foundation (Bronze Tier)

## Context
Reference: MASTER_PLAN.md
Timeline: 8-12 hours
Goal: Minimum viable tutoring system in Obsidian

## Scope - Phase 1 Only

### Must Build
1. Obsidian vault structure
   - Dashboard.md (student overview + ERI display)
   - Company_Handbook.md (tutor behavior rules)
   - Folders: /Inbox, /Needs_Action, /Done, /Students, /Question-Bank

2. File system watcher
   - Monitor /Inbox for new student requests
   - Move processed files to appropriate folders

3. Question bank foundation
   - Scrape/collect SPSC, PPSC, KPPSC past papers
   - Store as structured JSON in /Question-Bank
   - Organize by exam > subject > topic

4. Basic student profile
   - profile.json (name, target exam, start date)
   - history.json (tests taken)
   - ERI score calculation (Accuracy×0.40 + Coverage×0.25 + Recency×0.20 + Consistency×0.15)

5. Core skills (Agent Skills)
   - student-profile-loader
   - question-bank-querier
   - answer-evaluator
   - eri-calculator

### Out of Scope (Later Phases)
- WhatsApp/Gmail integration
- LinkedIn posting
- Adaptive tests
- Odoo integration
- Leaderboard
- Payment tracking

## Deliverables
1. Folder structure diagram
2. File schemas (JSON structures)
3. Skill specifications (inputs/outputs/MCP tools)
4. Watcher script logic
5. ERI calculation formula
6. Done criteria checklist

## Response snapshot

Created comprehensive specification for Exam Tutor Phase 1 Foundation (Bronze Tier) including:

1. **Overview & Scope Boundaries**: Clear in-scope (vault structure, file watcher, question bank, student profiles, core skills) and out-of-scope (WhatsApp, adaptive tests, payments) definitions

2. **4 Prioritized User Stories**:
   - P1: Complete First Practice Test (core Q&A loop)
   - P2: View Exam Readiness Score (ERI display)
   - P3: Register as New Student (profile creation)
   - P4: Review Company Handbook (documentation)

3. **20 Functional Requirements** organized by:
   - Vault Structure (FR-001 to FR-003)
   - File Watcher (FR-004 to FR-006)
   - Question Bank (FR-007 to FR-010)
   - Student Profile (FR-011 to FR-013)
   - Core Skills (FR-014 to FR-017)
   - Performance Tracking (FR-018 to FR-020)

4. **8 Measurable Success Criteria** (SC-001 to SC-008)

5. **Appendices**:
   - ERI Calculation Details with component definitions
   - Vault Folder Structure diagram
   - Test Request Format template

6. **Quality Checklist**: All items passed validation

## Outcome

- ✅ Impact: Created complete Phase 1 specification enabling implementation planning
- 🧪 Tests: N/A - specification document
- 📁 Files: spec.md (327 lines), checklists/requirements.md (47 lines)
- 🔁 Next prompts: /sp.clarify (if needed) or /sp.plan (to create implementation plan)
- 🧠 Reflection: Spec successfully captures MVP scope from MASTER_PLAN.md Phase 1 with clear boundaries

## Evaluation notes (flywheel)

- Failure modes observed: None - spec completed successfully
- Graders run and results (PASS/FAIL): Manual checklist validation PASS
- Prompt variant (if applicable): Standard /sp.specify flow
- Next experiment (smallest change to try): N/A - proceed to /sp.plan
