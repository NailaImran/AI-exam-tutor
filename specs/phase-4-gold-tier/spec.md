# Phase 4: Autonomous Coach

> Transform the tutor into a fully autonomous, deeply personalized exam coach that proactively manages the student's entire preparation journey.

**Status:** Planned
**Spec Version:** 1.0.0
**Last Updated:** 2025-02-02

---

## Phase Goal

Evolve from a reactive Q&A system to an **autonomous Digital FTE** that:
- Proactively initiates learning sessions based on patterns
- Deeply understands individual learning behavior
- Simulates real exam conditions
- Predicts knowledge gaps before they become problems
- Manages the complete preparation lifecycle without manual intervention

---

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Single Student Focus** | All features serve one student's journey |
| **Proactive Autonomy** | System initiates, not just responds |
| **Deep Personalization** | Learns and adapts to individual patterns |
| **Exam Simulation Fidelity** | Authentic practice under real conditions |
| **Zero Manual Intervention** | Self-managing preparation lifecycle |

---

## Deliverables

| ID | Deliverable | Description | Skills Involved |
|----|-------------|-------------|-----------------|
| D4.1 | Mock Exam Engine | Full-length timed exams matching real SPSC/PPSC/KPPSC format | mock-exam-generator, mock-exam-evaluator, exam-pressure-simulator |
| D4.2 | Deep Diagnostic Analyzer | Root-cause analysis of weak areas with actionable insights | deep-dive-analyzer |
| D4.3 | Learning Pattern Detector | Identify optimal study times, methods, and learning velocity | learning-pattern-detector |
| D4.4 | Autonomous Session Manager | Proactive session initiation based on multiple factors | autonomous-session-initiator |
| D4.5 | Knowledge Gap Predictor | Anticipate weaknesses before they manifest | knowledge-gap-predictor |
| D4.6 | Revision Cycle Engine | Spaced repetition with forgetting curve tracking | revision-cycle-manager, forgetting-curve-tracker |
| D4.7 | Exam Countdown Intelligence | Smart urgency calibration based on exam date | exam-countdown-calibrator |
| D4.8 | Cross-Exam Syllabus Mapper | Topic equivalence mapping across SPSC/PPSC/KPPSC | syllabus-mapper |

---

## Skills Inventory

### CORE (Foundation for Autonomy)

| ID | Skill | Purpose | Inputs | Outputs |
|----|-------|---------|--------|---------|
| P4-001 | `session-logger` | Audit trail for all interactions | session_data | log_entry |
| P4-002 | `syllabus-mapper` | Map topics across exam types | source_exam, target_exam, topic | equivalent_topics |

### MASTERY (Exam Simulation)

| ID | Skill | Purpose | Inputs | Outputs |
|----|-------|---------|--------|---------|
| P4-003 | `mock-exam-generator` | Full timed exam matching real format | student_id, exam_type, duration | mock_exam_session |
| P4-004 | `mock-exam-evaluator` | Comprehensive mock scoring with insights | session_id, answers | detailed_results |
| P4-005 | `exam-pressure-simulator` | Add time pressure and distractions | session_id, pressure_level | modified_session |

### INTELLIGENCE (Deep Analysis)

| ID | Skill | Purpose | Inputs | Outputs |
|----|-------|---------|--------|---------|
| P4-006 | `deep-dive-analyzer` | Root-cause analysis of weak areas | student_id, topic | diagnostic_report |
| P4-007 | `learning-pattern-detector` | Identify when/how student learns best | student_id | learning_profile |
| P4-008 | `knowledge-gap-predictor` | Predict future weak areas | student_id, syllabus_coverage | predicted_gaps |
| P4-009 | `forgetting-curve-tracker` | Track knowledge decay per topic | student_id | decay_predictions |

### AUTONOMY (Self-Managing)

| ID | Skill | Purpose | Inputs | Outputs |
|----|-------|---------|--------|---------|
| P4-010 | `autonomous-session-initiator` | Decide when to start sessions | student_id, context | session_trigger |
| P4-011 | `study-pattern-optimizer` | Optimize study schedule | student_id, constraints | optimized_schedule |
| P4-012 | `revision-cycle-manager` | Manage spaced repetition | student_id | revision_queue |
| P4-013 | `exam-countdown-calibrator` | Adjust urgency based on date | student_id, exam_date | urgency_config |
| P4-014 | `motivation-monitor` | Track engagement, prevent burnout | student_id | engagement_status |

---

## Subagents

| ID | Subagent | Purpose | Orchestrates |
|----|----------|---------|--------------|
| P4-015 | `autonomous-coach-coordinator` | Master orchestrator for proactive coaching | All Phase 4 skills |
| P4-016 | `mock-exam-conductor` | End-to-end mock exam management | mock-exam-generator, mock-exam-evaluator, exam-pressure-simulator |
| P4-017 | `deep-diagnostic-analyst` | Comprehensive weakness analysis | deep-dive-analyzer, knowledge-gap-predictor, forgetting-curve-tracker |

---

## Workflows

### Autonomous Daily Coaching
```
1. autonomous-session-initiator  → Check if session needed (time, gap, urgency)
2. learning-pattern-detector     → Get optimal study window for student
3. motivation-monitor            → Check engagement level (prevent burnout)
4. revision-cycle-manager        → Get due revision items (spaced repetition)
5. knowledge-gap-predictor       → Identify at-risk topics
6. [Generate personalized session based on all factors]
7. whatsapp-message-sender       → Proactively engage student
8. session-logger                → Record session initiation
```

### Full Mock Exam Session
```
1. mock-exam-generator           → Create full exam (100 questions, 3 hours)
2. exam-pressure-simulator       → Configure time pressure level
3. whatsapp-message-sender       → Deliver exam to student
4. [Student completes mock under timed conditions]
5. mock-exam-evaluator           → Score with detailed breakdown by section
6. deep-dive-analyzer            → Analyze weak sections (root cause)
7. study-plan-generator          → Update plan based on results
8. exam-countdown-calibrator     → Recalibrate urgency
9. whatsapp-message-sender       → Send comprehensive results
10. session-logger               → Record mock exam completion
```

### Predictive Gap Intervention
```
1. forgetting-curve-tracker      → Identify decaying knowledge (retention < 50%)
2. knowledge-gap-predictor       → Project future weak areas
3. revision-cycle-manager        → Schedule preventive revision
4. autonomous-session-initiator  → Trigger intervention session
5. whatsapp-message-sender       → "You haven't practiced X in 2 weeks..."
6. session-logger                → Record intervention
```

### Cross-Exam Preparation
```
1. syllabus-mapper               → Map current knowledge to target exam
2. knowledge-gap-predictor       → Identify gaps specific to new exam
3. adaptive-test-generator       → Generate exam-specific practice
4. study-plan-generator          → Create transition plan
```

---

## Data Schemas

### memory/students/{id}/learning-profile.json
```json
{
  "student_id": "string",
  "optimal_study_times": ["morning", "evening"],
  "session_duration_preference": 30,
  "learning_velocity": {
    "fast_topics": ["current_affairs", "general_knowledge"],
    "slow_topics": ["constitutional_law", "islamic_studies"]
  },
  "engagement_patterns": {
    "peak_days": ["monday", "wednesday", "saturday"],
    "low_engagement_days": ["friday"],
    "average_sessions_per_week": 5,
    "dropout_risk_indicators": []
  },
  "preferred_difficulty_ramp": "gradual",
  "response_to_pressure": "moderate",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### memory/students/{id}/mock-exams/{session_id}.json
```json
{
  "session_id": "string",
  "student_id": "string",
  "exam_type": "PPSC",
  "exam_format": {
    "total_questions": 100,
    "duration_minutes": 180,
    "sections": ["pakistan_studies", "general_knowledge", "current_affairs", "english", "math"]
  },
  "results": {
    "completed_questions": 95,
    "time_taken_minutes": 165,
    "time_per_question_avg_seconds": 104,
    "section_breakdown": {
      "pakistan_studies": { "correct": 18, "total": 20, "time_avg": 95 },
      "general_knowledge": { "correct": 15, "total": 20, "time_avg": 120 },
      "current_affairs": { "correct": 17, "total": 20, "time_avg": 85 },
      "english": { "correct": 14, "total": 20, "time_avg": 110 },
      "math": { "correct": 12, "total": 20, "time_avg": 130 }
    },
    "overall_score": 76,
    "percentile_estimate": 72
  },
  "analysis": {
    "pressure_handling": "moderate",
    "fatigue_detected_at_question": 85,
    "accuracy_trend": "declining_after_q70",
    "time_management": "rushed_final_section"
  },
  "predictions": {
    "predicted_real_exam_score": 72,
    "confidence_interval": [68, 76],
    "ready_for_exam": false,
    "recommended_mock_count": 3
  },
  "created_at": "ISO8601"
}
```

### memory/students/{id}/revision-queue.json
```json
{
  "student_id": "string",
  "queue": [
    {
      "topic_id": "constitutional_amendments",
      "subject": "pakistan_studies",
      "last_reviewed": "ISO8601",
      "retention_score": 0.45,
      "decay_rate": 0.08,
      "due_date": "ISO8601",
      "priority": "urgent",
      "revision_count": 3,
      "optimal_interval_days": 7
    }
  ],
  "settings": {
    "algorithm": "sm2",
    "minimum_retention_target": 0.70,
    "daily_revision_limit": 10
  },
  "updated_at": "ISO8601"
}
```

### memory/students/{id}/gap-predictions.json
```json
{
  "student_id": "string",
  "predictions": [
    {
      "topic_id": "federal_structure",
      "subject": "pakistan_studies",
      "current_score": 0.65,
      "predicted_score_7d": 0.52,
      "predicted_score_14d": 0.41,
      "risk_level": "high",
      "contributing_factors": [
        "no_practice_last_10_days",
        "historically_difficult_topic",
        "related_topics_also_weak"
      ],
      "recommended_action": "schedule_revision_immediately"
    }
  ],
  "generated_at": "ISO8601"
}
```

### logs/sessions/{student_id}/{date}.json
```json
{
  "date": "ISO8601",
  "sessions": [
    {
      "session_id": "string",
      "type": "autonomous_daily|mock_exam|intervention|student_initiated",
      "initiated_by": "system|student",
      "trigger_reason": "scheduled|gap_detected|revision_due|student_request",
      "started_at": "ISO8601",
      "ended_at": "ISO8601",
      "duration_minutes": 25,
      "activities": [
        {
          "activity": "adaptive_test",
          "questions_count": 10,
          "score": 0.70
        }
      ],
      "eri_before": 58,
      "eri_after": 59,
      "notes": "string"
    }
  ]
}
```

---

## MCP Integrations

| Server | Purpose | Phase 4 Usage |
|--------|---------|---------------|
| `filesystem` | Core data persistence | All skills - reading/writing student data |
| `whatsapp` | Student communication | Proactive session triggers, mock exam delivery, results |
| `github` | Version control | Optional backup of student progress |

**Explicitly NOT Included:**
- No Odoo integration (no payments/subscriptions)
- No LinkedIn posting (completed in Phase 3)
- No multi-user dashboards or analytics

---

## Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Proactive session acceptance | >60% | Sessions initiated by system that student completes |
| Prediction accuracy | >75% | Gap predictions that manifest within 2 weeks |
| Mock-to-real correlation | >0.85 | Mock exam scores vs actual exam performance |
| Revision compliance | >70% | Spaced repetition items completed on schedule |
| Zero-touch days | >80% | Days where system operates without admin input |
| Student ERI improvement | +15pts/month | Average ERI growth during active use |

---

## Dependencies

### From Phase 3
- `whatsapp-message-sender` - for student communication
- `study-plan-generator` - for plan updates after mocks
- `scheduled-task-runner` - for autonomous triggers
- `adaptive-test-generator` - for session content

### From Phase 2
- `exam-readiness-calculator` - for ERI updates
- `weak-area-identifier` - feeds into deep analysis

### From Phase 1
- `student-profile-loader` - all sessions need profile
- `answer-evaluator` - for all evaluations
- `performance-tracker` - for all results persistence

---

## Implementation Priority

| Priority | Skills | Rationale |
|----------|--------|-----------|
| P0 (Critical) | session-logger, mock-exam-generator, mock-exam-evaluator | Core functionality |
| P1 (High) | autonomous-session-initiator, revision-cycle-manager, forgetting-curve-tracker | Autonomy foundation |
| P2 (Medium) | deep-dive-analyzer, learning-pattern-detector, knowledge-gap-predictor | Intelligence layer |
| P3 (Lower) | exam-pressure-simulator, study-pattern-optimizer, motivation-monitor | Enhancement features |
| P4 (Final) | syllabus-mapper, exam-countdown-calibrator | Polish features |

---

## Non-Goals (Explicitly Excluded)

- B2B / Academy / Institution features
- Multi-student dashboards or comparisons
- Payment or subscription management
- Parent/guardian portals or reports
- Business analytics or metrics
- SaaS infrastructure or multi-tenancy
- User authentication or login systems
- Instructor or admin interfaces

---

## Migration Notes

### Skills Promoted from OPTIONAL to CORE
| Skill | Old Category | New Category | Changes |
|-------|--------------|--------------|---------|
| session-logger | OPTIONAL | CORE | Now mandatory for audit trail |
| syllabus-mapper | OPTIONAL | CORE | Essential for cross-exam prep |

### Skills Removed (B2B/Business)
| Skill | Reason |
|-------|--------|
| batch-test-assigner | B2B feature - multi-student |
| performance-comparator | B2B feature - multi-student |
| parent-report-generator | B2B feature - external stakeholder |
| payment-tracker | Business feature |
| subscription-manager | Business feature |
| business-audit-generator | Business feature |

---

## Appendix: Exam Format Reference

### PPSC Format
- 100 MCQs
- 180 minutes
- Sections: Pakistan Studies (20), General Knowledge (20), Current Affairs (20), English (20), Math/Reasoning (20)

### SPSC Format
- 100 MCQs
- 180 minutes
- Sections: Similar to PPSC with Sindh-specific content

### KPPSC Format
- 100 MCQs
- 180 minutes
- Sections: Similar to PPSC with KPK-specific content
