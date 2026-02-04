---
name: motivation-monitor
description: Tracks student engagement, detects dropout risk indicators, monitors engagement decline, and implements graduated nudging strategy (1 day → 3 days → 7 days). Use to prevent disengagement and proactively intervene when motivation wanes.
phase: 4
category: AUTONOMY
priority: P3
---

# Motivation Monitor

Monitors student engagement patterns to detect early signs of disengagement and implements graduated intervention strategies to maintain motivation.

## MCP Integration

This skill uses the **filesystem MCP server** for reading engagement data and writing intervention records.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read session history and engagement data
- `mcp__filesystem__write_file` - Save engagement status and intervention records

## Dropout Risk Indicators Detection

### Risk Indicator Categories

| Indicator | Code | Detection Criteria | Weight |
|-----------|------|-------------------|--------|
| Declining frequency | `declining_frequency` | Session count down 50%+ vs previous period | 0.25 |
| Declining performance | `declining_performance` | Accuracy down 10%+ vs previous period | 0.20 |
| Long session gaps | `long_gaps` | >7 days between sessions | 0.20 |
| High abandonment | `high_abandonment` | >30% incomplete sessions | 0.15 |
| Shortened sessions | `shortened_sessions` | Avg duration down 40%+ | 0.10 |
| Reduced question count | `reduced_questions` | Questions per session down 50%+ | 0.10 |

### Detection Algorithm

```
# Compare recent period (14 days) to baseline (previous 14 days)
recent_period = get_sessions(today - 14, today)
baseline_period = get_sessions(today - 28, today - 14)

dropout_risk_indicators = []
risk_score = 0

# 1. Declining frequency
recent_count = len(recent_period)
baseline_count = len(baseline_period)
If baseline_count > 0:
  frequency_ratio = recent_count / baseline_count
  If frequency_ratio < 0.50:
    dropout_risk_indicators.append("declining_frequency")
    risk_score += 0.25

# 2. Declining performance
recent_accuracy = avg(s.accuracy for s in recent_period)
baseline_accuracy = avg(s.accuracy for s in baseline_period)
If recent_accuracy < baseline_accuracy - 10:
  dropout_risk_indicators.append("declining_performance")
  risk_score += 0.20

# 3. Long session gaps
session_dates = sorted([s.date for s in recent_period])
max_gap_days = 0
For i in range(1, len(session_dates)):
  gap = (session_dates[i] - session_dates[i-1]).days
  max_gap_days = max(max_gap_days, gap)
If max_gap_days > 7:
  dropout_risk_indicators.append("long_gaps")
  risk_score += 0.20

# 4. High abandonment rate
incomplete = count(s for s in recent_period if not s.completed)
abandonment_rate = incomplete / len(recent_period) if recent_period else 0
If abandonment_rate > 0.30:
  dropout_risk_indicators.append("high_abandonment")
  risk_score += 0.15

# 5. Shortened sessions
recent_avg_duration = avg(s.duration_minutes for s in recent_period)
baseline_avg_duration = avg(s.duration_minutes for s in baseline_period)
If baseline_avg_duration > 0:
  duration_ratio = recent_avg_duration / baseline_avg_duration
  If duration_ratio < 0.60:
    dropout_risk_indicators.append("shortened_sessions")
    risk_score += 0.10

# 6. Reduced question count
recent_avg_questions = avg(s.questions_attempted for s in recent_period)
baseline_avg_questions = avg(s.questions_attempted for s in baseline_period)
If baseline_avg_questions > 0:
  questions_ratio = recent_avg_questions / baseline_avg_questions
  If questions_ratio < 0.50:
    dropout_risk_indicators.append("reduced_questions")
    risk_score += 0.10
```

### Risk Level Classification

```
risk_score = sum(indicator_weights)

If risk_score >= 0.60:
  dropout_risk_level = "high"
Elif risk_score >= 0.35:
  dropout_risk_level = "medium"
Else:
  dropout_risk_level = "low"
```

## Engagement Decline Alerting

### Decline Detection

```
# Calculate engagement score over time
engagement_history = []

For week in last_8_weeks:
  week_sessions = get_sessions(week.start, week.end)

  engagement_score = (
    session_count_score × 0.30 +      # Frequency
    completion_rate × 0.25 +           # Commitment
    avg_accuracy × 0.25 +              # Quality
    avg_duration_score × 0.20          # Focus
  )

  engagement_history.append({
    "week": week.number,
    "score": engagement_score
  })

# Detect decline trend
If len(engagement_history) >= 4:
  recent_4 = engagement_history[-4:]
  trend_slope = linear_regression_slope([w.score for w in recent_4])

  If trend_slope < -0.05:
    engagement_trend = "declining"
    generate_alert = True
  Elif trend_slope < -0.02:
    engagement_trend = "slightly_declining"
    generate_alert = False
  Elif trend_slope > 0.02:
    engagement_trend = "improving"
    generate_alert = False
  Else:
    engagement_trend = "stable"
    generate_alert = False
```

### Alert Types

| Alert Type | Trigger | Urgency |
|------------|---------|---------|
| `critical_disengagement` | No sessions in 7+ days AND dropout_risk = high | immediate |
| `declining_engagement` | 4-week declining trend | this_week |
| `performance_drop` | Accuracy down 15%+ | this_week |
| `abandonment_pattern` | 3+ incomplete sessions in a row | this_week |
| `inactivity_warning` | No sessions in 5+ days | this_week |

### Alert Generation

```
alerts = []

# Check for critical disengagement
days_since_last = (today - last_session_date).days
If days_since_last >= 7 AND dropout_risk_level == "high":
  alerts.append({
    "type": "critical_disengagement",
    "message": f"No activity for {days_since_last} days with multiple risk indicators",
    "urgency": "immediate",
    "recommended_action": "personal_outreach"
  })

# Check for declining engagement
If engagement_trend == "declining":
  alerts.append({
    "type": "declining_engagement",
    "message": "Engagement has declined over the past 4 weeks",
    "urgency": "this_week",
    "recommended_action": "graduated_nudge"
  })

# Check for performance drop
If "declining_performance" in dropout_risk_indicators:
  alerts.append({
    "type": "performance_drop",
    "message": f"Performance dropped {accuracy_drop}% from baseline",
    "urgency": "this_week",
    "recommended_action": "support_session"
  })
```

## Graduated Nudging Strategy

### Nudge Levels

| Level | Days Since Activity | Nudge Type | Tone |
|-------|---------------------|------------|------|
| 1 | 1-2 days | Gentle reminder | Friendly, casual |
| 2 | 3-5 days | Encouraging check-in | Supportive, motivating |
| 3 | 7+ days | Re-engagement outreach | Concerned, offering help |

### Nudge Implementation

```
1-Day Nudge (Level 1):
  trigger_after_hours = 24
  message_template = "gentle_reminder"
  content = "Quick check-in: You have {urgent_topics} topics that could use some attention. Just 10 minutes today can make a difference!"
  action_offered = "quick_5_question_session"

3-Day Nudge (Level 2):
  trigger_after_hours = 72
  message_template = "encouraging_checkin"
  content = "We miss your progress! Your ERI is at {eri}. A short session today could help maintain your momentum. Would you like a personalized 15-minute review?"
  action_offered = "personalized_review_session"

7-Day Nudge (Level 3):
  trigger_after_hours = 168
  message_template = "reengagement_outreach"
  content = "It's been a week since we practiced together. Your exam is {days_until_exam} days away. I've prepared a special catch-up session focusing on {top_weak_topic}. Ready when you are!"
  action_offered = "catch_up_session"
```

### Nudge Execution Logic

```
For student:
  days_since_last = (today - last_session_date).days
  hours_since_last = days_since_last × 24

  # Check current nudge state
  last_nudge = get_last_nudge(student_id)

  If last_nudge exists:
    hours_since_nudge = (now - last_nudge.sent_at).hours

    # Don't re-nudge too soon (minimum 24 hours between nudges)
    If hours_since_nudge < 24:
      return None

    # Escalate if no response to previous nudge
    If last_nudge.level < 3 AND not last_nudge.responded:
      If hours_since_nudge >= 48:
        next_level = last_nudge.level + 1
        send_nudge(student_id, level=next_level)

  Else:
    # No previous nudge - check if nudge needed
    If hours_since_last >= 24:
      send_nudge(student_id, level=1)

  # Escalation schedule
  If hours_since_last >= 168 AND (last_nudge is None OR last_nudge.level < 3):
    send_nudge(student_id, level=3)
  Elif hours_since_last >= 72 AND (last_nudge is None OR last_nudge.level < 2):
    send_nudge(student_id, level=2)
  Elif hours_since_last >= 24 AND last_nudge is None:
    send_nudge(student_id, level=1)
```

### Response Tracking

```
For each nudge sent:
  record = {
    "nudge_id": generate_id(),
    "student_id": student_id,
    "level": nudge_level,
    "sent_at": now,
    "message_template": template_name,
    "channel": "whatsapp",
    "responded": false,
    "responded_at": null,
    "response_type": null,  # session_started | message_reply | ignored
    "session_started_after": null  # session_id if applicable
  }

# When student starts a session after nudge
If session_started AND pending_nudge exists:
  pending_nudge.responded = true
  pending_nudge.responded_at = now
  pending_nudge.response_type = "session_started"
  pending_nudge.session_started_after = session_id

  # Calculate nudge effectiveness
  response_time_hours = (responded_at - sent_at).hours
```

## Execution Steps

1. **Load engagement data**
   ```
   history = read_file(memory/students/{student_id}/history.json)
   sessions = read_file(memory/students/{student_id}/sessions/*.json)
   nudge_history = read_file(logs/nudges/{student_id}.json)
   ```

2. **Detect dropout risk indicators**
   ```
   indicators = detect_dropout_indicators(history, sessions)
   risk_level = classify_risk(indicators)
   ```

3. **Calculate engagement trend**
   ```
   engagement_history = calculate_weekly_engagement(sessions)
   trend = analyze_trend(engagement_history)
   ```

4. **Generate alerts**
   ```
   alerts = generate_alerts(indicators, trend, last_session_date)
   ```

5. **Determine nudge action**
   ```
   nudge = determine_nudge(last_session_date, nudge_history)
   If nudge:
     execute_nudge(nudge)
   ```

6. **Save engagement status**
   ```
   write_file(memory/students/{student_id}/engagement-status.json)
   ```

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "action": {
    "type": "string",
    "enum": ["check_status", "send_nudge", "record_response"],
    "required": true
  },
  "nudge_response": {
    "type": "object",
    "required": false,
    "description": "Required for record_response action",
    "properties": {
      "nudge_id": "string",
      "response_type": "session_started | message_reply | ignored"
    }
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "checked_at": "string ISO 8601",
  "engagement_status": {
    "current_score": "number 0-1",
    "trend": "improving | stable | slightly_declining | declining",
    "trend_slope": "number",
    "last_session_date": "string ISO 8601",
    "days_since_last_session": "integer"
  },
  "dropout_risk": {
    "level": "low | medium | high",
    "score": "number 0-1",
    "indicators": ["string indicator codes"],
    "indicator_details": {
      "<indicator>": {
        "detected": "boolean",
        "value": "number",
        "threshold": "number"
      }
    }
  },
  "alerts": [
    {
      "type": "string alert type",
      "message": "string",
      "urgency": "immediate | this_week | this_month",
      "recommended_action": "string"
    }
  ],
  "nudge_status": {
    "nudge_needed": "boolean",
    "current_level": "integer 1-3 | null",
    "last_nudge": {
      "sent_at": "string ISO 8601",
      "level": "integer",
      "responded": "boolean"
    },
    "next_nudge": {
      "level": "integer",
      "scheduled_for": "string ISO 8601",
      "message_preview": "string"
    }
  },
  "recommendations": [
    {
      "type": "intervention | content | scheduling",
      "message": "string",
      "priority": "high | medium | low"
    }
  ]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/history.json` |
| Read | `memory/students/{student_id}/sessions/*.json` |
| Read | `logs/nudges/{student_id}.json` |
| Write | `memory/students/{student_id}/engagement-status.json` |
| Write | `logs/nudges/{student_id}.json` |

## Engagement Status Schema

Location: `memory/students/{student_id}/engagement-status.json`

```json
{
  "$schema": "exam-tutor/engagement-status/v1",
  "student_id": "string (required)",
  "current_score": "number 0-1 (required)",
  "trend": "improving | stable | slightly_declining | declining (required)",
  "dropout_risk_level": "low | medium | high (required)",
  "dropout_risk_indicators": ["string indicator codes"],
  "last_checked": "string ISO 8601 (required)",
  "engagement_history": [
    {
      "week_start": "string ISO 8601",
      "score": "number 0-1",
      "sessions_count": "integer",
      "avg_accuracy": "number 0-100"
    }
  ],
  "nudge_effectiveness": {
    "total_nudges_sent": "integer",
    "nudges_responded": "integer",
    "response_rate": "number 0-1",
    "avg_response_time_hours": "number"
  }
}
```

## Example Output

```json
{
  "student_id": "student_123",
  "checked_at": "2025-02-03T15:00:00Z",
  "engagement_status": {
    "current_score": 0.45,
    "trend": "declining",
    "trend_slope": -0.08,
    "last_session_date": "2025-01-29T18:30:00Z",
    "days_since_last_session": 5
  },
  "dropout_risk": {
    "level": "medium",
    "score": 0.45,
    "indicators": ["declining_frequency", "long_gaps"],
    "indicator_details": {
      "declining_frequency": {
        "detected": true,
        "value": 0.40,
        "threshold": 0.50
      },
      "long_gaps": {
        "detected": true,
        "value": 5,
        "threshold": 7
      }
    }
  },
  "alerts": [
    {
      "type": "declining_engagement",
      "message": "Engagement has declined over the past 4 weeks",
      "urgency": "this_week",
      "recommended_action": "graduated_nudge"
    }
  ],
  "nudge_status": {
    "nudge_needed": true,
    "current_level": 2,
    "last_nudge": {
      "sent_at": "2025-02-01T10:00:00Z",
      "level": 1,
      "responded": false
    },
    "next_nudge": {
      "level": 2,
      "scheduled_for": "2025-02-03T10:00:00Z",
      "message_preview": "We miss your progress! Your ERI is at 58. A short session today could help maintain your momentum..."
    }
  },
  "recommendations": [
    {
      "type": "intervention",
      "message": "Student showing signs of disengagement - escalate to level 2 nudge",
      "priority": "high"
    },
    {
      "type": "content",
      "message": "Consider offering shorter, easier sessions to rebuild momentum",
      "priority": "medium"
    }
  ]
}
```

## Constraints

- Maximum 1 nudge per 24 hours
- Maximum 3 nudge levels before requiring human intervention
- Must respect student quiet hours from profile
- Track nudge effectiveness to improve messaging
- Don't nudge if student explicitly requested break
- Alert human if 3 consecutive nudges get no response

## Usage Notes

- Run engagement check daily for all active students
- Integrate with autonomous-session-initiator for trigger decisions
- Use nudge response data to personalize future interventions
- Escalate to human support if automated nudges aren't working
- Consider exam proximity when determining nudge urgency
