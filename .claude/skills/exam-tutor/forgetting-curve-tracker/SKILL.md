---
name: forgetting-curve-tracker
description: Tracks knowledge decay per topic using SM-2 spaced repetition algorithm. Calculates retention scores, decay rates, and optimal review intervals. Use to predict when knowledge will fall below retention threshold and schedule preventive revision.
phase: 4
category: INTELLIGENCE
priority: P1
---

# Forgetting Curve Tracker

Implements the SM-2 (SuperMemo 2) spaced repetition algorithm to track knowledge retention and predict optimal review times for each topic.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and updating retention metrics.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read topic stats, session history
- `mcp__filesystem__write_file` - Update retention predictions

## SM-2 Spaced Repetition Algorithm

### Core Algorithm

The SM-2 algorithm calculates optimal review intervals based on performance quality.

```
Input: quality (0-5 scale based on accuracy)
  5 = Perfect response (100% accuracy)
  4 = Correct after hesitation (90-99%)
  3 = Correct with difficulty (70-89%)
  2 = Incorrect, easy to recall correct (50-69%)
  1 = Incorrect, hard to recall correct (30-49%)
  0 = Complete blackout (<30%)

Parameters:
  EF = Easiness Factor (starts at 2.5, minimum 1.3)
  n = Repetition number
  I = Interval in days

Algorithm:
  1. Convert accuracy to quality:
     quality = floor(accuracy / 20)  # Maps 0-100 to 0-5

  2. Update Easiness Factor:
     EF' = EF + (0.1 - (5 - quality) × (0.08 + (5 - quality) × 0.02))
     EF = max(1.3, EF')

  3. Calculate next interval:
     If quality < 3:
       n = 0  # Reset repetition count
       I = 1  # Review tomorrow
     Else:
       If n == 0:
         I = 1
       Elif n == 1:
         I = 6
       Else:
         I = round(I_prev × EF)
       n = n + 1

  4. Calculate due_date:
     due_date = last_reviewed + I days
```

### Retention Score Calculation

The retention score represents estimated memory strength (0-1).

```
retention_score = e^(-time_elapsed / stability)

Where:
  time_elapsed = days since last_reviewed
  stability = optimal_interval_days × EF

Simplified formula:
  days_since = (today - last_reviewed).days
  decay_rate = 1 / (optimal_interval_days × EF)
  retention_score = e^(-decay_rate × days_since)

Clamped to [0.0, 1.0]
```

### Decay Rate Calculation

```
decay_rate = ln(minimum_retention_target) / -optimal_interval_days

Example:
  If minimum_retention_target = 0.70
  And optimal_interval_days = 7
  Then decay_rate = ln(0.70) / -7 = 0.051

This means retention drops by ~5.1% per day
```

## Execution Steps

1. **Load student topic stats**
   ```
   topic_stats = read_file(memory/students/{student_id}/topic-stats.json)
   ```

2. **Load existing retention data (if any)**
   ```
   existing = read_file(memory/students/{student_id}/retention-data.json)
   # Initialize if not exists
   ```

3. **For each topic, calculate retention metrics**
   ```
   For topic in topic_stats.topics:
     days_since = (today - topic.last_practiced).days

     # Get or initialize SM-2 parameters
     ef = existing[topic].easiness_factor OR 2.5
     n = existing[topic].repetition_count OR 0
     interval = existing[topic].optimal_interval_days OR 1

     # Calculate current retention
     stability = interval × ef
     retention_score = e^(-days_since / stability)

     # Calculate decay rate
     decay_rate = 1 / stability

     # Determine if review needed
     due_date = topic.last_practiced + interval days
     is_due = today >= due_date
   ```

4. **Update after review session**
   ```
   If topic was reviewed today:
     quality = accuracy_to_quality(session_accuracy)
     ef' = update_easiness_factor(ef, quality)
     interval' = calculate_next_interval(quality, n, interval, ef')
     n' = update_repetition_count(quality, n)

     # Reset retention to 1.0 after successful review
     retention_score = 1.0
     last_reviewed = today
   ```

5. **Build predictions**
   ```
   For each topic:
     predicted_7d = retention_score × e^(-decay_rate × 7)
     predicted_14d = retention_score × e^(-decay_rate × 14)
     predicted_30d = retention_score × e^(-decay_rate × 30)

     # Days until minimum retention reached
     days_until_threshold = -ln(minimum_retention_target / retention_score) / decay_rate
   ```

6. **Save retention data**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "action": {
    "type": "string",
    "enum": ["calculate", "update_after_review"],
    "required": true
  },
  "review_data": {
    "type": "object",
    "required": false,
    "description": "Required if action is update_after_review",
    "properties": {
      "topic_id": "string",
      "accuracy": "number 0-100",
      "reviewed_at": "string ISO 8601"
    }
  },
  "minimum_retention_target": {
    "type": "number",
    "default": 0.70,
    "description": "Retention threshold below which review is urgent"
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "calculated_at": "string ISO 8601",
  "minimum_retention_target": "number (default: 0.70)",
  "topics": [
    {
      "topic_id": "string",
      "subject": "string",
      "last_reviewed": "string ISO 8601",
      "retention_score": "number 0-1",
      "decay_rate": "number per day",
      "easiness_factor": "number >= 1.3",
      "repetition_count": "integer",
      "optimal_interval_days": "integer",
      "due_date": "string ISO 8601",
      "is_due": "boolean",
      "days_until_due": "integer (negative if overdue)",
      "predictions": {
        "retention_7d": "number 0-1",
        "retention_14d": "number 0-1",
        "retention_30d": "number 0-1",
        "days_until_threshold": "integer"
      },
      "status": "strong | stable | weakening | critical"
    }
  ],
  "summary": {
    "total_topics": "integer",
    "topics_due_today": "integer",
    "topics_overdue": "integer",
    "topics_at_risk": "integer (retention < 0.70)",
    "topics_critical": "integer (retention < 0.50)",
    "average_retention": "number 0-1"
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `memory/students/{student_id}/history.json` |
| Read/Write | `memory/students/{student_id}/retention-data.json` |

## Retention Data Schema

Location: `memory/students/{student_id}/retention-data.json`

```json
{
  "$schema": "exam-tutor/retention-data/v1",
  "student_id": "string (required)",
  "topics": {
    "<topic_id>": {
      "easiness_factor": "number >= 1.3 (default: 2.5)",
      "repetition_count": "integer (default: 0)",
      "optimal_interval_days": "integer (default: 1)",
      "last_quality": "integer 0-5",
      "last_reviewed": "string ISO 8601",
      "review_history": [
        {
          "date": "string ISO 8601",
          "accuracy": "number 0-100",
          "quality": "integer 0-5",
          "interval_before": "integer days",
          "interval_after": "integer days"
        }
      ]
    }
  },
  "settings": {
    "algorithm": "sm2",
    "minimum_retention_target": "number (default: 0.70)",
    "initial_easiness_factor": "number (default: 2.5)"
  },
  "updated_at": "string ISO 8601"
}
```

## Status Classification

```
If retention_score >= 0.85:
  status = "strong"
Elif retention_score >= 0.70:
  status = "stable"
Elif retention_score >= 0.50:
  status = "weakening"
Else:
  status = "critical"
```

## Quality Conversion

```
accuracy_to_quality(accuracy):
  If accuracy >= 100:
    return 5
  Elif accuracy >= 90:
    return 4
  Elif accuracy >= 70:
    return 3
  Elif accuracy >= 50:
    return 2
  Elif accuracy >= 30:
    return 1
  Else:
    return 0
```

## Example Output

```json
{
  "student_id": "student_123",
  "calculated_at": "2025-02-03T10:00:00Z",
  "minimum_retention_target": 0.70,
  "topics": [
    {
      "topic_id": "constitutional_amendments",
      "subject": "pakistan_studies",
      "last_reviewed": "2025-01-25T14:00:00Z",
      "retention_score": 0.52,
      "decay_rate": 0.08,
      "easiness_factor": 2.1,
      "repetition_count": 3,
      "optimal_interval_days": 7,
      "due_date": "2025-02-01T14:00:00Z",
      "is_due": true,
      "days_until_due": -2,
      "predictions": {
        "retention_7d": 0.31,
        "retention_14d": 0.19,
        "retention_30d": 0.07,
        "days_until_threshold": -3
      },
      "status": "critical"
    },
    {
      "topic_id": "current_affairs_jan_2025",
      "subject": "current_affairs",
      "last_reviewed": "2025-02-02T09:00:00Z",
      "retention_score": 0.92,
      "decay_rate": 0.04,
      "easiness_factor": 2.8,
      "repetition_count": 5,
      "optimal_interval_days": 14,
      "due_date": "2025-02-16T09:00:00Z",
      "is_due": false,
      "days_until_due": 13,
      "predictions": {
        "retention_7d": 0.70,
        "retention_14d": 0.54,
        "retention_30d": 0.31,
        "days_until_threshold": 8
      },
      "status": "strong"
    }
  ],
  "summary": {
    "total_topics": 25,
    "topics_due_today": 3,
    "topics_overdue": 2,
    "topics_at_risk": 5,
    "topics_critical": 2,
    "average_retention": 0.68
  }
}
```

## Constraints

- Easiness Factor must never drop below 1.3
- Retention score must be clamped to [0.0, 1.0]
- Default minimum_retention_target is 0.70
- Reset repetition count to 0 on quality < 3 (poor recall)
- Track full review history for algorithm tuning
- Must handle topics with no review history (initialize defaults)

## Usage Notes

- Call after each practice session to update retention metrics
- Use predictions to feed into revision-cycle-manager
- Topics with status "critical" should trigger immediate intervention
- Average retention is a key health metric for the student's knowledge
- Easiness Factor adapts over time - difficult topics get lower EF, easier ones get higher
