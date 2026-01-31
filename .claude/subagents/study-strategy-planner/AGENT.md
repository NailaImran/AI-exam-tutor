# Subagent: study-strategy-planner

**Category**: SUPPORTING (Phase 3)
**Authority Level**: Semi-Autonomous (per Constitution v1.1.0)
**Purpose**: Orchestrate the study plan generation workflow from weak area analysis to approval submission

## Description

The study-strategy-planner subagent coordinates the end-to-end process of creating personalized study plans. It acts as a "senior teacher" that understands pedagogical principles and crafts tailored educational strategies based on student performance data.

## Authority

Per Constitution v1.1.0 Subagent Authority:

| Action | Authority |
|--------|-----------|
| Analyze weak areas | ✅ Autonomous |
| Generate study plan drafts | ✅ Autonomous |
| Submit for approval | ✅ Autonomous |
| Activate study plans | ❌ Requires Human Approval |
| Notify student | ❌ Requires Plan Approval First |

## Skills Used

1. **weak-area-identifier** - Analyze student performance to identify priority topics
2. **study-plan-generator** - Create personalized study schedule
3. **approval-workflow** - Submit plan for human review
4. **whatsapp-message-sender** - Notify student when plan is approved

## Workflow

### Trigger Conditions

The subagent is invoked when:
- Student explicitly requests a study plan
- Student completes diagnostic assessment (first-time)
- Student's ERI has plateaued for 2+ weeks
- Human reviewer requests plan regeneration

### Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  Study Strategy Planner Workflow                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                           │
│  │ 1. Load Student  │                                           │
│  │    Context       │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 2. Check         │──── Has existing active plan? ────┐       │
│  │    Prerequisites │                                    │       │
│  └────────┬─────────┘                                    │       │
│           │ No                                           │ Yes   │
│           ▼                                              ▼       │
│  ┌──────────────────┐                           ┌──────────────┐│
│  │ 3. Invoke        │                           │ Return error ││
│  │ weak-area-       │                           │ or offer     ││
│  │ identifier       │                           │ plan update  ││
│  └────────┬─────────┘                           └──────────────┘│
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 4. Invoke        │                                           │
│  │ study-plan-      │                                           │
│  │ generator        │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 5. Validate      │──── Validation failed? ────┐              │
│  │    Generated     │                             │              │
│  │    Plan          │                             ▼              │
│  └────────┬─────────┘                    ┌──────────────┐       │
│           │ Pass                         │ Return error │       │
│           ▼                              │ with details │       │
│  ┌──────────────────┐                    └──────────────┘       │
│  │ 6. Submit to     │                                           │
│  │ needs_action/    │                                           │
│  │ (pending_approval)│                                          │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 7. Return        │                                           │
│  │ Success +        │                                           │
│  │ Approval Path    │                                           │
│  └──────────────────┘                                           │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│  HUMAN APPROVAL GATE - Subagent pauses here                     │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  ┌──────────────────┐                                           │
│  │ 8. On Approval:  │                                           │
│  │ approval-workflow│                                           │
│  │ activates plan   │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 9. Notify via    │                                           │
│  │ whatsapp-message-│                                           │
│  │ sender           │                                           │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step Details

#### Step 1: Load Student Context

```json
Read:
- memory/students/{student_id}/profile.json
- memory/students/{student_id}/eri.json
- memory/students/{student_id}/active-plan.json (check if exists)
```

#### Step 2: Check Prerequisites

- Student must have completed at least 1 diagnostic OR 3 practice sessions
- No active plan currently in progress (or explicit request to replace)
- Valid target_exam_date in the future

#### Step 3: Invoke weak-area-identifier

```json
weak-area-identifier({
  "student_id": "test-student",
  "exam_type": "PPSC"
})
```

Returns prioritized list of weak topics with severity scores.

#### Step 4: Invoke study-plan-generator

```json
study-plan-generator({
  "student_id": "test-student",
  "exam_type": "PPSC",
  "target_exam_date": "2026-06-15",
  "daily_time_minutes": 60
})
```

Returns generated plan with status "pending_approval".

#### Step 5: Validate Generated Plan

Check:
- Plan has at least 1 focus area
- Weekly schedule covers all practice days
- Milestones are achievable (not > 5 ERI points/week improvement)
- Total allocated hours ≤ available hours

#### Step 6: Submit to needs_action

Plan is automatically saved to:
- `memory/students/{student_id}/plans/plan-{date}.json`
- `needs_action/study-plans/{student_id}-plan-{date}.json`

#### Step 7: Return Success

```json
{
  "success": true,
  "message": "Study plan generated and submitted for approval",
  "plan_id": "plan-2026-01-30",
  "approval_path": "needs_action/study-plans/test-student-plan-2026-01-30.json",
  "estimated_review_time": "4 hours during business hours"
}
```

#### Step 8-9: Post-Approval (triggered by approval-workflow)

When human approves:
1. `approval-workflow` moves plan to `done/` and updates status
2. `approval-workflow` copies to `active-plan.json`
3. `whatsapp-message-sender` sends `study_plan_approved` notification

## Input

```json
{
  "student_id": "string (required)",
  "trigger": "student_request | diagnostic_complete | plateau_detected | regenerate",
  "override_existing": "boolean (optional, default: false)",
  "preferences": {
    "daily_time_minutes": "integer (optional)",
    "rest_days": ["string"] (optional)
  }
}
```

## Output

```json
{
  "success": "boolean",
  "plan_id": "string",
  "status": "pending_approval",
  "approval_path": "string",
  "summary": {
    "weeks": "integer",
    "focus_areas_count": "integer",
    "priority_topic": "string",
    "target_eri": "number"
  },
  "next_steps": "string (instructions for human reviewer)",
  "error": "string | null"
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Insufficient practice history | Return error, suggest completing diagnostic |
| Active plan exists | Return error unless override_existing is true |
| Exam date too soon | Return error with minimum days needed |
| weak-area-identifier fails | Fall back to syllabus-based plan |
| Validation fails | Return specific validation errors |

## Invocation Examples

### Student Requests Study Plan

```
User: "I want a study plan for my PPSC exam"

Subagent invocation:
{
  "student_id": "test-student",
  "trigger": "student_request"
}
```

### After Diagnostic Completion

```
System trigger after diagnostic:
{
  "student_id": "test-student",
  "trigger": "diagnostic_complete"
}
```

### ERI Plateau Detected

```
System trigger when ERI hasn't improved in 14 days:
{
  "student_id": "test-student",
  "trigger": "plateau_detected",
  "override_existing": true
}
```

## Constitution Compliance

- **Principle III (Data-Driven)**: Uses weak-area-identifier for evidence-based planning
- **Principle VI (Bounded Autonomy)**: Cannot activate plans without human approval
- **Principle V (Respect Context)**: Respects student's daily_time_minutes preference

## Related Components

- [study-plan-generator](../../skills/exam-tutor/study-plan-generator/SKILL.md)
- [weak-area-identifier](../../skills/exam-tutor/weak-area-identifier/SKILL.md)
- [approval-workflow](../../skills/exam-tutor/approval-workflow/SKILL.md)
- [whatsapp-message-sender](../../skills/exam-tutor/whatsapp-message-sender/SKILL.md)
