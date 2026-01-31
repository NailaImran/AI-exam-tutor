# Skill Contract: student-profile-loader

**Version**: 1.0
**Category**: CORE
**MCP Tools**: read_file, list_directory

## Purpose

Loads student profile, preferences, and historical context from file-based storage.

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true,
    "pattern": "^[a-zA-Z0-9_-]+$",
    "description": "Unique identifier for the student"
  }
}
```

## Output Schema

```json
{
  "profile": {
    "type": "object",
    "properties": {
      "student_id": "string",
      "name": "string",
      "email": "string | null",
      "exam_target": "SPSC | PPSC | KPPSC",
      "target_exam_date": "string ISO 8601 | null",
      "created_at": "string ISO 8601",
      "updated_at": "string ISO 8601",
      "preferences": {
        "daily_time_minutes": "integer",
        "difficulty_preference": "string",
        "notification_enabled": "boolean"
      },
      "status": "active | inactive | completed"
    }
  },
  "history_summary": {
    "total_sessions": "integer",
    "total_questions_attempted": "integer",
    "overall_accuracy": "number 0-100",
    "last_session_date": "string ISO 8601 | null",
    "current_eri": "number 0-100 | null",
    "eri_band": "string | null"
  },
  "load_status": "found | not_found | corrupted"
}
```

## MCP Operations

1. `mcp__filesystem__list_directory` → Check `Students/{student_id}/` exists
2. `mcp__filesystem__read_file` → Read `Students/{student_id}/profile.json`
3. `mcp__filesystem__read_file` → Read `Students/{student_id}/history.json` (optional)

## Error Handling

| Condition | Response |
|-----------|----------|
| Directory not found | `load_status: "not_found"` |
| Invalid JSON | `load_status: "corrupted"` |
| Missing history.json | Return profile with null history_summary |
| Invalid student_id format | Error before MCP calls |

## Example

**Input**:
```json
{ "student_id": "STU001" }
```

**Output**:
```json
{
  "profile": {
    "student_id": "STU001",
    "name": "Ahmed Khan",
    "exam_target": "PPSC",
    "status": "active"
  },
  "history_summary": {
    "total_sessions": 3,
    "current_eri": 52.0,
    "eri_band": "approaching"
  },
  "load_status": "found"
}
```
