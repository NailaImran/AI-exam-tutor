# Subagent: progress-reporting-coordinator

**Category**: SUPPORTING (Phase 3)
**Authority Level**: Semi-Autonomous (per Constitution v1.1.0)
**Purpose**: Orchestrate the weekly progress report generation and delivery workflow

## Description

The progress-reporting-coordinator subagent manages the end-to-end process of generating and delivering weekly progress reports to students. It coordinates data gathering, report generation, and WhatsApp delivery for all opted-in students.

## Authority

Per Constitution v1.1.0 Subagent Authority:

| Action | Authority |
|--------|-----------|
| Read student data | Autonomous |
| Generate reports | Autonomous |
| Save reports to memory | Autonomous |
| Send via WhatsApp | Autonomous (opt-in verified) |
| Access session history | Autonomous |

**Note**: Unlike study plans, progress reports do NOT require human approval before delivery since they are purely informational and based on factual data.

## Skills Used

1. **progress-report-generator** - Generate weekly progress report
2. **weak-area-identifier** - Get current weak areas for focus recommendations
3. **whatsapp-message-sender** - Deliver summary via WhatsApp

## Workflow

### Trigger Conditions

The subagent is invoked when:
- Weekly schedule fires (Sunday 9 AM PKT via scheduled-task-runner)
- Student explicitly requests a progress report
- Human admin requests batch report generation
- Student reaches a milestone (automatic report trigger)

### Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│             Progress Reporting Coordinator Workflow              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                           │
│  │ 1. Determine     │                                           │
│  │    Scope         │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 2. Get Student   │───── Single student? ─────┐               │
│  │    List          │                            │               │
│  └────────┬─────────┘                            │               │
│           │ Batch                                │ Single        │
│           ▼                                      ▼               │
│  ┌──────────────────┐                   ┌──────────────┐        │
│  │ 3. Filter by     │                   │ Skip filter  │        │
│  │ opted_in_reports │                   └──────┬───────┘        │
│  └────────┬─────────┘                          │                │
│           │                                     │                │
│           └──────────────┬──────────────────────┘                │
│                          ▼                                       │
│           ┌──────────────────────────┐                          │
│           │ FOR EACH STUDENT:        │                          │
│           │                          │                          │
│           │  ┌──────────────────┐    │                          │
│           │  │ 4. Check Last    │    │                          │
│           │  │    Report Date   │────┼── Recently sent? Skip    │
│           │  └────────┬─────────┘    │                          │
│           │           │ OK           │                          │
│           │           ▼              │                          │
│           │  ┌──────────────────┐    │                          │
│           │  │ 5. Invoke        │    │                          │
│           │  │ progress-report- │    │                          │
│           │  │ generator        │    │                          │
│           │  └────────┬─────────┘    │                          │
│           │           │              │                          │
│           │           ▼              │                          │
│           │  ┌──────────────────┐    │                          │
│           │  │ 6. Check Delivery│    │                          │
│           │  │    Preference    │────┼── No WhatsApp? Skip      │
│           │  └────────┬─────────┘    │                          │
│           │           │ WhatsApp     │                          │
│           │           ▼              │                          │
│           │  ┌──────────────────┐    │                          │
│           │  │ 7. Invoke        │    │                          │
│           │  │ whatsapp-message-│    │                          │
│           │  │ sender           │    │                          │
│           │  └────────┬─────────┘    │                          │
│           │           │              │                          │
│           │           ▼              │                          │
│           │  ┌──────────────────┐    │                          │
│           │  │ 8. Update Report │    │                          │
│           │  │    Metadata      │    │                          │
│           │  └──────────────────┘    │                          │
│           │                          │                          │
│           └──────────────────────────┘                          │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────┐                                           │
│  │ 9. Return        │                                           │
│  │ Batch Summary    │                                           │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step Details

#### Step 1: Determine Scope

```json
if (trigger === "scheduled") {
  scope = "all_opted_in"
} else if (trigger === "student_request") {
  scope = "single_student"
  student_id = input.student_id
} else if (trigger === "admin_batch") {
  scope = "all_active"
}
```

#### Step 2: Get Student List

```json
if (scope === "all_opted_in" || scope === "all_active") {
  students = list_directory("memory/students/")
} else {
  students = [student_id]
}
```

#### Step 3: Filter by Opt-In

```json
for each student in students:
  profile = read_file(`memory/students/${student}/profile.json`)

  if (scope === "all_opted_in") {
    if (!profile.notifications.weekly_report) {
      skip(student, "not opted in")
      continue
    }
  }
```

#### Step 4: Check Last Report Date

```json
// Prevent duplicate reports within 6 days
reports = list_directory(`memory/students/${student}/reports/`)
last_report = get_latest(reports)

if (last_report && last_report.date > today - 6 days) {
  skip(student, "report sent recently")
  continue
}
```

#### Step 5: Invoke progress-report-generator

```json
progress-report-generator({
  "student_id": student,
  "period_start": today - 7 days,
  "period_end": today,
  "include_recommendations": true,
  "delivery_method": "none"  // We handle delivery separately
})
```

Returns: report object with summary, topic_performance, recommendations

#### Step 6: Check Delivery Preference

```json
if (!profile.whatsapp || !profile.whatsapp.opted_in_reports) {
  // Save report but don't send
  results.push({
    student: student,
    report_generated: true,
    delivered: false,
    reason: "no WhatsApp delivery configured"
  })
  continue
}

// Check quiet hours
if (is_quiet_hours(profile.whatsapp.quiet_hours)) {
  queue_for_later(student, report)
  continue
}
```

#### Step 7: Invoke whatsapp-message-sender

```json
whatsapp-message-sender({
  "student_id": student,
  "message_type": "weekly_report_summary",
  "template_variables": {
    "display_name": profile.sharing_consent.display_name,
    "eri_start": report.summary.eri_start,
    "eri_end": report.summary.eri_end,
    "eri_change": format_change(report.summary.eri_change),
    "sessions_count": report.summary.sessions_count,
    "accuracy": report.summary.overall_accuracy.toFixed(1),
    "weak_topic": report.weak_areas[0]?.topic || "N/A",
    "recommendation": report.recommendations[0]?.message || "Keep practicing!",
    "report_link": "[Full report in app]"
  }
})
```

#### Step 8: Update Report Metadata

```json
metadata = read_file(`memory/students/${student}/reports/${report.report_id}.json`)
metadata.delivered_via = "whatsapp"
metadata.delivered_at = now()
write_file(`memory/students/${student}/reports/${report.report_id}.json`, metadata)
```

#### Step 9: Return Batch Summary

```json
{
  "success": true,
  "trigger": trigger,
  "timestamp": now(),
  "students_processed": total_count,
  "reports_generated": generated_count,
  "reports_delivered": delivered_count,
  "skipped": [
    { "student": "...", "reason": "..." }
  ],
  "errors": [
    { "student": "...", "error": "..." }
  ]
}
```

## Input

```json
{
  "trigger": "scheduled | student_request | admin_batch | milestone",
  "student_id": "string (required if trigger is student_request or milestone)",
  "force_regenerate": "boolean (optional, default: false)",
  "period_override": {
    "start": "ISO-8601 date (optional)",
    "end": "ISO-8601 date (optional)"
  }
}
```

## Output

```json
{
  "success": "boolean",
  "trigger": "string",
  "timestamp": "ISO-8601 datetime",
  "results": {
    "students_processed": "integer",
    "reports_generated": "integer",
    "reports_delivered": "integer"
  },
  "details": [
    {
      "student_id": "string",
      "report_id": "string",
      "generated": "boolean",
      "delivered": "boolean",
      "delivery_method": "whatsapp | none",
      "error": "string | null"
    }
  ],
  "skipped": [
    {
      "student_id": "string",
      "reason": "string"
    }
  ],
  "errors": [
    {
      "student_id": "string",
      "error": "string"
    }
  ]
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Student not found | Log error, continue with next student |
| No session data | Generate report with zeros, note in report |
| WhatsApp send fails | Queue for retry, mark as pending |
| Report generation fails | Log error, skip student, continue batch |
| Rate limit hit | Pause, retry with backoff |

## Milestone Trigger

When invoked with `trigger: "milestone"`:

```json
// Called by exam-readiness-calculator when milestone crossed
Input: {
  "trigger": "milestone",
  "student_id": "test-student",
  "milestone": {
    "type": "reached_60",
    "previous_eri": 58,
    "new_eri": 62
  }
}

// Generate special milestone report
report = progress-report-generator({
  "student_id": student_id,
  "period_start": today - 7 days,
  "period_end": today,
  "include_recommendations": true
})

// Add milestone celebration to message
message_vars.milestone = milestone.type
message_vars.celebration = "🎉 You've reached the 'approaching' readiness band!"
```

## Schedule Integration

The scheduled-task-runner invokes this subagent based on `schedules/weekly-reports.json`:

```json
{
  "task_type": "weekly_report",
  "enabled": true,
  "schedule": {
    "frequency": "weekly",
    "day_of_week": 0,  // Sunday
    "hour": 9,
    "minute": 0,
    "timezone": "Asia/Karachi"
  },
  "target": {
    "scope": "all_opted_in"
  }
}
```

## Invocation Examples

### Scheduled Weekly Run

```json
// Triggered by scheduled-task-runner on Sunday 9 AM
{
  "trigger": "scheduled"
}

// Returns
{
  "success": true,
  "trigger": "scheduled",
  "timestamp": "2026-01-30T09:00:00+05:00",
  "results": {
    "students_processed": 15,
    "reports_generated": 12,
    "reports_delivered": 10
  },
  "skipped": [
    { "student_id": "inactive-user", "reason": "no activity in 30 days" },
    { "student_id": "no-whatsapp", "reason": "WhatsApp not configured" }
  ]
}
```

### Student Request

```json
// Student asks "show me my progress"
{
  "trigger": "student_request",
  "student_id": "test-student"
}

// Returns
{
  "success": true,
  "trigger": "student_request",
  "timestamp": "2026-01-30T14:30:00+05:00",
  "results": {
    "students_processed": 1,
    "reports_generated": 1,
    "reports_delivered": 1
  },
  "details": [
    {
      "student_id": "test-student",
      "report_id": "report-2026-01-30",
      "generated": true,
      "delivered": true,
      "delivery_method": "whatsapp"
    }
  ]
}
```

### Milestone Achievement

```json
// Student crosses ERI 60 threshold
{
  "trigger": "milestone",
  "student_id": "test-student",
  "milestone": {
    "type": "reached_60",
    "previous_eri": 58,
    "new_eri": 62
  }
}
```

## Constitution Compliance

- **Principle III (Data-Driven)**: Reports based on actual session and performance data
- **Principle V (Respect Context)**: Honors quiet hours and opt-in preferences
- **Principle VI (Bounded Autonomy)**: Operates within student's notification preferences

## Related Components

- [progress-report-generator](../../skills/exam-tutor/progress-report-generator/SKILL.md)
- [whatsapp-message-sender](../../skills/exam-tutor/whatsapp-message-sender/SKILL.md)
- [weak-area-identifier](../../skills/exam-tutor/weak-area-identifier/SKILL.md)
- [scheduled-task-runner](../../skills/exam-tutor/scheduled-task-runner/SKILL.md)
