---
name: progress-report-generator
description: Generates a structured progress report in Markdown format. Use this skill for weekly summaries or on-demand progress checks. Summarizes recent performance, ERI trend, topic improvements, and areas needing attention. Outputs both machine-readable data and human-readable Markdown.
---

# Progress Report Generator

Creates comprehensive progress reports analyzing student performance over time.

## MCP Integration

This skill uses the **filesystem MCP server** for reading and writing reports.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read history and session files
- `mcp__filesystem__write_file` - Save report to student's reports folder
- `mcp__filesystem__list_directory` - List session files for the period

## Execution Steps

1. **Validate inputs**
   - student_id must be valid
   - exam_type must be SPSC, PPSC, or KPPSC
   - report_period_days default: 7

2. **Load student history**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/history.json
   ```

3. **Load topic statistics**
   ```
   Use: mcp__filesystem__read_file
   Path: memory/students/{student_id}/topic-stats.json
   ```

4. **Filter sessions for report period**
   ```
   period_start = today - report_period_days
   period_sessions = history.sessions.filter(
     session.date >= period_start
   )
   ```

5. **Load individual session details**
   ```
   For each session in period_sessions:
     Use: mcp__filesystem__read_file
     Path: memory/students/{student_id}/sessions/{session_id}.json
   ```

6. **Calculate period statistics**
   ```
   period_stats = {
     sessions_count: period_sessions.length,
     total_questions: sum(session.total_questions),
     total_correct: sum(session.correct),
     period_accuracy: total_correct / total_questions * 100,
     total_time_minutes: sum(session.duration) / 60,
     avg_session_length: total_time_minutes / sessions_count
   }
   ```

7. **Calculate ERI trend**
   ```
   // Get ERI at period start (from first session)
   eri_start = calculate_eri_at_date(period_start)
   eri_current = current_eri

   eri_trend = {
     start: eri_start,
     current: eri_current,
     change: eri_current - eri_start,
     direction: "improving" | "stable" | "declining"
   }
   ```

8. **Identify improvements and concerns**
   ```
   improvements = []
   concerns = []

   For each topic in topic_stats:
     period_accuracy = calculate_period_accuracy(topic, period_sessions)
     previous_accuracy = topic.accuracy_before_period

     delta = period_accuracy - previous_accuracy

     if delta > 10:
       improvements.push({topic, delta, new_accuracy})
     if delta < -10 OR period_accuracy < 50:
       concerns.push({topic, delta, accuracy})

   Sort improvements by delta desc, take top 3
   Sort concerns by severity, take top 3
   ```

9. **Generate recommendations (if enabled)**
   ```
   if include_recommendations:
     recommendations = []

     if concerns.length > 0:
       recommendations.push("Focus on: " + concerns[0].topic)

     if eri_trend.direction == "declining":
       recommendations.push("Increase practice frequency")

     if coverage < 50:
       recommendations.push("Explore untested topics")
   ```

10. **Generate Markdown report**
    ```
    Build structured Markdown with sections:
    - Summary
    - ERI Progress
    - Performance Metrics
    - Top Improvements
    - Areas of Concern
    - Recommendations (if enabled)
    ```

11. **Write report file**
    ```
    Use: mcp__filesystem__write_file
    Path: memory/students/{student_id}/reports/{report_date}.md
    ```

12. **Return structured output**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "report_period_days": {
    "type": "integer",
    "default": 7,
    "minimum": 1,
    "maximum": 90
  },
  "include_recommendations": {
    "type": "boolean",
    "default": true,
    "description": "Whether to include next-step recommendations"
  }
}
```

## Output Schema

```json
{
  "report_markdown": {
    "type": "string",
    "description": "Complete progress report in Markdown format"
  },
  "report_data": {
    "period": {
      "start_date": "string",
      "end_date": "string",
      "days": "integer"
    },
    "sessions": {
      "count": "integer",
      "total_questions": "integer",
      "total_correct": "integer",
      "accuracy": "number",
      "total_time_minutes": "number"
    },
    "eri_trend": {
      "start": "number",
      "current": "number",
      "change": "number",
      "direction": "improving | stable | declining"
    },
    "top_improvements": [
      {"topic": "string", "delta": "number", "accuracy": "number"}
    ],
    "areas_of_concern": [
      {"topic": "string", "accuracy": "number", "reason": "string"}
    ],
    "recommendations": ["string"]
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/history.json` |
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `memory/students/{student_id}/sessions/*.json` |
| Write | `memory/students/{student_id}/reports/{report_date}.md` |

## Markdown Report Template

```markdown
# Progress Report: {student_name}
**Period:** {start_date} to {end_date}
**Exam Target:** {exam_type}

## Summary
- Sessions completed: {count}
- Questions practiced: {total}
- Overall accuracy: {accuracy}%

## ERI Progress
- Start of period: {eri_start}
- Current: {eri_current}
- Change: {change} ({direction})

## Top 3 Improvements
1. {topic1}: +{delta}% (now at {accuracy}%)
2. {topic2}: +{delta}% (now at {accuracy}%)
3. {topic3}: +{delta}% (now at {accuracy}%)

## Areas Needing Attention
1. {topic1}: {accuracy}% - {reason}
2. {topic2}: {accuracy}% - {reason}
3. {topic3}: {accuracy}% - {reason}

## Recommendations
- {recommendation1}
- {recommendation2}
- {recommendation3}
```

## Constraints

- Must use consistent Markdown structure
- Must include ERI trend (current vs period start)
- Must highlight top 3 improvements and top 3 concerns
- Must not include motivational language (data only)
- Report must be objective and factual
