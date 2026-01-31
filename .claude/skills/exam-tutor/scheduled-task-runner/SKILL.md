# Skill: scheduled-task-runner

**Category**: CORE (Phase 3)
**Purpose**: Execute scheduled tasks (daily questions, weekly reports, LinkedIn posts) based on schedule configuration

## Description

The scheduled-task-runner skill checks schedule configuration files and executes due tasks. It manages the cron-like scheduling for Phase 3 automated workflows without requiring a persistent daemon.

## Input

```json
{
  "task_type": "daily_question | weekly_report | linkedin_post | all",
  "force_run": "boolean (optional, default: false, ignores schedule check)",
  "dry_run": "boolean (optional, default: false, simulates without executing)"
}
```

## Output

```json
{
  "task_type": "string",
  "executed": "boolean",
  "reason": "string (why executed or skipped)",
  "items_processed": "integer",
  "next_run": "string ISO 8601",
  "errors": ["string"],
  "details": {
    "students_notified": "integer (for daily_question/weekly_report)",
    "posts_created": "integer (for linkedin_post)"
  }
}
```

## Workflow

### 1. Load Schedule Configuration

Read from `schedules/{task_type}.json`:
- Check if `enabled` is true
- Compare current time against `schedule` settings
- Check `last_run` to prevent duplicate execution

### 2. Determine If Due

```
is_due = (
  enabled == true AND
  current_time >= scheduled_time AND
  (last_run is null OR last_run.timestamp < today's scheduled time)
)
```

### 3. Execute Task

**For daily_question**:
1. List all students with `whatsapp.opted_in_daily_questions == true`
2. For each student:
   - Check timezone and preferred_time
   - If due, invoke daily-question-selector skill
   - Queue message via whatsapp-message-sender skill
3. Update last_run in schedule file

**For weekly_report**:
1. List all students with `notifications.weekly_report == true`
2. For each student:
   - Invoke progress-report-generator skill
   - Queue WhatsApp summary via whatsapp-message-sender
3. Update last_run in schedule file

**For linkedin_post**:
1. Invoke social-post-generator skill
2. Save draft to `needs_action/social-posts/`
3. Update last_run in schedule file
4. Note: Actual posting requires human approval

### 4. Update Schedule State

```json
{
  "last_run": {
    "timestamp": "current ISO 8601",
    "status": "success | failed",
    "items_processed": "count"
  },
  "next_run": "calculated next scheduled time"
}
```

## MCP Tools Used

- `mcp__filesystem__read_file` - Load schedule configs, student profiles
- `mcp__filesystem__write_file` - Update schedule state
- `mcp__filesystem__list_directory` - List students for batch processing

## Schedule File Format

```json
{
  "task_type": "daily_question",
  "enabled": true,
  "schedule": {
    "frequency": "daily",
    "hour": 8,
    "minute": 0,
    "timezone": "Asia/Karachi"
  },
  "target": {
    "scope": "all_opted_in"
  },
  "last_run": null,
  "next_run": "2026-01-31T08:00:00+05:00"
}
```

## Timezone Handling

1. Read student's `whatsapp.timezone` (default: Asia/Karachi)
2. Convert schedule time to student's local time
3. Only process if within delivery window (±5 minutes)
4. Respect `quiet_hours` settings

## Error Handling

- **Schedule file missing**: Create default disabled schedule
- **Student processing failure**: Log error, continue with next student
- **Partial completion**: Record items_processed, log failures
- **All failures**: Set last_run.status = "failed", include error summary

## Constitution Compliance

- **Principle V (Respect Context)**: Respects student timezone and quiet hours
- **Principle VI (Bounded Autonomy)**: LinkedIn posts go to approval queue

## Example Usage

```
Input: {
  "task_type": "daily_question",
  "force_run": false
}

Output: {
  "task_type": "daily_question",
  "executed": true,
  "reason": "Scheduled time reached (08:00 PKT)",
  "items_processed": 5,
  "next_run": "2026-01-31T08:00:00+05:00",
  "errors": [],
  "details": {
    "students_notified": 5
  }
}
```

## Manual Trigger

The skill can be invoked manually with `force_run: true` to execute regardless of schedule. Useful for testing and catch-up scenarios.

## Related Skills

- daily-question-selector (selects questions for daily delivery)
- progress-report-generator (generates weekly reports)
- social-post-generator (creates LinkedIn drafts)
- whatsapp-message-sender (delivers messages)
