---
name: adaptive-test-generator
description: Generates a practice test adapted to student's current weak areas and learning trajectory. Use this skill for daily practice sessions after initial diagnosis. Prioritizes topics needing reinforcement while maintaining minimum coverage of other areas. Requires weak-area-identifier output as input.
---

# Adaptive Test Generator

Creates personalized practice tests focused on weak areas while maintaining balanced coverage.

## MCP Integration

This skill uses the **filesystem MCP server** for reading questions and history.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read question bank and student history
- `mcp__filesystem__list_directory` - List question files

## Execution Steps

1. **Validate inputs**
   - student_id must be valid
   - exam_type must be SPSC, PPSC, or KPPSC
   - weak_topics must be array (can be empty)
   - question_count default: 25
   - focus_ratio default: 0.6

2. **Load student history**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/history.json

   Extract recent question IDs (last 3 sessions)
   → recent_question_ids
   ```

3. **Calculate question allocation**
   ```
   weak_area_count = round(question_count * focus_ratio)
   balanced_count = question_count - weak_area_count

   Example (25 questions, 0.6 ratio):
     weak_area_count = 15
     balanced_count = 10
   ```

4. **Allocate weak area questions**
   ```
   For each weak_topic (sorted by severity_rank):
     allocation = ceil(weak_area_count / weak_topics.length)
     // Ensure at least 1 question per weak topic
   ```

5. **Query weak area questions**
   ```
   For each weak_topic:
     Use: mcp__filesystem__read_file
     Path: question-bank/{exam_type}/{subject}/*.json

     Filter by:
       - topic matches weak_topic
       - id not in recent_question_ids
       - difficulty skews easier (60% easy/medium for weak areas)
   ```

6. **Query balanced questions**
   ```
   remaining_count = balanced_count
   covered_topics = weak_topics

   For each syllabus_topic not in covered_topics:
     Query 1-2 questions (mixed difficulty)
     Until remaining_count exhausted
   ```

7. **Apply difficulty adjustment for weak areas**
   ```
   Weak area difficulty distribution:
     easy:   30%
     medium: 50%
     hard:   20%

   (Skews easier to build confidence)
   ```

8. **Combine and shuffle**
   ```
   all_questions = weak_area_questions + balanced_questions
   shuffle(all_questions)

   test_id = "{exam_type}-ADAPT-{student_id}-{timestamp}"
   ```

9. **Build adaptation summary**
   ```
   adaptation_summary = {
     weak_topic_count: weak_area_questions.length,
     balanced_count: balanced_questions.length,
     focus_ratio_actual: weak_area_questions.length / total,
     weak_topics_covered: [list],
     difficulty_distribution: {easy: n, medium: n, hard: n}
   }
   ```

10. **Return structured output**

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
  "weak_topics": {
    "type": "array",
    "required": true,
    "description": "Output from weak-area-identifier skill",
    "items": {
      "topic_name": "string",
      "subject": "string",
      "severity_rank": "integer"
    }
  },
  "question_count": {
    "type": "integer",
    "default": 25,
    "minimum": 10,
    "maximum": 100
  },
  "focus_ratio": {
    "type": "number",
    "default": 0.6,
    "minimum": 0.3,
    "maximum": 0.8,
    "description": "Ratio of questions from weak areas vs balanced"
  }
}
```

## Output Schema

```json
{
  "test": {
    "id": "string",
    "type": "adaptive",
    "exam_type": "SPSC | PPSC | KPPSC",
    "student_id": "string",
    "created_at": "string (ISO 8601)",
    "questions": [
      {
        "id": "string",
        "text": "string",
        "options": {"A": "", "B": "", "C": "", "D": ""},
        "correct_answer": "A | B | C | D",
        "topic": "string",
        "subject": "string",
        "difficulty": "easy | medium | hard",
        "is_weak_area": "boolean"
      }
    ],
    "topic_distribution": {
      "topic_name": "integer (question count)"
    }
  },
  "adaptation_summary": {
    "weak_topic_count": "integer",
    "balanced_count": "integer",
    "focus_ratio_actual": "number",
    "weak_topics_covered": ["string"],
    "difficulty_distribution": {
      "easy": "integer",
      "medium": "integer",
      "hard": "integer"
    }
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `question-bank/{exam_type}/{subject}/*.json` |
| Read | `memory/students/{student_id}/history.json` |

## Adaptation Logic

### Focus Ratio Guidelines

| Scenario | Recommended Ratio |
|----------|-------------------|
| Many weak areas (>10) | 0.7 - Focus heavily |
| Moderate weak areas (5-10) | 0.6 - Balanced focus |
| Few weak areas (<5) | 0.5 - Maintain breadth |
| Near exam date | 0.8 - Intensive remediation |

### Question Freshness

- Questions from last 3 sessions are excluded
- This prevents memorization and ensures variety
- If insufficient fresh questions, warn but allow repeats

## Constraints

- Must allocate `focus_ratio` of questions to weak_topics
- Must not repeat questions from last 3 sessions
- Difficulty for weak topics should skew easier (60% easy/medium)
- Must include at least one question from each weak topic if possible
- If no weak_topics provided, generate balanced test only
