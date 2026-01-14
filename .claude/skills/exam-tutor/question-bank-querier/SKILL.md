---
name: question-bank-querier
description: Queries the question bank and returns questions matching specified criteria (exam type, subject, topic, difficulty). Use this skill when generating tests, assessments, or retrieving practice questions. Does not generate questions—only retrieves existing ones from the file-based question bank.
---

# Question Bank Querier

Retrieves questions from the structured question bank based on filtering criteria.

## MCP Integration

This skill uses the **filesystem MCP server** for question retrieval.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read question JSON files
- `mcp__filesystem__list_directory` - List available subjects and question files
- `mcp__filesystem__search_files` - Search for questions by pattern (if available)

## Execution Steps

1. **Validate inputs**
   - exam_type must be one of: SPSC, PPSC, KPPSC
   - difficulty must be one of: easy, medium, hard, mixed
   - count must be positive integer

2. **Build question bank path**
   ```
   Base path: question-bank/{exam_type}/{subject}/
   ```

3. **List available question files**
   ```
   Use: mcp__filesystem__list_directory
   Path: question-bank/{exam_type}/{subject}
   ```

4. **Load and filter questions**
   ```
   Use: mcp__filesystem__read_file
   For each question file in directory
   ```
   - Filter by topics array (if provided)
   - Filter by difficulty (unless "mixed")
   - Exclude questions in exclude_ids array

5. **Sample questions**
   - Randomly sample up to `count` questions
   - Ensure even distribution across topics when possible

6. **Return structured output**

## Input Schema

```json
{
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "subject": {
    "type": "string",
    "required": true,
    "description": "Subject area (e.g., 'Pakistan Studies', 'General Knowledge')"
  },
  "topics": {
    "type": "array",
    "items": "string",
    "required": false,
    "description": "List of topic tags to filter by"
  },
  "difficulty": {
    "type": "enum",
    "values": ["easy", "medium", "hard", "mixed"],
    "default": "mixed"
  },
  "count": {
    "type": "integer",
    "minimum": 1,
    "required": true
  },
  "exclude_ids": {
    "type": "array",
    "items": "string",
    "default": [],
    "description": "Question IDs to exclude (previously seen)"
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
      "difficulty": "easy | medium | hard",
      "explanation": "string (optional)"
    }
  },
  "retrieval_count": {
    "type": "integer",
    "description": "Actual number of questions retrieved"
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `question-bank/{exam_type}/{subject}/*.json` |
| Read | `question-bank/metadata/topic-index.json` |

## Question File Structure

Each question file should follow this format:
```json
{
  "questions": [
    {
      "id": "SPSC-PK-001",
      "text": "When was Pakistan founded?",
      "options": {
        "A": "1945",
        "B": "1947",
        "C": "1948",
        "D": "1950"
      },
      "correct_answer": "B",
      "topic": "Independence Movement",
      "difficulty": "easy",
      "explanation": "Pakistan gained independence on August 14, 1947."
    }
  ]
}
```

## Constraints

- Must never return more than `count` questions
- Must respect `exclude_ids` strictly
- Must return empty array if no matches (never error)
- Questions must include `correct_answer` field
- Must not modify question bank files

## Difficulty Distribution for "mixed"

When difficulty is "mixed", sample with distribution:
- 30% easy
- 50% medium
- 20% hard
