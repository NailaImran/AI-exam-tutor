---
name: question-bank-manager
description: Manages the question bank by adding validated questions, updating existing entries, tracking statistics, and maintaining cross-exam links. Use this skill after question-validator to import questions into the question bank. Generates unique IDs, organizes by exam/subject/topic, and maintains the master index.
---

# Question Bank Manager

Organizes and maintains the expanded question bank with full metadata tracking.

## MCP Integration

This skill uses the **filesystem MCP server** for all question bank operations.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read existing question files and indexes
- `mcp__filesystem__write_file` - Write question files and indexes
- `mcp__filesystem__list_directory` - List question bank contents
- `mcp__filesystem__create_directory` - Create new topic directories

## Execution Steps

### For ADD action:

1. **Validate input**
   - validated_question must have status "VALID"
   - All required fields must be present

2. **Generate unique ID**
   ```
   Use: mcp__filesystem__read_file
   Path: Question-Bank-Index/master-index.json

   Find highest ID for exam-subject combo
   New ID = {EXAM}-{SUBJECT_CODE}-{NNNNN+1}
   ```

3. **Check/create topic file**
   ```
   Path: Question-Bank/{exam}/{subject}/{topic}.json

   If not exists:
     Use: mcp__filesystem__create_directory
     Then create empty topic file
   ```

4. **Add question to topic file**
   ```
   Use: mcp__filesystem__read_file
   Path: Question-Bank/{exam}/{subject}/{topic}.json

   Append new question to questions array

   Use: mcp__filesystem__write_file
   Path: Question-Bank/{exam}/{subject}/{topic}.json
   ```

5. **Update master index**
   ```
   Use: mcp__filesystem__read_file
   Path: Question-Bank-Index/master-index.json

   Add entry: {
     id: new_id,
     exam: exam_type,
     subject: subject,
     topic: topic,
     difficulty: difficulty,
     file_path: topic_file_path
   }

   Use: mcp__filesystem__write_file
   Path: Question-Bank-Index/master-index.json
   ```

6. **Handle cross-exam links**
   ```
   If question has duplicate_of reference:
     Use: mcp__filesystem__read_file
     Path: Question-Bank-Index/cross-exam-links.json

     Add bidirectional link

     Use: mcp__filesystem__write_file
   ```

7. **Update statistics**
   ```
   Use: mcp__filesystem__read_file
   Path: Question-Bank-Index/statistics.json

   Increment counts for exam, subject, topic

   Use: mcp__filesystem__write_file
   ```

8. **Return confirmation**

### For UPDATE action:

1. **Locate existing question by ID**
2. **Validate update fields**
3. **Apply updates to topic file**
4. **Update master index if metadata changed**
5. **Return confirmation**

### For DEACTIVATE action:

1. **Locate existing question by ID**
2. **Set metadata.active = false**
3. **Keep in topic file (no hard delete)**
4. **Update statistics (decrement active count)**
5. **Return confirmation**

### For STATS action:

1. **Read statistics.json**
2. **Calculate derived metrics**
3. **Return structured statistics**

## Input Schema

```json
{
  "action": {
    "type": "enum",
    "values": ["ADD", "UPDATE", "DEACTIVATE", "STATS"],
    "required": true
  },
  "validated_question": {
    "type": "object",
    "required": "if action is ADD",
    "description": "Output from question-validator"
  },
  "question_id": {
    "type": "string",
    "required": "if action is UPDATE or DEACTIVATE",
    "description": "ID of question to modify"
  },
  "update_fields": {
    "type": "object",
    "required": "if action is UPDATE",
    "description": "Fields to update"
  },
  "stats_filter": {
    "type": "object",
    "properties": {
      "exam_type": "SPSC | PPSC | KPPSC | all",
      "subject": "string | all",
      "include_inactive": "boolean"
    },
    "required": "if action is STATS"
  }
}
```

## Output Schema

### For ADD action:
```json
{
  "status": "success | failure",
  "question_id": "string (newly assigned ID)",
  "file_path": "string (where question was stored)",
  "cross_exam_links": ["string (linked question IDs)"],
  "updated_statistics": {
    "exam_total": "integer",
    "subject_total": "integer",
    "topic_total": "integer"
  }
}
```

### For UPDATE action:
```json
{
  "status": "success | failure",
  "question_id": "string",
  "updated_fields": ["string (list of changed fields)"],
  "error_message": "string (if failure)"
}
```

### For DEACTIVATE action:
```json
{
  "status": "success | failure",
  "question_id": "string",
  "was_active": "boolean",
  "error_message": "string (if failure)"
}
```

### For STATS action:
```json
{
  "statistics": {
    "total_questions": "integer",
    "active_questions": "integer",
    "by_exam": {
      "SPSC": {"total": 0, "by_subject": {}},
      "PPSC": {"total": 0, "by_subject": {}},
      "KPPSC": {"total": 0, "by_subject": {}}
    },
    "by_difficulty": {
      "easy": "integer",
      "medium": "integer",
      "hard": "integer"
    },
    "by_source_type": {
      "official": "integer",
      "verified": "integer",
      "unverified": "integer"
    },
    "coverage_gaps": [
      {
        "exam": "string",
        "subject": "string",
        "topic": "string",
        "question_count": "integer",
        "status": "low | adequate | good"
      }
    ],
    "cross_exam_links_count": "integer",
    "last_updated": "ISO 8601 timestamp"
  }
}
```

## Question ID Format

```
{EXAM}-{SUBJECT_CODE}-{NNNNN}

EXAM: SPSC | PPSC | KPPSC
SUBJECT_CODE:
  - PK = Pakistan Studies
  - GK = General Knowledge
  - CA = Current Affairs
  - EN = English
  - MA = Math
NNNNN: 5-digit sequential number, zero-padded

Examples:
  PPSC-PK-00001 (PPSC Pakistan Studies, question 1)
  SPSC-GK-00156 (SPSC General Knowledge, question 156)
  KPPSC-CA-00042 (KPPSC Current Affairs, question 42)
```

## Coverage Gap Thresholds

| Question Count | Status |
|----------------|--------|
| < 10 | low (flag for expansion) |
| 10-30 | adequate |
| > 30 | good |

## File Structures

### master-index.json
```json
{
  "version": "2.0",
  "last_updated": "ISO 8601",
  "total_questions": 1500,
  "questions": [
    {
      "id": "PPSC-PK-00001",
      "exam": "PPSC",
      "subject": "Pakistan-Studies",
      "topic": "constitutional-history",
      "difficulty": "medium",
      "file_path": "Question-Bank/PPSC/Pakistan-Studies/constitutional-history.json",
      "active": true
    }
  ]
}
```

### cross-exam-links.json
```json
{
  "version": "1.0",
  "last_updated": "ISO 8601",
  "links": [
    {
      "questions": ["PPSC-PK-00001", "SPSC-PK-00089", "KPPSC-PK-00112"],
      "link_type": "cross_exam_duplicate",
      "created": "ISO 8601"
    }
  ]
}
```

### statistics.json
```json
{
  "version": "1.0",
  "last_updated": "ISO 8601",
  "totals": {
    "all": 1500,
    "active": 1485,
    "inactive": 15
  },
  "by_exam": {
    "SPSC": 500,
    "PPSC": 500,
    "KPPSC": 500
  },
  "by_subject": {
    "Pakistan-Studies": 600,
    "General-Knowledge": 400
  },
  "by_topic": {},
  "by_difficulty": {},
  "by_source_type": {},
  "by_year": {}
}
```

## Constraints

- Must never hard-delete questions (deactivate only)
- Must maintain backward compatibility with Phase 1 question format
- Must update statistics atomically with question changes
- Must preserve full audit trail in question metadata
- Must generate sequential IDs without gaps within exam-subject
