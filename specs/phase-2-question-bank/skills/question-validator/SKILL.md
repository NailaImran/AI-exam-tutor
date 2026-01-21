---
name: question-validator
description: Validates extracted questions for completeness, correctness, and uniqueness before adding to the question bank. Use this skill to ensure question quality. Checks for missing options, valid answers, duplicates, and auto-assigns difficulty and topics. Returns validated questions or rejection reasons.
---

# Question Validator

Ensures extracted questions meet quality standards before question bank import.

## MCP Integration

This skill uses the **filesystem MCP server** for reading question bank and writing validation results.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read existing questions for duplicate check
- `mcp__filesystem__write_file` - Save validation results
- `mcp__filesystem__list_directory` - List question bank files

## Execution Steps

1. **Validate input structure**
   - extracted_question must have required fields
   - exam_type must be valid

2. **Check completeness**
   ```
   Verify:
   - text is non-empty and > 10 characters
   - options.A, B, C, D all non-empty
   - correct_answer is one of A, B, C, D
   ```

3. **Check for duplicates**
   ```
   Use: mcp__filesystem__read_file
   Path: Question-Bank-Index/master-index.json

   Compare question text against existing:
   - Calculate similarity score
   - If similarity > 90%, flag as duplicate
   - Check cross-exam duplicates separately
   ```

4. **Auto-assign difficulty**
   ```
   If historical data available:
     difficulty = based on accuracy rate
       > 80% correct → "easy"
       50-80% correct → "medium"
       < 50% correct → "hard"
   Else:
     difficulty = "medium" (default)
   ```

5. **Auto-suggest topic**
   ```
   Use: mcp__filesystem__read_file
   Path: Syllabus/{exam_type}/syllabus-structure.json

   Match question keywords against topic list
   Assign highest-confidence topic match
   ```

6. **Generate validation result**
   - VALID: All checks pass → ready for import
   - REJECTED: Critical issues → provide reasons
   - NEEDS_REVIEW: Non-critical issues → flag for human

7. **Return structured output**

## Input Schema

```json
{
  "extracted_question": {
    "type": "object",
    "required": true,
    "properties": {
      "text": "string",
      "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      },
      "correct_answer": "A | B | C | D | null",
      "extraction_confidence": "number",
      "source_reference": "object"
    }
  },
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "subject": {
    "type": "string",
    "required": true
  },
  "year": {
    "type": "integer",
    "required": true
  },
  "skip_duplicate_check": {
    "type": "boolean",
    "default": false,
    "description": "Skip duplicate check (use for re-validation)"
  }
}
```

## Output Schema

```json
{
  "validation_result": {
    "status": "VALID | REJECTED | NEEDS_REVIEW",
    "validated_question": {
      "text": "string",
      "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      },
      "correct_answer": "A | B | C | D",
      "explanation": "string (if available)",
      "topic": "string (auto-assigned)",
      "difficulty": "easy | medium | hard",
      "source": {
        "type": "official | verified | unverified",
        "exam": "string",
        "year": "integer",
        "url": "string"
      },
      "metadata": {
        "validation_status": "verified | unverified_answer | needs_review",
        "extraction_confidence": "number",
        "duplicate_of": "string | null (question ID if duplicate)"
      }
    },
    "issues": [
      {
        "code": "string",
        "severity": "critical | warning | info",
        "message": "string",
        "field": "string (which field has issue)"
      }
    ]
  }
}
```

## Validation Rules

### Critical Issues (REJECTED)

| Code | Rule | Message |
|------|------|---------|
| EMPTY_TEXT | Question text < 10 chars | "Question text is empty or too short" |
| MISSING_OPTION | Any option A-D is empty | "Missing option {X}" |
| INVALID_ANSWER | correct_answer not A-D | "Invalid correct answer value" |
| EXACT_DUPLICATE | 100% text match exists | "Exact duplicate of {question_id}" |

### Warning Issues (NEEDS_REVIEW)

| Code | Rule | Message |
|------|------|---------|
| NEAR_DUPLICATE | 90-99% similarity match | "Possible duplicate of {question_id}" |
| NO_ANSWER_KEY | correct_answer is null | "No correct answer found" |
| LOW_CONFIDENCE | extraction_confidence < 0.8 | "Low extraction confidence" |
| TOPIC_UNCERTAIN | No clear topic match | "Could not auto-assign topic" |

### Info Issues (logged but VALID)

| Code | Rule | Message |
|------|------|---------|
| DIFFICULTY_DEFAULT | No historical data | "Using default difficulty: medium" |
| CROSS_EXAM_LINK | Same Q in another exam | "Linked to {exam}-{id}" |

## Duplicate Detection Algorithm

```
1. Normalize both texts:
   - Lowercase
   - Remove punctuation
   - Remove extra whitespace

2. Calculate similarity:
   - Token overlap percentage
   - Levenshtein distance ratio

3. Combine scores:
   similarity = (token_overlap * 0.6) + (levenshtein_ratio * 0.4)

4. Thresholds:
   - >= 1.0: Exact duplicate (REJECTED)
   - >= 0.9: Near duplicate (NEEDS_REVIEW)
   - < 0.9: Not duplicate (continue)
```

## Topic Matching

```
1. Extract keywords from question text
2. For each syllabus topic:
   - Count keyword matches
   - Weight by keyword importance
3. Assign topic with highest match score
4. If no topic scores > 0.3, flag as TOPIC_UNCERTAIN
```

## Constraints

- Must not modify original extracted question
- Must preserve source reference chain
- Must check both same-exam and cross-exam duplicates
- Must provide specific rejection reasons
- Must not approve questions with null correct_answer for student practice
