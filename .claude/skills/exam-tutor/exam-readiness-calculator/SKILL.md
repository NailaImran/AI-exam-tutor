---
name: exam-readiness-calculator
description: Calculates the Exam Readiness Index (ERI) based on historical performance, topic coverage, recency, and consistency. Use this skill to assess student preparedness before tests or when generating progress reports. Returns a score from 0-100 with component breakdown and readiness band classification.
---

# Exam Readiness Calculator

Computes the Exam Readiness Index (ERI) using a weighted formula based on multiple performance factors.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read history, topic-stats, and syllabus files

## ERI Formula

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

### Component Definitions

| Component | Weight | Calculation |
|-----------|--------|-------------|
| **Accuracy** | 40% | Weighted average accuracy across all topics |
| **Coverage** | 25% | Percentage of syllabus topics practiced |
| **Recency** | 20% | Decay-weighted score based on session dates |
| **Consistency** | 15% | Regularity of practice sessions |

## Execution Steps

1. **Load student history**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/history.json
   ```

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

4. **Calculate Accuracy Score (0-100)**
   ```
   For each topic in topic_stats:
     weight = syllabus_weight[topic] or 1
     weighted_accuracy += topic.accuracy * weight

   accuracy_score = weighted_accuracy / total_weight
   ```

5. **Calculate Coverage Score (0-100)**
   ```
   syllabus_topics = all topics in syllabus
   practiced_topics = topics with attempts >= 5

   coverage_score = (practiced_topics.length / syllabus_topics.length) * 100
   ```

6. **Calculate Recency Score (0-100)**
   ```
   For each session in last 30 days:
     days_ago = today - session_date
     decay_factor = 1 - (days_ago / 30) * 0.5
     recency_contribution += session.accuracy * decay_factor

   recency_score = recency_contribution / sessions_count
   ```
   - Sessions older than 30 days contribute 50% weight

7. **Calculate Consistency Score (0-100)**
   ```
   expected_sessions = days_since_first_session / 2  (every other day)
   actual_sessions = total_sessions

   consistency_ratio = min(actual_sessions / expected_sessions, 1)

   // Also factor in session spacing regularity
   spacing_variance = calculate_variance(session_gaps)
   regularity_factor = 1 - min(spacing_variance / 7, 0.5)

   consistency_score = consistency_ratio * regularity_factor * 100
   ```

8. **Compute final ERI**
   ```
   eri_score = round(
     accuracy_score * 0.40 +
     coverage_score * 0.25 +
     recency_score * 0.20 +
     consistency_score * 0.15
   , 2)
   ```

9. **Determine readiness band**
   ```
   0-20:   not_ready
   21-40:  developing
   41-60:  approaching
   61-80:  ready
   81-100: exam_ready
   ```

10. **Calculate syllabus coverage breakdown**

11. **Return structured output**

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
  }
}
```

## Output Schema

```json
{
  "eri_score": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "description": "Overall Exam Readiness Index"
  },
  "components": {
    "accuracy_score": "number (0-100)",
    "coverage_score": "number (0-100)",
    "recency_score": "number (0-100)",
    "consistency_score": "number (0-100)"
  },
  "readiness_band": {
    "type": "enum",
    "values": ["not_ready", "developing", "approaching", "ready", "exam_ready"]
  },
  "syllabus_coverage": {
    "total_topics": "integer",
    "practiced_topics": "integer",
    "coverage_percentage": "number",
    "per_subject": [
      {
        "subject": "string",
        "total_topics": "integer",
        "practiced": "integer",
        "coverage_percentage": "number"
      }
    ]
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/history.json` |
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `syllabus/{exam_type}/syllabus-structure.json` |

## Readiness Bands

| Band | ERI Range | Description |
|------|-----------|-------------|
| `not_ready` | 0-20 | Significant preparation needed |
| `developing` | 21-40 | Building foundational knowledge |
| `approaching` | 41-60 | Moderate readiness, gaps remain |
| `ready` | 61-80 | Good preparation level |
| `exam_ready` | 81-100 | Strong readiness for examination |

## Constraints

- ERI formula must weight: accuracy (40%), coverage (25%), recency (20%), consistency (15%)
- Recency decay: sessions older than 30 days contribute 50% weight
- Must return `eri_score: 0` if no history exists
- Must be deterministic for same input data
- All scores rounded to 2 decimal places
