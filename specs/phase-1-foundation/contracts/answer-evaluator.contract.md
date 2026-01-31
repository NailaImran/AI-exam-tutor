# Skill Contract: answer-evaluator

**Version**: 1.0
**Category**: CORE
**MCP Tools**: None (pure computation)

## Purpose

Evaluates student answers against correct answers and computes performance metrics.

## Input Schema

```json
{
  "questions": {
    "type": "array",
    "required": true,
    "items": {
      "id": "string",
      "correct_answer": "A | B | C | D",
      "topic": "string",
      "difficulty": "easy | medium | hard"
    },
    "description": "Questions from question-bank-querier"
  },
  "student_answers": {
    "type": "array",
    "required": true,
    "items": {
      "question_id": "string",
      "selected_answer": "A | B | C | D | null",
      "time_spent_seconds": "integer"
    },
    "description": "Student's submitted answers"
  }
}
```

## Output Schema

```json
{
  "results": {
    "type": "array",
    "items": {
      "question_id": "string",
      "is_correct": "boolean",
      "correct_answer": "string",
      "student_answer": "string | null",
      "topic": "string",
      "difficulty": "string",
      "time_spent_seconds": "integer"
    }
  },
  "summary": {
    "total": "integer",
    "correct": "integer",
    "incorrect": "integer",
    "skipped": "integer",
    "accuracy_percentage": "number (2 decimal places)",
    "avg_time_per_question": "number (seconds)"
  },
  "topic_breakdown": {
    "type": "array",
    "items": {
      "topic_name": "string",
      "attempted": "integer",
      "correct": "integer",
      "accuracy_percentage": "number"
    }
  },
  "difficulty_breakdown": {
    "type": "array",
    "items": {
      "difficulty": "easy | medium | hard",
      "attempted": "integer",
      "correct": "integer",
      "accuracy_percentage": "number"
    }
  }
}
```

## Computation Logic

```
For each question:
  student_answer = find_answer(student_answers, question.id)
  is_correct = (student_answer == question.correct_answer)

Summary:
  correct = count(is_correct == true)
  incorrect = count(is_correct == false AND answer != null)
  skipped = count(answer == null)
  accuracy = round((correct / total) * 100, 2)

Topic/Difficulty breakdown:
  Group by attribute, calculate per-group accuracy
```

## Constraints

- Pure computation: no file I/O
- Handle null answers (skipped) without error
- Accuracy rounded to 2 decimal places
- Preserve question order in results
- Must handle empty answers array

## Example

**Input**:
```json
{
  "questions": [
    {"id": "Q1", "correct_answer": "B", "topic": "History", "difficulty": "easy"},
    {"id": "Q2", "correct_answer": "A", "topic": "History", "difficulty": "medium"},
    {"id": "Q3", "correct_answer": "C", "topic": "Geography", "difficulty": "easy"}
  ],
  "student_answers": [
    {"question_id": "Q1", "selected_answer": "B", "time_spent_seconds": 30},
    {"question_id": "Q2", "selected_answer": "C", "time_spent_seconds": 45},
    {"question_id": "Q3", "selected_answer": null, "time_spent_seconds": 0}
  ]
}
```

**Output**:
```json
{
  "results": [
    {"question_id": "Q1", "is_correct": true, "student_answer": "B", "correct_answer": "B"},
    {"question_id": "Q2", "is_correct": false, "student_answer": "C", "correct_answer": "A"},
    {"question_id": "Q3", "is_correct": false, "student_answer": null, "correct_answer": "C"}
  ],
  "summary": {
    "total": 3,
    "correct": 1,
    "incorrect": 1,
    "skipped": 1,
    "accuracy_percentage": 33.33,
    "avg_time_per_question": 25.0
  },
  "topic_breakdown": [
    {"topic_name": "History", "attempted": 2, "correct": 1, "accuracy_percentage": 50.0},
    {"topic_name": "Geography", "attempted": 0, "correct": 0, "accuracy_percentage": 0.0}
  ]
}
```
