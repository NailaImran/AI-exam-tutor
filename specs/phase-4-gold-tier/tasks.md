# Tasks: Phase 4 - Autonomous Coach

**Input**: Design documents from `/specs/phase-4-gold-tier/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Tests**: Not explicitly requested - omitting test tasks.

**Organization**: Tasks grouped by deliverable (D4.1-D4.8) mapped to implementation priorities (P0-P4).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which deliverable this task belongs to (D4.1-D4.8)
- Include exact file paths in descriptions

## Path Conventions

- **Skills**: `.claude/skills/exam-tutor/{skill-name}/SKILL.md`
- **Subagents**: `.claude/agents/{subagent-name}.md`
- **Memory schemas**: `memory/students/{id}/*.json`
- **Logs**: `logs/sessions/{student_id}/*.json`
- **References**: `.claude/skills/exam-tutor/references/*.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory structure and update references for Phase 4

- [x] T001 Create skill directories for all 14 Phase 4 skills in `.claude/skills/exam-tutor/`
- [x] T002 [P] Update `.claude/skills/exam-tutor/references/schemas.md` with Phase 4 data schemas
- [x] T003 [P] Update `.claude/skills/exam-tutor/references/skill-orchestration.md` with Phase 4 workflows
- [x] T004 [P] Create `memory/students/{id}/mock-exams/` directory structure documentation
- [x] T005 [P] Create `memory/students/{id}/learning-profile.json` schema template
- [x] T006 [P] Create `memory/students/{id}/revision-queue.json` schema template
- [x] T007 [P] Create `memory/students/{id}/gap-predictions.json` schema template
- [x] T008 [P] Create `logs/sessions/{student_id}/{date}.json` schema template

---

## Phase 2: Foundational - Core Skills (P0 Priority)

**Purpose**: Establish session logging and mock exam foundation - BLOCKS all autonomy features

**⚠️ CRITICAL**: No autonomy work can begin until session-logger and mock exam skills are complete

### D4.1: Mock Exam Engine (Core Skills)

- [x] T009 [D4.1] Create `session-logger` skill in `.claude/skills/exam-tutor/session-logger/SKILL.md`
- [x] T010 [P] [D4.1] Create `mock-exam-generator` skill in `.claude/skills/exam-tutor/mock-exam-generator/SKILL.md`
- [x] T011 [P] [D4.1] Create `mock-exam-evaluator` skill in `.claude/skills/exam-tutor/mock-exam-evaluator/SKILL.md`
- [x] T012 [D4.1] Define mock exam format configuration (100 questions, 180 minutes, 5 sections)
- [x] T013 [D4.1] Implement section breakdown logic in mock-exam-evaluator (pakistan_studies, general_knowledge, current_affairs, english, math)
- [x] T014 [D4.1] Implement fatigue detection algorithm (accuracy decline after question N)
- [x] T015 [D4.1] Implement real exam score prediction with confidence intervals
- [x] T016 [D4.1] Create `mock-exam-conductor` subagent in `.claude/agents/mock-exam-conductor.md`

**Checkpoint**: Student can complete and receive scored mock exam with section breakdown

---

## Phase 3: Autonomy Foundation (P1 Priority)

**Purpose**: Enable proactive session management and spaced repetition

**Goal**: System can suggest sessions and manage revision cycles

### D4.4: Autonomous Session Manager

- [x] T017 [D4.4] Create `autonomous-session-initiator` skill in `.claude/skills/exam-tutor/autonomous-session-initiator/SKILL.md`
- [x] T018 [D4.4] Implement session trigger decision logic (time, gaps, urgency factors)
- [x] T019 [D4.4] Implement daily interaction limits (max 2 proactive triggers/day)
- [x] T020 [D4.4] Implement 4-hour cooldown between proactive triggers

### D4.6: Revision Cycle Engine

- [x] T021 [P] [D4.6] Create `forgetting-curve-tracker` skill in `.claude/skills/exam-tutor/forgetting-curve-tracker/SKILL.md`
- [x] T022 [P] [D4.6] Create `revision-cycle-manager` skill in `.claude/skills/exam-tutor/revision-cycle-manager/SKILL.md`
- [x] T023 [D4.6] Implement SM-2 spaced repetition algorithm in forgetting-curve-tracker
- [x] T024 [D4.6] Implement retention score calculation (decay_rate, optimal_interval_days)
- [x] T025 [D4.6] Implement revision queue prioritization (urgent, high, normal, low)
- [x] T026 [D4.6] Implement minimum_retention_target threshold (0.70 default)
- [x] T027 [D4.6] Implement daily_revision_limit enforcement (10 items default)

**Checkpoint**: System can proactively suggest sessions and manage spaced repetition queue

---

## Phase 4: Intelligence Layer (P2 Priority)

**Purpose**: Enable deep analysis and predictive capabilities

**Goal**: System can explain weak areas and predict future gaps

### D4.2: Deep Diagnostic Analyzer

- [x] T028 [D4.2] Create `deep-dive-analyzer` skill in `.claude/skills/exam-tutor/deep-dive-analyzer/SKILL.md`
- [x] T029 [D4.2] Implement root cause identification (no_practice, historically_difficult, related_weakness)
- [x] T030 [D4.2] Implement contributing factors analysis
- [x] T031 [D4.2] Implement recommended_action generation

### D4.3: Learning Pattern Detector

- [x] T032 [P] [D4.3] Create `learning-pattern-detector` skill in `.claude/skills/exam-tutor/learning-pattern-detector/SKILL.md`
- [x] T033 [D4.3] Implement optimal_study_times detection from session history
- [x] T034 [D4.3] Implement learning_velocity calculation per topic (fast_topics, slow_topics)
- [x] T035 [D4.3] Implement engagement_patterns analysis (peak_days, low_engagement_days)
- [x] T036 [D4.3] Implement preferred_difficulty_ramp detection (gradual, aggressive, mixed)

### D4.5: Knowledge Gap Predictor

- [x] T037 [P] [D4.5] Create `knowledge-gap-predictor` skill in `.claude/skills/exam-tutor/knowledge-gap-predictor/SKILL.md`
- [x] T038 [D4.5] Implement 7-day and 14-day score projections
- [x] T039 [D4.5] Implement risk_level classification (high, medium, low)
- [x] T040 [D4.5] Implement prediction confidence scoring
- [x] T041 [D4.5] Create `deep-diagnostic-analyst` subagent in `.claude/agents/deep-diagnostic-analyst.md`

**Checkpoint**: System can explain why topics are weak and predict future gaps with confidence

---

## Phase 5: Enhancement Features (P3 Priority)

**Purpose**: Add pressure simulation, schedule optimization, and engagement monitoring

**Goal**: Full personalization pipeline operational

### D4.1: Mock Exam Engine (Enhancement)

- [x] T042 [D4.1] Create `exam-pressure-simulator` skill in `.claude/skills/exam-tutor/exam-pressure-simulator/SKILL.md`
- [x] T043 [D4.1] Implement pressure levels (standard, high, extreme)
- [x] T044 [D4.1] Implement response_to_pressure profile tracking
- [x] T045 [D4.1] Integrate fatigue_detected_at tracking with mock evaluator

### D4.4: Autonomous Session Manager (Enhancement)

- [x] T046 [P] [D4.4] Create `study-pattern-optimizer` skill in `.claude/skills/exam-tutor/study-pattern-optimizer/SKILL.md`
- [x] T047 [P] [D4.4] Create `motivation-monitor` skill in `.claude/skills/exam-tutor/motivation-monitor/SKILL.md`
- [x] T048 [D4.4] Implement schedule optimization based on learning patterns
- [x] T049 [D4.4] Implement dropout_risk_indicators detection
- [x] T050 [D4.4] Implement engagement decline alerting
- [x] T051 [D4.4] Implement graduated nudging strategy (1 day → 3 days → 7 days)

**Checkpoint**: Full personalization pipeline operational, engagement metrics tracked

---

## Phase 6: Polish Features (P4 Priority)

**Purpose**: Cross-exam mapping and urgency calibration

**Goal**: Student can switch exam targets, final readiness assessment accurate

### D4.7: Exam Countdown Intelligence

- [x] T052 [D4.7] Create `exam-countdown-calibrator` skill in `.claude/skills/exam-tutor/exam-countdown-calibrator/SKILL.md`
- [x] T053 [D4.7] Implement urgency scaling based on days until exam
- [x] T054 [D4.7] Implement session frequency adjustment per urgency level
- [x] T055 [D4.7] Implement final readiness band determination (exam_ready, ready, approaching)
- [x] T056 [D4.7] Implement confidence interval calculation for predicted real exam score

### D4.8: Cross-Exam Syllabus Mapper

- [x] T057 [P] [D4.8] Create `syllabus-mapper` skill in `.claude/skills/exam-tutor/syllabus-mapper/SKILL.md`
- [x] T058 [D4.8] Implement topic equivalence mapping (SPSC ↔ PPSC ↔ KPPSC)
- [x] T059 [D4.8] Implement knowledge transfer calculation when switching exams
- [x] T060 [D4.8] Update `syllabus/cross-exam-mapping.json` with complete topic mappings

**Checkpoint**: Student can switch exam targets seamlessly, final readiness assessment accurate

---

## Phase 7: Master Orchestration

**Purpose**: Create the autonomous coach coordinator that ties everything together

- [x] T061 Create `autonomous-coach-coordinator` subagent in `.claude/agents/autonomous-coach-coordinator.md`
- [x] T062 Implement proactive session check workflow (every 4 hours)
- [x] T063 Implement skill coordination logic (learning-pattern → motivation → revision → gap-predictor)
- [x] T064 Implement daily limit enforcement across all proactive triggers
- [x] T065 Implement escalation for student disengagement patterns
- [x] T066 Update `.claude/skills/exam-tutor/SKILL.md` with Phase 4 skill inventory
- [x] T067 Update `CLAUDE.md` with Phase 4 workflows and skill references

---

## Phase 8: Integration & Documentation

**Purpose**: Final integration and documentation updates

- [x] T068 [P] Update `MASTER_PLAN.md` with Phase 4 completion status
- [x] T069 [P] Update `TASKS-ARCHIVE.md` with completed Phase 4 tasks
- [x] T070 [P] Create Phase 4 quickstart guide in `specs/phase-4-gold-tier/quickstart.md`
- [x] T071 Validate all Phase 4 workflows end-to-end
- [x] T072 Update constitution version to 1.4.0 with any Phase 4 learnings
- [x] T073 Create ADR for Phase 4 architectural decisions in `history/adrs/`

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (P0) ─── BLOCKS ALL SUBSEQUENT PHASES
    ↓
Phase 3: Autonomy Foundation (P1)
    ↓
Phase 4: Intelligence Layer (P2)
    ↓
Phase 5: Enhancement Features (P3)
    ↓
Phase 6: Polish Features (P4)
    ↓
Phase 7: Master Orchestration
    ↓
Phase 8: Integration & Documentation
```

### Deliverable Dependencies

| Deliverable | Depends On | Blocks |
|-------------|------------|--------|
| D4.1 Mock Exam Engine | None | D4.2, D4.4, D4.7 |
| D4.2 Deep Diagnostic | D4.1 (session-logger) | D4.5 |
| D4.3 Learning Pattern | D4.1 (session-logger) | D4.4 |
| D4.4 Autonomous Session | D4.1, D4.3, D4.6 | D4.7 |
| D4.5 Knowledge Gap | D4.2, D4.6 | D4.7 |
| D4.6 Revision Cycle | D4.1 (session-logger) | D4.4, D4.5 |
| D4.7 Exam Countdown | D4.1, D4.4, D4.5 | None |
| D4.8 Syllabus Mapper | None | None |

### Within Each Phase

- Skills can be created in parallel [P] if they don't share dependencies
- Subagents must be created AFTER all skills they orchestrate
- Schema updates should happen in Phase 1 before skill implementation

### Parallel Opportunities

**Phase 1** (All parallelizable):
- T002, T003, T004, T005, T006, T007, T008

**Phase 2**:
- T010, T011 (mock-exam-generator and evaluator)

**Phase 3**:
- T021, T022 (forgetting-curve-tracker and revision-cycle-manager)

**Phase 4**:
- T028, T032, T037 (deep-dive-analyzer, learning-pattern-detector, knowledge-gap-predictor)

**Phase 5**:
- T046, T047 (study-pattern-optimizer and motivation-monitor)

---

## Parallel Example: Phase 4 Intelligence Layer

```bash
# Launch all intelligence skills in parallel:
Task: "Create deep-dive-analyzer skill in .claude/skills/exam-tutor/deep-dive-analyzer/SKILL.md"
Task: "Create learning-pattern-detector skill in .claude/skills/exam-tutor/learning-pattern-detector/SKILL.md"
Task: "Create knowledge-gap-predictor skill in .claude/skills/exam-tutor/knowledge-gap-predictor/SKILL.md"

# Then sequentially implement algorithms:
Task: "Implement root cause identification"
Task: "Implement optimal_study_times detection"
Task: "Implement 7-day and 14-day score projections"
```

---

## Implementation Strategy

### MVP First (D4.1 + D4.6 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (mock exam engine)
3. Complete Phase 3: D4.6 only (revision cycle)
4. **STOP and VALIDATE**: Test mock exams + spaced repetition
5. Deploy/demo - student can take mocks and get revision suggestions

### Incremental Delivery

| Increment | Deliverables | Value Delivered |
|-----------|--------------|-----------------|
| MVP | D4.1, D4.6 | Mock exams, spaced repetition |
| +Intelligence | D4.2, D4.3, D4.5 | Weak area analysis, pattern detection, gap prediction |
| +Autonomy | D4.4 | Proactive session initiation |
| +Polish | D4.7, D4.8 | Urgency calibration, cross-exam support |

### Validation Gates

| Transition | Required Validation |
|------------|---------------------|
| Phase 2 → 3 | Mock exam flow complete, logging verified |
| Phase 3 → 4 | Spaced repetition working, daily limits respected |
| Phase 4 → 5 | Predictions generated with confidence scores |
| Phase 5 → 6 | Full personalization pipeline operational |
| Phase 6 → 7 | All skills tested independently |
| Phase 7 → 8 | End-to-end autonomous coaching workflow validated |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Tasks** | 73 |
| **Phase 1 (Setup)** | 8 |
| **Phase 2 (P0 Foundational)** | 8 |
| **Phase 3 (P1 Autonomy)** | 11 |
| **Phase 4 (P2 Intelligence)** | 14 |
| **Phase 5 (P3 Enhancement)** | 10 |
| **Phase 6 (P4 Polish)** | 9 |
| **Phase 7 (Orchestration)** | 7 |
| **Phase 8 (Documentation)** | 6 |
| **Parallel Opportunities** | 20 tasks marked [P] |
| **Skills to Create** | 14 |
| **Subagents to Create** | 3 |

---

## Notes

- [P] tasks = different files, no dependencies
- [D4.x] label maps task to specific deliverable for traceability
- Each phase should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate deliverable independently
- Avoid: vague tasks, same file conflicts, cross-phase dependencies that break independence
