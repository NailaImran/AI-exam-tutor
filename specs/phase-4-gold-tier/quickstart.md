# Phase 4: Autonomous Coach - Quickstart Guide

> Get started with the fully autonomous exam coaching system

## Overview

Phase 4 transforms the AI Exam Tutor from a reactive Q&A system into a **fully autonomous Digital FTE** that proactively manages student preparation without manual intervention.

---

## Key Capabilities

| Capability | Skills Involved | What It Does |
|------------|-----------------|--------------|
| **Mock Exams** | mock-exam-generator, mock-exam-evaluator, exam-pressure-simulator | Full 100-question, 3-hour timed exams matching real SPSC/PPSC/KPPSC format |
| **Deep Diagnosis** | deep-dive-analyzer, knowledge-gap-predictor, forgetting-curve-tracker | Root-cause weak area analysis with predictive gap detection |
| **Proactive Coaching** | autonomous-session-initiator, learning-pattern-detector, motivation-monitor | System-initiated sessions based on optimal timing and engagement |
| **Spaced Repetition** | revision-cycle-manager, forgetting-curve-tracker | SM-2 based revision scheduling with decay tracking |
| **Exam Countdown** | exam-countdown-calibrator | Smart urgency adjustment (6 levels) as exam approaches |
| **Cross-Exam Prep** | syllabus-mapper | Switch between SPSC/PPSC/KPPSC with knowledge transfer |

---

## Quick Start Workflows

### 1. Trigger a Mock Exam

```
User: "I want to take a mock PPSC exam"

System Flow:
1. mock-exam-conductor orchestrates the workflow
2. mock-exam-generator creates 100 questions across 5 sections
3. exam-pressure-simulator configures time pressure
4. whatsapp-message-sender delivers exam
5. [Student completes exam under timed conditions]
6. mock-exam-evaluator scores with section breakdown
7. deep-dive-analyzer analyzes weak sections
8. Results include predicted real exam score with confidence interval
```

### 2. Enable Proactive Coaching

Proactive coaching runs automatically every 4 hours (8 AM, 12 PM, 4 PM, 8 PM PKT).

**What triggers a proactive session:**
- Revision items overdue (>= 5 items)
- Knowledge gap predicted (risk >= 0.7)
- Optimal study window detected + student idle >= 2 days
- High urgency (exam < 30 days away)

**What blocks a session:**
- Daily message limit reached
- Last message < 4 hours ago
- Student requested DND
- Quiet hours (11 PM - 6 AM PKT)

### 3. Switch Exam Target

```
User: "I'm switching from PPSC to SPSC"

System Flow:
1. syllabus-mapper loads cross-exam-mapping.json
2. Calculates knowledge transfer for each topic
3. Identifies:
   - Topics with high transfer (>90% overlap)
   - Partial coverage topics (30-90% overlap)
   - New topics unique to SPSC (Sindh-specific)
4. Generates transition plan with estimated hours
5. Updates study plan with SPSC priorities
```

### 4. Check Predicted Weak Areas

```
User: "What topics am I at risk of forgetting?"

System Flow:
1. forgetting-curve-tracker analyzes retention scores
2. knowledge-gap-predictor projects 7-day and 14-day scores
3. Returns at-risk topics ranked by severity
4. revision-cycle-manager schedules preventive revision
```

---

## Data Files (Phase 4)

All Phase 4 data is stored in `memory/students/{student_id}/`:

| File | Purpose | Updated By |
|------|---------|------------|
| `learning-profile.json` | Optimal study times, velocity, preferences | learning-pattern-detector |
| `revision-queue.json` | Spaced repetition queue with priorities | revision-cycle-manager |
| `gap-predictions.json` | Predicted weak areas with risk levels | knowledge-gap-predictor |
| `urgency-config.json` | Current urgency level and session adjustments | exam-countdown-calibrator |
| `engagement-tracking.json` | Disengagement state and nudge history | motivation-monitor |
| `daily-interactions.json` | Today's message counts for limit enforcement | autonomous-coach-coordinator |
| `mock-exams/{session_id}.json` | Individual mock exam results | mock-exam-evaluator |

---

## Subagent Reference

### autonomous-coach-coordinator
The master orchestrator that coordinates all proactive coaching.

**When to invoke:**
- Scheduled proactive checks
- Detecting disengagement patterns
- Deciding session type for a student

**Key features:**
- Skill coordination with weighted decision-making
- Daily limit enforcement by urgency level
- Graduated disengagement escalation (Day 1/3/7/14+)

### mock-exam-conductor
Manages end-to-end mock exam lifecycle.

**When to invoke:**
- Student requests mock exam
- Weekly scheduled mock (if enabled)
- Pre-exam final assessment

### deep-diagnostic-analyst
Comprehensive weakness analysis coordinator.

**When to invoke:**
- After mock exam completion
- Weekly diagnostic reviews
- When ERI declines unexpectedly

---

## Urgency Levels

The system automatically adjusts intensity based on days until exam:

| Level | Days Until Exam | Session Multiplier | Focus |
|-------|-----------------|-------------------|-------|
| `relaxed` | > 90 | 0.8x | Broad coverage, foundation |
| `normal` | 61-90 | 1.0x | Balanced, weak area focus |
| `elevated` | 31-60 | 1.3x | Intensive weak areas, mocks |
| `high` | 15-30 | 1.5x | Mock exams, revision cycles |
| `critical` | 8-14 | 1.8x | Rapid revision, confidence |
| `final_push` | 1-7 | 2.0x | Light review, stress management |

---

## Daily Limits

To prevent message fatigue, proactive messages are capped:

| Urgency Level | Max Messages/Day |
|---------------|------------------|
| relaxed | 2 |
| normal | 3 |
| elevated | 4 |
| high | 5 |
| critical | 6 |
| final_push | 4 (reduced to avoid stress) |

Student-initiated sessions have no limit.

---

## Disengagement Escalation

When a student stops practicing, the system escalates gradually:

| Idle Days | Action | Tone |
|-----------|--------|------|
| 1-2 | Quick reminder with question preview | Casual |
| 3 | Streak/ERI warning | Encouraging |
| 7 | Check-in with re-engagement options | Concerned |
| 14+ | Plan modification offer | Direct but caring |

---

## Success Metrics

Phase 4 targets these outcomes:

| Metric | Target | How Measured |
|--------|--------|--------------|
| Proactive session acceptance | >60% | Sessions completed / triggers sent |
| Prediction accuracy | >75% | Gap predictions that manifest in 2 weeks |
| Mock-to-real correlation | >0.85 | Mock scores vs actual exam results |
| Revision compliance | >70% | Revision items completed on schedule |
| Zero-touch days | >80% | Days without admin intervention |

---

## Integration Points

Phase 4 builds on previous phases:

| From | Used By Phase 4 |
|------|-----------------|
| Phase 1 | student-profile-loader, question-bank-querier, answer-evaluator, performance-tracker |
| Phase 2 | exam-readiness-calculator, weak-area-identifier, adaptive-test-generator |
| Phase 3 | whatsapp-message-sender, scheduled-task-runner, study-plan-generator |

---

## Troubleshooting

### "Proactive sessions aren't triggering"
1. Check `daily-interactions.json` - limit may be reached
2. Verify student hasn't enabled DND
3. Check if current time is in quiet hours

### "Mock exam predictions seem off"
1. Need at least 3 mock exams for reliable predictions
2. Check `mock-exams/` folder for recent results
3. Review confidence interval width (narrow = reliable)

### "Knowledge decay not tracking properly"
1. Verify `revision-queue.json` has topics with `last_reviewed` dates
2. Check if student has completed any recent sessions
3. Run manual forgetting-curve-tracker update

---

## File References

| File | Purpose |
|------|---------|
| `specs/phase-4-gold-tier/spec.md` | Full specification |
| `specs/phase-4-gold-tier/tasks.md` | Implementation tasks |
| `.claude/skills/exam-tutor/SKILL.md` | Skill bundle documentation |
| `.claude/agents/*.md` | Subagent definitions |
| `CLAUDE.md` | Project rules and workflows |
