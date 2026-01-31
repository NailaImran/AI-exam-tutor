---
id: 0002
title: phase-2-spec-update
stage: spec
date: 2026-01-20
surface: CLI
model: claude-sonnet-4-5
feature: phase-2-question-bank
branch: 002-question-bank-automation
user: system
command: /sp.specify
labels: [spec, update, phase-2, question-bank-automation]
links:
  spec: /specs/phase-2-question-bank/SPEC.md
  ticket: none
  adr: none
  pr: none
files:
  - path: /specs/phase-2-question-bank/SPEC.md
    status: updated
    lines: 433
  - path: /specs/phase-2-question-bank/checklists/requirements.md
    status: updated
    lines: 58
tests:
  - none
---

## Prompt

Update my SPEC.md of phase 2 Create SPEC.md for Exam Tutor Phase 2: Question Bank Automation

## Context
Location: /specs/phase-2-question-bank/SPEC.md
Reference: /specs/MASTER_PLAN.md, /specs/CONSTITUTION.md
Depends on: /specs/phase-1-foundation/ (must be 100% complete)
Timeline: 6-8 hours
Goal: Automate past paper collection and expand question bank to 1500+

## Requested Changes
- Add Phase 2 folder structure documentation
- Expand scope section with "Must Build" details
- Add detailed skill specifications (past-paper-scraper, question-extractor, question-validator, question-bank-manager)
- Include technical requirements section
- Add deliverables section
- Include acceptance criteria checklist
- Update MCP configuration with all three servers

## Response snapshot

Successfully updated Phase 2 SPEC.md with comprehensive enhancements:

**Key Additions**:
1. **Phase 2 Folder Structure**: Complete directory layout showing SPEC.md, PLAN.md, TASKS.md, data-model.md, contracts/, checklists/, and skills/
2. **Must Build Section**: Detailed breakdown of 6 major components:
   - Source documentation (sources.md)
   - Raw papers storage (/Raw-Papers/)
   - Review queue (/Needs-Review/)
   - 4 Phase 2 skills with detailed specifications
   - Batch pipeline workflow
   - Question bank expansion goals
3. **Skill Specifications**: Tables for each skill showing Input, Output, MCP Tools, and Logic
4. **Technical Requirements**: High-level technology considerations (PDF parsing, HTML parsing, duplicate detection, rate limiting)
5. **Deliverables**: 6 concrete deliverables for Phase 2
6. **Acceptance Criteria**: 12-item checklist for phase completion
7. **Updated MCP Config**: Added github and context7 servers alongside filesystem

**Spec Structure**:
- Overview with timeline and goals
- Phase 2 folder structure
- Scope with Must Build (6 components)
- Integration with Phase 1
- MCP configuration
- Out of scope (Phase 3-5)
- Technical requirements
- Deliverables
- User scenarios (4 user stories P1-P4)
- Edge cases (6 scenarios)
- Functional requirements (29 requirements)
- Key entities (5 entities)
- Success criteria (10 measurable outcomes)
- Acceptance criteria (12 checklist items)
- Assumptions (8 assumptions)
- Appendices (folder structure, skills summary, question schema)

**Quality Validation**: All 16 checklist items PASS ✅

## Outcome

- ✅ Impact: Comprehensive SPEC.md update aligning with user's simplified format while preserving detailed content
- 🧪 Tests: No automated tests - validation via requirements checklist (16/16 PASS)
- 📁 Files: Updated SPEC.md (433 lines) and requirements.md checklist (58 lines)
- 🔁 Next prompts: Ready for implementation via /sp.plan or /sp.implement
- 🧠 Reflection: Spec now includes both high-level "Must Build" overview and detailed functional requirements, making it accessible to stakeholders while maintaining technical rigor

## Evaluation notes (flywheel)

- Failure modes observed: None - spec update completed successfully
- Graders run and results (PASS/FAIL): Checklist validation PASS (16/16 items)
- Prompt variant (if applicable): Standard /sp.specify workflow for existing spec update
- Next experiment (smallest change to try): Proceed with implementation planning via /sp.plan
