# Contract: question-bank-manager

**Skill**: question-bank-manager
**Version**: 1.0
**Date**: 2026-01-19

## Purpose

Manages the question bank by adding validated questions, updating entries, tracking statistics, and maintaining cross-exam links.

## Input Contract

```json
{
  "action": {
    "type": "enum",
    "values": ["ADD", "UPDATE", "DEACTIVATE", "STATS"],
    "required": true
  },
  "validated_question": {
    "type": "object",
    "required_if": "action == ADD",
    "description": "Output from question-validator"
  },
  "question_id": {
    "type": "string",
    "required_if": "action in [UPDATE, DEACTIVATE]"
  },
  "update_fields": {
    "type": "object",
    "required_if": "action == UPDATE"
  },
  "stats_filter": {
    "type": "object",
    "required_if": "action == STATS",
    "properties": {
      "exam_type": "SPSC | PPSC | KPPSC | all",
      "subject": "string | all",
      "include_inactive": "boolean"
    }
  }
}
```

## Output Contract (ADD)

```json
{
  "status": "success | failure",
  "question_id": "string",
  "file_path": "string",
  "cross_exam_links": ["string"],
  "updated_statistics": {
    "exam_total": "integer",
    "subject_total": "integer",
    "topic_total": "integer"
  }
}
```

## Output Contract (UPDATE)

```json
{
  "status": "success | failure",
  "question_id": "string",
  "updated_fields": ["string"],
  "error_message": "string | null"
}
```

## Output Contract (DEACTIVATE)

```json
{
  "status": "success | failure",
  "question_id": "string",
  "was_active": "boolean",
  "error_message": "string | null"
}
```

## Output Contract (STATS)

```json
{
  "statistics": {
    "total_questions": "integer",
    "active_questions": "integer",
    "by_exam": {},
    "by_difficulty": {},
    "by_source_type": {},
    "coverage_gaps": [],
    "cross_exam_links_count": "integer",
    "last_updated": "ISO 8601"
  }
}
```

## MCP Tools Required

- `mcp__filesystem__read_file` - Read existing question files and indexes
- `mcp__filesystem__write_file` - Write question files and indexes
- `mcp__filesystem__list_directory` - List question bank contents
- `mcp__filesystem__create_directory` - Create new topic directories

## Constraints

- Must never hard-delete questions (deactivate only)
- Must maintain backward compatibility with Phase 1 format
- Must update statistics atomically with question changes
- Question ID format: `{EXAM}-{SUBJECT_CODE}-{NNNNN}`
