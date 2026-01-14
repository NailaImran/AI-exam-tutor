---
name: session-logger
description: Creates an audit log entry for a practice session. Use this skill at the end of every practice session for debugging, analytics, and audit trail purposes. Records session metadata, duration, and key events. Optional skill for compliance and troubleshooting.
---

# Session Logger

Creates detailed audit logs for practice sessions.

## MCP Integration

This skill uses the **filesystem MCP server** for writing log files.

### Required MCP Tools
- `mcp__filesystem__write_file` - Write log entry to logs directory
- `mcp__filesystem__create_directory` - Ensure log directory exists

## Execution Steps

1. **Validate inputs**
   - student_id must be valid
   - session_id must be unique
   - session_type must be valid enum
   - start_time and end_time must be valid ISO 8601

2. **Calculate session duration**
   ```
   duration_seconds = end_time - start_time
   duration_minutes = duration_seconds / 60
   ```

3. **Process events array**
   ```
   For each event in events:
     Validate event structure:
       - timestamp: ISO 8601
       - event_type: string
       - data: object (optional)

     Normalize timestamps to relative offsets
   ```

4. **Build log entry**
   ```json
   {
     "log_id": "{session_id}-LOG",
     "student_id": "{student_id}",
     "session_id": "{session_id}",
     "session_type": "{session_type}",
     "start_time": "{start_time}",
     "end_time": "{end_time}",
     "duration_seconds": duration_seconds,
     "duration_minutes": duration_minutes,
     "events_count": events.length,
     "events": events,
     "metadata": {
       "logged_at": now(),
       "version": "1.0"
     }
   }
   ```

5. **Ensure directory exists**
   ```
   Use: mcp__filesystem__create_directory
   Path: logs/sessions/{student_id}
   ```

6. **Write log file**
   ```
   Use: mcp__filesystem__write_file
   Path: logs/sessions/{student_id}/{session_id}.json
   Content: log_entry
   ```

7. **Return status**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "session_id": {
    "type": "string",
    "required": true,
    "description": "Unique identifier for this session"
  },
  "session_type": {
    "type": "enum",
    "values": ["diagnostic", "adaptive", "timed", "review"],
    "required": true
  },
  "start_time": {
    "type": "string",
    "format": "ISO 8601",
    "required": true
  },
  "end_time": {
    "type": "string",
    "format": "ISO 8601",
    "required": true
  },
  "events": {
    "type": "array",
    "required": false,
    "default": [],
    "items": {
      "timestamp": "string (ISO 8601)",
      "event_type": "string",
      "data": "object (optional)"
    }
  }
}
```

## Output Schema

```json
{
  "log_id": {
    "type": "string",
    "description": "Unique identifier for the log entry"
  },
  "write_status": {
    "type": "enum",
    "values": ["success", "failure"]
  },
  "duration_seconds": {
    "type": "integer",
    "description": "Calculated session duration"
  },
  "log_path": {
    "type": "string",
    "description": "Path where log was written"
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Write | `logs/sessions/{student_id}/{session_id}.json` |

## Event Types

| Event Type | Description | Data Fields |
|------------|-------------|-------------|
| `session_started` | Session initialization | exam_type, question_count |
| `question_displayed` | Question shown to student | question_id, question_number |
| `answer_submitted` | Student submitted answer | question_id, answer, time_spent |
| `question_skipped` | Student skipped question | question_id |
| `session_paused` | Session temporarily paused | pause_reason |
| `session_resumed` | Session resumed | pause_duration |
| `session_completed` | Session finished normally | completion_reason |
| `session_abandoned` | Session ended early | abandonment_reason |

## Example Log Entry

```json
{
  "log_id": "PPSC-ADAPT-001-20240115-LOG",
  "student_id": "student_123",
  "session_id": "PPSC-ADAPT-001-20240115",
  "session_type": "adaptive",
  "start_time": "2024-01-15T10:00:00Z",
  "end_time": "2024-01-15T10:45:00Z",
  "duration_seconds": 2700,
  "duration_minutes": 45,
  "events_count": 52,
  "events": [
    {
      "timestamp": "2024-01-15T10:00:00Z",
      "event_type": "session_started",
      "data": {"exam_type": "PPSC", "question_count": 25}
    },
    {
      "timestamp": "2024-01-15T10:00:05Z",
      "event_type": "question_displayed",
      "data": {"question_id": "PPSC-PK-042", "question_number": 1}
    }
  ],
  "metadata": {
    "logged_at": "2024-01-15T10:45:01Z",
    "version": "1.0"
  }
}
```

## Constraints

- Must write atomically (no partial logs)
- Must include duration_seconds in output
- Log format must be machine-parseable (valid JSON)
- Must not fail silently—always return status
- Events array is optional; empty sessions are valid

## Usage Notes

This skill is optional but recommended for:
- Debugging unexpected behavior
- Analytics on student engagement
- Audit compliance requirements
- Identifying UX issues (long pauses, abandonment)
