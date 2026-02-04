---
name: study-pattern-optimizer
description: Optimizes study schedules based on learning patterns, engagement data, and student constraints. Generates personalized weekly schedules that maximize learning efficiency by aligning sessions with optimal times and avoiding low-engagement periods.
phase: 4
category: AUTONOMY
priority: P3
---

# Study Pattern Optimizer

Generates optimized study schedules by combining learning pattern analysis with student constraints and exam urgency.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and writing optimized schedules.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read learning profile, active plan, and constraints
- `mcp__filesystem__write_file` - Save optimized schedule

## Schedule Optimization Based on Learning Patterns

### Input Data Sources

```
1. Learning Profile (from learning-pattern-detector):
   - optimal_study_times: [morning, evening]
   - peak_days: [wednesday, saturday, sunday]
   - low_engagement_days: [friday]
   - session_duration_preference: 30 minutes
   - preferred_difficulty_ramp: gradual

2. Student Constraints:
   - available_hours_per_day: {monday: 2, tuesday: 1, ...}
   - unavailable_times: [{day: friday, from: 18:00, to: 22:00}]
   - target_hours_per_week: 10
   - preferred_session_length: 30-45 minutes

3. Exam Context:
   - days_until_exam: 45
   - weak_topics: from knowledge-gap-predictor
   - revision_queue: from revision-cycle-manager
```

### Optimization Algorithm

```
1. Calculate time slots per day:
   For each day in week:
     available_slots = []

     # Check each hour of the day
     For hour in range(5, 24):
       If hour in student.available_hours[day]:
         If not in student.unavailable_times:
           slot = {
             "day": day,
             "start_hour": hour,
             "optimal_score": calculate_slot_score(hour, day)
           }
           available_slots.append(slot)

2. Score each slot based on learning patterns:
   calculate_slot_score(hour, day):
     score = 0.5  # Base score

     # Time period alignment
     time_period = get_time_period(hour)
     If time_period in learning_profile.optimal_study_times:
       If time_period == learning_profile.optimal_study_times[0]:
         score += 0.30  # Primary optimal time
       Else:
         score += 0.20  # Secondary optimal time

     # Day alignment
     If day in learning_profile.peak_days:
       score += 0.20
     Elif day in learning_profile.low_engagement_days:
       score -= 0.30  # Penalty

     # Consistency bonus (similar times across days)
     If hour matches previous_day_session_hour ± 1:
       score += 0.10

     return min(1.0, max(0.0, score))

3. Allocate sessions to optimize total score:
   target_sessions = target_hours_per_week / session_duration_hours
   sorted_slots = sort(available_slots, key=optimal_score, descending=True)

   scheduled_sessions = []
   For slot in sorted_slots:
     If len(scheduled_sessions) >= target_sessions:
       break

     # Check constraints
     If day_has_room(slot.day) AND respects_spacing(slot):
       scheduled_sessions.append(slot)

4. Assign content to sessions:
   For each session:
     # Priority: urgent revision > high-risk gaps > weak topics > maintenance
     content = assign_content_by_priority(session, revision_queue, gap_predictions)
```

### Spacing Rules

```
# Ensure recovery time between sessions
min_hours_between_sessions_same_day = 3
max_sessions_per_day = 2
min_rest_days_per_week = 1

respects_spacing(new_slot, existing_sessions):
  same_day_sessions = [s for s in existing_sessions if s.day == new_slot.day]

  # Check max sessions per day
  If len(same_day_sessions) >= max_sessions_per_day:
    return False

  # Check minimum gap
  For session in same_day_sessions:
    gap = abs(new_slot.start_hour - session.start_hour)
    If gap < min_hours_between_sessions_same_day:
      return False

  return True
```

## Content Assignment

### Priority-Based Assignment

```
For each scheduled session:
  content_options = []

  # Priority 1: Urgent revision (retention < 0.50)
  urgent_revision = revision_queue.filter(priority == "urgent")
  If urgent_revision:
    content_options.append({
      "type": "revision",
      "topic": urgent_revision[0].topic_id,
      "priority": 1,
      "estimated_time": 30
    })

  # Priority 2: High-risk gaps (predicted to fall below threshold)
  high_risk_gaps = gap_predictions.filter(risk_level == "high")
  If high_risk_gaps:
    content_options.append({
      "type": "gap_intervention",
      "topic": high_risk_gaps[0].topic_id,
      "priority": 2,
      "estimated_time": 25
    })

  # Priority 3: Current weak topics
  weak_topics = topic_stats.filter(accuracy < 60)
  If weak_topics:
    content_options.append({
      "type": "practice",
      "topic": weak_topics[0].topic_id,
      "priority": 3,
      "estimated_time": 30
    })

  # Priority 4: Maintenance practice
  content_options.append({
    "type": "maintenance",
    "topic": "adaptive",
    "priority": 4,
    "estimated_time": 25
  })

  # Select highest priority that fits session duration
  session.content = select_best_fit(content_options, session.duration)
```

### Difficulty Progression Within Sessions

```
If learning_profile.preferred_difficulty_ramp == "gradual":
  session_structure = {
    "warmup": {"difficulty": "easy", "questions": 3, "minutes": 5},
    "core": {"difficulty": "medium", "questions": 10, "minutes": 20},
    "challenge": {"difficulty": "hard", "questions": 2, "minutes": 5}
  }

Elif learning_profile.preferred_difficulty_ramp == "aggressive":
  session_structure = {
    "warmup": {"difficulty": "medium", "questions": 2, "minutes": 3},
    "core": {"difficulty": "hard", "questions": 8, "minutes": 20},
    "challenge": {"difficulty": "hard", "questions": 5, "minutes": 7}
  }

Else:  # mixed
  session_structure = {
    "warmup": {"difficulty": "easy", "questions": 2, "minutes": 3},
    "core": {"difficulty": "adaptive", "questions": 10, "minutes": 22},
    "challenge": {"difficulty": "hard", "questions": 3, "minutes": 5}
  }
```

## Execution Steps

1. **Load learning patterns**
   ```
   learning_profile = read_file(memory/students/{student_id}/learning-profile.json)
   ```

2. **Load constraints**
   ```
   profile = read_file(memory/students/{student_id}/profile.json)
   active_plan = read_file(memory/students/{student_id}/active-plan.json)
   ```

3. **Load content priorities**
   ```
   revision_queue = read_file(memory/students/{student_id}/revision-queue.json)
   gap_predictions = read_file(memory/students/{student_id}/gap-predictions.json)
   topic_stats = read_file(memory/students/{student_id}/topic-stats.json)
   ```

4. **Calculate available slots**
   ```
   slots = calculate_available_slots(constraints)
   scored_slots = score_slots(slots, learning_profile)
   ```

5. **Optimize schedule**
   ```
   optimized_schedule = allocate_sessions(scored_slots, target_hours)
   ```

6. **Assign content**
   ```
   For session in optimized_schedule:
     session.content = assign_content(session, priorities)
     session.structure = get_session_structure(learning_profile)
   ```

7. **Save optimized schedule**
   ```
   write_file(memory/students/{student_id}/optimized-schedule.json)
   ```

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "week_start_date": {
    "type": "string",
    "format": "ISO 8601",
    "required": false,
    "description": "Start date for schedule (default: next Monday)"
  },
  "constraints": {
    "type": "object",
    "required": false,
    "properties": {
      "available_hours": {"<day>": "array of hours 0-23"},
      "unavailable_times": [{"day": "string", "from": "HH:MM", "to": "HH:MM"}],
      "target_hours_per_week": "integer",
      "max_session_length_minutes": "integer",
      "min_session_length_minutes": "integer"
    }
  },
  "optimization_goal": {
    "type": "string",
    "enum": ["maximize_learning", "minimize_time", "balanced"],
    "default": "balanced"
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "generated_at": "string ISO 8601",
  "week_start_date": "string ISO 8601",
  "optimization_goal": "string",
  "schedule": {
    "monday": [
      {
        "start_time": "HH:MM",
        "end_time": "HH:MM",
        "duration_minutes": "integer",
        "optimal_score": "number 0-1",
        "content": {
          "type": "revision | gap_intervention | practice | maintenance",
          "topic_id": "string",
          "topic_name": "string",
          "priority": "integer",
          "difficulty_ramp": "gradual | aggressive | mixed"
        },
        "session_structure": {
          "warmup": {"difficulty": "string", "questions": "integer", "minutes": "integer"},
          "core": {"difficulty": "string", "questions": "integer", "minutes": "integer"},
          "challenge": {"difficulty": "string", "questions": "integer", "minutes": "integer"}
        }
      }
    ],
    "tuesday": [],
    "wednesday": [],
    "thursday": [],
    "friday": [],
    "saturday": [],
    "sunday": []
  },
  "summary": {
    "total_sessions": "integer",
    "total_hours": "number",
    "average_session_length_minutes": "integer",
    "peak_day_sessions": "integer",
    "low_engagement_day_sessions": "integer (should be 0 or minimal)",
    "optimal_time_coverage": "number 0-1 (% of sessions in optimal times)"
  },
  "content_allocation": {
    "revision_sessions": "integer",
    "gap_intervention_sessions": "integer",
    "practice_sessions": "integer",
    "maintenance_sessions": "integer"
  },
  "recommendations": [
    {
      "type": "scheduling | content | pacing",
      "message": "string",
      "priority": "high | medium | low"
    }
  ]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/learning-profile.json` |
| Read | `memory/students/{student_id}/profile.json` |
| Read | `memory/students/{student_id}/active-plan.json` |
| Read | `memory/students/{student_id}/revision-queue.json` |
| Read | `memory/students/{student_id}/gap-predictions.json` |
| Read | `memory/students/{student_id}/topic-stats.json` |
| Write | `memory/students/{student_id}/optimized-schedule.json` |

## Example Output

```json
{
  "student_id": "student_123",
  "generated_at": "2025-02-03T14:00:00Z",
  "week_start_date": "2025-02-10",
  "optimization_goal": "balanced",
  "schedule": {
    "monday": [],
    "tuesday": [
      {
        "start_time": "19:00",
        "end_time": "19:30",
        "duration_minutes": 30,
        "optimal_score": 0.72,
        "content": {
          "type": "revision",
          "topic_id": "constitutional_amendments",
          "topic_name": "Constitutional Amendments",
          "priority": 1,
          "difficulty_ramp": "gradual"
        },
        "session_structure": {
          "warmup": {"difficulty": "easy", "questions": 3, "minutes": 5},
          "core": {"difficulty": "medium", "questions": 10, "minutes": 20},
          "challenge": {"difficulty": "hard", "questions": 2, "minutes": 5}
        }
      }
    ],
    "wednesday": [
      {
        "start_time": "18:00",
        "end_time": "18:45",
        "duration_minutes": 45,
        "optimal_score": 0.88,
        "content": {
          "type": "gap_intervention",
          "topic_id": "federal_structure",
          "topic_name": "Federal Structure",
          "priority": 2,
          "difficulty_ramp": "gradual"
        },
        "session_structure": {
          "warmup": {"difficulty": "easy", "questions": 3, "minutes": 5},
          "core": {"difficulty": "medium", "questions": 15, "minutes": 30},
          "challenge": {"difficulty": "hard", "questions": 4, "minutes": 10}
        }
      }
    ],
    "thursday": [],
    "friday": [],
    "saturday": [
      {
        "start_time": "10:00",
        "end_time": "10:45",
        "duration_minutes": 45,
        "optimal_score": 0.85,
        "content": {
          "type": "practice",
          "topic_id": "current_affairs_jan_2025",
          "topic_name": "Current Affairs - January 2025",
          "priority": 3,
          "difficulty_ramp": "gradual"
        }
      },
      {
        "start_time": "16:00",
        "end_time": "16:30",
        "duration_minutes": 30,
        "optimal_score": 0.78,
        "content": {
          "type": "maintenance",
          "topic_id": "adaptive",
          "topic_name": "Adaptive Practice",
          "priority": 4,
          "difficulty_ramp": "mixed"
        }
      }
    ],
    "sunday": [
      {
        "start_time": "11:00",
        "end_time": "11:45",
        "duration_minutes": 45,
        "optimal_score": 0.82,
        "content": {
          "type": "revision",
          "topic_id": "islamic_studies_basics",
          "topic_name": "Islamic Studies Basics",
          "priority": 1,
          "difficulty_ramp": "gradual"
        }
      }
    ]
  },
  "summary": {
    "total_sessions": 5,
    "total_hours": 3.25,
    "average_session_length_minutes": 39,
    "peak_day_sessions": 3,
    "low_engagement_day_sessions": 0,
    "optimal_time_coverage": 0.80
  },
  "content_allocation": {
    "revision_sessions": 2,
    "gap_intervention_sessions": 1,
    "practice_sessions": 1,
    "maintenance_sessions": 1
  },
  "recommendations": [
    {
      "type": "scheduling",
      "message": "80% of sessions scheduled during optimal study times (evening)",
      "priority": "low"
    },
    {
      "type": "content",
      "message": "2 urgent revision topics scheduled - complete these first",
      "priority": "high"
    }
  ]
}
```

## Constraints

- Must respect student's unavailable times
- Maximum 2 sessions per day with 3+ hour gap
- At least 1 rest day per week (prefer low-engagement day)
- Session length must be within student's preference range
- Prioritize urgent revision and high-risk gaps
- 80%+ sessions should be in optimal time periods

## Usage Notes

- Regenerate weekly based on updated learning patterns
- Adjust dynamically if sessions are missed
- Integrate with autonomous-session-initiator for proactive triggers
- Use revision-queue priorities for content assignment
- Consider exam countdown urgency for session frequency
