---
id: 0003
title: phase-2-plan-update
stage: plan
date: 2026-01-20
surface: CLI
model: claude-sonnet-4-5
feature: phase-2-question-bank
branch: 002-question-bank-automation
user: system
command: /sp.plan
labels: [plan, update, phase-2, question-bank-automation, task-breakdown]
links:
  spec: /specs/phase-2-question-bank/SPEC.md
  ticket: none
  adr: none
  pr: none
files:
  - path: /specs/phase-2-question-bank/PLAN.md
    status: updated
    lines: 503
tests:
  - none
---

## Prompt

Update PLAN.md for Phase 2: Question Bank Automation with detailed task breakdown

## Context
Location: /specs/phase-2-question-bank/PLAN.md
Reference: /specs/phase-2-question-bank/SPEC.md
Depends on: Phase 1 100% complete
Timeline: 6-8 hours
Approach: Spec-driven development with Claude Code

## Requested Structure
- 10 detailed task sections with objectives, tasks, outputs, and done criteria
- Deliverable format table with task IDs, time estimates, dependencies
- Dependencies graph showing critical path and parallel opportunities
- Total time estimate of 6-8 hours

## Response snapshot

Successfully updated Phase 2 PLAN.md with comprehensive task breakdown:

**Key Enhancements**:
1. **10 Detailed Task Sections** (replacing generic tables):
   - 1. Source Research & Documentation (1h)
   - 2. Folder Structure Setup (30m)
   - 3. MCP Configuration Update (30m)
   - 4. Skill: past-paper-scraper (1.5h)
   - 5. Skill: question-extractor (1.5h)
   - 6. Skill: question-validator (1h)
   - 7. Skill: question-bank-manager (1h)
   - 8. Batch Pipeline Orchestration (1h)
   - 9. Mass Scraping & Processing (1.5h)
   - 10. Validation & Quality Assurance (30m)

2. **Each Section Includes**:
   - Objective: Clear goal statement
   - Tasks: Bulleted checklist of specific actions
   - Output: Concrete deliverable(s)
   - Testing: Validation approach (where applicable)
   - Done Criteria: Measurable completion standard

3. **Deliverable Format Table**: 14-row table showing task IDs (P2-001 through P2-014), time estimates, dependencies, outputs, and done criteria

4. **Dependencies Graph**: ASCII visualization showing:
   - Critical path: P2-001 → P2-002 → P2-003 → (Skills) → P2-012 → P2-013 → P2-014
   - Parallel opportunities: All 4 SKILL.md files and implementations can run in parallel
   - Bottlenecks: P2-003 blocks all skill work, P2-012 requires all 4 skills, P2-013 is longest task

5. **Total Estimated Time**: 8 hours (realistic upper bound of 6-8h range)

**Plan Structure**:
- Summary and technical context (preserved)
- Constitution check (preserved)
- Project structure (preserved)
- **NEW**: Task Breakdown - Phase 2 Only (10 detailed sections)
- **NEW**: Deliverable Format table
- Definition of Done (preserved)
- Research decisions summary (preserved)
- Data model summary (preserved)
- Skill contracts summary (preserved)
- Complexity tracking (preserved)
- Dependencies (preserved)
- **NEW**: Dependencies Graph with critical path analysis
- Next steps (updated)

**Task Organization**: Sequential with clear dependencies, enabling systematic implementation from source research through validation

## Outcome

- ✅ Impact: Comprehensive PLAN.md update providing detailed, actionable task breakdown for Phase 2 implementation
- 🧪 Tests: No automated tests - manual validation checkpoints defined in each task's "Done Criteria"
- 📁 Files: Updated PLAN.md (503 lines)
- 🔁 Next prompts: Begin implementation with P2-001 (Source Research) or run /sp.implement to start automated implementation
- 🧠 Reflection: Detailed task breakdown transforms high-level plan into executable workflow, with clear objectives, dependencies, and completion criteria for each step

## Evaluation notes (flywheel)

- Failure modes observed: None - plan update completed successfully
- Graders run and results (PASS/FAIL): Manual review PASS - all 10 tasks have clear objectives, tasks, outputs, and done criteria
- Prompt variant (if applicable): Standard /sp.plan workflow for existing plan update
- Next experiment (smallest change to try): Execute P2-001 to begin Phase 2 implementation
