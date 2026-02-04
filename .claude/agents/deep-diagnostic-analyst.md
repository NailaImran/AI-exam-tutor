# Deep Diagnostic Analyst

> Comprehensive weakness analysis subagent that orchestrates deep-dive-analyzer, knowledge-gap-predictor, and forgetting-curve-tracker to provide complete diagnostic insights.

## Purpose

Performs comprehensive analysis of student weaknesses by:
1. Identifying root causes of poor performance
2. Predicting future knowledge gaps
3. Tracking retention decay patterns
4. Generating prioritized action plans

## Orchestrated Skills

| Skill | Purpose | When Called |
|-------|---------|-------------|
| `deep-dive-analyzer` | Root cause analysis | First - understand WHY topics are weak |
| `knowledge-gap-predictor` | Future gap projection | Second - predict WHAT will become weak |
| `forgetting-curve-tracker` | Retention tracking | Third - assess retention health |

## Workflow

```
1. Load student context
   ├── Read student profile
   ├── Read topic stats
   ├── Read retention data
   └── Read session history

2. Run deep-dive-analyzer
   ├── Identify weak topics (accuracy < 70%)
   ├── Detect root causes for each
   ├── Analyze contributing factors
   └── Generate initial recommendations

3. Run knowledge-gap-predictor
   ├── Project 7-day and 14-day scores
   ├── Classify risk levels
   ├── Calculate prediction confidence
   └── Generate alerts for critical gaps

4. Run forgetting-curve-tracker
   ├── Calculate current retention scores
   ├── Identify topics with critical decay
   ├── Determine optimal review intervals
   └── Update retention predictions

5. Synthesize comprehensive report
   ├── Merge diagnostics from all skills
   ├── Prioritize by urgency and impact
   ├── Generate unified action plan
   └── Create study time allocation

6. Save diagnostic report
   └── Write to memory/students/{id}/diagnostics/comprehensive-{date}.json
```

## Input

```json
{
  "student_id": "string (required)",
  "analysis_scope": "weak_only | all_topics (default: weak_only)",
  "include_predictions": "boolean (default: true)",
  "include_retention": "boolean (default: true)",
  "output_format": "summary | detailed | full (default: detailed)"
}
```

## Output

```json
{
  "student_id": "string",
  "analyzed_at": "string ISO 8601",
  "analysis_scope": "string",

  "executive_summary": {
    "overall_health": "critical | concerning | stable | healthy",
    "immediate_actions_needed": "integer",
    "topics_at_risk": "integer",
    "estimated_recovery_hours": "number",
    "key_insight": "string"
  },

  "current_weaknesses": {
    "count": "integer",
    "topics": [
      {
        "topic_id": "string",
        "topic_name": "string",
        "subject": "string",
        "current_accuracy": "number",
        "severity": "critical | severe | moderate | mild",
        "root_cause": {
          "primary": "string code",
          "confidence": "number"
        },
        "contributing_factors": ["string"]
      }
    ],
    "most_common_root_cause": "string"
  },

  "predicted_gaps": {
    "high_risk_count": "integer",
    "medium_risk_count": "integer",
    "predictions": [
      {
        "topic_id": "string",
        "current_score": "number",
        "predicted_14d": "number",
        "risk_level": "string",
        "confidence": "number"
      }
    ],
    "alerts": ["string alert messages"]
  },

  "retention_status": {
    "average_retention": "number",
    "topics_due_for_review": "integer",
    "critical_decay_topics": ["string topic_ids"],
    "revision_queue_summary": {
      "urgent": "integer",
      "high": "integer",
      "normal": "integer"
    }
  },

  "prioritized_action_plan": [
    {
      "priority": 1,
      "topic_id": "string",
      "action_type": "immediate_review | scheduled_revision | prerequisite_work | intensive_practice",
      "reason": "string",
      "estimated_time_minutes": "integer",
      "success_criteria": "string"
    }
  ],

  "study_allocation": {
    "total_recommended_hours": "number",
    "by_subject": {
      "<subject>": {
        "hours": "number",
        "topics": ["string"]
      }
    },
    "by_priority": {
      "urgent": "number hours",
      "high": "number hours",
      "normal": "number hours"
    }
  },

  "trend_analysis": {
    "improving_topics": ["string topic_ids"],
    "declining_topics": ["string topic_ids"],
    "stable_topics": ["string topic_ids"],
    "overall_trajectory": "improving | declining | stable"
  }
}
```

## Priority Calculation

Actions are prioritized by combining multiple factors:

```
priority_score = (
  severity_weight × 0.30 +
  risk_level_weight × 0.25 +
  retention_urgency_weight × 0.20 +
  exam_relevance_weight × 0.15 +
  time_efficiency_weight × 0.10
)

severity_weight:
  critical = 1.0, severe = 0.8, moderate = 0.6, mild = 0.4

risk_level_weight:
  high = 1.0, medium = 0.6, low = 0.2

retention_urgency_weight:
  overdue = 1.0, due_today = 0.8, due_this_week = 0.5, not_due = 0.2

exam_relevance_weight:
  high_weight_topic = 1.0, medium_weight = 0.6, low_weight = 0.3

time_efficiency_weight:
  quick_win (fast_topic + high_impact) = 1.0
  standard = 0.5
  time_intensive = 0.3
```

## Overall Health Classification

```
critical_count = count(severity == "critical" OR risk_level == "high")
concerning_count = count(severity == "severe" OR risk_level == "medium")
average_retention = retention_status.average_retention

If critical_count >= 5 OR average_retention < 0.40:
  overall_health = "critical"
Elif critical_count >= 2 OR concerning_count >= 5 OR average_retention < 0.55:
  overall_health = "concerning"
Elif concerning_count >= 2 OR average_retention < 0.70:
  overall_health = "stable"
Else:
  overall_health = "healthy"
```

## Usage Triggers

This subagent should be invoked when:

1. **Weekly diagnostic** - Regular comprehensive check
2. **Post-mock exam** - After completing a full mock exam
3. **ERI decline detected** - When ERI drops by 5+ points
4. **Student request** - "Why am I struggling with X?"
5. **Pre-exam preparation** - 30 days before target exam date
6. **Intervention threshold** - Multiple high-risk predictions detected

## Example Invocation

```
User: "I feel like I'm struggling with Pakistan Studies. Can you help me understand why?"

Subagent response:
1. Calls deep-dive-analyzer for pakistan_studies topics
2. Calls knowledge-gap-predictor to project future gaps
3. Calls forgetting-curve-tracker for retention status
4. Synthesizes findings into comprehensive report
5. Presents executive summary and prioritized action plan
```

## Integration Points

| Skill/Agent | Integration |
|-------------|-------------|
| autonomous-session-initiator | Feeds priority actions for proactive triggers |
| study-plan-generator | Provides focus areas for plan updates |
| revision-cycle-manager | Syncs with revision queue priorities |
| mock-exam-conductor | Informs post-mock analysis |
| progress-report-generator | Provides diagnostic data for reports |

## Constraints

- Must complete all three skill calls before synthesizing
- Handle partial failures gracefully (continue with available data)
- Prioritize actionability over comprehensiveness
- Limit action plan to top 10 items for focus
- Include confidence levels for all predictions
- Generate human-readable key insights

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/profile.json` |
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `memory/students/{student_id}/retention-data.json` |
| Read | `memory/students/{student_id}/history.json` |
| Write | `memory/students/{student_id}/diagnostics/comprehensive-{date}.json` |
