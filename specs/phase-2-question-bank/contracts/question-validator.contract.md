# Contract: question-validator

**Skill**: question-validator
**Version**: 1.0
**Date**: 2026-01-19

## Purpose

Validates extracted questions for completeness, correctness, and uniqueness before adding to question bank.

## Input Contract

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
    "default": false
  }
}
```

## Output Contract

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
      "explanation": "string",
      "topic": "string",
      "difficulty": "easy | medium | hard",
      "source": "object",
      "metadata": {
        "validation_status": "verified | unverified_answer | needs_review",
        "extraction_confidence": "number",
        "duplicate_of": "string | null"
      }
    },
    "issues": [
      {
        "code": "string",
        "severity": "critical | warning | info",
        "message": "string",
        "field": "string"
      }
    ]
  }
}
```

## MCP Tools Required

- `mcp__filesystem__read_file` - Read existing questions for duplicate check
- `mcp__filesystem__write_file` - Save validation results
- `mcp__filesystem__list_directory` - List question bank files

## Constraints

- Must not modify original extracted question
- Must check both same-exam and cross-exam duplicates
- Duplicate threshold: 90% text similarity
