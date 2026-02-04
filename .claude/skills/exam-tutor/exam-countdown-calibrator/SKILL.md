---
name: exam-countdown-calibrator
description: Calibrates urgency levels and session frequency based on days until exam. Implements final readiness band determination (exam_ready, ready, approaching) and calculates confidence intervals for predicted real exam scores. Use to adjust preparation intensity as exam approaches.
phase: 4
category: AUTONOMY
priority: P4
---

# Exam Countdown Calibrator

Dynamically adjusts preparation intensity, session frequency, and content focus based on proximity to exam date.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and writing urgency configuration.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read student profile, ERI, mock exam results
- `mcp__filesystem__write_file` - Save urgency configuration

## Urgency Scaling Based on Days Until Exam

### Urgency Levels

| Level | Days Until Exam | Multiplier | Focus |
|-------|-----------------|------------|-------|
| `relaxed` | > 90 days | 0.8x | Broad coverage, foundation building |
| `normal` | 61-90 days | 1.0x | Balanced practice, weak area focus |
| `elevated` | 31-60 days | 1.3x | Intensive weak area work, mock exams |
| `high` | 15-30 days | 1.5x | Mock exams, revision cycles |
| `critical` | 8-14 days | 1.8x | Rapid revision, confidence building |
| `final_push` | 1-7 days | 2.0x | Light review, stress management |

### Urgency Calculation

```
days_until_exam = (target_exam_date - today).days

If days_until_exam > 90:
  urgency_level = "relaxed"
  urgency_multiplier = 0.8
Elif days_until_exam > 60:
  urgency_level = "normal"
  urgency_multiplier = 1.0
Elif days_until_exam > 30:
  urgency_level = "elevated"
  urgency_multiplier = 1.3
Elif days_until_exam > 14:
  urgency_level = "high"
  urgency_multiplier = 1.5
Elif days_until_exam > 7:
  urgency_level = "critical"
  urgency_multiplier = 1.8
Else:
  urgency_level = "final_push"
  urgency_multiplier = 2.0

# Handle no exam date set
If target_exam_date is null:
  urgency_level = "normal"
  urgency_multiplier = 1.0
  days_until_exam = null
```

## Session Frequency Adjustment

### Base Frequencies

```
base_sessions_per_week = student.preferences.target_sessions_per_week OR 5

# Adjust based on urgency
adjusted_frequency = base_sessions_per_week × urgency_multiplier

# Cap at reasonable limits
min_sessions = 3
max_sessions = 14  # 2 per day maximum
adjusted_frequency = max(min_sessions, min(max_sessions, adjusted_frequency))
```

### Session Duration Adjustment

```
base_duration = student.preferences.session_duration_minutes OR 30

# Urgency-based duration adjustment
If urgency_level in ["relaxed", "normal"]:
  duration_factor = 1.0
Elif urgency_level == "elevated":
  duration_factor = 1.1
Elif urgency_level == "high":
  duration_factor = 1.2
Elif urgency_level == "critical":
  duration_factor = 1.0  # Keep shorter to avoid burnout
Else:  # final_push
  duration_factor = 0.8  # Light sessions only

adjusted_duration = round(base_duration × duration_factor)
```

### Content Mix by Urgency

```
content_mix = {
  "relaxed": {
    "new_topics": 0.40,
    "weak_area_practice": 0.30,
    "revision": 0.20,
    "mock_exams": 0.10
  },
  "normal": {
    "new_topics": 0.25,
    "weak_area_practice": 0.35,
    "revision": 0.25,
    "mock_exams": 0.15
  },
  "elevated": {
    "new_topics": 0.10,
    "weak_area_practice": 0.40,
    "revision": 0.30,
    "mock_exams": 0.20
  },
  "high": {
    "new_topics": 0.05,
    "weak_area_practice": 0.30,
    "revision": 0.35,
    "mock_exams": 0.30
  },
  "critical": {
    "new_topics": 0.00,
    "weak_area_practice": 0.25,
    "revision": 0.45,
    "mock_exams": 0.30
  },
  "final_push": {
    "new_topics": 0.00,
    "weak_area_practice": 0.10,
    "revision": 0.60,
    "mock_exams": 0.10,
    "rest_and_confidence": 0.20
  }
}
```

## Final Readiness Band Determination

### Readiness Calculation

```
# Inputs
current_eri = student.eri.current_score
mock_average = average(last_3_mock_scores) OR current_eri
mock_trend = calculate_trend(mock_scores)
coverage_score = student.eri.components.coverage.value
consistency_score = student.eri.components.consistency.value

# Weighted readiness score
readiness_score = (
  current_eri × 0.35 +
  mock_average × 0.35 +
  coverage_score × 0.15 +
  consistency_score × 0.15
)

# Trend adjustment
If mock_trend == "improving":
  readiness_score += 3
Elif mock_trend == "declining":
  readiness_score -= 5
```

### Readiness Bands

| Band | Score Range | Meaning | Recommendation |
|------|-------------|---------|----------------|
| `exam_ready` | >= 80 | Strong preparation | Maintain and build confidence |
| `ready` | 70-79 | Good preparation | Focus on weak spots |
| `approaching` | 60-69 | Moderate readiness | Intensive practice needed |
| `developing` | 50-59 | Building knowledge | Significant work required |
| `not_ready` | < 50 | Major gaps | Consider postponing exam |

### Band Assignment

```
If readiness_score >= 80:
  readiness_band = "exam_ready"
  can_take_exam = True
  confidence_level = "high"
Elif readiness_score >= 70:
  readiness_band = "ready"
  can_take_exam = True
  confidence_level = "moderate"
Elif readiness_score >= 60:
  readiness_band = "approaching"
  can_take_exam = True
  confidence_level = "cautious"
Elif readiness_score >= 50:
  readiness_band = "developing"
  can_take_exam = False
  confidence_level = "low"
Else:
  readiness_band = "not_ready"
  can_take_exam = False
  confidence_level = "very_low"
```

## Confidence Interval Calculation for Predicted Score

### Prediction Model

```
# Base prediction from mock exams and ERI
If mock_count >= 3:
  base_prediction = weighted_average(mock_scores, weights=[0.5, 0.3, 0.2])  # Recent weighted more
Elif mock_count >= 1:
  base_prediction = average(mock_scores)
Else:
  base_prediction = current_eri × 0.85  # Conservative estimate without mocks

# Apply exam day factor (typical pressure decline)
exam_day_adjustment = -5  # Points typically lost under real exam pressure
predicted_score = base_prediction + exam_day_adjustment

# Clamp to valid range
predicted_score = max(0, min(100, predicted_score))
```

### Confidence Interval Calculation

```
# Standard deviation from available data
If mock_count >= 3:
  std_dev = standard_deviation(mock_scores)
Elif mock_count >= 1:
  std_dev = 10  # Default uncertainty with limited data
Else:
  std_dev = 15  # High uncertainty without mock data

# Sample size factor (more mocks = tighter confidence)
If mock_count >= 5:
  sample_factor = 1.0
Elif mock_count >= 3:
  sample_factor = 1.2
Elif mock_count >= 1:
  sample_factor = 1.5
Else:
  sample_factor = 2.0

# Calculate margin of error (95% confidence)
z_score = 1.96  # 95% confidence
margin = z_score × std_dev × sample_factor / sqrt(max(1, mock_count))

# Confidence interval
confidence_interval = [
  max(0, predicted_score - margin),
  min(100, predicted_score + margin)
]

# Interval width indicates confidence
interval_width = confidence_interval[1] - confidence_interval[0]
If interval_width <= 10:
  prediction_confidence = "high"
Elif interval_width <= 20:
  prediction_confidence = "moderate"
Else:
  prediction_confidence = "low"
```

### Prediction Quality Factors

```
prediction_quality = {
  "mock_exam_count": mock_count,
  "mock_recency_days": days_since_last_mock,
  "score_consistency": 100 - (std_dev × 2),  # Lower variance = higher consistency
  "coverage_completeness": coverage_score,
  "data_quality_score": calculate_data_quality(mock_count, std_dev, coverage_score)
}

calculate_data_quality(mock_count, std_dev, coverage):
  If mock_count >= 3 AND std_dev < 8 AND coverage >= 80:
    return "excellent"
  Elif mock_count >= 2 AND std_dev < 12 AND coverage >= 60:
    return "good"
  Elif mock_count >= 1:
    return "fair"
  Else:
    return "limited"
```

## Execution Steps

1. **Load student data**
   ```
   profile = read_file(memory/students/{student_id}/profile.json)
   eri = read_file(memory/students/{student_id}/eri.json)
   mock_history = read_file(memory/students/{student_id}/mock-exams/*.json)
   ```

2. **Calculate days until exam**
   ```
   days_until_exam = calculate_days_until(profile.target_exam_date)
   ```

3. **Determine urgency level**
   ```
   urgency = calculate_urgency(days_until_exam)
   ```

4. **Adjust session frequency**
   ```
   frequency = adjust_frequency(urgency, profile.preferences)
   ```

5. **Determine content mix**
   ```
   content_mix = get_content_mix(urgency.level)
   ```

6. **Calculate readiness band**
   ```
   readiness = calculate_readiness(eri, mock_history)
   ```

7. **Calculate prediction with confidence interval**
   ```
   prediction = calculate_prediction(mock_history, eri)
   confidence_interval = calculate_confidence_interval(mock_history, prediction)
   ```

8. **Generate recommendations**

9. **Save urgency configuration**
   ```
   write_file(memory/students/{student_id}/urgency-config.json)
   ```

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "target_exam_date": {
    "type": "string",
    "format": "ISO 8601",
    "required": false,
    "description": "Override exam date (uses profile date if not provided)"
  },
  "include_prediction": {
    "type": "boolean",
    "default": true,
    "description": "Include score prediction with confidence interval"
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "calculated_at": "string ISO 8601",
  "exam_date": "string ISO 8601 | null",
  "days_until_exam": "integer | null",
  "urgency": {
    "level": "relaxed | normal | elevated | high | critical | final_push",
    "multiplier": "number",
    "description": "string"
  },
  "session_adjustments": {
    "base_sessions_per_week": "integer",
    "adjusted_sessions_per_week": "integer",
    "base_duration_minutes": "integer",
    "adjusted_duration_minutes": "integer",
    "content_mix": {
      "new_topics": "number 0-1",
      "weak_area_practice": "number 0-1",
      "revision": "number 0-1",
      "mock_exams": "number 0-1",
      "rest_and_confidence": "number 0-1 (final_push only)"
    }
  },
  "readiness": {
    "score": "number 0-100",
    "band": "exam_ready | ready | approaching | developing | not_ready",
    "can_take_exam": "boolean",
    "confidence_level": "high | moderate | cautious | low | very_low",
    "components": {
      "eri_contribution": "number",
      "mock_contribution": "number",
      "coverage_contribution": "number",
      "consistency_contribution": "number"
    }
  },
  "prediction": {
    "predicted_score": "number 0-100",
    "confidence_interval": ["number lower", "number upper"],
    "interval_width": "number",
    "prediction_confidence": "high | moderate | low",
    "data_quality": "excellent | good | fair | limited",
    "factors": {
      "mock_exam_count": "integer",
      "mock_recency_days": "integer",
      "score_consistency": "number 0-100"
    }
  },
  "recommendations": [
    {
      "type": "frequency | content | timing | strategy",
      "message": "string",
      "priority": "high | medium | low"
    }
  ],
  "milestones": [
    {
      "days_before_exam": "integer",
      "target_eri": "number",
      "target_mock_score": "number",
      "focus": "string"
    }
  ]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/profile.json` |
| Read | `memory/students/{student_id}/eri.json` |
| Read | `memory/students/{student_id}/mock-exams/*.json` |
| Write | `memory/students/{student_id}/urgency-config.json` |

## Urgency Config Schema

Location: `memory/students/{student_id}/urgency-config.json`

```json
{
  "$schema": "exam-tutor/urgency-config/v1",
  "student_id": "string (required)",
  "exam_date": "string ISO 8601 | null",
  "days_until_exam": "integer | null",
  "urgency_level": "relaxed | normal | elevated | high | critical | final_push (required)",
  "urgency_multiplier": "number (required)",
  "adjusted_sessions_per_week": "integer (required)",
  "adjusted_duration_minutes": "integer (required)",
  "content_mix": {
    "new_topics": "number",
    "weak_area_practice": "number",
    "revision": "number",
    "mock_exams": "number"
  },
  "readiness_band": "string (required)",
  "predicted_score": "number (required)",
  "confidence_interval": ["number", "number"],
  "calculated_at": "string ISO 8601 (required)"
}
```

## Milestone Generation

```
If days_until_exam is not null:
  milestones = []

  # 30-day milestone
  If days_until_exam > 30:
    milestones.append({
      "days_before_exam": 30,
      "target_eri": current_eri + 10,
      "target_mock_score": current_eri + 5,
      "focus": "Complete coverage of weak areas"
    })

  # 14-day milestone
  If days_until_exam > 14:
    milestones.append({
      "days_before_exam": 14,
      "target_eri": max(70, current_eri + 5),
      "target_mock_score": max(70, current_eri),
      "focus": "Mock exam performance and revision"
    })

  # 7-day milestone
  If days_until_exam > 7:
    milestones.append({
      "days_before_exam": 7,
      "target_eri": max(75, current_eri),
      "target_mock_score": max(72, current_eri),
      "focus": "Final revision and confidence building"
    })

  # 1-day milestone
  milestones.append({
    "days_before_exam": 1,
    "target_eri": "maintain",
    "target_mock_score": "N/A",
    "focus": "Rest, light review, stress management"
  })
```

## Example Output

```json
{
  "student_id": "student_123",
  "calculated_at": "2025-02-03T16:00:00Z",
  "exam_date": "2025-03-15T09:00:00Z",
  "days_until_exam": 40,
  "urgency": {
    "level": "elevated",
    "multiplier": 1.3,
    "description": "Intensive preparation phase - focus on weak areas and mock exams"
  },
  "session_adjustments": {
    "base_sessions_per_week": 5,
    "adjusted_sessions_per_week": 7,
    "base_duration_minutes": 30,
    "adjusted_duration_minutes": 33,
    "content_mix": {
      "new_topics": 0.10,
      "weak_area_practice": 0.40,
      "revision": 0.30,
      "mock_exams": 0.20
    }
  },
  "readiness": {
    "score": 68,
    "band": "approaching",
    "can_take_exam": true,
    "confidence_level": "cautious",
    "components": {
      "eri_contribution": 23.8,
      "mock_contribution": 24.5,
      "coverage_contribution": 10.5,
      "consistency_contribution": 9.2
    }
  },
  "prediction": {
    "predicted_score": 65,
    "confidence_interval": [58, 72],
    "interval_width": 14,
    "prediction_confidence": "moderate",
    "data_quality": "good",
    "factors": {
      "mock_exam_count": 3,
      "mock_recency_days": 5,
      "score_consistency": 82
    }
  },
  "recommendations": [
    {
      "type": "frequency",
      "message": "Increase to 7 sessions per week for the next 40 days",
      "priority": "high"
    },
    {
      "type": "content",
      "message": "Focus 40% of time on weak areas, 30% on revision",
      "priority": "high"
    },
    {
      "type": "strategy",
      "message": "Schedule at least 1 mock exam per week until exam day",
      "priority": "medium"
    }
  ],
  "milestones": [
    {
      "days_before_exam": 30,
      "target_eri": 75,
      "target_mock_score": 72,
      "focus": "Complete coverage of weak areas"
    },
    {
      "days_before_exam": 14,
      "target_eri": 78,
      "target_mock_score": 75,
      "focus": "Mock exam performance and revision"
    },
    {
      "days_before_exam": 7,
      "target_eri": 80,
      "target_mock_score": 77,
      "focus": "Final revision and confidence building"
    }
  ]
}
```

## Constraints

- Urgency multiplier capped at 2.0x to prevent burnout
- Session frequency capped at 14/week (2/day max)
- Confidence interval must widen with less data
- Readiness band must account for trend direction
- Final push phase must include rest component
- Predictions require at least ERI data (mocks optional but improve quality)

## Usage Notes

- Recalculate daily as exam approaches
- Feed into study-pattern-optimizer for schedule adjustments
- Use milestones to track progress checkpoints
- Adjust recommendations if student consistently misses targets
- Consider student stress levels in final_push phase
