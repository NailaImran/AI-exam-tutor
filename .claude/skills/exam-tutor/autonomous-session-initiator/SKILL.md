---
name: autonomous-session-initiator
description: Decides when to proactively initiate learning sessions based on time, gaps, urgency, and engagement factors. Implements daily limits (max 2 triggers) and 4-hour cooldown. Use when the autonomous coach needs to determine if a session should be triggered for a student.
phase: 4
category: AUTONOMY
priority: P1
---

# Autonomous Session Initiator

Determines whether to proactively initiate a learning session for a student based on multiple factors including time since last session, knowledge gaps, exam urgency, and engagement patterns.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and trigger logs.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read student profile, learning profile, revision queue, and trigger logs
- `mcp__filesystem__write_file` - Write trigger log entries

## Session Trigger Decision Logic

### Factor Weights

| Factor | Weight | Description |
|--------|--------|-------------|
| Time Gap | 0.25 | Days since last session |
| Knowledge Decay | 0.30 | Urgent revision items in queue |
| Exam Urgency | 0.25 | Days until target exam date |
| Engagement Pattern | 0.20 | Optimal study time alignment |

### Trigger Score Calculation

```
trigger_score = (
  time_gap_score × 0.25 +
  knowledge_decay_score × 0.30 +
  exam_urgency_score × 0.25 +
  engagement_score × 0.20
)

If trigger_score >= 0.60:
  should_trigger = true
```

### Time Gap Score (0-1)

```
days_since_last = today - last_session_date

If days_since_last == 0:
  time_gap_score = 0.0  # Already had session today
Elif days_since_last == 1:
  time_gap_score = 0.3  # Recent, low urgency
Elif days_since_last == 2:
  time_gap_score = 0.6  # Moderate gap
Elif days_since_last >= 3:
  time_gap_score = min(1.0, 0.6 + (days_since_last - 2) × 0.1)
```

### Knowledge Decay Score (0-1)

```
urgent_items = count(revision_queue where priority == "urgent")
high_items = count(revision_queue where priority == "high")

knowledge_decay_score = min(1.0, (urgent_items × 0.25) + (high_items × 0.10))
```

### Exam Urgency Score (0-1)

```
days_until_exam = target_exam_date - today

If days_until_exam <= 7:
  exam_urgency_score = 1.0  # Critical
Elif days_until_exam <= 14:
  exam_urgency_score = 0.8  # High
Elif days_until_exam <= 30:
  exam_urgency_score = 0.6  # Moderate
Elif days_until_exam <= 60:
  exam_urgency_score = 0.4  # Low
Else:
  exam_urgency_score = 0.2  # Distant

If no target_exam_date:
  exam_urgency_score = 0.3  # Default moderate
```

### Engagement Score (0-1)

```
current_time = now()
current_day = day_of_week(today)

# Check if current time is in optimal study window
If current_time in student.optimal_study_times:
  time_alignment = 0.5
Else:
  time_alignment = 0.0

# Check if current day is a peak engagement day
If current_day in student.engagement_patterns.peak_days:
  day_alignment = 0.5
Elif current_day in student.engagement_patterns.low_engagement_days:
  day_alignment = -0.2  # Penalty for low engagement day
Else:
  day_alignment = 0.2

engagement_score = max(0.0, time_alignment + day_alignment)
```

## Daily Interaction Limits

### Maximum Triggers Per Day
```
MAX_DAILY_TRIGGERS = 2

# Count triggers for today
today_triggers = count(trigger_log where date == today AND status == "triggered")

If today_triggers >= MAX_DAILY_TRIGGERS:
  can_trigger = false
  rejection_reason = "daily_limit_reached"
```

### 4-Hour Cooldown

```
COOLDOWN_HOURS = 4

# Get last trigger time
last_trigger = most_recent(trigger_log where status == "triggered")

If last_trigger exists:
  hours_since_last = (now() - last_trigger.triggered_at) / 3600

  If hours_since_last < COOLDOWN_HOURS:
    can_trigger = false
    rejection_reason = "cooldown_active"
    cooldown_remaining_minutes = (COOLDOWN_HOURS × 60) - (hours_since_last × 60)
```

## Execution Steps

1. **Check daily limit**
   ```
   Read trigger_log for today
   If count >= 2:
     Return {should_trigger: false, reason: "daily_limit_reached"}
   ```

2. **Check cooldown**
   ```
   Get most recent trigger
   If triggered within last 4 hours:
     Return {should_trigger: false, reason: "cooldown_active", cooldown_remaining_minutes: X}
   ```

3. **Load student context**
   ```
   profile = read_file(memory/students/{student_id}/profile.json)
   learning_profile = read_file(memory/students/{student_id}/learning-profile.json)
   revision_queue = read_file(memory/students/{student_id}/revision-queue.json)
   history = read_file(memory/students/{student_id}/history.json)
   ```

4. **Calculate factor scores**
   ```
   time_gap_score = calculate_time_gap(history.last_session_date)
   knowledge_decay_score = calculate_knowledge_decay(revision_queue)
   exam_urgency_score = calculate_exam_urgency(profile.target_exam_date)
   engagement_score = calculate_engagement(learning_profile, current_time)
   ```

5. **Calculate trigger score**
   ```
   trigger_score = weighted_sum(all_factor_scores)
   ```

6. **Make decision**
   ```
   If trigger_score >= 0.60:
     should_trigger = true
     Determine session_type based on highest factor
   Else:
     should_trigger = false
   ```

7. **Log decision**
   ```
   Write trigger decision to trigger_log
   ```

8. **Return decision**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true,
    "description": "Student ID to check for session trigger"
  },
  "current_time": {
    "type": "string",
    "format": "ISO 8601",
    "required": false,
    "description": "Current timestamp (defaults to now)"
  },
  "override_cooldown": {
    "type": "boolean",
    "required": false,
    "default": false,
    "description": "Override cooldown for urgent interventions only"
  }
}
```

## Output Schema

```json
{
  "should_trigger": "boolean (required)",
  "decision_id": "string UUID (required)",
  "student_id": "string (required)",
  "trigger_score": "number 0-1 (required)",
  "threshold": "number (always 0.60)",
  "factor_scores": {
    "time_gap": "number 0-1",
    "knowledge_decay": "number 0-1",
    "exam_urgency": "number 0-1",
    "engagement": "number 0-1"
  },
  "rejection_reason": "daily_limit_reached | cooldown_active | score_below_threshold | null",
  "cooldown_remaining_minutes": "integer | null",
  "recommended_session_type": "revision | gap_intervention | regular_practice | urgent_review | null",
  "session_focus": {
    "primary_topic": "string | null",
    "reason": "string | null"
  },
  "daily_triggers_used": "integer 0-2",
  "daily_triggers_remaining": "integer 0-2",
  "next_check_recommended_at": "string ISO 8601 | null",
  "decided_at": "string ISO 8601"
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/profile.json` |
| Read | `memory/students/{student_id}/learning-profile.json` |
| Read | `memory/students/{student_id}/revision-queue.json` |
| Read | `memory/students/{student_id}/history.json` |
| Read/Write | `logs/triggers/{student_id}/{YYYY-MM-DD}.json` |

## Trigger Log Schema

Location: `logs/triggers/{student_id}/{YYYY-MM-DD}.json`

```json
{
  "$schema": "exam-tutor/trigger-log/v1",
  "student_id": "string (required)",
  "date": "string ISO 8601 date (required)",
  "decisions": [
    {
      "decision_id": "string UUID (required)",
      "checked_at": "string ISO 8601 (required)",
      "trigger_score": "number 0-1 (required)",
      "factor_scores": {
        "time_gap": "number",
        "knowledge_decay": "number",
        "exam_urgency": "number",
        "engagement": "number"
      },
      "should_trigger": "boolean (required)",
      "status": "triggered | rejected | deferred",
      "rejection_reason": "string | null",
      "triggered_at": "string ISO 8601 | null",
      "session_id": "string | null (if session was started)"
    }
  ],
  "daily_summary": {
    "total_checks": "integer",
    "total_triggers": "integer",
    "total_rejections": "integer"
  }
}
```

## Session Type Determination

Based on the highest contributing factor:

```
If knowledge_decay_score is highest AND urgent_items > 0:
  recommended_session_type = "urgent_review"
  session_focus.primary_topic = first_urgent_item.topic_id
  session_focus.reason = "retention_below_threshold"

Elif knowledge_decay_score is highest:
  recommended_session_type = "revision"
  session_focus.primary_topic = first_high_item.topic_id
  session_focus.reason = "scheduled_revision_due"

Elif time_gap_score is highest:
  recommended_session_type = "regular_practice"
  session_focus.primary_topic = null  # Adaptive selection
  session_focus.reason = "maintain_consistency"

Elif exam_urgency_score is highest:
  recommended_session_type = "gap_intervention"
  session_focus.primary_topic = weakest_topic
  session_focus.reason = "exam_approaching"

Else:
  recommended_session_type = "regular_practice"
```

## Quiet Hours Respect

```
If profile.whatsapp.quiet_hours.enabled:
  quiet_start = profile.whatsapp.quiet_hours.start
  quiet_end = profile.whatsapp.quiet_hours.end

  If current_time is between quiet_start and quiet_end:
    should_trigger = false
    rejection_reason = "quiet_hours_active"
    next_check_recommended_at = quiet_end
```

## Constraints

- Must enforce maximum 2 proactive triggers per day
- Must enforce 4-hour cooldown between triggers
- Must respect student quiet hours settings
- Must not trigger on low engagement days unless urgent
- Override cooldown only for retention_score < 0.30 (critical decay)
- Must log all decisions (triggered or rejected)
- Must calculate all factor scores even when rejecting early

## Example Output

### Trigger Approved

```json
{
  "should_trigger": true,
  "decision_id": "dec-2025-02-03-001",
  "student_id": "student_123",
  "trigger_score": 0.72,
  "threshold": 0.60,
  "factor_scores": {
    "time_gap": 0.60,
    "knowledge_decay": 0.85,
    "exam_urgency": 0.80,
    "engagement": 0.50
  },
  "rejection_reason": null,
  "cooldown_remaining_minutes": null,
  "recommended_session_type": "urgent_review",
  "session_focus": {
    "primary_topic": "constitutional_amendments",
    "reason": "retention_below_threshold"
  },
  "daily_triggers_used": 0,
  "daily_triggers_remaining": 2,
  "next_check_recommended_at": null,
  "decided_at": "2025-02-03T09:15:00Z"
}
```

### Trigger Rejected (Cooldown)

```json
{
  "should_trigger": false,
  "decision_id": "dec-2025-02-03-002",
  "student_id": "student_123",
  "trigger_score": 0.68,
  "threshold": 0.60,
  "factor_scores": {
    "time_gap": 0.30,
    "knowledge_decay": 0.75,
    "exam_urgency": 0.80,
    "engagement": 0.70
  },
  "rejection_reason": "cooldown_active",
  "cooldown_remaining_minutes": 127,
  "recommended_session_type": null,
  "session_focus": null,
  "daily_triggers_used": 1,
  "daily_triggers_remaining": 1,
  "next_check_recommended_at": "2025-02-03T13:15:00Z",
  "decided_at": "2025-02-03T11:08:00Z"
}
```

### Trigger Rejected (Score Below Threshold)

```json
{
  "should_trigger": false,
  "decision_id": "dec-2025-02-03-003",
  "student_id": "student_123",
  "trigger_score": 0.42,
  "threshold": 0.60,
  "factor_scores": {
    "time_gap": 0.30,
    "knowledge_decay": 0.25,
    "exam_urgency": 0.40,
    "engagement": 1.00
  },
  "rejection_reason": "score_below_threshold",
  "cooldown_remaining_minutes": null,
  "recommended_session_type": null,
  "session_focus": null,
  "daily_triggers_used": 0,
  "daily_triggers_remaining": 2,
  "next_check_recommended_at": "2025-02-03T18:00:00Z",
  "decided_at": "2025-02-03T14:30:00Z"
}
```

## Usage Notes

- Call this skill periodically (every 2-4 hours) to check if session should be triggered
- Integrate with scheduled-task-runner for automated checks
- Use with learning-pattern-detector to refine engagement scoring
- Combine with motivation-monitor to avoid triggering for disengaged students
- Always log decisions for audit trail and pattern analysis
- Override cooldown only in emergency situations (critical knowledge decay)
