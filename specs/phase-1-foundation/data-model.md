# Data Model: Exam Tutor Phase 1

**Feature**: 001-phase1-foundation
**Date**: 2026-01-17

## Entity Overview

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Student Profile │────▶│  Session History │────▶│  Session Detail  │
│                  │     │                  │     │                  │
│  profile.json    │     │  history.json    │     │  {id}.json       │
└────────┬─────────┘     └──────────────────┘     └────────┬─────────┘
         │                                                  │
         │                                                  │
         ▼                                                  ▼
┌──────────────────┐                              ┌──────────────────┐
│   Topic Stats    │◀─────────────────────────────│  Per-Question    │
│                  │       (aggregated from)      │  Results         │
│  topic-stats.json│                              │                  │
└────────┬─────────┘                              └────────┬─────────┘
         │                                                  │
         │                                                  │
         ▼                                                  ▼
┌──────────────────┐                              ┌──────────────────┐
│  ERI Calculation │                              │  Question Bank   │
│                  │◀─────────────────────────────│                  │
│  (computed)      │       (references)           │  {topic}.json    │
└──────────────────┘                              └──────────────────┘
                                                           │
                                                           ▼
                                                  ┌──────────────────┐
                                                  │  Syllabus        │
                                                  │                  │
                                                  │  structure.json  │
                                                  └──────────────────┘
```

---

## Entity: Student Profile

**Location**: `Students/{student_id}/profile.json`
**Purpose**: Core student identity and preferences

### Schema

```json
{
  "$schema": "exam-tutor/student-profile/v1",
  "student_id": "string (required, pattern: ^[a-zA-Z0-9_-]+$)",
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

### Example

```json
{
  "$schema": "exam-tutor/student-profile/v1",
  "student_id": "STU001",
  "name": "Ahmed Khan",
  "email": "ahmed@example.com",
  "exam_target": "PPSC",
  "target_exam_date": "2026-06-15",
  "created_at": "2026-01-17T10:00:00Z",
  "updated_at": "2026-01-17T10:00:00Z",
  "preferences": {
    "daily_time_minutes": 60,
    "difficulty_preference": "adaptive",
    "notification_enabled": true
  },
  "status": "active"
}
```

### Validation Rules

- `student_id`: Alphanumeric with hyphens/underscores only
- `exam_target`: Must be one of SPSC, PPSC, KPPSC
- `created_at`: Must be valid ISO 8601 timestamp
- `status`: Must be one of active, inactive, completed

---

## Entity: Session History

**Location**: `Students/{student_id}/history.json`
**Purpose**: Summary of all practice sessions

### Schema

```json
{
  "$schema": "exam-tutor/student-history/v1",
  "student_id": "string (required)",
  "total_sessions": "integer (required)",
  "total_questions_attempted": "integer (required)",
  "total_correct": "integer (required)",
  "overall_accuracy": "number 0-100 (required)",
  "first_session_date": "string ISO 8601 (required)",
  "last_session_date": "string ISO 8601 (required)",
  "current_eri": "number 0-100 (optional)",
  "eri_band": "not_ready | developing | approaching | ready | exam_ready (optional)",
  "sessions": [
    {
      "session_id": "string",
      "session_date": "string ISO 8601",
      "exam_type": "SPSC | PPSC | KPPSC",
      "session_type": "practice | diagnostic | timed",
      "total_questions": "integer",
      "correct": "integer",
      "accuracy": "number 0-100",
      "topics_covered": ["string"],
      "duration_seconds": "integer"
    }
  ]
}
```

### Example

```json
{
  "$schema": "exam-tutor/student-history/v1",
  "student_id": "STU001",
  "total_sessions": 1,
  "total_questions_attempted": 5,
  "total_correct": 4,
  "overall_accuracy": 80.0,
  "first_session_date": "2026-01-17T14:30:00Z",
  "last_session_date": "2026-01-17T14:30:00Z",
  "current_eri": 52.0,
  "eri_band": "approaching",
  "sessions": [
    {
      "session_id": "STU001-20260117-143000",
      "session_date": "2026-01-17T14:30:00Z",
      "exam_type": "PPSC",
      "session_type": "practice",
      "total_questions": 5,
      "correct": 4,
      "accuracy": 80.0,
      "topics_covered": ["Constitutional History", "Independence Movement"],
      "duration_seconds": 180
    }
  ]
}
```

---

## Entity: Topic Statistics

**Location**: `Students/{student_id}/topic-stats.json`
**Purpose**: Per-topic performance tracking for coverage calculation

### Schema

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
      "accuracy": "number 0-100",
      "last_practiced": "string ISO 8601",
      "difficulty_breakdown": {
        "easy": { "attempted": "integer", "correct": "integer" },
        "medium": { "attempted": "integer", "correct": "integer" },
        "hard": { "attempted": "integer", "correct": "integer" }
      },
      "trend": "improving | stable | declining"
    }
  }
}
```

---

## Entity: Session Detail

**Location**: `Students/{student_id}/sessions/{session_id}.json`
**Purpose**: Complete record of a single practice session

### Schema

```json
{
  "$schema": "exam-tutor/session/v1",
  "session_id": "string (required)",
  "student_id": "string (required)",
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "session_type": "practice | diagnostic | timed (required)",
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
    "accuracy": "number 0-100"
  },
  "topic_breakdown": [
    {
      "topic": "string",
      "attempted": "integer",
      "correct": "integer",
      "accuracy": "number 0-100"
    }
  ],
  "eri_before": "number 0-100 (optional)",
  "eri_after": "number 0-100 (optional)"
}
```

---

## Entity: Question

**Location**: `Question-Bank/{exam_type}/{subject}/{topic}.json`
**Purpose**: MCQ content storage

### Schema

```json
{
  "$schema": "exam-tutor/question-bank/v1",
  "metadata": {
    "exam_type": "SPSC | PPSC | KPPSC",
    "subject": "string",
    "topic": "string",
    "created_at": "string ISO 8601",
    "updated_at": "string ISO 8601",
    "question_count": "integer"
  },
  "questions": [
    {
      "id": "string (unique, required, pattern: {EXAM}-{SUBJ}-{NNNNN})",
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
      "reference": "string (optional)",
      "tags": ["string (optional)"],
      "year": "integer (optional)"
    }
  ]
}
```

### Example Question

```json
{
  "id": "PPSC-PK-00001",
  "text": "When was the first constitution of Pakistan enacted?",
  "options": {
    "A": "1947",
    "B": "1956",
    "C": "1962",
    "D": "1973"
  },
  "correct_answer": "B",
  "topic": "Constitutional History",
  "difficulty": "easy",
  "explanation": "The first constitution of Pakistan was enacted on March 23, 1956, establishing Pakistan as an Islamic Republic.",
  "tags": ["constitution", "1956", "history"]
}
```

---

## Entity: Syllabus Structure

**Location**: `Syllabus/{exam_type}/syllabus-structure.json`
**Purpose**: Defines exam structure and topic organization

### Schema

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

---

## Entity: Topic Weights

**Location**: `Syllabus/{exam_type}/topic-weights.json`
**Purpose**: Historical frequency and importance of topics

### Schema

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

---

## Computed Values

### ERI (Exam Readiness Index)

Not stored directly; computed from:

| Component | Source | Calculation |
|-----------|--------|-------------|
| Accuracy (40%) | history.json | overall_accuracy |
| Coverage (25%) | topic-stats.json | practiced_topics / total_syllabus_topics |
| Recency (20%) | history.json | decay(days_since_last_session) |
| Consistency (15%) | history.json | 100 - (sd(recent_accuracies) * 5) |

**Result stored in**: `eri.json` as dedicated file with full component breakdown

---

## Entity: ERI Score

**Location**: `Students/{student_id}/eri.json`
**Purpose**: Exam Readiness Index score with component breakdown

### Schema

```json
{
  "$schema": "exam-tutor/eri/v1",
  "student_id": "string (required)",
  "current_score": "number 0-100 (required)",
  "band": "not_ready | developing | approaching | ready | exam_ready (required)",
  "components": {
    "accuracy": {
      "value": "number 0-100",
      "weight": 0.40,
      "weighted_contribution": "number"
    },
    "coverage": {
      "value": "number 0-100",
      "weight": 0.25,
      "weighted_contribution": "number",
      "topics_practiced": "integer",
      "total_topics": "integer"
    },
    "recency": {
      "value": "number 0-100",
      "weight": 0.20,
      "weighted_contribution": "number",
      "days_since_last_session": "integer"
    },
    "consistency": {
      "value": "number 0-100",
      "weight": 0.15,
      "weighted_contribution": "number",
      "score_std_dev": "number"
    }
  },
  "sessions_count": "integer (required)",
  "last_calculated": "string ISO 8601 (required)",
  "trend": "improving | stable | declining (optional)"
}
```

### Example

```json
{
  "$schema": "exam-tutor/eri/v1",
  "student_id": "STU001",
  "current_score": 52.0,
  "band": "approaching",
  "components": {
    "accuracy": {
      "value": 80.0,
      "weight": 0.40,
      "weighted_contribution": 32.0
    },
    "coverage": {
      "value": 10.0,
      "weight": 0.25,
      "weighted_contribution": 2.5,
      "topics_practiced": 2,
      "total_topics": 20
    },
    "recency": {
      "value": 100.0,
      "weight": 0.20,
      "weighted_contribution": 20.0,
      "days_since_last_session": 0
    },
    "consistency": {
      "value": 100.0,
      "weight": 0.15,
      "weighted_contribution": 15.0,
      "score_std_dev": 0.0
    }
  },
  "sessions_count": 1,
  "last_calculated": "2026-01-17T14:35:00Z",
  "trend": "stable"
}
```

---

## State Transitions

### Student Status

```
    ┌──────────┐
    │  (new)   │
    └────┬─────┘
         │ create profile
         ▼
    ┌──────────┐
    │  active  │◀──────────┐
    └────┬─────┘           │
         │                 │ resume
         │ pause           │
         ▼                 │
    ┌──────────┐           │
    │ inactive │───────────┘
    └────┬─────┘
         │ complete exam
         ▼
    ┌──────────┐
    │completed │
    └──────────┘
```

### Session Flow

```
    ┌──────────┐
    │ request  │  (file in /Inbox)
    └────┬─────┘
         │ valid
         ▼
    ┌──────────┐
    │ active   │  (questions generated)
    └────┬─────┘
         │ answers submitted
         ▼
    ┌──────────┐
    │evaluated │  (results calculated)
    └────┬─────┘
         │ saved
         ▼
    ┌──────────┐
    │ complete │  (files in /Done)
    └──────────┘
```

---

## Indexing Strategy

For Phase 1, no database indexing is needed. File-based lookup:

| Query | Method |
|-------|--------|
| Find student | List `Students/` directory |
| Find session | List `Students/{id}/sessions/` directory |
| Find questions by topic | Read `Question-Bank/{exam}/{subject}/{topic}.json` |
| Find topics practiced | Read `topic-stats.json` keys |
