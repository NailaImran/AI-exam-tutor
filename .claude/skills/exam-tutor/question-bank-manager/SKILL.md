---
name: question-bank-manager
description: Manages question bank operations including adding validated questions, generating unique IDs, organizing by exam/subject/topic, updating indexes and statistics, and maintaining cross-exam links for duplicates.
---

# Question Bank Manager

Manages the question bank lifecycle: add, update, deactivate questions, maintain indexes, and update statistics.

## MCP Integration

This skill uses the **filesystem MCP server** for all file operations.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read master-index.json, statistics.json, existing question files
- `mcp__filesystem__write_file` - Write questions, update indexes and statistics
- `mcp__filesystem__list_directory` - List existing question files
- `mcp__filesystem__create_directory` - Create subject/topic directories

## Execution Steps

### Operation: ADD (Primary Operation)

1. **Validate input**
   - Ensure validated_question has all required fields
   - Verify exam_type is valid (SPSC, PPSC, KPPSC)
   - Verify subject and topic are non-empty

2. **Generate unique question ID**
   ```
   Format: {EXAM}-{SUBJECT_CODE}-{NNNNN}
   Example: PPSC-PK-00124

   SUBJECT_CODES:
   - PK: Pakistan Studies
   - GK: General Knowledge
   - CA: Current Affairs
   - EN: English
   ```
   - Read master-index.json to get next ID number
   - Increment counter for exam + subject combination
   - Format with zero-padding (5 digits)

3. **Check for duplicates**
   ```
   Use: mcp__filesystem__read_file
   Path: question-bank/master-index.json
   ```
   - Search master index for existing question ID
   - If ID exists, increment and retry
   - Verify uniqueness before proceeding

4. **Determine file path**
   ```
   Format: question-bank/{Exam}/{Subject}/{topic}.json
   Example: question-bank/PPSC/Pakistan-Studies/constitutional-amendments.json
   ```
   - Create directory if it doesn't exist
   ```
   Use: mcp__filesystem__create_directory
   Path: question-bank/{Exam}/{Subject}/
   ```

5. **Read existing topic file (if exists)**
   ```
   Use: mcp__filesystem__read_file
   Path: question-bank/{Exam}/{Subject}/{topic}.json
   ```
   - Load existing questions array
   - If file doesn't exist, create empty array

6. **Add question to topic file**
   - Append new question to questions array
   - Include metadata: id, created_at, validation_status, source
   ```
   Use: mcp__filesystem__write_file
   Path: question-bank/{Exam}/{Subject}/{topic}.json
   ```

7. **Update master-index.json**
   ```
   Structure:
   {
     "questions": {
       "PPSC-PK-00124": {
         "id": "PPSC-PK-00124",
         "exam": "PPSC",
         "subject": "Pakistan Studies",
         "topic": "Constitutional Amendments",
         "file_path": "question-bank/PPSC/Pakistan-Studies/constitutional-amendments.json",
         "created_at": "2026-01-20T10:30:00Z",
         "difficulty": "medium",
         "source_id": "ppsc-official-2023"
       }
     },
     "next_id_counters": {
       "PPSC-PK": 125,
       "SPSC-GK": 89,
       ...
     }
   }
   ```
   - Add question entry to questions object
   - Increment next_id_counters for exam+subject

8. **Update statistics.json**
   ```
   Structure:
   {
     "total_questions": 1547,
     "by_exam": {
       "PPSC": 523,
       "SPSC": 512,
       "KPPSC": 512
     },
     "by_subject": {
       "Pakistan Studies": 387,
       "General Knowledge": 412,
       ...
     },
     "by_difficulty": {
       "easy": 310,
       "medium": 924,
       "hard": 313
     },
     "by_source": {
       "ppsc-official": 145,
       "spsc-official": 138,
       ...
     },
     "last_updated": "2026-01-20T10:30:00Z"
   }
   ```
   - Increment total_questions
   - Update exam, subject, difficulty, source counters

9. **Check for cross-exam duplicates**
   - If similar question exists in different exam (similarity > 95%)
   - Create bidirectional link in cross-exam-links.json
   ```
   Structure:
   {
     "links": [
       {
         "question_ids": ["PPSC-PK-00124", "SPSC-PK-00089"],
         "similarity_score": 0.97,
         "created_at": "2026-01-20T10:30:00Z"
       }
     ]
   }
   ```

10. **Return confirmation**

### Operation: UPDATE

1. **Validate question_id exists**
2. **Read question from file**
3. **Merge updates (preserve ID, created_at)**
4. **Write updated question**
5. **Update master index if metadata changed**

### Operation: DEACTIVATE

1. **Validate question_id exists**
2. **Mark question as deactivated (never delete)**
   ```json
   {
     "status": "deactivated",
     "deactivated_at": "2026-01-20T10:30:00Z",
     "deactivation_reason": "string"
   }
   ```
3. **Update statistics (decrement active counts)**

### Operation: STATS

1. **Read statistics.json**
2. **Return current statistics**

## Input Schema

```json
{
  "action": {
    "type": "enum",
    "required": true,
    "values": ["ADD", "UPDATE", "DEACTIVATE", "STATS"]
  },
  "validated_question": {
    "type": "object",
    "required_for": ["ADD", "UPDATE"],
    "properties": {
      "question_text": "string",
      "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      },
      "correct_answer": "A | B | C | D",
      "difficulty": "easy | medium | hard",
      "topics": ["array of strings"],
      "source_reference": "object",
      "confidence_score": "float"
    }
  },
  "question_id": {
    "type": "string",
    "required_for": ["UPDATE", "DEACTIVATE"],
    "description": "Existing question ID (e.g., 'PPSC-PK-00124')"
  },
  "exam_type": {
    "type": "string",
    "required_for": ["ADD"],
    "enum": ["SPSC", "PPSC", "KPPSC"]
  },
  "subject": {
    "type": "string",
    "required_for": ["ADD"]
  }
}
```

## Output Schema

```json
{
  "operation_result": {
    "type": "object",
    "properties": {
      "action": "ADD | UPDATE | DEACTIVATE | STATS",
      "status": "success | failed",
      "question_id": "string (for ADD, UPDATE, DEACTIVATE)",
      "file_path": "string (for ADD, UPDATE)",
      "statistics": {
        "total_questions": "integer",
        "by_exam": "object",
        "by_subject": "object",
        "by_difficulty": "object"
      },
      "cross_exam_link_created": "boolean",
      "timestamp": "string (ISO 8601)"
    }
  },
  "execution_status": {
    "type": "enum",
    "values": ["success", "failed"]
  },
  "error_message": {
    "type": "string | null"
  }
}
```

## File Paths

| Operation | Path Template |
|-----------|---------------|
| Read/Write | `question-bank/{Exam}/{Subject}/{topic}.json` |
| Read/Write | `question-bank/master-index.json` |
| Read/Write | `question-bank/statistics.json` |
| Read/Write | `question-bank/cross-exam-links.json` |
| Create Dir | `question-bank/{Exam}/{Subject}/` |

## Subject Code Mapping

| Subject | Code |
|---------|------|
| Pakistan Studies | PK |
| General Knowledge | GK |
| Current Affairs | CA |
| English | EN |
| Islamic Studies | IS |
| Urdu | UR |
| Mathematics | MA |
| Computer Science | CS |

**ID Format**: `{EXAM}-{CODE}-{NNNNN}`
- EXAM: SPSC, PPSC, KPPSC
- CODE: 2-3 letter subject code
- NNNNN: 5-digit zero-padded number (00001-99999)

## Topic File Structure

```json
{
  "topic": "Constitutional Amendments",
  "exam": "PPSC",
  "subject": "Pakistan Studies",
  "questions": [
    {
      "id": "PPSC-PK-00124",
      "question_text": "Which amendment...",
      "options": {
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
      },
      "correct_answer": "C",
      "difficulty": "medium",
      "topics": ["Constitutional Amendments", "1973 Constitution"],
      "source_reference": {
        "file_path": "Raw-Papers/PPSC/2023/pakistan-studies.pdf",
        "page_number": 5,
        "line_range": "45-52",
        "source_id": "ppsc-official-2023",
        "year": 2023
      },
      "confidence_score": 1.0,
      "created_at": "2026-01-20T10:30:00Z",
      "validation_status": "validated",
      "status": "active"
    }
  ],
  "last_updated": "2026-01-20T10:30:00Z",
  "total_questions": 15
}
```

## Deduplication Logic

Before adding a question:
1. Read master-index.json
2. Calculate text similarity with all existing questions
3. If similarity > 95% with any existing question:
   - If same exam → Reject as duplicate, do not add
   - If different exam → Create cross-exam link, add question
4. If similarity 90-95% → Flag as possible duplicate, add with warning

## Cross-Exam Link Creation

When same question appears in multiple exams:
```json
{
  "links": [
    {
      "link_id": "link-001",
      "question_ids": [
        "PPSC-PK-00124",
        "SPSC-PK-00089",
        "KPPSC-PK-00067"
      ],
      "similarity_score": 0.98,
      "note": "Same question across all 3 exams, year 2023",
      "created_at": "2026-01-20T10:30:00Z"
    }
  ]
}
```

**Bidirectional**: All linked questions reference the same link_id in their metadata.

## Statistics Calculation

Update statistics.json atomically:
1. Read current statistics
2. Apply increments based on operation
3. Write updated statistics
4. Update last_updated timestamp

**Accuracy Requirement**: Statistics must be within 1% of actual count (verified by periodic audit).

## Constraints

- Must generate unique IDs (no collisions)
- Must update all indexes atomically (master-index, statistics, cross-exam-links)
- Must never delete questions (deactivate instead)
- Must maintain referential integrity (IDs in index match IDs in topic files)
- Must handle concurrent access safely (if multiple processes adding questions)
- Must validate all writes (no corrupt JSON files)

## Error Handling

| Condition | Response |
|-----------|----------|
| Invalid action | Return error "INVALID_ACTION" |
| Question ID already exists | Increment and retry (max 10 attempts) |
| File write fails | Rollback all changes, return error |
| Master index corrupted | Backup corrupted file, rebuild from topic files |
| Statistics mismatch | Log warning, recalculate from ground truth |

## Atomic Transaction Pattern

To ensure data consistency:
1. **Prepare**: Validate inputs, generate IDs
2. **Write Question**: Add to topic file
3. **Update Master Index**: Add entry
4. **Update Statistics**: Increment counters
5. **Update Cross-Links** (if needed): Add link entry
6. **Commit**: Return success

If any step fails after "Write Question":
- Log error with context
- Attempt rollback (remove question from topic file)
- Mark transaction as failed
- Return error to caller

## Success Criteria

- 100% unique ID generation (no collisions)
- All questions added to correct file paths
- Master index 100% accurate (all question IDs present)
- Statistics within 1% of actual counts
- Cross-exam links correctly bidirectional
- No corrupt JSON files written
- Execution completes within 200ms per operation
