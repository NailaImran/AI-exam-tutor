# Skill Contract: question-bank-querier

**Version**: 1.0
**Category**: CORE
**MCP Tools**: read_file, list_directory

## Purpose

Retrieves questions from the question bank based on specified criteria.

## Input Schema

```json
{
  "exam_type": {
    "type": "string",
    "required": true,
    "enum": ["SPSC", "PPSC", "KPPSC"],
    "description": "Target exam type"
  },
  "subject": {
    "type": "string",
    "required": true,
    "description": "Subject name (e.g., 'PakistanStudies')"
  },
  "topic": {
    "type": "string",
    "required": false,
    "description": "Specific topic within subject (optional)"
  },
  "difficulty": {
    "type": "string",
    "required": false,
    "enum": ["easy", "medium", "hard", "mixed"],
    "default": "mixed",
    "description": "Difficulty filter"
  },
  "count": {
    "type": "integer",
    "required": true,
    "minimum": 1,
    "maximum": 100,
    "description": "Number of questions to retrieve"
  },
  "exclude_ids": {
    "type": "array",
    "required": false,
    "items": "string",
    "description": "Question IDs to exclude (already seen)"
  }
}
```

## Output Schema

```json
{
  "questions": {
    "type": "array",
    "items": {
      "id": "string",
      "text": "string",
      "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      },
      "correct_answer": "A | B | C | D",
      "topic": "string",
      "difficulty": "easy | medium | hard"
    }
  },
  "metadata": {
    "requested": "integer",
    "returned": "integer",
    "available": "integer",
    "topics_included": ["string"],
    "difficulty_distribution": {
      "easy": "integer",
      "medium": "integer",
      "hard": "integer"
    }
  },
  "query_status": "success | partial | no_questions"
}
```

## MCP Operations

1. `mcp__filesystem__list_directory` → List `Question-Bank/{exam_type}/{subject}/`
2. `mcp__filesystem__read_file` → Read question files matching topic filter
3. Filter, shuffle, and select questions based on criteria

## Selection Logic

1. If topic specified: Read only `{topic}.json`
2. If topic not specified: Read all topic files in subject
3. Apply difficulty filter (or mix if "mixed")
4. Exclude questions in `exclude_ids`
5. Shuffle and return up to `count` questions

## Error Handling

| Condition | Response |
|-----------|----------|
| No questions found | `query_status: "no_questions"` |
| Fewer than requested | `query_status: "partial"`, return available |
| Invalid exam_type | Error before MCP calls |
| Subject directory missing | `query_status: "no_questions"` |

## Example

**Input**:
```json
{
  "exam_type": "PPSC",
  "subject": "PakistanStudies",
  "topic": "Constitutional History",
  "difficulty": "medium",
  "count": 5
}
```

**Output**:
```json
{
  "questions": [
    {
      "id": "PPSC-PK-00005",
      "text": "The 18th Amendment was passed in which year?",
      "options": {
        "A": "2008",
        "B": "2010",
        "C": "2012",
        "D": "2015"
      },
      "correct_answer": "B",
      "topic": "Constitutional History",
      "difficulty": "medium"
    }
  ],
  "metadata": {
    "requested": 5,
    "returned": 5,
    "available": 12,
    "topics_included": ["Constitutional History"],
    "difficulty_distribution": { "medium": 5 }
  },
  "query_status": "success"
}
```
