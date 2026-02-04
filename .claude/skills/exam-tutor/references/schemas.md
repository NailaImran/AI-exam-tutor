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

---

## Phase 4: Autonomous Coach Schemas

### learning-profile.json

Location: `memory/students/{student_id}/learning-profile.json`

```json
{
  "$schema": "exam-tutor/learning-profile/v1",
  "student_id": "string (required)",
  "optimal_study_times": ["morning", "evening"],
  "session_duration_preference": "integer minutes (default: 30)",
  "learning_velocity": {
    "fast_topics": ["string topic names"],
    "slow_topics": ["string topic names"]
  },
  "engagement_patterns": {
    "peak_days": ["monday", "wednesday", "saturday"],
    "low_engagement_days": ["friday"],
    "average_sessions_per_week": "number",
    "dropout_risk_indicators": ["string indicators"]
  },
  "preferred_difficulty_ramp": "gradual | aggressive | mixed (default: gradual)",
  "response_to_pressure": "low | moderate | high (default: moderate)",
  "created_at": "string ISO 8601 (required)",
  "updated_at": "string ISO 8601 (required)"
}
```

### mock-exam-result.json

Location: `memory/students/{student_id}/mock-exams/{session_id}.json`

```json
{
  "$schema": "exam-tutor/mock-exam-result/v1",
  "session_id": "string (required)",
  "student_id": "string (required)",
  "exam_type": "SPSC | PPSC | KPPSC (required)",
  "exam_format": {
    "total_questions": "integer (default: 100)",
    "duration_minutes": "integer (default: 180)",
    "sections": ["pakistan_studies", "general_knowledge", "current_affairs", "english", "math"]
  },
  "results": {
    "completed_questions": "integer (required)",
    "time_taken_minutes": "integer (required)",
    "time_per_question_avg_seconds": "number (required)",
    "section_breakdown": {
      "<section_name>": {
        "correct": "integer",
        "total": "integer",
        "time_avg": "number seconds"
      }
    },
    "overall_score": "number 0-100 (required)",
    "percentile_estimate": "number 0-100 (optional)"
  },
  "analysis": {
    "pressure_handling": "low | moderate | high (required)",
    "fatigue_detected_at_question": "integer | null",
    "accuracy_trend": "string description (required)",
    "time_management": "string description (required)"
  },
  "predictions": {
    "predicted_real_exam_score": "number 0-100 (required)",
    "confidence_interval": ["number lower", "number upper"],
    "ready_for_exam": "boolean (required)",
    "recommended_mock_count": "integer (required)"
  },
  "created_at": "string ISO 8601 (required)"
}
```

### retention-data.json

Location: `memory/students/{student_id}/retention-data.json`

```json
{
  "$schema": "exam-tutor/retention-data/v1",
  "student_id": "string (required)",
  "topics": {
    "<topic_id>": {
      "easiness_factor": "number >= 1.3 (default: 2.5)",
      "repetition_count": "integer (default: 0)",
      "optimal_interval_days": "integer (default: 1)",
      "last_quality": "integer 0-5",
      "last_reviewed": "string ISO 8601",
      "retention_score": "number 0-1",
      "decay_rate": "number per day",
      "status": "strong | stable | weakening | critical",
      "review_history": [
        {
          "date": "string ISO 8601",
          "accuracy": "number 0-100",
          "quality": "integer 0-5",
          "interval_before": "integer days",
          "interval_after": "integer days"
        }
      ]
    }
  },
  "settings": {
    "algorithm": "sm2",
    "minimum_retention_target": "number (default: 0.70)",
    "initial_easiness_factor": "number (default: 2.5)"
  },
  "updated_at": "string ISO 8601"
}
```

### revision-queue.json

Location: `memory/students/{student_id}/revision-queue.json`

```json
{
  "$schema": "exam-tutor/revision-queue/v1",
  "student_id": "string (required)",
  "queue": [
    {
      "topic_id": "string (required)",
      "subject": "string (required)",
      "last_reviewed": "string ISO 8601 (required)",
      "retention_score": "number 0-1 (required)",
      "decay_rate": "number 0-1 (required)",
      "due_date": "string ISO 8601 (required)",
      "priority": "urgent | high | normal | low (required)",
      "revision_count": "integer (required)",
      "optimal_interval_days": "integer (required)"
    }
  ],
  "settings": {
    "algorithm": "sm2 (default)",
    "minimum_retention_target": "number 0-1 (default: 0.70)",
    "daily_revision_limit": "integer (default: 10)"
  },
  "updated_at": "string ISO 8601 (required)"
}
```

### gap-predictions.json

Location: `memory/students/{student_id}/gap-predictions.json`

```json
{
  "$schema": "exam-tutor/gap-predictions/v1",
  "student_id": "string (required)",
  "predictions": [
    {
      "topic_id": "string (required)",
      "subject": "string (required)",
      "current_score": "number 0-1 (required)",
      "predicted_score_7d": "number 0-1 (required)",
      "predicted_score_14d": "number 0-1 (required)",
      "risk_level": "high | medium | low (required)",
      "contributing_factors": ["string factors"],
      "recommended_action": "string action (required)"
    }
  ],
  "generated_at": "string ISO 8601 (required)"
}
```

### Session Audit Log (Phase 4)

Location: `logs/sessions/{student_id}/{YYYY-MM-DD}.json`

```json
{
  "$schema": "exam-tutor/session-audit-log/v1",
  "date": "string ISO 8601 date (required)",
  "sessions": [
    {
      "session_id": "string (required)",
      "type": "autonomous_daily | mock_exam | intervention | student_initiated (required)",
      "initiated_by": "system | student (required)",
      "trigger_reason": "scheduled | gap_detected | revision_due | student_request (required)",
      "started_at": "string ISO 8601 (required)",
      "ended_at": "string ISO 8601 (required)",
      "duration_minutes": "integer (required)",
      "activities": [
        {
          "activity": "string activity type",
          "questions_count": "integer",
          "score": "number 0-1"
        }
      ],
      "eri_before": "number 0-100 (required)",
      "eri_after": "number 0-100 (required)",
      "notes": "string (optional)"
    }
  ]
}
```

### diagnostic-report.json

Location: `memory/students/{student_id}/diagnostics/{topic_id}-{date}.json`

```json
{
  "$schema": "exam-tutor/diagnostic-report/v1",
  "student_id": "string (required)",
  "topic_id": "string (required)",
  "analyzed_at": "string ISO 8601 (required)",
  "depth": "quick | standard | comprehensive (required)",
  "current_accuracy": "number 0-100 (required)",
  "severity": "critical | severe | moderate | mild (required)",
  "root_causes": {
    "primary": {
      "code": "no_practice | insufficient_practice | historically_difficult | related_weakness | knowledge_decay | concept_confusion | time_pressure | difficulty_mismatch (required)",
      "name": "string human readable (required)",
      "confidence": "number 0-1 (required)",
      "evidence": ["string data points (required)"]
    },
    "secondary": [
      {
        "code": "string (required)",
        "name": "string (required)",
        "confidence": "number 0-1 (required)"
      }
    ]
  },
  "contributing_factors": {
    "negative": [
      {
        "factor": "practice_recency | practice_volume | retention_health | trend_direction | related_topic_health | difficulty_progression (required)",
        "impact": "negative (required)",
        "value": "number 0-1 (required)",
        "description": "string (required)"
      }
    ],
    "positive": [
      {
        "factor": "string (required)",
        "impact": "positive (required)",
        "value": "number 0-1 (required)",
        "description": "string (required)"
      }
    ]
  },
  "recommendations": {
    "primary_action": {
      "action_type": "practice | review | prerequisite | drill (required)",
      "description": "string (required)",
      "specific_instruction": "string (required)",
      "topic_focus": "string topic_id (required)",
      "difficulty_level": "easy | medium | hard | adaptive (required)",
      "questions_recommended": "integer (required)",
      "estimated_time_minutes": "integer (required)",
      "priority": "urgent | high | medium | low (required)",
      "success_criteria": "string (required)"
    },
    "secondary_actions": [
      {
        "action_type": "string (required)",
        "description": "string (required)",
        "priority": "string (required)"
      }
    ]
  }
}
```

### trigger-log.json

Location: `logs/triggers/{student_id}/{YYYY-MM-DD}.json`

```json
{
  "$schema": "exam-tutor/trigger-log/v1",
  "student_id": "string (required)",
  "date": "string ISO 8601 date (required)",
  "decisions": [
    {
      "decision_id": "string UUID (required)",
      "checked_at": "string ISO 8601 (required)",
      "trigger_score": "number 0-1 (required)",
      "factor_scores": {
        "time_gap": "number 0-1",
        "knowledge_decay": "number 0-1",
        "exam_urgency": "number 0-1",
        "engagement": "number 0-1"
      },
      "should_trigger": "boolean (required)",
      "status": "triggered | rejected | deferred (required)",
      "rejection_reason": "daily_limit_reached | cooldown_active | score_below_threshold | quiet_hours_active | null",
      "triggered_at": "string ISO 8601 | null",
      "session_id": "string | null (if session was started)"
    }
  ],
  "daily_summary": {
    "total_checks": "integer (required)",
    "total_triggers": "integer (required)",
    "total_rejections": "integer (required)"
  }
}
```

### engagement-status.json

Location: `memory/students/{student_id}/engagement-status.json`

```json
{
  "$schema": "exam-tutor/engagement-status/v1",
  "student_id": "string (required)",
  "current_score": "number 0-1 (required)",
  "trend": "improving | stable | slightly_declining | declining (required)",
  "dropout_risk_level": "low | medium | high (required)",
  "dropout_risk_indicators": ["declining_frequency | declining_performance | long_gaps | high_abandonment | shortened_sessions | reduced_questions"],
  "last_checked": "string ISO 8601 (required)",
  "engagement_history": [
    {
      "week_start": "string ISO 8601",
      "score": "number 0-1",
      "sessions_count": "integer",
      "avg_accuracy": "number 0-100"
    }
  ],
  "nudge_effectiveness": {
    "total_nudges_sent": "integer",
    "nudges_responded": "integer",
    "response_rate": "number 0-1",
    "avg_response_time_hours": "number"
  }
}
```

### optimized-schedule.json

Location: `memory/students/{student_id}/optimized-schedule.json`

```json
{
  "$schema": "exam-tutor/optimized-schedule/v1",
  "student_id": "string (required)",
  "generated_at": "string ISO 8601 (required)",
  "week_start_date": "string ISO 8601 (required)",
  "schedule": {
    "<day_name>": [
      {
        "start_time": "HH:MM (required)",
        "end_time": "HH:MM (required)",
        "duration_minutes": "integer (required)",
        "optimal_score": "number 0-1 (required)",
        "content": {
          "type": "revision | gap_intervention | practice | maintenance (required)",
          "topic_id": "string (required)",
          "priority": "integer (required)"
        }
      }
    ]
  },
  "summary": {
    "total_sessions": "integer (required)",
    "total_hours": "number (required)",
    "optimal_time_coverage": "number 0-1 (required)"
  }
}
```

### Phase 4 Validation Rules

#### Autonomy Limits
- Maximum 2 proactive session triggers per day
- Minimum 4 hours cooldown between proactive triggers
- Student preferences override algorithmic recommendations

#### Retention Thresholds
- `retention_score < 0.50`: Intervention required (urgent)
- `retention_score < 0.70`: Revision due (high priority)
- `retention_score >= 0.70`: On track (normal priority)

#### Engagement Monitoring
- Dropout risk indicators checked against 14-day windows
- Graduated nudging: 1 day → 3 days → 7 days
- Maximum 1 nudge per 24 hours
- Escalate to human after 3 consecutive unresponsive nudges

#### Mock Exam Format
- PPSC/SPSC/KPPSC: 100 questions, 180 minutes, 5 sections
- Section weights: 20 questions per section
- Fatigue detection: Track accuracy decline after question 70
