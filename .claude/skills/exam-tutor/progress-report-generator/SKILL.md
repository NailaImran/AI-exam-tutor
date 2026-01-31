# Skill: progress-report-generator

**Category**: SUPPORTING (Phase 3)
**Purpose**: Generate weekly progress reports with ERI trends, session statistics, topic performance, and personalized recommendations

## Description

The progress-report-generator skill creates comprehensive weekly progress reports for students preparing for SPSC, PPSC, or KPPSC exams. It aggregates session data, calculates ERI trends, identifies topic performance patterns, and generates actionable recommendations.

## Input

```json
{
  "student_id": "string (required)",
  "period_start": "string ISO 8601 (optional, defaults to 7 days ago)",
  "period_end": "string ISO 8601 (optional, defaults to today)",
  "include_recommendations": "boolean (optional, default: true)",
  "delivery_method": "whatsapp | none (optional, default: none)"
}
```

## Output

```json
{
  "success": "boolean",
  "report": {
    "report_id": "string report-YYYY-MM-DD",
    "student_id": "string",
    "period_start": "string ISO 8601",
    "period_end": "string ISO 8601",
    "generated_at": "string ISO 8601",
    "summary": {
      "eri_start": "number",
      "eri_end": "number",
      "eri_change": "number",
      "sessions_count": "integer",
      "questions_count": "integer",
      "overall_accuracy": "number"
    },
    "topic_performance": [...],
    "weak_areas": [...],
    "recommendations": [...],
    "next_week_goals": {...}
  },
  "report_path": "string (markdown file path)",
  "metadata_path": "string (JSON file path)",
  "error": "string | null"
}
```

## Workflow

### 1. Load Student Context

```
Read: memory/students/{student_id}/profile.json
Read: memory/students/{student_id}/eri.json
Read: memory/students/{student_id}/topic-stats.json
Read: memory/students/{student_id}/history.json
```

### 2. Calculate Period Boundaries

```javascript
// Default to last 7 days if not specified
if (!period_start) {
  period_start = today - 7 days
}
if (!period_end) {
  period_end = today
}

// Validate
if (period_end <= period_start) {
  return error("period_end must be after period_start")
}
```

### 3. Aggregate Session Data

```javascript
// Read all session files within period
sessions = list_directory(`memory/students/${student_id}/sessions/`)
  .filter(file => file.date >= period_start && file.date <= period_end)

sessions_count = sessions.length
questions_count = 0
correct_count = 0

for each session in sessions:
  session_data = read_file(session.path)
  questions_count += session_data.questions_attempted
  correct_count += session_data.questions_correct

overall_accuracy = questions_count > 0
  ? (correct_count / questions_count) * 100
  : 0
```

### 4. Calculate ERI Trend

```javascript
// Get ERI at period start and end
history = read_file(`memory/students/${student_id}/history.json`)

// Find ERI closest to period_start
eri_start = find_eri_at_date(history, period_start)

// Current ERI
eri_end = read_file(`memory/students/${student_id}/eri.json`).current_score

eri_change = eri_end - eri_start

// Determine trend direction
if (eri_change >= 5) {
  eri_trend = "significant_improvement"
} else if (eri_change > 0) {
  eri_trend = "slight_improvement"
} else if (eri_change === 0) {
  eri_trend = "stable"
} else if (eri_change >= -5) {
  eri_trend = "slight_decline"
} else {
  eri_trend = "significant_decline"
}
```

### 5. Build Topic Performance Breakdown

```javascript
topic_stats = read_file(`memory/students/${student_id}/topic-stats.json`)

topic_performance = []
for each topic in topic_stats:
  // Get period-specific stats from sessions
  period_attempts = get_topic_attempts_in_period(sessions, topic.name)
  period_correct = get_topic_correct_in_period(sessions, topic.name)
  period_accuracy = period_attempts > 0 ? (period_correct / period_attempts) * 100 : null

  // Calculate trend vs overall accuracy
  overall_topic_accuracy = topic.accuracy
  trend = calculate_trend(period_accuracy, topic.previous_period_accuracy)

  topic_performance.push({
    topic: topic.name,
    period_attempts: period_attempts,
    period_accuracy: period_accuracy,
    overall_accuracy: overall_topic_accuracy,
    trend: trend  // "improving" | "stable" | "declining"
  })

// Sort by period_attempts descending (most practiced first)
topic_performance.sort((a, b) => b.period_attempts - a.period_attempts)
```

### 6. Identify Weak Areas

Integration with `weak-area-identifier` skill:

```json
weak_areas = weak-area-identifier({
  student_id: student_id,
  exam_type: profile.exam_target
})
```

Select top 3 weak areas for report focus:

```javascript
weak_area_summary = weak_areas.slice(0, 3).map(wa => ({
  topic: wa.topic,
  accuracy: wa.accuracy,
  severity: wa.severity_score,
  priority: "high" | "medium" | "low"
}))
```

### 7. Generate Recommendations

```javascript
recommendations = []

// Based on ERI trend
if (eri_trend === "significant_decline") {
  recommendations.push({
    type: "urgency",
    message: "Your ERI has dropped this week. Consider focusing on your weak areas with more practice sessions."
  })
} else if (eri_trend === "significant_improvement") {
  recommendations.push({
    type: "encouragement",
    message: "Excellent progress! Your consistent practice is paying off. Keep the momentum going!"
  })
}

// Based on weak areas
if (weak_area_summary.length > 0) {
  top_weak = weak_area_summary[0]
  recommendations.push({
    type: "focus",
    message: `Focus on ${top_weak.topic} this week - it's your highest priority area at ${top_weak.accuracy}% accuracy.`
  })
}

// Based on session count
if (sessions_count < 3) {
  recommendations.push({
    type: "consistency",
    message: "Try to complete at least 5 practice sessions per week for optimal improvement."
  })
} else if (sessions_count >= 7) {
  recommendations.push({
    type: "praise",
    message: "Great consistency! You practiced every day this week."
  })
}

// Based on accuracy
if (overall_accuracy < 50) {
  recommendations.push({
    type: "difficulty",
    message: "Consider starting with easier questions to build confidence before tackling harder ones."
  })
} else if (overall_accuracy > 80) {
  recommendations.push({
    type: "challenge",
    message: "Your accuracy is excellent! Try challenging yourself with harder questions."
  })
}

// Limit to top 3 recommendations
recommendations = recommendations.slice(0, 3)
```

### 8. Set Next Week Goals

```javascript
// Calculate target ERI (aim for 3-5 point improvement)
target_eri = Math.min(eri_end + 5, 100)

// Get band progression target
current_band = get_readiness_band(eri_end)
next_band_threshold = get_next_band_threshold(current_band)

next_week_goals = {
  target_eri: target_eri,
  focus_topics: weak_area_summary.slice(0, 2).map(wa => wa.topic),
  recommended_sessions: 5,
  next_milestone: next_band_threshold
}
```

### 9. Generate Markdown Report

```javascript
report_content = `# Weekly Progress Report

**Student**: ${profile.sharing_consent.display_name || profile.name}
**Period**: ${format_date(period_start)} to ${format_date(period_end)}
**Generated**: ${format_datetime(now())}

## ERI Summary

| Metric | Start | End | Change |
|--------|-------|-----|--------|
| ERI Score | ${eri_start} | ${eri_end} | ${format_change(eri_change)} |
| Band | ${get_band(eri_start)} | ${get_band(eri_end)} | ${band_changed ? "↑" : "-"} |

${eri_change >= 5 ? "🎉 **Great progress this week!**" : ""}

## Practice Activity

- Sessions completed: ${sessions_count}
- Questions attempted: ${questions_count}
- Overall accuracy: ${overall_accuracy.toFixed(1)}%

## Topic Performance

| Topic | Attempts | Accuracy | Trend |
|-------|----------|----------|-------|
${topic_performance.map(tp =>
  `| ${tp.topic} | ${tp.period_attempts} | ${tp.period_accuracy?.toFixed(1) || "N/A"}% | ${get_trend_arrow(tp.trend)} |`
).join("\n")}

## Weak Areas

${weak_area_summary.map((wa, i) =>
  `${i + 1}. **${wa.topic}** - ${wa.accuracy.toFixed(1)}% accuracy (${wa.priority} priority)`
).join("\n")}

## Recommendations

${recommendations.map(rec => `- ${rec.message}`).join("\n")}

## Next Week Goals

- **Target ERI**: ${next_week_goals.target_eri}
- **Focus topics**: ${next_week_goals.focus_topics.join(", ")}
- **Recommended sessions**: ${next_week_goals.recommended_sessions}
${next_week_goals.next_milestone ? `- **Next milestone**: ERI ${next_week_goals.next_milestone}` : ""}

---
*Generated by AI Exam Tutor*
`
```

### 10. Save Report and Metadata

```javascript
// Generate report ID
today = format_date(now(), "YYYY-MM-DD")
report_id = `report-${today}`

// Save markdown report
report_path = `memory/students/${student_id}/reports/${report_id}.md`
write_file(report_path, report_content)

// Save metadata JSON
metadata = {
  "$schema": "exam-tutor/progress-report/v1",
  "report_id": report_id,
  "student_id": student_id,
  "period_start": period_start,
  "period_end": period_end,
  "generated_at": now(),
  "delivered_via": delivery_method === "whatsapp" ? "whatsapp" : "none",
  "delivered_at": null,
  "summary": {
    "eri_start": eri_start,
    "eri_end": eri_end,
    "eri_change": eri_change,
    "sessions_count": sessions_count,
    "questions_count": questions_count,
    "overall_accuracy": overall_accuracy
  }
}

metadata_path = `memory/students/${student_id}/reports/${report_id}.json`
write_file(metadata_path, metadata)
```

### 11. WhatsApp Delivery (Optional)

If `delivery_method === "whatsapp"`:

```javascript
// Use whatsapp-message-sender skill
whatsapp-message-sender({
  student_id: student_id,
  message_type: "weekly_report_summary",
  template_variables: {
    display_name: profile.sharing_consent.display_name || profile.name,
    eri_start: eri_start,
    eri_end: eri_end,
    eri_change: format_change(eri_change),
    sessions_count: sessions_count,
    accuracy: overall_accuracy.toFixed(1),
    weak_topic: weak_area_summary[0]?.topic || "N/A",
    recommendation: recommendations[0]?.message || "Keep up the practice!",
    report_link: `[Full report in app]`
  }
})

// Update metadata with delivery status
metadata.delivered_via = "whatsapp"
metadata.delivered_at = now()
write_file(metadata_path, metadata)
```

## ERI Improvement Highlighting

When `eri_change >= 5`, the report includes special highlighting:

```javascript
if (eri_change >= 5) {
  // Add celebration header
  report_header += "\n\n🎉 **Congratulations! You made significant progress this week!** 🎉\n"

  // Add to recommendations
  recommendations.unshift({
    type: "celebration",
    message: `Amazing work! You improved your ERI by ${eri_change} points this week!`
  })

  // Check for milestone achievements
  if (crossed_milestone(eri_start, eri_end)) {
    milestone = get_crossed_milestone(eri_start, eri_end)
    report_header += `\n🏆 **Milestone Achieved: ${milestone.name}!**\n`
  }
}
```

## Helper Functions

### get_trend_arrow(trend)

```javascript
switch(trend) {
  case "improving": return "↑"
  case "stable": return "→"
  case "declining": return "↓"
  default: return "-"
}
```

### format_change(change)

```javascript
if (change > 0) return `+${change}`
if (change < 0) return `${change}`
return "0"
```

### get_readiness_band(eri)

```javascript
if (eri >= 81) return "exam_ready"
if (eri >= 61) return "ready"
if (eri >= 41) return "approaching"
if (eri >= 21) return "developing"
return "not_ready"
```

### get_next_band_threshold(band)

```javascript
switch(band) {
  case "not_ready": return 21
  case "developing": return 41
  case "approaching": return 61
  case "ready": return 81
  case "exam_ready": return null  // Already at top
}
```

### crossed_milestone(eri_start, eri_end)

```javascript
milestones = [40, 60, 80]
for each milestone in milestones:
  if (eri_start < milestone && eri_end >= milestone) {
    return true
  }
return false
```

## MCP Tools Used

- `mcp__filesystem__read_file` - Load student data, sessions, history
- `mcp__filesystem__write_file` - Save report and metadata
- `mcp__filesystem__list_directory` - List session files

## Validation Rules

- `period_end` MUST be after `period_start`
- `period_start` MUST not be more than 90 days in the past
- `eri_change` MUST equal `eri_end - eri_start`
- Report MUST be generated even if no sessions exist (show zeros)

## Error Handling

| Error | Action |
|-------|--------|
| Student not found | Return error with student_id |
| No profile.json | Return error, cannot generate report |
| No sessions in period | Generate report with zero statistics |
| No eri.json | Use default ERI of 0 |
| No topic-stats.json | Skip topic performance section |

## Constitution Compliance

- **Principle III (Data-Driven)**: Reports based on actual session data
- **Principle V (Respect Context)**: Uses display_name from sharing_consent

## Example Usage

```json
Input: {
  "student_id": "test-student",
  "period_start": "2026-01-23",
  "period_end": "2026-01-30",
  "delivery_method": "whatsapp"
}

Output: {
  "success": true,
  "report": {
    "report_id": "report-2026-01-30",
    "student_id": "test-student",
    "period_start": "2026-01-23T00:00:00Z",
    "period_end": "2026-01-30T23:59:59Z",
    "generated_at": "2026-01-30T10:00:00Z",
    "summary": {
      "eri_start": 52,
      "eri_end": 58,
      "eri_change": 6,
      "sessions_count": 5,
      "questions_count": 47,
      "overall_accuracy": 68.1
    },
    "topic_performance": [
      {
        "topic": "Independence Movement",
        "period_attempts": 15,
        "period_accuracy": 73.3,
        "overall_accuracy": 71.2,
        "trend": "improving"
      },
      {
        "topic": "Constitutional Amendments",
        "period_attempts": 12,
        "period_accuracy": 58.3,
        "overall_accuracy": 55.0,
        "trend": "improving"
      }
    ],
    "weak_areas": [
      {
        "topic": "Economic Policies",
        "accuracy": 45.0,
        "severity": 85,
        "priority": "high"
      }
    ],
    "recommendations": [
      {
        "type": "celebration",
        "message": "Amazing work! You improved your ERI by 6 points this week!"
      },
      {
        "type": "focus",
        "message": "Focus on Economic Policies this week - it's your highest priority area at 45.0% accuracy."
      }
    ],
    "next_week_goals": {
      "target_eri": 63,
      "focus_topics": ["Economic Policies", "Constitutional Amendments"],
      "recommended_sessions": 5,
      "next_milestone": 61
    }
  },
  "report_path": "memory/students/test-student/reports/report-2026-01-30.md",
  "metadata_path": "memory/students/test-student/reports/report-2026-01-30.json",
  "error": null
}
```

## Related Skills

- weak-area-identifier (provides weak area data)
- whatsapp-message-sender (handles delivery)
- exam-readiness-calculator (provides ERI context)
