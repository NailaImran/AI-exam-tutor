---
name: answer-evaluator
description: Evaluates a set of student answers against correct answers. Use this skill after a student completes any test or assessment. Returns per-question results and aggregate statistics. Pure computation skill with no file operations or side effects.
---

# Answer Evaluator

Evaluates student responses against correct answers and computes performance metrics.

## MCP Integration

This skill is **pure computation** and does not require MCP tools. It operates entirely on input data without file system access.

### No MCP Tools Required
- All computation is done in-memory
- Input data contains all necessary information
- No external data sources needed

## Execution Steps

1. **Validate inputs**
   - Questions array must not be empty
   - Each question must have `id` and `correct_answer`
   - Student answers must reference valid question IDs

2. **Create answer lookup map**
   ```
   For each student_answer:
     answer_map[question_id] = selected_answer
   ```

3. **Evaluate each question**
   ```
   For each question:
     student_answer = answer_map.get(question.id, null)
     is_correct = (student_answer == question.correct_answer)

     result = {
       question_id: question.id,
       is_correct: is_correct,
       correct_answer: question.correct_answer,
       student_answer: student_answer,
       topic: question.topic,
       time_spent: student_answers[question.id].time_spent_seconds
     }
   ```

4. **Compute aggregate statistics**
   ```
   total = questions.length
   correct = count(is_correct == true)
   incorrect = count(is_correct == false AND student_answer != null)
   skipped = count(student_answer == null)
   accuracy_percentage = round((correct / total) * 100, 2)
   avg_time = sum(time_spent) / total
   ```

5. **Compute topic breakdown**
   ```
   Group results by topic
   For each topic:
     attempted = count(answers for topic)
     correct = count(correct answers for topic)
     accuracy_percentage = round((correct / attempted) * 100, 2)
   ```

6. **Return structured output**

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
    }
  },
  "student_answers": {
    "type": "array",
    "required": true,
    "items": {
      "question_id": "string",
      "selected_answer": "A | B | C | D | null",
      "time_spent_seconds": "integer"
    }
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
  }
}
```

## File Paths

This skill does not read or write any files.

## Constraints

- Must handle skipped questions (null answers) without error
- `accuracy_percentage` must be rounded to 2 decimal places
- Must be purely functional—no file reads or writes
- Must not throw errors for empty student_answers array
- Must preserve question order in results array

## Example Computation

```
Input:
  questions: [
    {id: "Q1", correct_answer: "B", topic: "History"},
    {id: "Q2", correct_answer: "A", topic: "History"},
    {id: "Q3", correct_answer: "C", topic: "Geography"}
  ]
  student_answers: [
    {question_id: "Q1", selected_answer: "B", time_spent_seconds: 30},
    {question_id: "Q2", selected_answer: "C", time_spent_seconds: 45},
    {question_id: "Q3", selected_answer: null, time_spent_seconds: 0}
  ]

Output:
  summary: {
    total: 3,
    correct: 1,
    incorrect: 1,
    skipped: 1,
    accuracy_percentage: 33.33,
    avg_time_per_question: 25
  }
  topic_breakdown: [
    {topic_name: "History", attempted: 2, correct: 1, accuracy_percentage: 50.00},
    {topic_name: "Geography", attempted: 0, correct: 0, accuracy_percentage: 0.00}
  ]
```
