# Skill Contract: performance-tracker

**Version**: 1.0
**Category**: CORE
**MCP Tools**: read_file, write_file

## Purpose

Persists session results and updates cumulative statistics.

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
    "pattern": "{student_id}-{YYYYMMDD}-{HHmmss}"
  },
  "exam_type": {
    "type": "string",
    "required": true,
    "enum": ["SPSC", "PPSC", "KPPSC"]
  },
  "session_type": {
    "type": "string",
    "required": true,
    "enum": ["practice", "diagnostic", "timed"]
  },
  "session_date": {
    "type": "string",
    "required": true,
    "format": "ISO 8601"
  },
  "duration_seconds": {
    "type": "integer",
    "required": true
  },
  "evaluation_results": {
    "type": "object",
    "required": true,
    "description": "Output from answer-evaluator skill"
  },
  "eri_update": {
    "type": "object",
    "required": false,
    "description": "Output from exam-readiness-calculator (optional)"
  }
}
```

## Output Schema

```json
{
  "saved_files": {
    "session_detail": "string (path)",
    "history_updated": "boolean",
    "topic_stats_updated": "boolean"
  },
  "updates": {
    "new_session_count": "integer",
    "new_overall_accuracy": "number",
    "new_eri": "number | null",
    "topics_updated": ["string"]
  },
  "save_status": "success | partial_failure | failed"
}
```

## MCP Operations

### Read Operations
1. `mcp__filesystem__read_file` → `Students/{student_id}/history.json`
2. `mcp__filesystem__read_file` → `Students/{student_id}/topic-stats.json`

### Write Operations
3. `mcp__filesystem__write_file` → `Students/{student_id}/sessions/{session_id}.json`
4. `mcp__filesystem__write_file` → `Students/{student_id}/history.json` (updated)
5. `mcp__filesystem__write_file` → `Students/{student_id}/topic-stats.json` (updated)

## Update Logic

### Session Detail File
Create new file at `sessions/{session_id}.json` with:
- Full question results from evaluation
- Summary statistics
- Topic breakdown
- Duration and timestamps

### History Update
1. Increment `total_sessions`
2. Add questions to `total_questions_attempted`
3. Add correct to `total_correct`
4. Recalculate `overall_accuracy`
5. Update `last_session_date`
6. Append session summary to `sessions` array
7. Update `current_eri` and `eri_band` if provided

### Topic Stats Update
For each topic in results:
1. If topic doesn't exist, create entry
2. Add to `total_attempted` and `total_correct`
3. Recalculate `accuracy`
4. Update `last_practiced`
5. Update difficulty breakdown
6. Calculate `trend` (improving/stable/declining)

## Atomicity

Operations should be atomic where possible:
1. Read all files first
2. Compute all updates in memory
3. Write all files (session first, then history, then stats)
4. If any write fails, report partial failure

## Example

**Input**:
```json
{
  "student_id": "STU001",
  "session_id": "STU001-20260117-143000",
  "exam_type": "PPSC",
  "session_type": "practice",
  "session_date": "2026-01-17T14:30:00Z",
  "duration_seconds": 180,
  "evaluation_results": {
    "summary": {
      "total": 5,
      "correct": 4,
      "accuracy_percentage": 80.0
    },
    "topic_breakdown": [
      {"topic_name": "Constitutional History", "correct": 3, "attempted": 4}
    ]
  },
  "eri_update": {
    "eri_score": 52.0,
    "eri_band": "approaching"
  }
}
```

**Output**:
```json
{
  "saved_files": {
    "session_detail": "Students/STU001/sessions/STU001-20260117-143000.json",
    "history_updated": true,
    "topic_stats_updated": true
  },
  "updates": {
    "new_session_count": 4,
    "new_overall_accuracy": 78.5,
    "new_eri": 52.0,
    "topics_updated": ["Constitutional History"]
  },
  "save_status": "success"
}
```

## Error Handling

| Condition | Response |
|-----------|----------|
| Student directory missing | `save_status: "failed"`, create directory first |
| History file missing | Initialize with first session data |
| Topic stats missing | Initialize with session topics |
| Write permission error | `save_status: "failed"` with error details |
| Partial writes | `save_status: "partial_failure"` with completed files |
