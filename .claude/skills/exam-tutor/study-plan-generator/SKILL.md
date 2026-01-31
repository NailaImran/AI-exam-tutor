# Skill: study-plan-generator

**Category**: SUPPORTING (Phase 3)
**Purpose**: Generate personalized study plans based on weak areas, syllabus coverage, and target exam date

## Description

The study-plan-generator skill creates customized study schedules for students preparing for SPSC, PPSC, or KPPSC exams. It analyzes weak areas, allocates time based on severity scores, generates weekly schedules with topic rotation, and sets ERI milestones.

## Input

```json
{
  "student_id": "string (required)",
  "exam_type": "SPSC | PPSC | KPPSC (optional, defaults to profile.exam_target)",
  "target_exam_date": "string ISO 8601 (optional, defaults to profile.target_exam_date)",
  "daily_time_minutes": "integer 15-180 (optional, defaults to profile.preferences.daily_time_minutes)",
  "include_rest_days": "boolean (optional, default: true)",
  "rest_days": ["Saturday", "Sunday"] (optional, default: ["Saturday"])
}
```

## Output

```json
{
  "success": "boolean",
  "plan": {
    "plan_id": "string plan-YYYY-MM-DD",
    "student_id": "string",
    "exam_type": "SPSC | PPSC | KPPSC",
    "status": "draft",
    "target_exam_date": "string ISO 8601",
    "days_remaining": "integer",
    "daily_time_minutes": "integer",
    "total_hours_available": "number",
    "focus_areas": [...],
    "weekly_schedule": [...],
    "milestones": [...]
  },
  "plan_path": "string (memory path)",
  "approval_path": "string (needs_action path)",
  "error": "string | null"
}
```

## Workflow

### 1. Load Student Context

```
Read: memory/students/{student_id}/profile.json
Read: memory/students/{student_id}/weak-areas.json
Read: memory/students/{student_id}/eri.json
Read: syllabus/{exam_type}/syllabus-structure.json
```

### 2. Calculate Time Budget

```javascript
// Calculate available time
days_remaining = (target_exam_date - today) in days
practice_days = days_remaining - (rest_days_per_week * weeks)
total_hours_available = (practice_days * daily_time_minutes) / 60

// Validate minimum requirements
if (days_remaining < 7) {
  return error("Exam too soon for study plan - need at least 7 days")
}
if (total_hours_available < 10) {
  return error("Insufficient time budget - increase daily time or extend target date")
}
```

### 3. Prioritize Weak Areas

Integration with `weak-area-identifier` skill:

```json
weak_areas = weak-area-identifier({
  student_id: student_id,
  exam_type: exam_type
})
```

Sort weak areas by severity_score (highest first).

### 4. Time Allocation Algorithm

```javascript
// Allocate hours based on severity score
total_severity = sum(weak_areas.map(w => w.severity_score))

for each weak_area in weak_areas:
  weight = weak_area.severity_score / total_severity
  allocated_hours = total_hours_available * weight * 0.8  // 80% to weak areas

// Reserve 20% for review and strong topics
review_hours = total_hours_available * 0.2

// Set priorities
priority = 1
for each weak_area sorted by severity_score desc:
  weak_area.priority = priority++
  weak_area.allocated_hours = calculated_hours
```

### 5. Generate Weekly Schedule

```javascript
weeks = Math.ceil(days_remaining / 7)
current_date = today

for week_number = 1 to weeks:
  week = {
    week_number: week_number,
    start_date: current_date,
    topics: [],
    rest_days: rest_days
  }

  for each day in ["Monday", "Tuesday", ..., "Sunday"]:
    if day in rest_days:
      continue

    // Rotate through topics
    topic = select_topic_for_day(focus_areas, week_number, day)

    week.topics.push({
      day: day,
      topic: topic.name,
      duration_minutes: daily_time_minutes,
      question_count: Math.floor(daily_time_minutes / 6)  // ~6 min per question
    })

  weekly_schedule.push(week)
  current_date += 7 days
```

### 6. Generate Milestones

```javascript
current_eri = eri.current_score
target_eri = 80  // exam_ready threshold

eri_gap = target_eri - current_eri
weekly_improvement = eri_gap / weeks

milestones = []
for week = 1 to weeks:
  milestones.push({
    week: week,
    target_eri: Math.min(current_eri + (weekly_improvement * week), 100),
    focus_achievement: get_focus_for_week(week, focus_areas)
  })
```

### 7. Create Draft Plan

```javascript
plan = {
  "$schema": "exam-tutor/study-plan/v1",
  "plan_id": `plan-${today}`,
  "student_id": student_id,
  "exam_type": exam_type,
  "created_at": now(),
  "updated_at": now(),
  "status": "draft",
  "approval": {
    "submitted_at": null,
    "reviewed_at": null,
    "reviewer": null,
    "decision": null,
    "feedback": null
  },
  "target_exam_date": target_exam_date,
  "days_remaining": days_remaining,
  "daily_time_minutes": daily_time_minutes,
  "total_hours_available": total_hours_available,
  "focus_areas": focus_areas,
  "weekly_schedule": weekly_schedule,
  "milestones": milestones
}
```

### 8. Save and Submit for Approval

```javascript
// Save to student's plans folder
plan_path = `memory/students/${student_id}/plans/plan-${today}.json`
write_file(plan_path, plan)

// Transition to pending_approval
plan.status = "pending_approval"
plan.approval.submitted_at = now()

// Copy to needs_action for human review
approval_path = `needs_action/study-plans/${student_id}-plan-${today}.json`
write_file(approval_path, plan)
```

## Topic Rotation Strategy

```
Week 1: Focus on highest-severity weak areas (priority 1-2)
Week 2: Rotate to medium-severity areas (priority 3-4)
Week 3: Mix of weak areas and review
Week 4+: Decreasing weak-area focus, increasing review

Daily rotation within week:
- Monday: Priority 1 topic
- Tuesday: Priority 2 topic
- Wednesday: Priority 3 topic
- Thursday: Review day (mix of topics)
- Friday: Priority 1 topic (reinforcement)
- Saturday: Rest (optional)
- Sunday: Light review (optional)
```

## MCP Tools Used

- `mcp__filesystem__read_file` - Load student data, syllabus
- `mcp__filesystem__write_file` - Save plan to memory and needs_action

## Validation Rules

- `days_remaining` MUST be > 0 (positive)
- `daily_time_minutes` MUST be between 15 and 180
- `focus_areas` MUST not be empty
- Sum of `allocated_hours` MUST not exceed `total_hours_available`
- Each `weekly_schedule` entry MUST have valid day names

## Error Handling

| Error | Action |
|-------|--------|
| Student not found | Return error with student_id |
| No weak areas identified | Generate plan with syllabus coverage |
| Exam date in past | Return error |
| Exam too soon (< 7 days) | Return error with recommendation |
| Insufficient time budget | Return error with suggestions |

## Constitution Compliance

- **Principle III (Data-Driven)**: Plans based on weak-area-identifier analysis
- **Principle VI (Bounded Autonomy)**: Plans require human approval before activation

## Example Usage

```json
Input: {
  "student_id": "test-student",
  "target_exam_date": "2026-06-15",
  "daily_time_minutes": 60
}

Output: {
  "success": true,
  "plan": {
    "plan_id": "plan-2026-01-30",
    "student_id": "test-student",
    "exam_type": "PPSC",
    "status": "pending_approval",
    "target_exam_date": "2026-06-15T00:00:00Z",
    "days_remaining": 136,
    "daily_time_minutes": 60,
    "total_hours_available": 116,
    "focus_areas": [
      {
        "topic": "Constitutional Amendments",
        "severity_score": 85,
        "allocated_hours": 25,
        "priority": 1
      },
      {
        "topic": "Economic Policies",
        "severity_score": 72,
        "allocated_hours": 20,
        "priority": 2
      }
    ],
    "weekly_schedule": [
      {
        "week_number": 1,
        "start_date": "2026-02-02",
        "topics": [
          {"day": "Monday", "topic": "Constitutional Amendments", "duration_minutes": 60, "question_count": 10},
          {"day": "Tuesday", "topic": "Economic Policies", "duration_minutes": 60, "question_count": 10}
        ],
        "rest_days": ["Saturday"]
      }
    ],
    "milestones": [
      {"week": 4, "target_eri": 50, "focus_achievement": "Complete Constitutional Amendments"},
      {"week": 8, "target_eri": 60, "focus_achievement": "Master Economic Policies"},
      {"week": 16, "target_eri": 75, "focus_achievement": "Full syllabus coverage"},
      {"week": 20, "target_eri": 80, "focus_achievement": "Exam ready"}
    ]
  },
  "plan_path": "memory/students/test-student/plans/plan-2026-01-30.json",
  "approval_path": "needs_action/study-plans/test-student-plan-2026-01-30.json",
  "error": null
}
```

## Related Skills

- weak-area-identifier (provides prioritization data)
- approval-workflow (handles approval process)
- whatsapp-message-sender (notifies on approval)
