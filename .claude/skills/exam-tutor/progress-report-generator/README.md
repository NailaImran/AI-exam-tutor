# Progress Report Generator - Flow Documentation

## Overview

This document describes the complete progress report generation and delivery flow for the AI Exam Tutor.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              Progress Report Generation Flow                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ scheduled-task-  │───>│ progress-        │                   │
│  │ runner           │    │ reporting-       │                   │
│  │ (Sunday 9AM)     │    │ coordinator      │                   │
│  └──────────────────┘    └────────┬─────────┘                   │
│                                   │                              │
│                    ┌──────────────┴──────────────┐               │
│                    │    For Each Student:        │               │
│                    │                             │               │
│                    │  ┌──────────────────┐       │               │
│                    │  │ Load student     │       │               │
│                    │  │ profile & data   │       │               │
│                    │  └────────┬─────────┘       │               │
│                    │           │                 │               │
│                    │           ▼                 │               │
│                    │  ┌──────────────────┐       │               │
│                    │  │ progress-report- │       │               │
│                    │  │ generator        │       │               │
│                    │  └────────┬─────────┘       │               │
│                    │           │                 │               │
│                    │           ├── Aggregate sessions            │
│                    │           ├── Calculate ERI trend           │
│                    │           ├── Build topic breakdown         │
│                    │           ├── Identify weak areas           │
│                    │           ├── Generate recommendations      │
│                    │           ├── Create markdown report        │
│                    │           └── Save report + metadata        │
│                    │                             │               │
│                    │           ▼                 │               │
│                    │  ┌──────────────────┐       │               │
│                    │  │ whatsapp-message-│       │               │
│                    │  │ sender           │       │               │
│                    │  │ (weekly_report_  │       │               │
│                    │  │  summary)        │       │               │
│                    │  └────────┬─────────┘       │               │
│                    │           │                 │               │
│                    │           ▼                 │               │
│                    │  ┌──────────────────┐       │               │
│                    │  │ Update delivery  │       │               │
│                    │  │ status in        │       │               │
│                    │  │ metadata.json    │       │               │
│                    │  └──────────────────┘       │               │
│                    │                             │               │
│                    └─────────────────────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Weekly Report Flow

### 1. Scheduled Trigger (Sunday 9:00 AM PKT)

The `scheduled-task-runner` checks `schedules/weekly-reports.json`:

```json
{
  "task_type": "weekly_report",
  "enabled": true,
  "schedule": {
    "frequency": "weekly",
    "day_of_week": 0,
    "hour": 9,
    "minute": 0,
    "timezone": "Asia/Karachi"
  }
}
```

### 2. Student Selection

For each student with `notifications.weekly_report == true`:

1. Check if report was already sent this week (avoid duplicates)
2. Check for activity in the past 7 days
3. Proceed to report generation

### 3. Data Aggregation

The `progress-report-generator` collects:

```
memory/students/{student_id}/
├── profile.json          → Display name, preferences
├── eri.json              → Current ERI score
├── history.json          → ERI history for trend
├── topic-stats.json      → Topic performance data
└── sessions/             → Session files for period
    ├── session-2026-01-23-001.json
    ├── session-2026-01-24-001.json
    └── ...
```

### 4. ERI Trend Calculation

```javascript
// Find ERI at start and end of period
eri_start = find_eri_at_date(history, period_start)
eri_end = current_eri

eri_change = eri_end - eri_start

// Classify trend
if (eri_change >= 5) trend = "significant_improvement"
if (eri_change > 0) trend = "slight_improvement"
if (eri_change === 0) trend = "stable"
if (eri_change > -5) trend = "slight_decline"
else trend = "significant_decline"
```

### 5. Report Generation

Generated markdown report structure:

```markdown
# Weekly Progress Report

**Student**: Ahmed K.
**Period**: January 23, 2026 to January 30, 2026
**Generated**: January 30, 2026, 9:00 AM

## ERI Summary

| Metric | Start | End | Change |
|--------|-------|-----|--------|
| ERI Score | 52 | 58 | +6 |
| Band | approaching | approaching | - |

🎉 **Great progress this week!**

## Practice Activity

- Sessions completed: 5
- Questions attempted: 47
- Overall accuracy: 68.1%

## Topic Performance

| Topic | Attempts | Accuracy | Trend |
|-------|----------|----------|-------|
| Independence Movement | 15 | 73.3% | ↑ |
| Constitutional Amendments | 12 | 58.3% | ↑ |

## Weak Areas

1. **Economic Policies** - 45.0% accuracy (high priority)

## Recommendations

- Amazing work! You improved your ERI by 6 points this week!
- Focus on Economic Policies - it's your highest priority area.

## Next Week Goals

- **Target ERI**: 63
- **Focus topics**: Economic Policies, Constitutional Amendments
```

### 6. WhatsApp Delivery

Using the `weekly_report_summary` template:

```
📈 Weekly Progress Report

Hi Ahmed K.! Here's your week in review:

📊 **ERI**: 52 → 58 (+6)
📝 **Sessions**: 5
✅ **Accuracy**: 68.1%

**Top Focus Area**: Economic Policies

Amazing work! You improved your ERI by 6 points this week!

Full report: [Full report in app]

Keep practicing! You're making progress.
```

### 7. Metadata Update

After successful delivery:

```json
{
  "$schema": "exam-tutor/progress-report/v1",
  "report_id": "report-2026-01-30",
  "student_id": "test-student",
  "delivered_via": "whatsapp",
  "delivered_at": "2026-01-30T09:00:15+05:00",
  "summary": {
    "eri_start": 52,
    "eri_end": 58,
    "eri_change": 6,
    "sessions_count": 5,
    "questions_count": 47,
    "overall_accuracy": 68.1
  }
}
```

## ERI Improvement Highlighting

When a student improves by 5+ points:

1. **Report Header**: Adds celebration emoji and message
2. **Recommendations**: Leads with congratulations
3. **Milestone Check**: If crossed 40/60/80 threshold, add milestone celebration
4. **WhatsApp Message**: Include celebration in summary

## Error Handling

### No Sessions in Period

```
## Practice Activity

- Sessions completed: 0
- Questions attempted: 0
- Overall accuracy: N/A

**Note**: No practice sessions were recorded this week.
Consider setting a daily practice reminder!
```

### WhatsApp Delivery Failure

1. Log error to queue/whatsapp/
2. Set status to "pending"
3. Retry up to 3 times with exponential backoff
4. After 3 failures, mark as "failed" and continue with next student

### Missing Student Data

| Missing Data | Fallback |
|--------------|----------|
| eri.json | Use ERI = 0, note in report |
| topic-stats.json | Skip topic performance section |
| sessions/ (empty) | Generate report with zeros |
| profile.json | Fail, cannot generate report |

## Testing

### Manual Test: Generate Report

```
/exam-tutor generate progress report for test-student
```

Expected:
1. Report generated at memory/students/test-student/reports/report-{date}.md
2. Metadata at memory/students/test-student/reports/report-{date}.json
3. If opted-in, WhatsApp summary sent

### Manual Test: Batch Weekly Reports

```
/exam-tutor run weekly reports
```

Expected:
1. All opted-in students processed
2. Reports generated for each
3. WhatsApp summaries delivered
4. Batch summary returned

## Configuration

### Schedule Configuration

In `schedules/weekly-reports.json`:

```json
{
  "task_type": "weekly_report",
  "enabled": true,
  "schedule": {
    "frequency": "weekly",
    "day_of_week": 0,
    "hour": 9,
    "minute": 0,
    "timezone": "Asia/Karachi"
  },
  "target": {
    "scope": "all_opted_in"
  }
}
```

### Student Opt-In

In student profile.json:

```json
{
  "notifications": {
    "weekly_report": true
  },
  "whatsapp": {
    "opted_in_reports": true
  }
}
```

## Metrics

### Report Metrics

- **Generation Success Rate**: % of reports successfully generated
- **Delivery Success Rate**: % of reports successfully delivered via WhatsApp
- **Average ERI Change**: Trend across all students
- **Most Improved Topic**: Topic with highest accuracy improvement

### Monitoring

- Check `schedules/weekly-reports.json` last_run status
- Monitor `queue/whatsapp/` for failed deliveries
- Review batch summary for skipped students

## Troubleshooting

### Report Not Generated

1. Verify student exists in memory/students/
2. Check profile.json is valid
3. Verify notifications.weekly_report is true
4. Check for recent report (min 6 days between reports)

### Wrong Statistics

1. Verify session files have correct date format
2. Check history.json has ERI entries for period
3. Verify topic-stats.json is up to date
4. Ensure session aggregation includes all sessions in period

### WhatsApp Not Delivered

1. Check whatsapp.opted_in_reports is true
2. Verify phone number in E.164 format
3. Check quiet hours configuration
4. Review queue/whatsapp/ for failed messages

## Related Documentation

- [SKILL.md](./SKILL.md) - Skill specification
- [progress-reporting-coordinator](../../../subagents/progress-reporting-coordinator/AGENT.md) - Coordinator subagent
- [whatsapp-message-sender](../whatsapp-message-sender/SKILL.md) - Delivery skill
- [contracts/whatsapp-templates.json](../../../../specs/phase-3-core-tutoring/contracts/whatsapp-templates.json) - Message templates
