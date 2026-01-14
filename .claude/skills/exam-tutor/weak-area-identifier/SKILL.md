---
name: weak-area-identifier
description: Analyzes topic-level performance data to identify weak areas requiring focused practice. Use this skill before generating adaptive tests or study plans. Ranks topics by weakness severity using accuracy and attempt count, categorizing all syllabus topics into weak, strong, or untested.
---

# Weak Area Identifier

Identifies and ranks topics requiring additional practice based on performance data.

## MCP Integration

This skill uses the **filesystem MCP server** for reading performance data.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read topic-stats and syllabus files

## Execution Steps

1. **Validate inputs**
   - student_id must be valid
   - exam_type must be SPSC, PPSC, or KPPSC
   - threshold_accuracy default: 60
   - min_attempts default: 5

2. **Load topic statistics**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/topic-stats.json
   ```

3. **Load syllabus structure**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/{exam_type}/syllabus-structure.json
   ```

4. **Categorize each syllabus topic**
   ```
   For each topic in syllabus:
     stats = topic_stats.get(topic, null)

     if stats is null OR stats.total_attempted < min_attempts:
       → Add to untested_topics
     else if stats.accuracy < threshold_accuracy:
       → Add to weak_topics with severity calculation
     else:
       → Add to strong_topics
   ```

5. **Calculate severity rank for weak topics**
   ```
   severity_score = (threshold_accuracy - accuracy) * attempt_weight

   where attempt_weight:
     - attempts >= 20: weight = 1.5 (persistent weakness)
     - attempts >= 10: weight = 1.2 (confirmed weakness)
     - attempts >= 5:  weight = 1.0 (emerging weakness)

   Rank by severity_score descending
   ```

6. **Build output arrays**
   - Sort weak_topics by severity_rank (1 = most severe)
   - Sort strong_topics by accuracy descending
   - Sort untested_topics by syllabus order

7. **Return structured output**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "threshold_accuracy": {
    "type": "number",
    "default": 60,
    "description": "Accuracy percentage below which a topic is considered weak"
  },
  "min_attempts": {
    "type": "integer",
    "default": 5,
    "description": "Minimum attempts required for a topic to be evaluated"
  }
}
```

## Output Schema

```json
{
  "weak_topics": {
    "type": "array",
    "items": {
      "topic_name": "string",
      "subject": "string",
      "accuracy": "number",
      "attempts": "integer",
      "severity_rank": "integer (1 = most severe)",
      "severity_score": "number",
      "last_practiced": "string (ISO 8601)"
    }
  },
  "strong_topics": {
    "type": "array",
    "items": {
      "topic_name": "string",
      "subject": "string",
      "accuracy": "number",
      "attempts": "integer",
      "last_practiced": "string (ISO 8601)"
    }
  },
  "untested_topics": {
    "type": "array",
    "items": {
      "topic_name": "string",
      "subject": "string",
      "attempts": "integer (0 to min_attempts-1)",
      "syllabus_weight": "number"
    }
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `syllabus/{exam_type}/syllabus-structure.json` |

## Severity Calculation Example

```
Topic: "Constitutional Law"
Accuracy: 45%
Attempts: 25
Threshold: 60%

severity_score = (60 - 45) * 1.5 = 22.5
(High severity due to persistent weakness with many attempts)

Topic: "Geography of Pakistan"
Accuracy: 55%
Attempts: 8
Threshold: 60%

severity_score = (60 - 55) * 1.2 = 6.0
(Lower severity, fewer attempts, closer to threshold)
```

## Constraints

- Severity rank must consider both accuracy and attempt count
- Must include all syllabus topics in one of three output arrays
- Must not include topics not in syllabus (ignore orphan stats)
- Topics with zero attempts go to untested_topics
- Must handle missing topic-stats.json gracefully (all topics untested)

## Usage Guidance

The output of this skill feeds directly into:
- `adaptive-test-generator` - to focus on weak areas
- `study-plan-generator` - to prioritize weak topics
- `progress-report-generator` - to highlight areas needing attention
