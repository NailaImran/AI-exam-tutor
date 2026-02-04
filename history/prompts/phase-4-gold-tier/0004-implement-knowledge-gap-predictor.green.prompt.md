---
id: "0004"
title: "Implement Knowledge Gap Predictor T037-T041"
stage: green
date: 2025-02-03
surface: claude-code
model: claude-opus-4-5-20251101
feature: phase-4-gold-tier
branch: master
user: lenovo
command: /sp.implement T037-T041
labels: [phase-4, knowledge-gap, prediction, intelligence, subagent]
links:
  spec: specs/phase-4-gold-tier/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - .claude/skills/exam-tutor/knowledge-gap-predictor/SKILL.md (created)
  - .claude/agents/deep-diagnostic-analyst.md (created)
  - specs/phase-4-gold-tier/tasks.md (updated)
tests:
  - N/A (skill definitions, no runtime tests)
---

## Prompt

/sp.implement T037-T041

Implement tasks T037-T041 from Phase 4 Gold Tier, which comprise the D4.5 Knowledge Gap Predictor deliverable:
- T037: Create knowledge-gap-predictor skill
- T038: Implement 7-day and 14-day score projections
- T039: Implement risk_level classification (high, medium, low)
- T040: Implement prediction confidence scoring
- T041: Create deep-diagnostic-analyst subagent

## Response snapshot

### knowledge-gap-predictor skill

Created predictive analysis skill with:

1. **Score Projections**:
   - Combines retention decay factor with trajectory adjustment
   - Formula: `predicted = current × decay_factor + trend_adjustment`
   - Projects for 7 and 14 days ahead

2. **Risk Classification**:
   - `high`: predicted_14d < 50% OR drop > 20 points
   - `medium`: predicted_14d < 70% OR drop > 10 points
   - `low`: predicted_14d >= 70% AND drop <= 10 points

3. **Confidence Scoring** (4 weighted factors):
   - Data volume (0.30) - session count with topic
   - Data recency (0.25) - days since last practice
   - Trend stability (0.25) - variance in performance
   - Decay rate reliability (0.20) - quality of retention data

4. **Contributing Factors Detection**:
   - no_practice_last_14_days, high_decay_rate, declining_performance_trend
   - related_topics_weak, historically_difficult_topic, low_current_retention

5. **Alert Generation**:
   - critical_gap, approaching_gap, cluster_weakness alerts

### deep-diagnostic-analyst subagent

Created orchestration subagent that:
- Orchestrates: deep-dive-analyzer, knowledge-gap-predictor, forgetting-curve-tracker
- Synthesizes comprehensive diagnostic reports
- Generates prioritized action plans
- Calculates overall health status (critical/concerning/stable/healthy)
- Produces study time allocation by subject and priority

## Outcome

- Impact: **Phase 4 Intelligence Layer COMPLETE** - system can now explain weak areas AND predict future gaps
- Tests: N/A (skill definitions)
- Files: 2 created, 1 updated
- Next prompts: T042-T051 (Phase 5: Enhancement Features)
- Reflection: Prediction model combines decay curves with trend analysis for more accurate projections; confidence scoring prevents over-reliance on low-quality predictions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: Validate prediction accuracy by comparing projected vs actual scores after 7/14 days
