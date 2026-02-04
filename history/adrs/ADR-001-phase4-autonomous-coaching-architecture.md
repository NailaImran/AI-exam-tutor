# ADR-001: Phase 4 Autonomous Coaching Architecture

**Status:** Accepted
**Date:** 2026-02-04
**Decision Makers:** System Architect
**Context:** Phase 4 Autonomous Coach implementation

---

## Context

Phase 4 transforms the AI Exam Tutor from a reactive Q&A system into a fully autonomous Digital FTE that proactively manages student preparation. This required significant architectural decisions about:

1. How to coordinate multiple intelligence skills
2. How to prevent message fatigue while remaining proactive
3. How to structure mock exam simulation
4. How to handle knowledge decay and spaced repetition
5. How to enable cross-exam preparation

---

## Decision 1: Hierarchical Subagent Coordination

### Problem
14 new skills needed coordination for autonomous coaching, mock exams, and deep diagnosis.

### Decision
Implement a **three-tier subagent hierarchy**:

```
autonomous-coach-coordinator (Master Orchestrator)
    ├── mock-exam-conductor (Mock Exam Lifecycle)
    │   ├── mock-exam-generator
    │   ├── mock-exam-evaluator
    │   └── exam-pressure-simulator
    │
    └── deep-diagnostic-analyst (Weakness Analysis)
        ├── deep-dive-analyzer
        ├── knowledge-gap-predictor
        └── forgetting-curve-tracker
```

### Rationale
- **Single responsibility**: Each subagent handles a coherent domain
- **Composability**: Can invoke subagents independently or through coordinator
- **Reduced complexity**: Main agent only talks to 3 orchestrators, not 14 skills

### Alternatives Considered
- Flat structure (all skills at same level) - rejected due to coordination complexity
- Single monolithic coordinator - rejected as too complex and harder to test

---

## Decision 2: Weighted Skill Coordination for Session Decisions

### Problem
Deciding when and how to proactively engage students requires balancing multiple factors.

### Decision
Implement **weighted skill coordination** with explicit decision matrix:

```
Weights:
- Revision due items: 30%
- Learning pattern fit: 25%
- Motivation/engagement: 25%
- Knowledge gap risk: 20%
```

### Rationale
- Revision (30%) highest because missed spaced repetition has measurable impact
- Engagement (25%) critical to avoid burnout and dropouts
- Patterns (25%) optimize for when student learns best
- Gaps (20%) preventive but less urgent than revision

### Alternatives Considered
- Rule-based system (if X then Y) - rejected as too rigid
- ML-based prediction - rejected as overkill for current scale
- Equal weights - rejected as not all factors have equal impact

---

## Decision 3: Urgency-Based Daily Limits

### Problem
Proactive messaging must not overwhelm students, but intensity should scale with exam proximity.

### Decision
Implement **6-level urgency system** with corresponding daily limits:

| Level | Days Until Exam | Messages/Day |
|-------|-----------------|--------------|
| relaxed | >90 | 2 |
| normal | 61-90 | 3 |
| elevated | 31-60 | 4 |
| high | 15-30 | 5 |
| critical | 8-14 | 6 |
| final_push | 1-7 | 4 (reduced) |

### Rationale
- **Graduated intensity**: Natural ramp-up as exam approaches
- **Final push reduction**: Last week should reduce stress, not add to it
- **Hard caps**: Even at critical, never more than 6/day (student-initiated exempt)

### Alternatives Considered
- Fixed limit regardless of urgency - rejected as too conservative
- No limits - rejected as would cause message fatigue
- Student-configurable limits - may add in future, but defaults needed first

---

## Decision 4: Graduated Disengagement Escalation

### Problem
Students who stop practicing need re-engagement, but aggressive follow-up feels spammy.

### Decision
Implement **4-stage escalation** over 14 days:

| Stage | Idle Days | Action | Tone |
|-------|-----------|--------|------|
| Day 1 | 1-2 | Question preview | Casual |
| Day 3 | 3 | Streak/ERI warning | Encouraging |
| Day 7 | 7 | Check-in with options | Concerned |
| Day 14 | 14+ | Plan modification offer | Direct |

### Rationale
- **Respectful patience**: Don't panic after 24 hours
- **Increasing concern**: Match tone to severity
- **Actionable exits**: Day 7+ always offer pause/modify options
- **No shame**: Never criticize absence, always supportive

### Alternatives Considered
- Single reminder after X days - rejected as too simplistic
- No automatic re-engagement - rejected as loses students
- Daily reminders - rejected as spammy

---

## Decision 5: SM-2 Based Spaced Repetition

### Problem
Need to track knowledge decay and schedule optimal revision times.

### Decision
Adapt **SuperMemo SM-2 algorithm** principles:

- Track retention score (0-100) per topic
- Calculate decay rate based on historical performance
- Schedule review when predicted retention drops below 70%
- Adjust intervals based on response quality

### Rationale
- **Proven algorithm**: SM-2 is well-researched and effective
- **Simplicity**: Doesn't require complex neural networks
- **Predictability**: Students can understand why topics are due
- **Flexibility**: Works with variable practice schedules

### Alternatives Considered
- Fixed interval review (every 7 days) - rejected as inefficient
- Free spaced repetition (Anki-style) - rejected as too user-driven for autonomous system
- Leitner box system - considered, but SM-2 more precise for our data

---

## Decision 6: Bidirectional Cross-Exam Mapping

### Problem
Students switching between SPSC/PPSC/KPPSC need knowledge transfer calculation.

### Decision
Maintain **complete bidirectional mapping** in `cross-exam-mapping.json`:

```json
{
  "mappings": {
    "PPSC": { "topic": { "equivalents": { "SPSC": {...}, "KPPSC": {...} }}},
    "SPSC": { "topic": { "equivalents": { "PPSC": {...}, "KPPSC": {...} }}},
    "KPPSC": { "topic": { "equivalents": { "PPSC": {...}, "SPSC": {...} }}}
  }
}
```

Each mapping includes:
- `confidence` (0-1): How similar the topics are
- `coverage_overlap` (0-1): Percentage of subtopics shared
- `notes`: Explanation of differences

### Rationale
- **Accuracy**: Different directions may have different transfer rates
- **Transparency**: Students see exactly what transfers
- **Maintainability**: One canonical file for all mappings

### Alternatives Considered
- One-directional mapping (calculate reverse) - rejected as asymmetric transfers exist
- No mapping (fresh start on switch) - rejected as unfair to students
- Automatic mapping generation - rejected as requires manual review for accuracy

---

## Decision 7: Mock Exam Confidence Intervals

### Problem
Predicting real exam scores from mocks requires communicating uncertainty.

### Decision
Always report predictions with **95% confidence intervals**:

```
Predicted score: 72
Confidence interval: [68, 76]
Prediction confidence: moderate
```

Interval width based on:
- Number of mock exams taken (more = tighter)
- Score consistency (lower SD = tighter)
- Exam-day adjustment (-5 points for pressure)

### Rationale
- **Honest uncertainty**: Don't overpromise accuracy
- **Actionable**: Narrow intervals mean reliable prediction
- **Motivating**: Even uncertain predictions set targets

### Alternatives Considered
- Single point prediction - rejected as misleading
- No predictions - rejected as students want guidance
- Percentage confidence (72% confident of passing) - rejected as harder to interpret

---

## Consequences

### Positive
- Clear separation of concerns with subagent hierarchy
- Predictable behavior with explicit decision matrices
- Respectful student engagement with graduated escalation
- Accurate knowledge transfer for cross-exam prep

### Negative
- More complexity than flat skill structure
- Urgency levels and limits may need tuning based on real usage
- SM-2 adaptation requires careful calibration

### Risks
- Proactive messaging may still feel intrusive to some students
- Prediction accuracy depends on sufficient mock exam data
- Cross-exam mapping requires maintenance when syllabi change

---

## Related Documents

- `specs/phase-4-gold-tier/spec.md` - Full Phase 4 specification
- `.claude/agents/autonomous-coach-coordinator.md` - Master orchestrator
- `syllabus/cross-exam-mapping.json` - Cross-exam topic mappings
- `.specify/memory/constitution.md` - Project principles (v1.4.0)
