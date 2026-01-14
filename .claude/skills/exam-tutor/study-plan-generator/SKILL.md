---
name: study-plan-generator
description: Generates a structured study plan based on weak areas, ERI score, and target exam date. Use this skill after diagnosis or when student requests a new plan. Produces daily/weekly topic schedule with practice targets and spaced repetition cycles. Requires outputs from exam-readiness-calculator and weak-area-identifier.
---

# Study Plan Generator

Creates personalized, time-bound study plans optimized for exam preparation.

## MCP Integration

This skill uses the **filesystem MCP server** for reading and writing plans.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read syllabus and topic weights
- `mcp__filesystem__write_file` - Save active plan to student memory

## Execution Steps

1. **Validate inputs**
   - student_id must be valid
   - exam_type must be SPSC, PPSC, or KPPSC
   - eri_data must contain eri_score and components
   - weak_topics must be array
   - daily_time_minutes must be positive

2. **Load syllabus data**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/{exam_type}/syllabus-structure.json

   Use: mcp__filesystem__read_file
   Path: syllabus/{exam_type}/topic-weights.json
   ```

3. **Calculate available study time**
   ```
   if target_exam_date:
     days_remaining = target_exam_date - today
   else:
     days_remaining = 90  // default 3-month horizon

   total_minutes = days_remaining * daily_time_minutes
   ```

4. **Prioritize topics**
   ```
   priority_sequence = []

   // Phase 1: Critical weak areas (severity 1-3)
   Add weak_topics where severity_rank <= 3

   // Phase 2: Remaining weak areas
   Add remaining weak_topics

   // Phase 3: Untested topics (high syllabus weight first)
   Add untested_topics sorted by syllabus_weight desc

   // Phase 4: Strong topics (maintenance)
   Add strong_topics for periodic review
   ```

5. **Calculate time allocation per topic**
   ```
   For each topic in priority_sequence:
     base_time = syllabus_weight * time_per_weight_unit

     // Adjust for weakness
     if topic in weak_topics:
       base_time *= 1.5  // 50% more time for weak areas

     // Adjust for ERI
     if eri_score < 40:
       // More time on fundamentals
       base_time *= 1.2 for easy topics
   ```

6. **Generate weekly schedule**
   ```
   weeks = ceil(days_remaining / 7)

   For each week:
     weekly_topics = select_topics_for_week(priority_sequence, week_number)
     daily_schedule = distribute_across_days(weekly_topics, daily_time_minutes)
   ```

7. **Insert spaced repetition cycles**
   ```
   Repetition schedule:
     - Initial learning: Day 1
     - First review: Day 3
     - Second review: Day 7
     - Third review: Day 14
     - Maintenance: Every 21 days

   Insert review sessions for previously covered topics
   ```

8. **Generate milestones**
   ```
   milestones = []

   // ERI targets at intervals
   if days_remaining > 30:
     milestone at day 30: target_eri = current_eri + 15
   if days_remaining > 60:
     milestone at day 60: target_eri = current_eri + 25
   // Final milestone
   milestone at target_exam_date: target_eri = 80
   ```

9. **Write active plan**
   ```
   Use: mcp__filesystem__write_file
   Path: memory/students/{student_id}/active-plan.json
   ```

10. **Return structured output**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "eri_data": {
    "type": "object",
    "required": true,
    "description": "Output from exam-readiness-calculator",
    "properties": {
      "eri_score": "number",
      "components": "object",
      "syllabus_coverage": "object"
    }
  },
  "weak_topics": {
    "type": "array",
    "required": true,
    "description": "Output from weak-area-identifier"
  },
  "target_exam_date": {
    "type": "string",
    "format": "ISO 8601",
    "required": false,
    "description": "Target exam date (optional)"
  },
  "daily_time_minutes": {
    "type": "integer",
    "required": true,
    "minimum": 30,
    "description": "Available study time per day in minutes"
  }
}
```

## Output Schema

```json
{
  "plan": {
    "id": "string",
    "student_id": "string",
    "exam_type": "SPSC | PPSC | KPPSC",
    "created_at": "string (ISO 8601)",
    "target_exam_date": "string | null",
    "daily_time_minutes": "integer",
    "total_days": "integer",
    "phases": [
      {
        "phase_number": "integer",
        "name": "string",
        "duration_days": "integer",
        "focus": "string",
        "topics": ["string"]
      }
    ],
    "weekly_schedule": [
      {
        "week_number": "integer",
        "start_date": "string",
        "topics": ["string"],
        "daily_targets": {
          "monday": {"topic": "", "duration_minutes": 0, "activity": ""},
          "tuesday": {},
          "...": {}
        },
        "review_topics": ["string"]
      }
    ]
  },
  "priority_sequence": ["string (ordered topic list)"],
  "milestones": [
    {
      "date": "string (ISO 8601)",
      "target_eri": "number",
      "description": "string"
    }
  ]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `syllabus/{exam_type}/syllabus-structure.json` |
| Read | `syllabus/{exam_type}/topic-weights.json` |
| Write | `memory/students/{student_id}/active-plan.json` |

## Study Phases

| Phase | Focus | Duration |
|-------|-------|----------|
| Foundation | Critical weak areas | 30% of time |
| Expansion | Remaining weak + untested | 40% of time |
| Consolidation | Full coverage + review | 20% of time |
| Intensive | Mock tests + final review | 10% of time |

## Spaced Repetition Schedule

| Review | Days After Initial | Purpose |
|--------|-------------------|---------|
| R1 | +2 days | Short-term reinforcement |
| R2 | +7 days | Medium-term retention |
| R3 | +14 days | Long-term consolidation |
| R4 | +30 days | Maintenance review |

## Constraints

- Weak topics must appear earlier in schedule
- Must respect daily_time_minutes constraint
- Must include revision cycles (spaced repetition logic)
- Plan duration must not exceed days until target_exam_date
- Must save plan to student's active-plan.json
