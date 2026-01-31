# Data Model: Growth Engine

**Feature**: phase-3-core-tutoring
**Date**: 2026-01-30

## Entity Schemas

### 1. StudyPlan

Personalized preparation schedule based on weak areas and target exam date.

**Storage**: `memory/students/{student_id}/plans/plan-{date}.json`
**Active Plan**: `memory/students/{student_id}/active-plan.json`

```json
{
  "$schema": "exam-tutor/study-plan/v1",
  "plan_id": "plan-2026-01-30",
  "student_id": "string",
  "exam_type": "SPSC | PPSC | KPPSC",
  "created_at": "ISO-8601 datetime",
  "updated_at": "ISO-8601 datetime",
  "status": "draft | pending_approval | active | completed | rejected",
  "approval": {
    "submitted_at": "ISO-8601 datetime | null",
    "reviewed_at": "ISO-8601 datetime | null",
    "reviewer": "string | null",
    "decision": "approved | rejected | null",
    "feedback": "string | null"
  },
  "target_exam_date": "ISO-8601 date",
  "days_remaining": "integer",
  "daily_time_minutes": "integer",
  "total_hours_available": "number",
  "focus_areas": [
    {
      "topic": "string",
      "severity_score": "number",
      "allocated_hours": "number",
      "priority": "integer"
    }
  ],
  "weekly_schedule": [
    {
      "week_number": "integer",
      "start_date": "ISO-8601 date",
      "topics": [
        {
          "day": "Monday | Tuesday | ... | Sunday",
          "topic": "string",
          "duration_minutes": "integer",
          "question_count": "integer"
        }
      ],
      "rest_days": ["Saturday"]
    }
  ],
  "milestones": [
    {
      "week": "integer",
      "target_eri": "number",
      "focus_achievement": "string"
    }
  ]
}
```

### 2. ProgressReport

Weekly summary of practice activity and progress.

**Storage**: `memory/students/{student_id}/reports/report-{date}.md`
**Metadata**: `memory/students/{student_id}/reports/report-{date}.json`

**Markdown Report Structure**:
```markdown
# Weekly Progress Report

**Student**: {display_name}
**Period**: {start_date} to {end_date}
**Generated**: {timestamp}

## ERI Summary

| Metric | Start | End | Change |
|--------|-------|-----|--------|
| ERI Score | {start_eri} | {end_eri} | {change} |
| Band | {start_band} | {end_band} | - |

## Practice Activity

- Sessions completed: {count}
- Questions attempted: {total}
- Overall accuracy: {percentage}%

## Topic Performance

| Topic | Attempts | Accuracy | Trend |
|-------|----------|----------|-------|
| {topic} | {count} | {accuracy}% | ↑/↓/→ |

## Weak Areas

1. {topic} - {accuracy}% (priority focus)

## Recommendations

- {recommendation_1}
- {recommendation_2}

## Next Week Goals

- Target ERI: {target}
- Focus topics: {topics}
```

**Metadata JSON**:
```json
{
  "$schema": "exam-tutor/progress-report/v1",
  "report_id": "report-2026-01-30",
  "student_id": "string",
  "period_start": "ISO-8601 date",
  "period_end": "ISO-8601 date",
  "generated_at": "ISO-8601 datetime",
  "delivered_via": "whatsapp | email | none",
  "delivered_at": "ISO-8601 datetime | null",
  "summary": {
    "eri_start": "number",
    "eri_end": "number",
    "eri_change": "number",
    "sessions_count": "integer",
    "questions_count": "integer",
    "overall_accuracy": "number"
  }
}
```

### 3. ERIBadge

Shareable image displaying ERI score.

**Storage**: `memory/students/{student_id}/badges/badge-{date}.png`
**Metadata**: `memory/students/{student_id}/badges/badge-{date}.json`

```json
{
  "$schema": "exam-tutor/eri-badge/v1",
  "badge_id": "badge-2026-01-30",
  "student_id": "string",
  "generated_at": "ISO-8601 datetime",
  "eri_score": "number",
  "readiness_band": "not_ready | developing | approaching | ready | exam_ready",
  "exam_type": "SPSC | PPSC | KPPSC",
  "display_name": "string | null",
  "is_milestone": "boolean",
  "milestone_type": "reached_40 | reached_60 | reached_80 | exam_ready | null",
  "file_path": "string",
  "share_url": "string | null"
}
```

### 4. SocialPost

LinkedIn post draft awaiting approval.

**Pending**: `needs_action/social-posts/linkedin-{date}.json`
**Completed**: `done/social-posts/linkedin-{date}.json`

```json
{
  "$schema": "exam-tutor/social-post/v1",
  "post_id": "linkedin-2026-01-30",
  "platform": "linkedin",
  "created_at": "ISO-8601 datetime",
  "scheduled_for": "ISO-8601 datetime",
  "status": "draft | pending_approval | approved | rejected | published",
  "approval": {
    "submitted_at": "ISO-8601 datetime | null",
    "reviewed_at": "ISO-8601 datetime | null",
    "reviewer": "string | null",
    "decision": "approved | rejected | null",
    "feedback": "string | null"
  },
  "content": {
    "text": "string (post body)",
    "hashtags": ["#SPSC", "#ExamPrep", "#Pakistan"],
    "question": {
      "id": "SPSC-PK-00123",
      "text": "string",
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "topic": "string",
      "exam_type": "SPSC | PPSC | KPPSC"
    },
    "image_path": "string | null"
  },
  "published_at": "ISO-8601 datetime | null",
  "engagement": {
    "likes": "integer | null",
    "comments": "integer | null",
    "shares": "integer | null"
  }
}
```

### 5. ScheduledTask

Cron-like schedule configuration.

**Storage**: `schedules/{task_type}.json`

```json
{
  "$schema": "exam-tutor/scheduled-task/v1",
  "task_type": "daily_question | weekly_report | linkedin_post",
  "enabled": "boolean",
  "schedule": {
    "frequency": "daily | weekly",
    "hour": "integer (0-23)",
    "minute": "integer (0-59)",
    "day_of_week": "integer (0-6, Sunday=0) | null",
    "timezone": "string (IANA timezone)"
  },
  "target": {
    "scope": "all_opted_in | specific_student | global",
    "student_id": "string | null"
  },
  "last_run": {
    "timestamp": "ISO-8601 datetime | null",
    "status": "success | failed | null",
    "items_processed": "integer | null"
  },
  "next_run": "ISO-8601 datetime"
}
```

### 6. MessageQueue

Outbound WhatsApp messages pending delivery.

**Storage**: `queue/whatsapp/{message_id}.json`

```json
{
  "$schema": "exam-tutor/message-queue/v1",
  "message_id": "msg-{uuid}",
  "created_at": "ISO-8601 datetime",
  "message_type": "daily_question | feedback | report_summary | test_question",
  "recipient": {
    "student_id": "string",
    "phone_number": "string (E.164 format)"
  },
  "content": {
    "template": "string | null",
    "text": "string",
    "variables": {}
  },
  "status": "pending | sent | delivered | failed",
  "attempts": "integer",
  "last_attempt": "ISO-8601 datetime | null",
  "error": "string | null",
  "delivered_at": "ISO-8601 datetime | null"
}
```

## Profile Extensions

Add to existing `memory/students/{student_id}/profile.json`:

```json
{
  "whatsapp": {
    "phone_number": "+92300XXXXXXX",
    "verified": true,
    "verified_at": "ISO-8601 datetime",
    "opted_in_daily_questions": true,
    "opted_in_reports": true,
    "preferred_time": "08:00",
    "timezone": "Asia/Karachi",
    "quiet_hours": {
      "enabled": false,
      "start": "22:00",
      "end": "07:00"
    }
  },
  "sharing_consent": {
    "display_name": "Fatima A.",
    "show_full_name": false,
    "allow_badge_sharing": true,
    "allow_achievement_posts": false,
    "consent_given_at": "ISO-8601 datetime"
  },
  "notifications": {
    "daily_question": true,
    "weekly_report": true,
    "milestone_alerts": true,
    "study_reminders": true
  }
}
```

## Entity Relationships

```
Student Profile
    │
    ├── StudyPlan (1:many)
    │       └── approval workflow → needs_action/ → done/
    │
    ├── ProgressReport (1:many, weekly)
    │       └── delivery via MessageQueue
    │
    ├── ERIBadge (1:many, on request/milestone)
    │
    └── WhatsApp conversations
            └── MessageQueue (outbound)
            └── incoming replies (processed immediately)

ScheduledTask (global)
    │
    ├── daily_question → MessageQueue → Student WhatsApp
    ├── weekly_report → ProgressReport → MessageQueue
    └── linkedin_post → SocialPost → needs_action/ → LinkedIn

SocialPost (global, 1/day)
    └── approval workflow → needs_action/ → done/ → LinkedIn
```

## Validation Rules

### StudyPlan
- `days_remaining` MUST be positive
- `daily_time_minutes` MUST be between 15 and 180
- `focus_areas` MUST not be empty
- Sum of `allocated_hours` MUST not exceed `total_hours_available`

### ProgressReport
- `period_end` MUST be after `period_start`
- `eri_change` MUST equal `eri_end - eri_start`

### ERIBadge
- `eri_score` MUST be between 0 and 100
- `display_name` MUST be present if `show_full_name` is false

### SocialPost
- `content.text` MUST not exceed 3000 characters (LinkedIn limit)
- `hashtags` MUST not exceed 5 items

### MessageQueue
- `attempts` MUST not exceed 3 before marking failed
- `phone_number` MUST be E.164 format
