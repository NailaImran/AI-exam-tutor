---
name: revision-cycle-manager
description: Manages spaced repetition queue with priority levels (urgent, high, normal, low). Enforces daily revision limits (10 items default) and minimum retention targets (0.70 default). Use to get the next revision items for a student and update queue after reviews.
phase: 4
category: AUTONOMY
priority: P1
---

# Revision Cycle Manager

Manages the spaced repetition revision queue, prioritizing topics based on retention scores and enforcing daily limits.

## MCP Integration

This skill uses the **filesystem MCP server** for reading and writing revision queue data.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read revision queue and retention data
- `mcp__filesystem__write_file` - Update revision queue

## Priority Classification

### Priority Levels

| Priority | Retention Score | Criteria | Action |
|----------|----------------|----------|--------|
| `urgent` | < 0.50 | Critical decay | Review immediately |
| `high` | 0.50 - 0.69 | Below threshold | Review today |
| `normal` | 0.70 - 0.84 | On track | Review when due |
| `low` | >= 0.85 | Strong retention | Can defer |

### Priority Assignment Algorithm

```
For each topic in retention_data:
  If retention_score < 0.50:
    priority = "urgent"
  Elif retention_score < minimum_retention_target:  # default 0.70
    priority = "high"
  Elif retention_score < 0.85:
    priority = "normal"
  Else:
    priority = "low"
```

## Queue Prioritization Algorithm

### Sorting Order

Items are sorted by multiple factors:

```
1. Priority level (urgent > high > normal > low)
2. Days overdue (more overdue = higher priority within level)
3. Retention score (lower score = higher priority within level)
4. Last reviewed date (older = higher priority for ties)

sort_key(item) = (
  priority_rank[item.priority],  # 0=urgent, 1=high, 2=normal, 3=low
  -max(0, days_overdue),         # Negative so overdue items come first
  item.retention_score,          # Lower scores first
  item.last_reviewed             # Older dates first
)
```

### Daily Revision Limit Enforcement

```
DAILY_REVISION_LIMIT = 10  # Default, configurable per student

# Get items revised today
revised_today = count(queue where revised_date == today)

# Calculate remaining capacity
remaining_capacity = DAILY_REVISION_LIMIT - revised_today

# Apply limit to queue
If remaining_capacity <= 0:
  available_for_revision = []
  limit_reached = true
Else:
  available_for_revision = sorted_queue[:remaining_capacity]
  limit_reached = remaining_capacity == 0
```

### Minimum Retention Target

```
MINIMUM_RETENTION_TARGET = 0.70  # Default, configurable

# Items below threshold need review
below_threshold = queue.filter(item => item.retention_score < MINIMUM_RETENTION_TARGET)

# These are "high" or "urgent" priority automatically
```

## Execution Steps

1. **Load retention data**
   ```
   retention_data = read_file(memory/students/{student_id}/retention-data.json)
   ```

2. **Load existing revision queue**
   ```
   queue = read_file(memory/students/{student_id}/revision-queue.json)
   settings = queue.settings OR defaults
   ```

3. **Sync queue with retention data**
   ```
   For each topic in retention_data.topics:
     If topic not in queue:
       Add topic to queue with retention metrics
     Else:
       Update topic metrics in queue

   Remove topics from queue that are no longer in retention_data
   ```

4. **Calculate priorities**
   ```
   For each item in queue:
     item.priority = calculate_priority(item.retention_score, settings.minimum_retention_target)
     item.days_overdue = (today - item.due_date).days if today > item.due_date else 0
   ```

5. **Sort queue by priority**
   ```
   queue.sort(key=sort_key)
   ```

6. **Apply daily limit**
   ```
   revised_today = count_revised_today(queue)
   remaining = settings.daily_revision_limit - revised_today
   available = queue[:remaining] if remaining > 0 else []
   ```

7. **Build response**

8. **Save updated queue**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "action": {
    "type": "string",
    "enum": ["get_queue", "mark_revised", "update_settings"],
    "required": true
  },
  "mark_revised_data": {
    "type": "object",
    "required": false,
    "description": "Required if action is mark_revised",
    "properties": {
      "topic_id": "string",
      "revised_at": "string ISO 8601"
    }
  },
  "settings_update": {
    "type": "object",
    "required": false,
    "description": "Required if action is update_settings",
    "properties": {
      "minimum_retention_target": "number 0-1",
      "daily_revision_limit": "integer >= 1"
    }
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "queue_updated_at": "string ISO 8601",
  "settings": {
    "algorithm": "sm2",
    "minimum_retention_target": "number (default: 0.70)",
    "daily_revision_limit": "integer (default: 10)"
  },
  "daily_status": {
    "revised_today": "integer",
    "remaining_capacity": "integer",
    "limit_reached": "boolean"
  },
  "available_for_revision": [
    {
      "topic_id": "string",
      "subject": "string",
      "priority": "urgent | high | normal | low",
      "retention_score": "number 0-1",
      "days_overdue": "integer",
      "due_date": "string ISO 8601",
      "last_reviewed": "string ISO 8601",
      "revision_count": "integer",
      "reason": "string explanation"
    }
  ],
  "queue_summary": {
    "total_items": "integer",
    "by_priority": {
      "urgent": "integer",
      "high": "integer",
      "normal": "integer",
      "low": "integer"
    },
    "items_due_today": "integer",
    "items_overdue": "integer"
  },
  "recommendations": {
    "focus_topic": "string | null",
    "focus_reason": "string | null",
    "estimated_session_minutes": "integer"
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/retention-data.json` |
| Read/Write | `memory/students/{student_id}/revision-queue.json` |

## Revision Queue Schema (Updated)

Location: `memory/students/{student_id}/revision-queue.json`

```json
{
  "$schema": "exam-tutor/revision-queue/v1",
  "student_id": "string (required)",
  "queue": [
    {
      "topic_id": "string (required)",
      "subject": "string (required)",
      "last_reviewed": "string ISO 8601 (required)",
      "retention_score": "number 0-1 (required)",
      "decay_rate": "number 0-1 (required)",
      "due_date": "string ISO 8601 (required)",
      "priority": "urgent | high | normal | low (required)",
      "revision_count": "integer (required)",
      "optimal_interval_days": "integer (required)",
      "revised_today": "boolean (default: false)",
      "days_overdue": "integer (calculated)"
    }
  ],
  "settings": {
    "algorithm": "sm2 (default)",
    "minimum_retention_target": "number 0-1 (default: 0.70)",
    "daily_revision_limit": "integer (default: 10)"
  },
  "daily_log": {
    "date": "string ISO 8601 date",
    "topics_revised": ["string topic_id"],
    "total_revised": "integer"
  },
  "updated_at": "string ISO 8601 (required)"
}
```

## Reason Generation

```
If priority == "urgent":
  If days_overdue > 0:
    reason = f"Critical: {days_overdue} days overdue, retention at {retention_score*100:.0f}%"
  Else:
    reason = f"Critical: Retention dropped to {retention_score*100:.0f}%"

Elif priority == "high":
  If days_overdue > 0:
    reason = f"Overdue by {days_overdue} days, retention below target"
  Else:
    reason = f"Retention at {retention_score*100:.0f}%, approaching critical threshold"

Elif priority == "normal":
  If is_due:
    reason = f"Scheduled review due today"
  Else:
    reason = f"Maintain retention, review in {days_until_due} days"

Else:  # low
  reason = f"Strong retention ({retention_score*100:.0f}%), no immediate action needed"
```

## Focus Topic Selection

```
# Select the single most important topic to focus on

If queue.filter(priority == "urgent").length > 0:
  focus_topic = first urgent item
  focus_reason = "Critical retention - immediate review needed"

Elif queue.filter(priority == "high").length > 0:
  focus_topic = first high item
  focus_reason = "Below target retention - prioritize today"

Elif queue.filter(is_due AND priority == "normal").length > 0:
  focus_topic = first due normal item
  focus_reason = "Scheduled review maintains optimal retention"

Else:
  focus_topic = null
  focus_reason = null
```

## Session Time Estimation

```
# Estimate time needed for available revisions

questions_per_topic = 5  # Default review session size
time_per_question = 90   # seconds

For available items:
  total_questions = len(available) × questions_per_topic
  estimated_minutes = ceil(total_questions × time_per_question / 60)
```

## Example Output

### Normal Queue Request

```json
{
  "student_id": "student_123",
  "queue_updated_at": "2025-02-03T10:00:00Z",
  "settings": {
    "algorithm": "sm2",
    "minimum_retention_target": 0.70,
    "daily_revision_limit": 10
  },
  "daily_status": {
    "revised_today": 2,
    "remaining_capacity": 8,
    "limit_reached": false
  },
  "available_for_revision": [
    {
      "topic_id": "constitutional_amendments",
      "subject": "pakistan_studies",
      "priority": "urgent",
      "retention_score": 0.45,
      "days_overdue": 3,
      "due_date": "2025-01-31T00:00:00Z",
      "last_reviewed": "2025-01-24T14:00:00Z",
      "revision_count": 2,
      "reason": "Critical: 3 days overdue, retention at 45%"
    },
    {
      "topic_id": "federal_structure",
      "subject": "pakistan_studies",
      "priority": "high",
      "retention_score": 0.62,
      "days_overdue": 1,
      "due_date": "2025-02-02T00:00:00Z",
      "last_reviewed": "2025-01-26T10:00:00Z",
      "revision_count": 3,
      "reason": "Overdue by 1 day, retention below target"
    },
    {
      "topic_id": "current_affairs_jan_2025",
      "subject": "current_affairs",
      "priority": "normal",
      "retention_score": 0.78,
      "days_overdue": 0,
      "due_date": "2025-02-03T00:00:00Z",
      "last_reviewed": "2025-01-27T09:00:00Z",
      "revision_count": 4,
      "reason": "Scheduled review due today"
    }
  ],
  "queue_summary": {
    "total_items": 25,
    "by_priority": {
      "urgent": 2,
      "high": 5,
      "normal": 12,
      "low": 6
    },
    "items_due_today": 4,
    "items_overdue": 3
  },
  "recommendations": {
    "focus_topic": "constitutional_amendments",
    "focus_reason": "Critical retention - immediate review needed",
    "estimated_session_minutes": 30
  }
}
```

### Daily Limit Reached

```json
{
  "student_id": "student_123",
  "queue_updated_at": "2025-02-03T18:00:00Z",
  "settings": {
    "algorithm": "sm2",
    "minimum_retention_target": 0.70,
    "daily_revision_limit": 10
  },
  "daily_status": {
    "revised_today": 10,
    "remaining_capacity": 0,
    "limit_reached": true
  },
  "available_for_revision": [],
  "queue_summary": {
    "total_items": 25,
    "by_priority": {
      "urgent": 1,
      "high": 3,
      "normal": 15,
      "low": 6
    },
    "items_due_today": 0,
    "items_overdue": 1
  },
  "recommendations": {
    "focus_topic": null,
    "focus_reason": "Daily revision limit reached. Resume tomorrow.",
    "estimated_session_minutes": 0
  }
}
```

## Constraints

- Must enforce daily_revision_limit (default: 10)
- Must enforce minimum_retention_target (default: 0.70)
- Queue must be sorted by priority before applying limit
- Urgent items should always be surfaced first
- Must track which topics were revised today
- Reset daily_log at midnight (based on student timezone)
- Must sync with forgetting-curve-tracker retention data
- Settings can be customized per student

## Usage Notes

- Call `get_queue` at the start of each study session
- Call `mark_revised` after each topic review is completed
- Use `update_settings` to customize for individual students
- Integrate with autonomous-session-initiator for trigger decisions
- Use focus_topic for single-topic intervention sessions
- Daily limit prevents burnout while ensuring consistent practice
