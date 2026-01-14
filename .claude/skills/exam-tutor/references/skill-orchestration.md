# Skill Orchestration Reference

This document describes how the parent agent should orchestrate the exam tutor skills.

## Skill Dependency Graph

```
                    ┌─────────────────────────┐
                    │  student-profile-loader │
                    └───────────┬─────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
┌───────────────────┐  ┌───────────────┐  ┌─────────────────┐
│ syllabus-mapper   │  │ weak-area-    │  │ exam-readiness- │
│ (optional)        │  │ identifier    │  │ calculator      │
└───────────────────┘  └───────┬───────┘  └────────┬────────┘
                               │                   │
                ┌──────────────┴──────────────┐    │
                │                             │    │
                ▼                             ▼    ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │ adaptive-test-      │      │ study-plan-         │
    │ generator           │      │ generator           │
    └──────────┬──────────┘      └─────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ question-bank-      │
    │ querier             │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ answer-evaluator    │
    │ (pure computation)  │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ performance-tracker │
    └──────────┬──────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌─────────────┐  ┌───────────────────┐
│ session-    │  │ progress-report-  │
│ logger      │  │ generator         │
└─────────────┘  └───────────────────┘
```

## Workflow Templates

### 1. New Student Onboarding

```yaml
workflow: new_student_onboarding
trigger: New student registration

steps:
  1. Create student profile
     - Write profile.json with initial data
     - Initialize empty history.json
     - Initialize empty topic-stats.json

  2. student-profile-loader
     - Verify profile was created correctly
     - Load for downstream skills

  3. diagnostic-assessment-generator
     - Generate initial diagnostic test
     - Cover full syllabus
     - assessment_type: "initial"

  4. [Student completes assessment]

  5. answer-evaluator
     - Evaluate diagnostic results
     - Generate topic_breakdown

  6. performance-tracker
     - Save first session data
     - Initialize topic-stats from results

  7. exam-readiness-calculator
     - Calculate initial ERI (baseline)

  8. weak-area-identifier
     - Identify initial weak areas
     - All untested topics will be flagged

  9. study-plan-generator
     - Generate personalized study plan
     - Based on weak areas and daily time

  10. session-logger (optional)
      - Log onboarding session

output: Student ready for daily practice
```

### 2. Daily Practice Session

```yaml
workflow: daily_practice_session
trigger: Student starts practice

steps:
  1. student-profile-loader
     - Load student context
     - Get exam_target, preferences

  2. weak-area-identifier
     - Get current weak areas
     - Prioritize by severity

  3. exam-readiness-calculator
     - Get current ERI
     - Determine session intensity

  4. adaptive-test-generator
     - Generate personalized test
     - Focus on weak areas (60%)
     - Include balanced coverage (40%)

  5. [Student completes test]

  6. answer-evaluator
     - Evaluate all answers
     - Calculate topic breakdown

  7. performance-tracker
     - Save session results
     - Update topic-stats
     - Update history

  8. exam-readiness-calculator
     - Recalculate ERI
     - Show improvement/decline

  9. weak-area-identifier
     - Update weak area list
     - Check for improvements

  10. session-logger (optional)
      - Log session events

output: Session complete, stats updated
```

### 3. Weekly Review

```yaml
workflow: weekly_review
trigger: End of week or on-demand

steps:
  1. student-profile-loader
     - Load student context

  2. exam-readiness-calculator
     - Get current ERI with components

  3. weak-area-identifier
     - Get current weak/strong/untested lists

  4. progress-report-generator
     - Generate weekly report
     - report_period_days: 7
     - include_recommendations: true

  5. study-plan-generator (if needed)
     - Regenerate plan if significant changes
     - Adjust based on progress

output: Weekly report generated
```

### 4. Exam Target Change

```yaml
workflow: exam_target_change
trigger: Student changes target exam (e.g., PPSC to SPSC)

steps:
  1. student-profile-loader
     - Load current profile

  2. syllabus-mapper
     - query_type: "cross_exam_map"
     - Map existing progress to new exam

  3. Update profile.json
     - Change exam_target
     - Note mapping confidence

  4. weak-area-identifier
     - Recalculate against new syllabus
     - Some topics may become untested

  5. exam-readiness-calculator
     - Recalculate ERI for new exam

  6. study-plan-generator
     - Generate new plan for new exam

output: Transition complete
```

## Error Handling Strategies

### Skill Failure Recovery

| Skill | Failure Impact | Recovery Strategy |
|-------|----------------|-------------------|
| student-profile-loader | Critical | Abort session, alert user |
| question-bank-querier | High | Reduce question count, warn |
| answer-evaluator | High | Retry, manual calculation fallback |
| performance-tracker | Medium | Queue for retry, continue session |
| exam-readiness-calculator | Low | Use last known ERI |
| weak-area-identifier | Low | Use previous weak areas |
| study-plan-generator | Low | Keep existing plan |
| progress-report-generator | Low | Skip report, notify user |
| session-logger | Very Low | Silent fail, log locally |
| syllabus-mapper | Low | Use direct syllabus query |

### Data Integrity Checks

Before each session:
1. Verify student profile exists and is valid
2. Verify history.json is parseable
3. Verify topic-stats.json is consistent
4. Verify question bank has sufficient questions

### Rollback Procedures

For failed writes:
1. Keep backup of previous state
2. Attempt atomic write
3. On failure, restore from backup
4. Log failure for debugging

## Parallelization Opportunities

### Safe to Run in Parallel

```
Group 1 (after profile load):
  - weak-area-identifier
  - exam-readiness-calculator
  - syllabus-mapper (if needed)

Group 2 (post-session):
  - session-logger
  - progress-report-generator (if scheduled)
```

### Must Run Sequentially

```
1. student-profile-loader (always first)
2. adaptive-test-generator (needs weak areas)
3. question-bank-querier (called by generator)
4. answer-evaluator (needs test completion)
5. performance-tracker (needs evaluation results)
```

## Caching Recommendations

### Cache Always (rarely changes)
- Syllabus structure
- Topic weights
- Cross-exam mappings

### Cache Per Session (changes per session)
- Student profile
- Recent question IDs (for exclusion)

### Never Cache (always fresh)
- History data
- Topic stats
- ERI calculations
