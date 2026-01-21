# Contract: question-extractor

**Skill**: question-extractor
**Version**: 1.0
**Date**: 2026-01-19

## Purpose

Extracts MCQ questions from raw past papers (PDF or HTML) into structured JSON format.

## Input Contract

```json
{
  "raw_paper_path": {
    "type": "string",
    "required": true,
    "description": "Path to raw paper file (PDF or HTML)"
  },
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "year": {
    "type": "integer",
    "required": true
  },
  "subject": {
    "type": "string",
    "required": true
  },
  "output_mode": {
    "type": "enum",
    "values": ["all", "clean_only", "flagged_only"],
    "default": "all"
  }
}
```

## Output Contract

```json
{
  "extraction_results": {
    "source_file": "string",
    "exam_type": "string",
    "year": "integer",
    "subject": "string",
    "total_questions_found": "integer",
    "clean_extractions": "integer",
    "flagged_extractions": "integer",
    "questions": [
      {
        "paper_question_number": "integer",
        "text": "string",
        "options": {
          "A": "string",
          "B": "string",
          "C": "string",
          "D": "string"
        },
        "correct_answer": "A | B | C | D | null",
        "extraction_confidence": "number (0-1)",
        "review_flags": ["string"],
        "source_reference": {
          "file": "string",
          "page": "integer",
          "line": "integer"
        }
      }
    ]
  },
  "output_files": {
    "clean_questions_path": "string | null",
    "flagged_questions_path": "string | null"
  }
}
```

## MCP Tools Required

- `mcp__filesystem__read_file` - Read raw paper files
- `mcp__filesystem__write_file` - Save extracted questions
- `mcp__filesystem__list_directory` - List papers to process

## Constraints

- Must preserve original question numbering
- Must maintain reference to source file
- Confidence threshold for "clean": >= 0.80
- Must flag rather than guess when uncertain
