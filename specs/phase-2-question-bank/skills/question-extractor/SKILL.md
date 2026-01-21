---
name: question-extractor
description: Extracts MCQ questions from raw past papers (PDF or HTML) into structured JSON format. Use this skill after past-paper-scraper to convert downloaded papers into question objects. Handles PDF text extraction, option parsing, and answer key detection. Flags questions needing manual review.
---

# Question Extractor

Parses raw exam papers and extracts structured MCQ questions.

## MCP Integration

This skill uses the **filesystem MCP server** for reading raw papers and writing extracted questions.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read raw paper files
- `mcp__filesystem__write_file` - Save extracted questions
- `mcp__filesystem__list_directory` - List papers to process

## Execution Steps

1. **Validate input**
   - raw_paper_path must exist
   - File must be PDF or HTML format

2. **Detect file type and parse**

   For PDF files:
   ```
   - Extract text using PDF parsing
   - Identify question blocks (numbered items)
   - Parse options (A, B, C, D patterns)
   - Locate answer key section
   ```

   For HTML files:
   ```
   - Parse DOM structure
   - Find question containers
   - Extract text and options
   - Locate answer indicators
   ```

3. **Extract question components**

   For each detected question:
   ```
   - question_number: Integer from paper
   - text: Full question text
   - options: {A: "...", B: "...", C: "...", D: "..."}
   - correct_answer: From answer key or marked option
   - extraction_confidence: 0.0 to 1.0
   ```

4. **Flag for review if needed**

   Add review flags for:
   - missing_option: Any option A-D is empty
   - no_correct_answer: Answer not found in key
   - low_ocr_confidence: Confidence < 0.80
   - ambiguous_format: Could not parse cleanly
   - language_unsupported: Non-English content detected

5. **Generate output**
   ```
   Use: mcp__filesystem__write_file
   Path: (based on validation status)
   ```
   - Clean extractions → Ready for validation
   - Flagged extractions → /Needs-Review/{exam}/{date}/

6. **Return extraction results**

## Input Schema

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

## Output Schema

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
          "page": "integer (if PDF)",
          "line": "integer (approx)"
        }
      }
    ]
  },
  "output_files": {
    "clean_questions_path": "string (if any)",
    "flagged_questions_path": "string (if any)"
  }
}
```

## Question Detection Patterns

### PDF Question Patterns
```
Pattern 1: "1. Question text here"
Pattern 2: "Q1: Question text here"
Pattern 3: "Question 1: Question text here"
```

### Option Patterns
```
Pattern 1: "(A) Option text"
Pattern 2: "A) Option text"
Pattern 3: "A. Option text"
Pattern 4: "a) Option text"
```

### Answer Key Patterns
```
Pattern 1: "Answer Key: 1-B, 2-A, 3-C..."
Pattern 2: "Answers: 1.B 2.A 3.C..."
Pattern 3: Table format with Q# and Ans columns
```

## Confidence Scoring

| Factor | Weight | Scoring |
|--------|--------|---------|
| All 4 options present | 0.3 | 0.3 if complete, 0.0 if missing |
| Answer found | 0.3 | 0.3 if found, 0.0 if missing |
| Clean text extraction | 0.2 | Based on character recognition |
| Format consistency | 0.2 | How well it matches patterns |

Total confidence = sum of weighted scores (0.0 to 1.0)

## Error Handling

| Condition | Response |
|-----------|----------|
| PDF unreadable | Flag entire file, log error |
| Question partially parsed | Extract what's possible, flag for review |
| Answer key missing | Extract questions, mark all answers as null |
| Mixed languages | Extract English, flag Urdu sections |
| Image-only content | Flag as "ocr_required", skip extraction |

## Constraints

- Must preserve original question numbering from paper
- Must maintain reference to source file and location
- Must not modify or delete raw paper files
- Must flag rather than guess when uncertain
- Confidence threshold for "clean" extraction: >= 0.80
