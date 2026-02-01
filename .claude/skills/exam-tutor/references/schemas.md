# Data Schemas Reference

This document defines the canonical schemas for all data structures used by the Exam Tutor skills.

## Student Data Schemas

### profile.json

Location: `memory/students/{student_id}/profile.json`

```json
{
  "$schema": "exam-tutor/student-profile/v2",
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
  "status": "active | inactive | completed (default: active)",

  "whatsapp": {
    "phone_number": "string E.164 format (optional)",
    "verified": "boolean (default: false)",
    "verified_at": "string ISO 8601 (optional)",
    "opted_in_daily_questions": "boolean (default: false)",
    "opted_in_reports": "boolean (default: false)",
    "preferred_time": "string HH:MM (default: 08:00)",
    "timezone": "string IANA timezone (default: Asia/Karachi)",
    "quiet_hours": {
      "enabled": "boolean (default: false)",
      "start": "string HH:MM (default: 22:00)",
      "end": "string HH:MM (default: 07:00)"
    }
  },

  "sharing_consent": {
    "display_name": "string (optional, public alias)",
    "show_full_name": "boolean (default: false)",
    "allow_badge_sharing": "boolean (default: false)",
    "allow_achievement_posts": "boolean (default: false)",
    "consent_given_at": "string ISO 8601 (optional)"
  },

  "notifications": {
    "daily_question": "boolean (default: true)",
    "weekly_report": "boolean (default: true)",
    "milestone_alerts": "boolean (default: true)",
    "study_reminders": "boolean (default: true)"
  }
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

## ERI Schema

### eri.json

Location: `memory/students/{student_id}/eri.json`

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

### ERI Band Definitions

| Band | Score Range | Description |
|------|-------------|-------------|
| not_ready | 0-20 | Significant preparation needed |
| developing | 21-40 | Building foundational knowledge |
| approaching | 41-60 | Moderate readiness, gaps remain |
| ready | 61-80 | Good preparation level |
| exam_ready | 81-100 | Strong readiness for examination |

### ERI Formula

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
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

## Phase 3: Growth Engine Schemas

### StudyPlan

Location: `memory/students/{student_id}/plans/plan-{date}.json`
Active Plan: `memory/students/{student_id}/active-plan.json`

```json
{
  "$schema": "exam-tutor/study-plan/v1",
  "plan_id": "string plan-YYYY-MM-DD (required)",
  "student_id": "string (required)",
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "created_at": "string ISO 8601 (required)",
  "updated_at": "string ISO 8601 (required)",
  "status": "draft | pending_approval | active | completed | rejected (required)",
  "approval": {
    "submitted_at": "string ISO 8601 | null",
    "reviewed_at": "string ISO 8601 | null",
    "reviewer": "string | null",
    "decision": "approved | rejected | null",
    "feedback": "string | null"
  },
  "target_exam_date": "string ISO 8601 (required)",
  "days_remaining": "integer > 0 (required)",
  "daily_time_minutes": "integer 15-180 (required)",
  "total_hours_available": "number (required)",
  "focus_areas": [
    {
      "topic": "string (required)",
      "severity_score": "number 0-100 (required)",
      "allocated_hours": "number (required)",
      "priority": "integer >= 1 (required)"
    }
  ],
  "weekly_schedule": [
    {
      "week_number": "integer >= 1 (required)",
      "start_date": "string ISO 8601 (required)",
      "topics": [
        {
          "day": "Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday (required)",
          "topic": "string (required)",
          "duration_minutes": "integer >= 15 (required)",
          "question_count": "integer >= 5 (default: 10)"
        }
      ],
      "rest_days": ["string day name (optional)"]
    }
  ],
  "milestones": [
    {
      "week": "integer >= 1 (required)",
      "target_eri": "number 0-100 (required)",
      "focus_achievement": "string (optional)"
    }
  ]
}
```

### ProgressReport

Location: `memory/students/{student_id}/reports/report-{date}.md` (content)
Metadata: `memory/students/{student_id}/reports/report-{date}.json`

```json
{
  "$schema": "exam-tutor/progress-report/v1",
  "report_id": "string report-YYYY-MM-DD (required)",
  "student_id": "string (required)",
  "period_start": "string ISO 8601 (required)",
  "period_end": "string ISO 8601 (required)",
  "generated_at": "string ISO 8601 (required)",
  "delivered_via": "whatsapp | email | none (required)",
  "delivered_at": "string ISO 8601 | null",
  "summary": {
    "eri_start": "number 0-100 (required)",
    "eri_end": "number 0-100 (required)",
    "eri_change": "number (required, must equal eri_end - eri_start)",
    "sessions_count": "integer (required)",
    "questions_count": "integer (required)",
    "overall_accuracy": "number 0-100 (required)"
  }
}
```

### SocialPost

Pending: `needs_action/social-posts/linkedin-{date}.json`
Completed: `done/social-posts/linkedin-{date}.json`

```json
{
  "$schema": "exam-tutor/social-post/v1",
  "post_id": "string linkedin-YYYY-MM-DD (required)",
  "platform": "linkedin (required)",
  "created_at": "string ISO 8601 (required)",
  "scheduled_for": "string ISO 8601 (required)",
  "status": "draft | pending_approval | approved | rejected | published (required)",
  "approval": {
    "submitted_at": "string ISO 8601 | null",
    "reviewed_at": "string ISO 8601 | null",
    "reviewer": "string | null",
    "decision": "approved | rejected | null",
    "feedback": "string | null"
  },
  "content": {
    "text": "string <= 3000 chars (required)",
    "hashtags": ["string (max 5 items)"],
    "question": {
      "id": "string question ID (required)",
      "text": "string (required)",
      "options": {
        "A": "string (required)",
        "B": "string (required)",
        "C": "string (required)",
        "D": "string (required)"
      },
      "topic": "string (required)",
      "exam_type": "SPSC | PPSC | KPPSC (required)"
    },
    "image_path": "string | null"
  },
  "published_at": "string ISO 8601 | null",
  "engagement": {
    "likes": "integer | null",
    "comments": "integer | null",
    "shares": "integer | null"
  }
}
```

### ScheduledTask

Location: `schedules/{task_type}.json`

```json
{
  "$schema": "exam-tutor/scheduled-task/v1",
  "task_type": "daily_question | weekly_report | linkedin_post (required)",
  "enabled": "boolean (required)",
  "schedule": {
    "frequency": "daily | weekly (required)",
    "hour": "integer 0-23 (required)",
    "minute": "integer 0-59 (required)",
    "day_of_week": "integer 0-6 (Sunday=0) | null (required for weekly)",
    "timezone": "string IANA timezone (required)"
  },
  "target": {
    "scope": "all_opted_in | specific_student | global (required)",
    "student_id": "string | null (required if scope is specific_student)"
  },
  "last_run": {
    "timestamp": "string ISO 8601 | null",
    "status": "success | failed | null",
    "items_processed": "integer | null"
  },
  "next_run": "string ISO 8601 (required)"
}
```

### MessageQueue

Location: `queue/whatsapp/{message_id}.json`

```json
{
  "$schema": "exam-tutor/message-queue/v1",
  "message_id": "string msg-{uuid} (required)",
  "created_at": "string ISO 8601 (required)",
  "message_type": "daily_question | feedback | report_summary | test_question | test_start | test_complete | milestone_badge | study_plan_approved (required)",
  "recipient": {
    "student_id": "string (required)",
    "phone_number": "string E.164 format (required)"
  },
  "content": {
    "template": "string template name | null",
    "text": "string (required)",
    "variables": "object key-value pairs (optional)"
  },
  "status": "pending | sent | delivered | failed (required)",
  "attempts": "integer <= 3 (required)",
  "last_attempt": "string ISO 8601 | null",
  "error": "string | null",
  "delivered_at": "string ISO 8601 | null"
}
```

### ERIBadge

Location: `memory/students/{student_id}/badges/badge-{date}.png` (image)
Metadata: `memory/students/{student_id}/badges/badge-{date}.json`

```json
{
  "$schema": "exam-tutor/eri-badge/v1",
  "badge_id": "string badge-YYYY-MM-DD (required)",
  "student_id": "string (required)",
  "generated_at": "string ISO 8601 (required)",
  "eri_score": "number 0-100 (required)",
  "readiness_band": "not_ready | developing | approaching | ready | exam_ready (required)",
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "display_name": "string | null (required if show_full_name is false)",
  "is_milestone": "boolean (required)",
  "milestone_type": "reached_40 | reached_60 | reached_80 | exam_ready | null",
  "file_path": "string (required)",
  "share_url": "string | null"
}
```

### ERIBadge Band Colors

| Band | Color Code | Hex |
|------|------------|-----|
| not_ready | Red | #e53e3e |
| developing | Orange | #ed8936 |
| approaching | Yellow | #ecc94b |
| ready | Green | #48bb78 |
| exam_ready | Dark Green | #38a169 |

### WhatsAppSession

Location: `memory/students/{student_id}/whatsapp-session.json`

```json
{
  "$schema": "exam-tutor/whatsapp-session/v1",
  "student_id": "string (required)",
  "active_test": {
    "test_id": "string | null",
    "started_at": "string ISO 8601 | null",
    "exam_type": "SPSC | PPSC | KPPSC",
    "focus_topic": "string | null",
    "difficulty": "easy | medium | hard | adaptive",
    "questions": [
      {
        "question_id": "string",
        "text": "string",
        "options": {"A": "", "B": "", "C": "", "D": ""},
        "topic": "string",
        "correct_answer": "string",
        "explanation": "string | null"
      }
    ],
    "current_question": "integer (0-based index)",
    "answers": [
      {
        "question_id": "string",
        "student_answer": "A | B | C | D | null",
        "answered_at": "string ISO 8601 | null"
      }
    ],
    "total_questions": "integer",
    "timeout_at": "string ISO 8601 (started_at + 30 minutes)"
  },
  "last_activity": "string ISO 8601 (required)",
  "session_status": "idle | active_test | awaiting_answer (required)"
}
```

### WhatsAppSession Validation Rules

- `timeout_at` MUST be 30 minutes after `started_at`
- `current_question` MUST be between 0 and `total_questions - 1`
- `answers` array length MUST equal `questions` array length
- `session_status` MUST be "active_test" when `active_test` is not null

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
