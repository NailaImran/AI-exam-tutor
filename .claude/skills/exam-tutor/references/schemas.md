# Data Schemas Reference

This document defines the canonical schemas for all data structures used by the Exam Tutor skills.

## Student Data Schemas

### profile.json

Location: `memory/students/{student_id}/profile.json`

```json
{
  "$schema": "exam-tutor/student-profile/v1",
  "student_id": "string (required)",
  "name": "string (required)",
  "email": "string (optional)",
  "exam_target": "SPSC | PPSC | KPPSC (required)",
  "target_exam_date": "string ISO 8601 (optional)",
  "created_at": "string ISO 8601 (required)",
  "updated_at": "string ISO 8601 (required)",
  "preferences": {
    "daily_time_minutes": "integer (default: 60)",
    "difficulty_preference": "easy | medium | hard | adaptive (default: adaptive)",
    "notification_enabled": "boolean (default: true)"
  },
  "status": "active | inactive | completed (default: active)"
}
```

### history.json

Location: `memory/students/{student_id}/history.json`

```json
{
  "$schema": "exam-tutor/student-history/v1",
  "student_id": "string (required)",
  "total_sessions": "integer (required)",
  "total_questions_attempted": "integer (required)",
  "total_correct": "integer (required)",
  "overall_accuracy": "number (required)",
  "first_session_date": "string ISO 8601 (required)",
  "last_session_date": "string ISO 8601 (required)",
  "sessions": [
    {
      "session_id": "string",
      "session_date": "string ISO 8601",
      "exam_type": "SPSC | PPSC | KPPSC",
      "session_type": "diagnostic | adaptive | timed | review",
      "total_questions": "integer",
      "correct": "integer",
      "accuracy": "number",
      "topics_covered": ["string"],
      "duration_seconds": "integer"
    }
  ]
}
```

### topic-stats.json

Location: `memory/students/{student_id}/topic-stats.json`

```json
{
  "$schema": "exam-tutor/topic-stats/v1",
  "student_id": "string (required)",
  "updated_at": "string ISO 8601 (required)",
  "topics": {
    "<topic_name>": {
      "subject": "string",
      "total_attempted": "integer",
      "total_correct": "integer",
      "accuracy": "number",
      "last_practiced": "string ISO 8601",
      "difficulty_breakdown": {
        "easy": {"attempted": "integer", "correct": "integer"},
        "medium": {"attempted": "integer", "correct": "integer"},
        "hard": {"attempted": "integer", "correct": "integer"}
      },
      "trend": "improving | stable | declining",
      "streak": "integer (consecutive correct)"
    }
  }
}
```

### active-plan.json

Location: `memory/students/{student_id}/active-plan.json`

```json
{
  "$schema": "exam-tutor/study-plan/v1",
  "plan_id": "string (required)",
  "student_id": "string (required)",
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "created_at": "string ISO 8601 (required)",
  "target_exam_date": "string ISO 8601 (optional)",
  "daily_time_minutes": "integer (required)",
  "status": "active | completed | abandoned (required)",
  "current_phase": "integer",
  "current_week": "integer",
  "phases": [
    {
      "phase_number": "integer",
      "name": "string",
      "duration_days": "integer",
      "focus": "string",
      "topics": ["string"],
      "completed": "boolean"
    }
  ],
  "weekly_schedule": [
    {
      "week_number": "integer",
      "start_date": "string ISO 8601",
      "topics": ["string"],
      "daily_targets": {
        "monday": {"topic": "string", "duration_minutes": "integer", "activity": "string"},
        "tuesday": {},
        "wednesday": {},
        "thursday": {},
        "friday": {},
        "saturday": {},
        "sunday": {}
      },
      "review_topics": ["string"],
      "completed": "boolean"
    }
  ],
  "milestones": [
    {
      "date": "string ISO 8601",
      "target_eri": "number",
      "description": "string",
      "achieved": "boolean"
    }
  ]
}
```

## Question Bank Schemas

### Question File

Location: `question-bank/{exam_type}/{subject}/{filename}.json`

```json
{
  "$schema": "exam-tutor/question-bank/v1",
  "metadata": {
    "exam_type": "SPSC | PPSC | KPPSC",
    "subject": "string",
    "created_at": "string ISO 8601",
    "updated_at": "string ISO 8601",
    "question_count": "integer"
  },
  "questions": [
    {
      "id": "string (unique, required)",
      "text": "string (required)",
      "options": {
        "A": "string (required)",
        "B": "string (required)",
        "C": "string (required)",
        "D": "string (required)"
      },
      "correct_answer": "A | B | C | D (required)",
      "topic": "string (required)",
      "difficulty": "easy | medium | hard (required)",
      "explanation": "string (optional)",
      "reference": "string (optional, source citation)",
      "tags": ["string (optional)"],
      "year": "integer (optional, exam year if from past paper)"
    }
  ]
}
```

### Question ID Format

```
{EXAM_TYPE}-{SUBJECT_CODE}-{NUMBER}

Examples:
  SPSC-PK-001     (SPSC, Pakistan Studies, Question 1)
  PPSC-GK-142     (PPSC, General Knowledge, Question 142)
  KPPSC-ENG-089   (KPPSC, English, Question 89)

Subject Codes:
  PK  - Pakistan Studies
  GK  - General Knowledge
  CA  - Current Affairs
  ENG - English
  MTH - Mathematics
  ISL - Islamiat
  CS  - Computer Science
```

## Syllabus Schemas

### syllabus-structure.json

Location: `syllabus/{exam_type}/syllabus-structure.json`

```json
{
  "$schema": "exam-tutor/syllabus/v1",
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "version": "string (year, required)",
  "last_updated": "string ISO 8601 (required)",
  "total_subjects": "integer",
  "total_topics": "integer",
  "subjects": [
    {
      "name": "string (required)",
      "code": "string (required)",
      "weight": "number 0-1 (required)",
      "topics": [
        {
          "name": "string (required)",
          "weight": "number 0-1 (required)",
          "description": "string (optional)",
          "subtopics": ["string (optional)"]
        }
      ]
    }
  ]
}
```

### topic-weights.json

Location: `syllabus/{exam_type}/topic-weights.json`

```json
{
  "$schema": "exam-tutor/topic-weights/v1",
  "exam_type": "SPSC | PPSC | KPPSC",
  "weights": {
    "<topic_name>": {
      "weight": "number 0-1",
      "importance": "high | medium | low",
      "frequency": "number (historical appearance rate)",
      "estimated_questions": "integer (typical count per exam)"
    }
  }
}
```

### cross-exam-mapping.json

Location: `syllabus/cross-exam-mapping.json`

```json
{
  "$schema": "exam-tutor/cross-exam-mapping/v1",
  "version": "string",
  "mappings": {
    "<source_exam>": {
      "<topic_name>": {
        "equivalents": {
          "<target_exam>": {
            "topic": "string",
            "confidence": "number 0-1",
            "notes": "string"
          }
        }
      }
    }
  }
}
```

## Session Schemas

### Session Detail File

Location: `memory/students/{student_id}/sessions/{session_id}.json`

```json
{
  "$schema": "exam-tutor/session/v1",
  "session_id": "string (required)",
  "student_id": "string (required)",
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "session_type": "diagnostic | adaptive | timed | review (required)",
  "session_date": "string ISO 8601 (required)",
  "start_time": "string ISO 8601 (required)",
  "end_time": "string ISO 8601 (required)",
  "duration_seconds": "integer (required)",
  "questions": [
    {
      "question_id": "string",
      "topic": "string",
      "difficulty": "easy | medium | hard",
      "student_answer": "A | B | C | D | null",
      "correct_answer": "A | B | C | D",
      "is_correct": "boolean",
      "time_spent_seconds": "integer"
    }
  ],
  "summary": {
    "total": "integer",
    "correct": "integer",
    "incorrect": "integer",
    "skipped": "integer",
    "accuracy": "number"
  },
  "topic_breakdown": [
    {
      "topic": "string",
      "attempted": "integer",
      "correct": "integer",
      "accuracy": "number"
    }
  ]
}
```

## Log Schemas

### Session Log

Location: `logs/sessions/{student_id}/{session_id}.json`

```json
{
  "$schema": "exam-tutor/session-log/v1",
  "log_id": "string (required)",
  "student_id": "string (required)",
  "session_id": "string (required)",
  "session_type": "diagnostic | adaptive | timed | review (required)",
  "start_time": "string ISO 8601 (required)",
  "end_time": "string ISO 8601 (required)",
  "duration_seconds": "integer (required)",
  "events_count": "integer (required)",
  "events": [
    {
      "timestamp": "string ISO 8601",
      "event_type": "string",
      "data": "object (optional)"
    }
  ],
  "metadata": {
    "logged_at": "string ISO 8601",
    "version": "string"
  }
}
```

## Validation Rules

### Required Fields

All schemas have required fields marked. Skills must validate:
- Required fields are present
- Field types match specification
- Enum values are valid
- Dates are valid ISO 8601 format

### ID Uniqueness

- `student_id`: Unique across all students
- `session_id`: Unique per student
- `question.id`: Unique within exam_type
- `plan_id`: Unique per student

### Numeric Ranges

- `accuracy`: 0.00 to 100.00
- `weight`: 0.00 to 1.00
- `confidence`: 0.00 to 1.00
- `eri_score`: 0 to 100
