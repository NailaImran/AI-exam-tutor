---
id: "0002"
title: "Implement Deep Diagnostic Analyzer T028-T031"
stage: green
date: 2025-02-03
surface: claude-code
model: claude-opus-4-5-20251101
feature: phase-4-gold-tier
branch: master
user: lenovo
command: /sp.implement T028-T031
labels: [phase-4, deep-diagnostic, root-cause-analysis, intelligence]
links:
  spec: specs/phase-4-gold-tier/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - .claude/skills/exam-tutor/deep-dive-analyzer/SKILL.md (created)
  - .claude/skills/exam-tutor/references/schemas.md (updated)
  - specs/phase-4-gold-tier/tasks.md (updated)
tests:
  - N/A (skill definitions, no runtime tests)
---

## Prompt

/sp.implement T028-T031

Implement tasks T028-T031 from Phase 4 Gold Tier, which comprise the D4.2 Deep Diagnostic Analyzer deliverable:
- T028: Create deep-dive-analyzer skill
- T029: Implement root cause identification (no_practice, historically_difficult, related_weakness)
- T030: Implement contributing factors analysis
- T031: Implement recommended_action generation

## Response snapshot

Created **deep-dive-analyzer** skill with comprehensive root-cause analysis:

1. **Root Cause Identification** (8 categories):
   - `no_practice` - No sessions in last 14 days
   - `insufficient_practice` - < 10 questions attempted
   - `historically_difficult` - Accuracy < 60% over 3+ sessions
   - `related_weakness` - Prerequisite topics also weak
   - `knowledge_decay` - Retention score < 0.50
   - `concept_confusion` - Similar topics have inverse performance
   - `time_pressure` - Accuracy drops in timed tests
   - `difficulty_mismatch` - Poor on medium/hard, good on easy

2. **Contributing Factors Analysis** (6 weighted factors):
   - Practice recency (0.20)
   - Practice volume (0.15)
   - Retention health (0.20)
   - Trend direction (0.15)
   - Related topic health (0.15)
   - Difficulty progression (0.15)

3. **Recommended Action Generation**:
   - Action templates per root cause
   - Context-aware customization
   - Primary + secondary actions
   - Time estimates and success criteria

Also added diagnostic-report.json schema to schemas.md.

## Outcome

- Impact: Intelligence Layer foundation established - system can explain WHY topics are weak
- Tests: N/A (skill definitions)
- Files: 1 created, 2 updated
- Next prompts: T032-T036 (Learning Pattern Detector) or T037-T041 (Knowledge Gap Predictor)
- Reflection: Root cause prioritization ensures most actionable item surfaces first; evidence-based diagnosis builds student trust

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: Validate root cause detection against real student performance patterns
