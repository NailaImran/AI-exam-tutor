---
name: question-extractor
description: Extracts MCQ questions from PDF and HTML past papers into structured JSON format. Detects question text, options A-D, correct answers, and assigns confidence scores. Flags low-confidence extractions for manual review.
---

# Question Extractor

Parses raw PDF/HTML past papers and extracts Multiple Choice Questions (MCQs) into structured JSON format.

## MCP Integration

This skill uses the **filesystem MCP server** for all file operations.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read raw paper files (PDF text or HTML)
- `mcp__filesystem__write_file` - Write extracted questions to temporary JSON files
- `mcp__filesystem__list_directory` - List papers in Raw-Papers/

## Execution Steps

1. **Validate input parameters**
   - raw_paper_path must exist in Raw-Papers/
   - exam_type must be one of: SPSC, PPSC, KPPSC
   - year and subject must be provided

2. **Read raw paper content**
   ```
   Use: mcp__filesystem__read_file
   Path: {raw_paper_path}
   ```
   - Detect file type (PDF or HTML) from extension
   - Extract text content

3. **Parse PDF files**
   - Extract plain text from PDF (using PDF text extraction)
   - Split into lines and detect MCQ patterns
   - Pattern: Question number → Question text → Options (A), (B), (C), (D) → Answer marker

4. **Parse HTML files**
   - Parse HTML structure
   - Find question blocks (typically `<div class="question">` or `<li>`)
   - Extract question text from heading elements
   - Extract options from list items or option divs
   - Extract answer from answer key section

5. **Detect MCQ structure**
   - Identify question boundaries (numbering: 1., 2., Q1, etc.)
   - Extract question text (everything before first option)
   - Extract options A, B, C, D (look for markers: A., (A), A), A:)
   - Extract correct answer indicator (e.g., "Answer: C", "Correct: B", marked option)

6. **Assign confidence score (0.0-1.0)**
   - 1.0: All 4 options found, correct answer clearly marked, clean formatting
   - 0.9: All 4 options found, answer inferred from context
   - 0.8: All 4 options found, but answer unclear or missing
   - 0.7: 3 options found, answer present
   - <0.7: Incomplete or malformed question

7. **Flag low-confidence questions (<0.80)**
   ```
   Use: mcp__filesystem__write_file
   Path: Needs-Review/{exam}/{date}/{subject}-{question_num}.json
   ```

8. **Structure extracted questions**
   - Create JSON array with all extracted questions
   - Include source metadata (file_path, page_number, line_number)
   - Include confidence score for each question

9. **Return extraction result**

## Input Schema

```json
{
  "raw_paper_path": {
    "type": "string",
    "required": true,
    "description": "Path to raw paper file in Raw-Papers/"
  },
  "exam_type": {
    "type": "string",
    "required": true,
    "enum": ["SPSC", "PPSC", "KPPSC"]
  },
  "year": {
    "type": "integer",
    "required": true,
    "description": "Exam year (e.g., 2023)"
  },
  "subject": {
    "type": "string",
    "required": true,
    "description": "Subject name (e.g., 'Pakistan Studies')"
  }
}
```

## Output Schema

```json
{
  "extraction_result": {
    "type": "object",
    "properties": {
      "source_file": "string",
      "exam": "string",
      "year": "integer",
      "subject": "string",
      "total_questions_found": "integer",
      "high_confidence_count": "integer (≥0.80)",
      "low_confidence_count": "integer (<0.80)",
      "extracted_questions": [
        {
          "question_number": "integer",
          "question_text": "string",
          "options": {
            "A": "string",
            "B": "string",
            "C": "string",
            "D": "string"
          },
          "correct_answer": "A | B | C | D | null",
          "confidence_score": "float (0.0-1.0)",
          "source_reference": {
            "file_path": "string",
            "page_number": "integer (for PDF) | null",
            "line_range": "string (e.g., '45-52')"
          },
          "extraction_notes": "string (e.g., 'Answer inferred from context', 'Option D incomplete')"
        }
      ],
      "flagged_questions": [
        {
          "question_number": "integer",
          "flagged_path": "string (path in Needs-Review/)",
          "confidence_score": "float",
          "reason": "string"
        }
      ]
    }
  },
  "execution_status": {
    "type": "enum",
    "values": ["success", "partial", "failed"]
  }
}
```

## File Paths

| Operation | Path Template |
|-----------|---------------|
| Read | `Raw-Papers/{exam}/{year}/{subject}.{pdf\|html}` |
| Write (flagged) | `Needs-Review/{exam}/{YYYY-MM-DD}/{subject}-Q{num}.json` |

## Extraction Patterns

### PDF Extraction
```
Pattern 1: Standard Numbered Format
-----------------------------------
1. What is the capital of Pakistan?
   A. Karachi
   B. Lahore
   C. Islamabad
   D. Peshawar
   Answer: C

Pattern 2: Parenthetical Options
----------------------------------
Q2. When was Pakistan founded?
   (A) 1945
   (B) 1947
   (C) 1950
   (D) 1952
   Correct Answer: (B)

Pattern 3: Inline Options
-------------------------
3. The national language of Pakistan is: A) Urdu B) English C) Punjabi D) Sindhi
   Answer: A
```

### HTML Extraction
```html
<div class="question">
  <h4>1. What is the capital of Pakistan?</h4>
  <ul class="options">
    <li class="option-a">Karachi</li>
    <li class="option-b">Lahore</li>
    <li class="option-c correct">Islamabad</li>
    <li class="option-d">Peshawar</li>
  </ul>
</div>
```

## Confidence Scoring Rules

| Score | Criteria |
|-------|----------|
| 1.0 | All 4 options present, correct answer explicitly marked, clean formatting |
| 0.9 | All 4 options present, answer inferred from formatting (bold, color) |
| 0.8 | All 4 options present, answer unclear or missing |
| 0.7 | 3 options found, answer present |
| 0.6 | 3 options found, answer missing |
| 0.5 | 2 options found |
| <0.5 | Malformed or incomplete |

**Threshold**: Flag for manual review if confidence < 0.80

## Constraints

- Must extract at least 80% of questions from well-formatted papers
- Must flag all low-confidence questions (<0.80)
- Must preserve exact question and option text (no paraphrasing)
- Must not guess or fabricate answers
- Must handle variations in formatting (numbering, option markers)
- Must handle scanned PDFs (OCR text) with potential errors

## Error Handling

| Condition | Response |
|-----------|----------|
| File not found | Return execution_status: "failed" |
| Unreadable PDF | Log error, attempt text extraction anyway |
| Malformed HTML | Use robust parsing, extract what's possible |
| No questions detected | Return empty array, log warning |
| Ambiguous answer | Set correct_answer: null, reduce confidence score |

## OCR Error Handling

Common OCR errors in scanned PDFs:
- "0" (zero) misread as "O" (letter)
- "1" (one) misread as "l" (lowercase L)
- "A" misread as "4"

**Mitigation**:
- Detect suspicious patterns
- Flag questions with OCR artifacts
- Reduce confidence score for questionable text

## Flagging Reasons

| Code | Description |
|------|-------------|
| MISSING_OPTION | Less than 4 options detected |
| NO_ANSWER | Correct answer not found |
| LOW_OCR_CONFIDENCE | Text quality poor (scanned PDF) |
| AMBIGUOUS_ANSWER | Multiple answers marked |
| INCOMPLETE_TEXT | Question text truncated |

## Success Criteria

- Extract 80%+ of questions from well-formatted papers
- Accurately detect all 4 options for 90%+ of questions
- Correctly identify answer markers for 85%+ of questions
- Flag all low-confidence extractions (<0.80)
- Execution completes within 30 seconds per paper
