---
name: knowledge-gap-predictor
description: Predicts future knowledge gaps using retention decay curves and practice patterns. Projects 7-day and 14-day scores, classifies risk levels (high, medium, low), and calculates prediction confidence. Use to proactively identify topics that will become weak before they actually decline.
phase: 4
category: INTELLIGENCE
priority: P2
---

# Knowledge Gap Predictor

Predicts future weak areas before they manifest by analyzing retention decay patterns, practice recency, and historical performance trajectories.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and writing predictions.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read retention data, topic stats, and learning profile
- `mcp__filesystem__write_file` - Save gap predictions

## 7-Day and 14-Day Score Projections

### Projection Model

The projection combines three factors:
1. **Retention decay** - Based on forgetting curve
2. **Practice trajectory** - Historical improvement/decline rate
3. **Coverage gap** - Topics not practiced recently

```
predicted_score(days) = current_score × decay_factor(days) + trajectory_adjustment(days)

Where:
  decay_factor(days) = e^(-decay_rate × days)
  trajectory_adjustment = trend_slope × days × trend_confidence
```

### Decay Factor Calculation

```
# From forgetting-curve-tracker data
decay_rate = retention_data[topic].decay_rate

# Calculate decay over projection period
decay_7d = e^(-decay_rate × 7)
decay_14d = e^(-decay_rate × 14)

# Apply to current score
base_7d = current_score × decay_7d
base_14d = current_score × decay_14d
```

### Trajectory Adjustment

```
# Analyze recent performance trend
recent_sessions = get_sessions_with_topic(topic, last_30_days)

If len(recent_sessions) >= 3:
  accuracies = [s.topic_accuracy for s in recent_sessions]
  trend_slope = linear_regression_slope(accuracies)

  # Calculate trend confidence based on R²
  trend_confidence = calculate_r_squared(accuracies)

  # Apply adjustment (capped to prevent extreme projections)
  trajectory_7d = min(10, max(-10, trend_slope × 7 × trend_confidence))
  trajectory_14d = min(15, max(-15, trend_slope × 14 × trend_confidence))
Else:
  # Insufficient data - no trajectory adjustment
  trajectory_7d = 0
  trajectory_14d = 0
  trend_confidence = 0
```

### Final Projection Calculation

```
predicted_score_7d = base_7d + trajectory_7d

# Ensure score stays in valid range [0, 100]
predicted_score_7d = max(0, min(100, predicted_score_7d))

predicted_score_14d = base_14d + trajectory_14d
predicted_score_14d = max(0, min(100, predicted_score_14d))

# Convert to 0-1 scale for output
predicted_score_7d_normalized = predicted_score_7d / 100
predicted_score_14d_normalized = predicted_score_14d / 100
```

## Risk Level Classification

### Risk Thresholds

| Risk Level | Criteria | Action Priority |
|------------|----------|-----------------|
| `high` | predicted_14d < 50% OR drop > 20 points | Immediate intervention |
| `medium` | predicted_14d < 70% OR drop > 10 points | Schedule revision |
| `low` | predicted_14d >= 70% AND drop <= 10 points | Monitor only |

### Classification Algorithm

```
For each topic:
  current = topic.current_accuracy / 100
  predicted_7d = predicted_score_7d_normalized
  predicted_14d = predicted_score_14d_normalized

  drop_7d = current - predicted_7d
  drop_14d = current - predicted_14d

  # High risk: Critical decline or very low projected score
  If predicted_14d < 0.50 OR drop_14d > 0.20:
    risk_level = "high"

  # Medium risk: Below threshold or moderate decline
  Elif predicted_14d < 0.70 OR drop_14d > 0.10:
    risk_level = "medium"

  # Low risk: Healthy projection
  Else:
    risk_level = "low"
```

### Contributing Factors Detection

```
contributing_factors = []

# Factor 1: No recent practice
days_since_practice = (today - topic.last_practiced).days
If days_since_practice > 14:
  contributing_factors.append("no_practice_last_14_days")
Elif days_since_practice > 7:
  contributing_factors.append("no_practice_last_7_days")

# Factor 2: High decay rate
If decay_rate > 0.10:
  contributing_factors.append("high_decay_rate")

# Factor 3: Declining trend
If trend_slope < -2:
  contributing_factors.append("declining_performance_trend")

# Factor 4: Related topics also weak
related_topics = get_related_topics(topic)
weak_related = [t for t in related_topics if t.current_accuracy < 60]
If len(weak_related) >= 2:
  contributing_factors.append("related_topics_weak")

# Factor 5: Historically difficult
If topic.historical_avg_accuracy < 55:
  contributing_factors.append("historically_difficult_topic")

# Factor 6: Low retention
If retention_score < 0.60:
  contributing_factors.append("low_current_retention")
```

## Prediction Confidence Scoring

### Confidence Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Data volume | 0.30 | Number of sessions with this topic |
| Data recency | 0.25 | How recent the data is |
| Trend stability | 0.25 | Variance in historical performance |
| Decay rate reliability | 0.20 | Quality of retention tracking |

### Confidence Calculation

```
# Data volume confidence (0-1)
session_count = count_sessions_with_topic(topic)
If session_count >= 20:
  volume_confidence = 1.0
Elif session_count >= 10:
  volume_confidence = 0.8
Elif session_count >= 5:
  volume_confidence = 0.6
Elif session_count >= 3:
  volume_confidence = 0.4
Else:
  volume_confidence = 0.2

# Data recency confidence (0-1)
days_since_last = (today - topic.last_practiced).days
If days_since_last <= 7:
  recency_confidence = 1.0
Elif days_since_last <= 14:
  recency_confidence = 0.8
Elif days_since_last <= 30:
  recency_confidence = 0.5
Else:
  recency_confidence = 0.3

# Trend stability confidence (0-1)
accuracy_variance = variance(recent_session_accuracies)
If accuracy_variance < 50:
  stability_confidence = 1.0
Elif accuracy_variance < 100:
  stability_confidence = 0.7
Elif accuracy_variance < 200:
  stability_confidence = 0.4
Else:
  stability_confidence = 0.2

# Decay rate reliability (0-1)
If retention_data exists AND revision_count >= 3:
  decay_confidence = 0.9
Elif retention_data exists:
  decay_confidence = 0.6
Else:
  decay_confidence = 0.3  # Using default decay rate

# Overall confidence
confidence = (
  volume_confidence × 0.30 +
  recency_confidence × 0.25 +
  stability_confidence × 0.25 +
  decay_confidence × 0.20
)

# Round to 2 decimal places
confidence = round(confidence, 2)
```

### Confidence Interpretation

| Confidence | Interpretation | Usage |
|------------|----------------|-------|
| >= 0.80 | High confidence | Reliable prediction |
| 0.60-0.79 | Moderate confidence | Useful but verify |
| 0.40-0.59 | Low confidence | Treat as estimate |
| < 0.40 | Very low confidence | Insufficient data |

## Recommended Action Generation

```
If risk_level == "high":
  If "no_practice_last_14_days" in contributing_factors:
    recommended_action = "schedule_immediate_review"
  Elif "declining_performance_trend" in contributing_factors:
    recommended_action = "intensive_practice_session"
  Elif "related_topics_weak" in contributing_factors:
    recommended_action = "address_prerequisite_gaps"
  Else:
    recommended_action = "urgent_intervention_needed"

Elif risk_level == "medium":
  If "no_practice_last_7_days" in contributing_factors:
    recommended_action = "schedule_revision_this_week"
  Elif "high_decay_rate" in contributing_factors:
    recommended_action = "increase_revision_frequency"
  Else:
    recommended_action = "add_to_revision_queue"

Else:  # low risk
  recommended_action = "continue_monitoring"
```

## Execution Steps

1. **Load student data**
   ```
   retention_data = read_file(memory/students/{student_id}/retention-data.json)
   topic_stats = read_file(memory/students/{student_id}/topic-stats.json)
   history = read_file(memory/students/{student_id}/history.json)
   syllabus = read_file(syllabus/{exam_type}/syllabus-structure.json)
   ```

2. **For each topic, calculate projections**
   ```
   For topic in topic_stats.topics:
     current_score = topic.accuracy
     decay_rate = get_decay_rate(topic, retention_data)
     trend_data = calculate_trend(topic, history)

     predicted_7d = project_score(current_score, decay_rate, trend_data, 7)
     predicted_14d = project_score(current_score, decay_rate, trend_data, 14)
   ```

3. **Classify risk levels**
   ```
   For each projection:
     risk_level = classify_risk(current_score, predicted_7d, predicted_14d)
   ```

4. **Identify contributing factors**
   ```
   For each topic:
     contributing_factors = detect_contributing_factors(topic, retention_data, syllabus)
   ```

5. **Calculate confidence scores**
   ```
   For each prediction:
     confidence = calculate_confidence(topic, history, retention_data)
   ```

6. **Generate recommended actions**
   ```
   For each prediction:
     recommended_action = generate_action(risk_level, contributing_factors)
   ```

7. **Build predictions output**

8. **Save gap predictions**
   ```
   write_file(memory/students/{student_id}/gap-predictions.json)
   ```

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "projection_days": {
    "type": "array",
    "default": [7, 14],
    "description": "Days ahead to project (default: 7 and 14)"
  },
  "risk_threshold": {
    "type": "number",
    "default": 0.70,
    "description": "Score below which topic is considered at risk"
  },
  "include_low_risk": {
    "type": "boolean",
    "default": false,
    "description": "Include low-risk topics in output"
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "generated_at": "string ISO 8601",
  "projection_parameters": {
    "risk_threshold": "number",
    "projection_days": [7, 14]
  },
  "predictions": [
    {
      "topic_id": "string",
      "topic_name": "string",
      "subject": "string",
      "current_score": "number 0-1",
      "predicted_score_7d": "number 0-1",
      "predicted_score_14d": "number 0-1",
      "drop_7d": "number (current - predicted_7d)",
      "drop_14d": "number (current - predicted_14d)",
      "risk_level": "high | medium | low",
      "contributing_factors": ["string factors"],
      "recommended_action": "string action",
      "confidence": "number 0-1",
      "confidence_level": "high | moderate | low | very_low",
      "days_since_practice": "integer",
      "decay_rate": "number"
    }
  ],
  "summary": {
    "total_topics_analyzed": "integer",
    "high_risk_count": "integer",
    "medium_risk_count": "integer",
    "low_risk_count": "integer",
    "average_confidence": "number 0-1",
    "topics_needing_immediate_attention": ["string topic_ids"],
    "estimated_study_hours_to_address": "number"
  },
  "alerts": [
    {
      "type": "critical_gap | approaching_gap | cluster_weakness",
      "topics": ["string topic_ids"],
      "message": "string",
      "urgency": "immediate | this_week | this_month"
    }
  ]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/retention-data.json` |
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `memory/students/{student_id}/history.json` |
| Read | `syllabus/{exam_type}/syllabus-structure.json` |
| Write | `memory/students/{student_id}/gap-predictions.json` |

## Alert Generation

```
alerts = []

# Critical gap alert
critical_topics = [p for p in predictions if p.risk_level == "high" AND p.confidence >= 0.60]
If len(critical_topics) > 0:
  alerts.append({
    "type": "critical_gap",
    "topics": [t.topic_id for t in critical_topics],
    "message": f"{len(critical_topics)} topics predicted to fall below 50% within 14 days",
    "urgency": "immediate"
  })

# Approaching gap alert
approaching_topics = [p for p in predictions if p.risk_level == "medium" AND p.drop_14d > 0.15]
If len(approaching_topics) > 0:
  alerts.append({
    "type": "approaching_gap",
    "topics": [t.topic_id for t in approaching_topics],
    "message": f"{len(approaching_topics)} topics showing significant decline trajectory",
    "urgency": "this_week"
  })

# Cluster weakness alert (multiple related topics at risk)
subjects_at_risk = group_by(high_risk_predictions, subject)
For subject, topics in subjects_at_risk:
  If len(topics) >= 3:
    alerts.append({
      "type": "cluster_weakness",
      "topics": [t.topic_id for t in topics],
      "message": f"Cluster weakness detected in {subject}: {len(topics)} related topics at risk",
      "urgency": "this_week"
    })
```

## Example Output

```json
{
  "student_id": "student_123",
  "generated_at": "2025-02-03T12:30:00Z",
  "projection_parameters": {
    "risk_threshold": 0.70,
    "projection_days": [7, 14]
  },
  "predictions": [
    {
      "topic_id": "constitutional_amendments",
      "topic_name": "Constitutional Amendments",
      "subject": "pakistan_studies",
      "current_score": 0.58,
      "predicted_score_7d": 0.47,
      "predicted_score_14d": 0.38,
      "drop_7d": 0.11,
      "drop_14d": 0.20,
      "risk_level": "high",
      "contributing_factors": [
        "no_practice_last_14_days",
        "high_decay_rate",
        "related_topics_weak"
      ],
      "recommended_action": "schedule_immediate_review",
      "confidence": 0.78,
      "confidence_level": "moderate",
      "days_since_practice": 16,
      "decay_rate": 0.085
    },
    {
      "topic_id": "federal_structure",
      "topic_name": "Federal Structure",
      "subject": "pakistan_studies",
      "current_score": 0.72,
      "predicted_score_7d": 0.65,
      "predicted_score_14d": 0.58,
      "drop_7d": 0.07,
      "drop_14d": 0.14,
      "risk_level": "medium",
      "contributing_factors": [
        "no_practice_last_7_days",
        "declining_performance_trend"
      ],
      "recommended_action": "schedule_revision_this_week",
      "confidence": 0.82,
      "confidence_level": "high",
      "days_since_practice": 9,
      "decay_rate": 0.055
    }
  ],
  "summary": {
    "total_topics_analyzed": 25,
    "high_risk_count": 3,
    "medium_risk_count": 7,
    "low_risk_count": 15,
    "average_confidence": 0.72,
    "topics_needing_immediate_attention": ["constitutional_amendments", "islamic_history", "sindh_geography"],
    "estimated_study_hours_to_address": 4.5
  },
  "alerts": [
    {
      "type": "critical_gap",
      "topics": ["constitutional_amendments", "islamic_history", "sindh_geography"],
      "message": "3 topics predicted to fall below 50% within 14 days",
      "urgency": "immediate"
    },
    {
      "type": "cluster_weakness",
      "topics": ["constitutional_amendments", "federal_structure", "provincial_autonomy"],
      "message": "Cluster weakness detected in pakistan_studies: 3 related topics at risk",
      "urgency": "this_week"
    }
  ]
}
```

## Constraints

- Predictions must include confidence scores
- High-risk predictions require confidence >= 0.40 to be actionable
- Must handle topics with no retention data (use default decay rate)
- Must identify cluster weaknesses (related topics)
- Projections capped at valid range [0, 1]
- Must generate alerts for critical situations

## Usage Notes

- Run daily or after each session to keep predictions current
- Feed high-risk predictions into autonomous-session-initiator
- Use alerts to trigger proactive interventions
- Combine with deep-dive-analyzer for root cause analysis
- Track prediction accuracy over time to improve model
