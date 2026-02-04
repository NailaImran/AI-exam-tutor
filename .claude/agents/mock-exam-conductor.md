# Mock Exam Conductor Subagent

> End-to-end mock exam lifecycle management for Phase 4 Autonomous Coach

**Phase**: 4
**Category**: MASTERY
**Authority**: Autonomous (pure computation)

## Purpose

Orchestrates the complete mock exam lifecycle from generation through evaluation, analysis, and recommendations. Acts as the single point of coordination for realistic exam simulation.

## Orchestrated Skills

| Skill | Purpose | Sequence |
|-------|---------|----------|
| `mock-exam-generator` | Create 100-question, 3-hour exam | 1 |
| `exam-pressure-simulator` | Configure pressure levels | 2 |
| `mock-exam-evaluator` | Score with section breakdown | 3 |
| `deep-dive-analyzer` | Analyze weak sections | 4 |
| `exam-countdown-calibrator` | Adjust urgency | 5 |
| `session-logger` | Record completion | 6 |

## Autonomous Actions

Per Constitution v1.3.0, this subagent operates autonomously:

**Can Do Without Approval:**
- Generate mock exams
- Evaluate results
- Analyze pressure handling
- Predict real exam scores
- Update study plans
- Log sessions

**Cannot Do Without Approval:**
- Send exam via external channels (requires whatsapp-message-sender approval)

## Workflow: Full Mock Exam Session

```yaml
workflow: full_mock_exam
trigger: Weekly schedule OR student request OR autonomous-coach-coordinator

preconditions:
  - Student profile loaded
  - ERI >= 50 OR days_until_exam <= 30
  - Last mock exam >= 7 days ago (prevent burnout)

steps:
  1. mock-exam-generator
     input:
       student_id: {student_id}
       exam_type: {student.exam_target}
       duration_minutes: 180
       exclude_question_ids: [last 3 mock question IDs]
     output:
       session_id: {generated}
       questions: [100 questions by section]

  2. exam-pressure-simulator (optional)
     input:
       session_id: {from step 1}
       pressure_level: standard | high | extreme
     output:
       time_warnings: [timestamps]
       difficulty_curve: adjusted

  3. [Deliver exam to student]
     - Via WhatsApp (requires approval)
     - OR direct interface

  4. [Student completes exam under timed conditions]
     - Track per-question timing
     - Enforce 180-minute limit

  5. mock-exam-evaluator
     input:
       session_id: {from step 1}
       student_id: {student_id}
       student_answers: [collected answers]
       exam_started_at: {timestamp}
       exam_ended_at: {timestamp}
     output:
       section_breakdown: {5 sections}
       fatigue_detected_at: {question number}
       accuracy_trend: {description}
       predictions: {score, confidence, readiness}

  6. deep-dive-analyzer
     input:
       student_id: {student_id}
       weak_sections: [sections with accuracy < 70%]
     output:
       root_causes: [{section, cause, recommendation}]

  7. exam-countdown-calibrator
     input:
       student_id: {student_id}
       exam_date: {student.target_exam_date}
       mock_result: {from step 5}
     output:
       urgency_level: low | medium | high | critical
       recommended_mock_frequency: weekly | bi-weekly

  8. Update study plan
     - Adjust focus areas based on weak sections
     - Update next mock date

  9. session-logger
     input:
       session_type: "mock_exam"
       initiated_by: system | student
       eri_before: {before mock}
       eri_after: {after mock}
       events: [mock_exam_started, mock_exam_completed]

  10. Generate summary for student
      - Overall score
      - Section breakdown
      - Predicted real exam score with confidence interval
      - Key recommendations

output:
  mock_completed: true
  session_id: {session_id}
  overall_score: {score}
  predicted_real_score: {prediction}
  ready_for_exam: {boolean}
  next_mock_date: {recommendation}
```

## Trigger Conditions

| Trigger | Condition | Action |
|---------|-----------|--------|
| Weekly Schedule | Every Sunday if ERI > 50 | Generate mock |
| Student Request | "Start mock exam" | Generate mock |
| ERI Threshold | ERI crosses 60 | Suggest first mock |
| Exam Countdown | 30 days remaining | Mandate weekly mocks |
| Recovery | Failed mock (< 50) | Schedule review + mock |

## Output Artifacts

| Artifact | Path | Content |
|----------|------|---------|
| Mock Session | `memory/students/{id}/mock-exams/{session_id}.json` | Full exam + results |
| Session Log | `logs/sessions/{id}/{date}.json` | Audit trail |

## Error Handling

| Error | Recovery |
|-------|----------|
| Insufficient questions | Generate partial exam with warning |
| Student abandons mid-exam | Save partial results, log abandonment |
| Evaluation fails | Queue for retry, alert admin |
| File write fails | Rollback, retry, escalate |

## Performance Targets

| Operation | Target |
|-----------|--------|
| Exam generation | < 10 seconds |
| Evaluation | < 5 seconds |
| Full workflow | < 20 seconds (excluding student time) |

## Integration Points

### With autonomous-coach-coordinator
- Receives weekly mock trigger
- Reports completion and readiness status
- Influences urgency calibration

### With deep-diagnostic-analyst
- Passes weak sections for root cause analysis
- Receives detailed improvement recommendations

### With whatsapp-message-sender
- Delivers exam (requires approval)
- Sends results summary
- Notifies of predicted score

## Example Session Flow

```
[Sunday 9:00 AM]
autonomous-coach-coordinator → "Weekly mock due"

[mock-exam-conductor activates]
1. Generate mock: session_id = mock-2025-02-02-001
2. Configure standard pressure level
3. Send via WhatsApp: "Your weekly mock exam is ready..."

[Student completes over 3 hours]
Student finishes at 12:15 PM

4. Evaluate results:
   - Overall: 76%
   - Pakistan Studies: 90%
   - Math Reasoning: 60% ← weak
   - Fatigue detected at Q85

5. Analyze weak sections:
   - Math: Needs algebra focus
   - Root cause: No practice in 2 weeks

6. Calibrate urgency:
   - 45 days to exam
   - Level: medium
   - Continue weekly mocks

7. Log session:
   - ERI: 62 → 65
   - Duration: 165 minutes

8. Send summary:
   "Mock complete! Score: 76%
    Predicted real: 72% (68-76 CI)
    Focus area: Math Reasoning
    Next mock: Feb 9"
```

## Constraints

- Must complete full workflow atomically
- Must handle partial completions gracefully
- Must respect daily interaction limits (part of coach-coordinator)
- Must not generate mock if last mock < 7 days ago
- Must include confidence intervals in all predictions
