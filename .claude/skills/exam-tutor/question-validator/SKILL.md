---
name: question-validator
description: Validates extracted questions for completeness, uniqueness, and quality. Checks for all 4 options, valid answers, detects duplicates, and auto-tags difficulty and topics. Rejects incomplete questions with specific reasons.
---

# Question Validator

Validates extracted MCQ questions for completeness, correctness, and uniqueness before adding to question bank.

## MCP Integration

This skill uses the **filesystem MCP server** for all file operations.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read master-index.json, syllabus structure
- `mcp__filesystem__write_file` - Write flagged questions to Needs-Review/
- `mcp__filesystem__list_directory` - List existing questions for duplicate check

## Execution Steps

1. **Validate input question structure**
   - Ensure all required fields present
   - Verify question_text is non-empty
   - Check options object has keys A, B, C, D

2. **Completeness check: 4 options**
   - Verify options.A exists and is non-empty
   - Verify options.B exists and is non-empty
   - Verify options.C exists and is non-empty
   - Verify options.D exists and is non-empty
   - **Reject** if any option missing → Reason: "MISSING_OPTION_{X}"

3. **Answer validation**
   - Verify correct_answer is one of: "A", "B", "C", "D"
   - **Reject** if correct_answer is null or invalid → Reason: "NO_CORRECT_ANSWER"
   - **Reject** if correct_answer references non-existent option → Reason: "INVALID_ANSWER_REFERENCE"

4. **Duplicate detection**
   ```
   Use: mcp__filesystem__read_file
   Path: question-bank/master-index.json
   ```
   - Load all existing question IDs and text hashes
   - Calculate similarity score for question_text (Levenshtein distance or simple token overlap)
   - **Reject** if similarity > 90% → Reason: "DUPLICATE_QUESTION"
   - **Flag** if similarity 80-90% → Reason: "POSSIBLE_DUPLICATE"

5. **Auto-tag difficulty level**
   - Scan question_text and options for difficulty keywords
   - **Easy**: "is", "what", "who", "when", basic facts
   - **Medium**: "how", "why", comparative questions
   - **Hard**: "analyze", "evaluate", multi-step reasoning, calculations
   - **Default**: "medium" if unable to determine

6. **Auto-tag topics**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/{exam}/syllabus-structure.json
   ```
   - Load syllabus topic tree
   - Match question_text keywords against topic names
   - Assign primary topic (best match)
   - Assign secondary topics if applicable
   - **Default**: Use subject name if no topic match found

7. **Quality checks**
   - Check question_text length (minimum 10 characters)
   - Check option text length (minimum 1 character each)
   - Check for malformed text (excessive special characters, encoding issues)
   - **Flag** if quality issues detected → Reason: "QUALITY_ISSUE"

8. **Return validation result**

## Input Schema

```json
{
  "extracted_question": {
    "type": "object",
    "required": true,
    "properties": {
      "question_text": "string",
      "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      },
      "correct_answer": "A | B | C | D | null",
      "source_reference": "object",
      "confidence_score": "float"
    }
  },
  "exam_type": {
    "type": "string",
    "required": true,
    "enum": ["SPSC", "PPSC", "KPPSC"]
  },
  "subject": {
    "type": "string",
    "required": true
  },
  "year": {
    "type": "integer",
    "required": true
  }
}
```

## Output Schema

```json
{
  "validation_result": {
    "type": "object",
    "properties": {
      "status": {
        "type": "enum",
        "values": ["VALID", "REJECTED", "FLAGGED"]
      },
      "validated_question": {
        "type": "object | null",
        "description": "Enriched question object if valid, null if rejected",
        "properties": {
          "question_text": "string",
          "options": "object",
          "correct_answer": "string",
          "difficulty": "easy | medium | hard",
          "topics": ["array of topic strings"],
          "source_reference": "object",
          "confidence_score": "float",
          "validation_timestamp": "string (ISO 8601)"
        }
      },
      "rejection_reason": {
        "type": "string | null",
        "description": "Specific reason code if rejected"
      },
      "validation_notes": [
        {
          "level": "error | warning | info",
          "code": "string",
          "message": "string"
        }
      ]
    }
  }
}
```

## File Paths

| Operation | Path Template |
|-----------|---------------|
| Read | `question-bank/master-index.json` |
| Read | `syllabus/{exam}/syllabus-structure.json` |
| Write (flagged) | `Needs-Review/{exam}/{YYYY-MM-DD}/{subject}-Q{num}.json` |

## Validation Rules

### Critical (Must Pass)
| Rule | Rejection Code | Description |
|------|----------------|-------------|
| All 4 options present | MISSING_OPTION_A/B/C/D | Options A, B, C, D must all exist and be non-empty |
| Valid answer | NO_CORRECT_ANSWER | correct_answer must be A, B, C, or D |
| Answer references existing option | INVALID_ANSWER_REFERENCE | If answer is "C", options.C must exist |
| No exact duplicates | DUPLICATE_QUESTION | Question text similarity < 90% with existing questions |
| Minimum question length | QUESTION_TOO_SHORT | Question text must be at least 10 characters |

### Warnings (Flag for Review)
| Rule | Flag Code | Description |
|------|-----------|-------------|
| Possible duplicate | POSSIBLE_DUPLICATE | Question text similarity 80-90% with existing |
| Low confidence score | LOW_CONFIDENCE | Confidence score < 0.80 from extraction |
| Quality issues | QUALITY_ISSUE | Malformed text, encoding issues, excessive special chars |
| Missing topic match | NO_TOPIC_MATCH | Unable to match question to syllabus topics |

## Duplicate Detection Algorithm

**Text Similarity Calculation**:
1. Normalize both texts (lowercase, remove punctuation)
2. Tokenize into words
3. Calculate Jaccard similarity: `|A ∩ B| / |A ∪ B|`
4. Alternative: Levenshtein distance normalized by max length

**Thresholds**:
- **90%+**: Reject as duplicate
- **80-89%**: Flag as possible duplicate
- **<80%**: Accept as unique

## Auto-Tagging: Difficulty

### Easy Keywords
```
is, are, was, were, what, who, when, where, which
capital, founded, established, year, date, name
```

### Medium Keywords
```
how, why, describe, explain, compare, difference
between, among, relationship, cause, effect
```

### Hard Keywords
```
analyze, evaluate, assess, calculate, derive
interpret, synthesize, justify, critique, prove
```

**Decision Logic**:
- If 3+ Hard keywords → difficulty: "hard"
- Else if 2+ Medium keywords → difficulty: "medium"
- Else if 3+ Easy keywords → difficulty: "easy"
- Else → difficulty: "medium" (default)

## Auto-Tagging: Topics

**Topic Matching Strategy**:
1. Load syllabus-structure.json for exam type
2. Extract topic keywords from syllabus
3. Search question_text for topic keyword matches
4. Rank matches by frequency and position (title match > body match)
5. Assign top-ranked topic as primary
6. Assign 2nd and 3rd as secondary (if score > threshold)

**Example** (Pakistan Studies):
```json
{
  "topics": [
    "Constitutional Amendments",
    "Geography of Pakistan",
    "Freedom Movement",
    "Government Structure"
  ]
}
```

Question: "Which amendment to the 1973 Constitution introduced Islamic provisions?"
→ Matches: "Constitutional Amendments" (high confidence)
→ Primary topic: "Constitutional Amendments"

## Constraints

- Must reject all questions with missing options
- Must reject all questions with invalid answers
- Must detect duplicates with 95%+ accuracy
- Must auto-tag difficulty for 90%+ of questions
- Must auto-tag at least one topic for 85%+ of questions
- Must provide specific rejection reasons (never generic "invalid")
- Must preserve original question text (no modifications)

## Error Handling

| Condition | Response |
|-----------|----------|
| master-index.json missing | Create empty index, proceed with validation |
| syllabus-structure.json missing | Log warning, skip topic tagging, use subject as topic |
| Malformed input question | Reject with reason "MALFORMED_INPUT" |
| Invalid exam_type | Return error immediately |

## Flagging Workflow

When question is flagged (status: "FLAGGED"):
1. Write flagged question to `Needs-Review/{exam}/{date}/{subject}-Q{num}.json`
2. Include validation notes explaining concerns
3. Return status: "FLAGGED" with full question data
4. Allow downstream processing to decide whether to include or skip

## Success Criteria

- Reject 100% of questions with missing options
- Reject 100% of questions with invalid answers
- Detect duplicates with 95%+ accuracy (manual verification on sample)
- Auto-tag difficulty for 90%+ of questions
- Auto-tag topics for 85%+ of questions
- Provide specific rejection codes for all rejected questions
- Execution completes within 100ms per question
