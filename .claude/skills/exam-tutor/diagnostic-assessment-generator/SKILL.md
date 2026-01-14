---
name: diagnostic-assessment-generator
description: Generates a comprehensive diagnostic assessment for new students or periodic baseline checks. Use this skill when onboarding a new student or when performing periodic re-assessment. Samples across all syllabus topics to establish initial performance baseline with balanced difficulty distribution.
---

# Diagnostic Assessment Generator

Creates comprehensive diagnostic tests that cover the full exam syllabus.

## MCP Integration

This skill uses the **filesystem MCP server** for reading syllabus and question bank.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read syllabus structure and question files
- `mcp__filesystem__list_directory` - List available question files per subject

## Execution Steps

1. **Validate inputs**
   - exam_type must be SPSC, PPSC, or KPPSC
   - assessment_type must be "initial" or "periodic"
   - questions_per_subject default: 10

2. **Load syllabus structure**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/{exam_type}/syllabus-structure.json
   ```

3. **Calculate questions per subject**
   ```
   For each subject in syllabus:
     question_count = questions_per_subject
     // Adjust by syllabus weight if specified
     if subject.weight:
       question_count = round(questions_per_subject * subject.weight)
   ```

4. **Calculate topic sampling per subject**
   ```
   For each subject:
     topics = subject.topics
     questions_per_topic = ceil(question_count / topics.length)
     // Ensure at least 1 question per topic when possible
   ```

5. **Query questions for each subject**
   ```
   For each subject:
     Use: mcp__filesystem__list_directory
     Path: question-bank/{exam_type}/{subject.name}

     For each question file:
       Use: mcp__filesystem__read_file
       Load questions, filter by topic coverage
   ```

6. **Apply difficulty distribution**
   ```
   Target distribution:
     easy:   30%
     medium: 50%
     hard:   20%

   Sample questions to match distribution
   ```

7. **Apply exclusions (for periodic assessments)**
   ```
   if assessment_type == "periodic":
     Remove questions in exclude_ids
   ```

8. **Shuffle and assign assessment ID**
   ```
   assessment_id = "{exam_type}-DIAG-{timestamp}"
   Shuffle questions to randomize order
   ```

9. **Build coverage map**
   ```
   coverage_map = {
     subject: [topics covered],
     ...
   }
   ```

10. **Return structured output**

## Input Schema

```json
{
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "assessment_type": {
    "type": "enum",
    "values": ["initial", "periodic"],
    "required": true
  },
  "questions_per_subject": {
    "type": "integer",
    "default": 10,
    "minimum": 5
  },
  "exclude_ids": {
    "type": "array",
    "items": "string",
    "default": [],
    "description": "Question IDs to exclude (for periodic assessments)"
  }
}
```

## Output Schema

```json
{
  "assessment": {
    "id": "string",
    "type": "diagnostic",
    "exam_type": "SPSC | PPSC | KPPSC",
    "created_at": "string (ISO 8601)",
    "questions": [
      {
        "id": "string",
        "text": "string",
        "options": {"A": "", "B": "", "C": "", "D": ""},
        "correct_answer": "A | B | C | D",
        "topic": "string",
        "subject": "string",
        "difficulty": "easy | medium | hard"
      }
    ],
    "subject_distribution": {
      "subject_name": "integer (question count)"
    },
    "total_questions": "integer"
  },
  "coverage_map": {
    "subject_name": ["topic1", "topic2"]
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `syllabus/{exam_type}/syllabus-structure.json` |
| Read | `question-bank/{exam_type}/{subject}/*.json` |

## Difficulty Distribution

| Difficulty | Percentage | Purpose |
|------------|------------|---------|
| Easy | 30% | Establish confidence, identify baseline |
| Medium | 50% | Core assessment of knowledge |
| Hard | 20% | Identify advanced understanding |

## Constraints

- Must cover all subjects in the syllabus
- Difficulty distribution must be 30% easy, 50% medium, 20% hard
- Must sample topics proportionally to syllabus weight
- Must not duplicate questions within assessment
- If insufficient questions for a topic, log warning but continue

## Diagnostic vs Periodic

| Type | Purpose | Exclusions |
|------|---------|------------|
| `initial` | First-time baseline | None |
| `periodic` | Re-assessment after practice | exclude_ids applied |

## Example Output Structure

```json
{
  "assessment": {
    "id": "PPSC-DIAG-20240115-1430",
    "type": "diagnostic",
    "exam_type": "PPSC",
    "total_questions": 50,
    "subject_distribution": {
      "Pakistan Studies": 10,
      "General Knowledge": 10,
      "Current Affairs": 10,
      "English": 10,
      "Mathematics": 10
    }
  },
  "coverage_map": {
    "Pakistan Studies": ["History", "Geography", "Constitution"],
    "General Knowledge": ["Science", "World Geography", "Famous Personalities"]
  }
}
```
