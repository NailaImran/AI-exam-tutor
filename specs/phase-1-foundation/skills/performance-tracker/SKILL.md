---
name: performance-tracker
description: Persists evaluation results to student history. Use this skill after answer-evaluator to save session data permanently. Appends session data, updates running statistics, and maintains topic-level performance metrics in file-based memory.
---

# Performance Tracker

Persists evaluation results and maintains cumulative performance statistics.

## MCP Integration

This skill uses the **filesystem MCP server** for all persistence operations.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read existing history and stats
- `mcp__filesystem__write_file` - Write updated files
- `mcp__filesystem__create_directory` - Create session directory if needed

## Execution Steps

1. **Validate inputs**
   - student_id must be valid
   - session_id must be unique
   - evaluation_results must contain required fields

2. **Load existing history**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/history.json
   ```
   - If file missing, initialize empty history array

3. **Load existing topic stats**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/topic-stats.json
   ```
   - If file missing, initialize empty stats object

4. **Create session record**
   ```json
   {
     "session_id": "{session_id}",
     "session_date": "{session_date}",
     "exam_type": "{exam_type}",
     "total_questions": evaluation_results.summary.total,
     "correct": evaluation_results.summary.correct,
     "accuracy": evaluation_results.summary.accuracy_percentage,
     "topics_covered": [list of topics],
     "duration_seconds": sum of time_spent
   }
   ```

5. **Append to history**
   ```
   history.sessions.push(session_record)
   history.total_sessions += 1
   history.last_session_date = session_date
   ```

6. **Update topic statistics**
   ```
   For each topic in topic_breakdown:
     topic_stats[topic].total_attempted += attempted
     topic_stats[topic].total_correct += correct
     topic_stats[topic].accuracy = recalculate
     topic_stats[topic].last_practiced = session_date
   ```

7. **Write updated history**
   ```
   Use: mcp__filesystem__write_file
   Path: memory/students/{student_id}/history.json
   Content: updated history object
   ```

8. **Write updated topic stats**
   ```
   Use: mcp__filesystem__write_file
   Path: memory/students/{student_id}/topic-stats.json
   Content: updated topic_stats object
   ```

9. **Write session detail file**
   ```
   Use: mcp__filesystem__write_file
   Path: memory/students/{student_id}/sessions/{session_id}.json
   Content: full evaluation_results with metadata
   ```

10. **Return status and updated totals**

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
    "description": "Unique identifier for this practice session"
  },
  "session_date": {
    "type": "string",
    "format": "ISO 8601",
    "required": true
  },
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "evaluation_results": {
    "type": "object",
    "required": true,
    "description": "Output from answer-evaluator skill",
    "properties": {
      "results": "array",
      "summary": "object",
      "topic_breakdown": "array"
    }
  }
}
```

## Output Schema

```json
{
  "write_status": {
    "type": "enum",
    "values": ["success", "failure"]
  },
  "updated_totals": {
    "total_sessions": "integer",
    "total_questions_attempted": "integer",
    "overall_accuracy": "number",
    "topics_practiced": "integer",
    "last_session_date": "string"
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read/Write | `memory/students/{student_id}/history.json` |
| Read/Write | `memory/students/{student_id}/topic-stats.json` |
| Write | `memory/students/{student_id}/sessions/{session_id}.json` |

## History File Schema

```json
{
  "student_id": "string",
  "total_sessions": "integer",
  "last_session_date": "string",
  "sessions": [
    {
      "session_id": "string",
      "session_date": "string",
      "exam_type": "string",
      "total_questions": "integer",
      "correct": "integer",
      "accuracy": "number",
      "topics_covered": ["array"],
      "duration_seconds": "integer"
    }
  ]
}
```

## Topic Stats File Schema

```json
{
  "topic_name": {
    "total_attempted": "integer",
    "total_correct": "integer",
    "accuracy": "number",
    "last_practiced": "string",
    "difficulty_breakdown": {
      "easy": {"attempted": 0, "correct": 0},
      "medium": {"attempted": 0, "correct": 0},
      "hard": {"attempted": 0, "correct": 0}
    }
  }
}
```

## Constraints

- Must append to history, never overwrite existing sessions
- Must maintain backward compatibility with existing history schema
- Must create session file atomically
- Must update topic-stats aggregates correctly
- Must handle concurrent writes safely (last write wins)

## Error Handling

| Condition | Response |
|-----------|----------|
| Student directory missing | Create directory, then proceed |
| History file corrupted | Return `write_status: "failure"`, do not overwrite |
| Disk write failure | Return `write_status: "failure"` with error details |
