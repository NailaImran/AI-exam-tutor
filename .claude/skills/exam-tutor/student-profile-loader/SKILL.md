---
name: student-profile-loader
description: Loads a student's profile, exam target, and historical performance data from persistent memory. Use this skill when initializing a session, before any assessment or practice activity, or when student context is needed. Returns structured profile object for downstream skills.
---

# Student Profile Loader

Loads student identity, preferences, exam target, and historical performance from file-based memory.

## MCP Integration

This skill uses the **filesystem MCP server** for all read operations.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read student profile and history JSON files
- `mcp__filesystem__list_directory` - Check for student directory existence

## Execution Steps

1. **Validate student_id format**
   - Must be non-empty string
   - Must match pattern: `^[a-zA-Z0-9_-]+$`

2. **Check student directory exists**
   ```
   Use: mcp__filesystem__list_directory
   Path: memory/students/{student_id}
   ```
   - If directory not found → return `load_status: "not_found"`

3. **Load profile.json**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/profile.json
   ```
   - Parse JSON and validate against schema
   - If parse fails → return `load_status: "corrupted"`

4. **Load history.json**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/history.json
   ```
   - Parse JSON, merge with profile object
   - If file missing, use empty history array

5. **Return structured output**

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
      "exam_target": "SPSC | PPSC | KPPSC",
      "target_exam_date": "string (ISO 8601)",
      "subjects": ["array of subject objects"],
      "historical_scores": ["array of score records"],
      "weak_areas": ["array of topic strings"],
      "last_session_date": "string (ISO 8601)",
      "total_sessions": "integer",
      "created_at": "string (ISO 8601)"
    }
  },
  "load_status": {
    "type": "enum",
    "values": ["found", "not_found", "corrupted"]
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/profile.json` |
| Read | `memory/students/{student_id}/history.json` |

## Constraints

- Must return `not_found` if profile does not exist (never create)
- Must validate JSON schema before returning
- Must not modify any files
- Must handle missing history.json gracefully (return empty array)

## Error Handling

| Condition | Response |
|-----------|----------|
| Student directory missing | `load_status: "not_found"` |
| Invalid JSON in profile | `load_status: "corrupted"` |
| Missing history.json | Return profile with empty `historical_scores` |
| Invalid student_id format | Return error before file operations |
