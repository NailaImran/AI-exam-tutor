---
name: exam-pressure-simulator
description: Simulates real exam pressure conditions with configurable levels (standard, high, extreme). Tracks response_to_pressure profile and integrates with fatigue detection. Use during mock exams to assess student performance under realistic conditions.
phase: 4
category: MASTERY
priority: P3
---

# Exam Pressure Simulator

Simulates real exam conditions by introducing time pressure, reduced review opportunities, and stress-inducing elements to assess student performance under pressure.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and writing pressure profiles.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read student profile and learning profile
- `mcp__filesystem__write_file` - Update pressure response profile

## Pressure Levels

### Level Definitions

| Level | Time Factor | Review Allowed | Skipping | Stress Elements |
|-------|-------------|----------------|----------|-----------------|
| `standard` | 1.0x (full time) | Yes, unlimited | Yes | None |
| `high` | 0.85x (reduced time) | Yes, limited (2x per question) | Limited (5 max) | Timer warning at 50%, 25% |
| `extreme` | 0.70x (severe reduction) | No | No | Timer warning every 10%, countdown beeps |

### Pressure Configuration

```json
{
  "standard": {
    "time_factor": 1.0,
    "time_per_question_seconds": 108,
    "review_allowed": true,
    "review_limit": null,
    "skip_allowed": true,
    "skip_limit": null,
    "timer_warnings": [],
    "stress_elements": []
  },
  "high": {
    "time_factor": 0.85,
    "time_per_question_seconds": 92,
    "review_allowed": true,
    "review_limit": 2,
    "skip_allowed": true,
    "skip_limit": 5,
    "timer_warnings": [0.50, 0.25],
    "stress_elements": ["timer_visible", "progress_bar"]
  },
  "extreme": {
    "time_factor": 0.70,
    "time_per_question_seconds": 76,
    "review_allowed": false,
    "review_limit": 0,
    "skip_allowed": false,
    "skip_limit": 0,
    "timer_warnings": [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10],
    "stress_elements": ["timer_visible", "progress_bar", "countdown_prominent", "no_going_back"]
  }
}
```

### Time Calculation

```
# Standard PPSC exam: 100 questions in 180 minutes
base_time_per_question = 108 seconds  # (180 × 60) / 100

For pressure_level:
  adjusted_time = base_time_per_question × time_factor
  total_exam_time = adjusted_time × total_questions

Example:
  standard: 108s × 100 = 10,800s = 180 min
  high: 92s × 100 = 9,200s = 153 min
  extreme: 76s × 100 = 7,600s = 127 min
```

## Response to Pressure Profile Tracking

### Performance Metrics Under Pressure

```
For each mock exam with pressure simulation:
  metrics = {
    "pressure_level": level,
    "baseline_accuracy": accuracy from standard mocks,
    "pressured_accuracy": accuracy in this mock,
    "accuracy_delta": pressured - baseline,
    "completion_rate": questions_answered / total_questions,
    "time_management": {
      "avg_time_per_question": calculated,
      "rushed_answers": count where time < 30s,
      "timeout_answers": count where time >= limit
    },
    "behavior_indicators": {
      "review_attempts": count (if allowed),
      "skip_attempts": count (if allowed),
      "changed_answers": count
    }
  }
```

### Response Classification

```
accuracy_delta = pressured_accuracy - baseline_accuracy

If accuracy_delta >= -5:
  response_to_pressure = "high"
  # Performs well under pressure, minimal decline
  recommendation = "Can handle real exam conditions"

Elif accuracy_delta >= -15:
  response_to_pressure = "moderate"
  # Some decline but manageable
  recommendation = "Practice more timed tests to build resilience"

Else:
  response_to_pressure = "low"
  # Significant decline under pressure
  recommendation = "Focus on stress management and time-boxing practice"
```

### Profile Update Algorithm

```
# Weighted moving average of pressure responses
For each new mock exam result:
  current_response = calculate_response(mock_result)

  If existing profile exists:
    # Weight recent results more heavily
    weight_new = 0.4
    weight_old = 0.6

    # Update classification thresholds
    avg_delta = (existing.avg_delta × weight_old) + (current_response.delta × weight_new)

    # Reclassify based on updated average
    response_to_pressure = classify_response(avg_delta)

  Else:
    # First mock - use current result
    response_to_pressure = current_response.classification

  # Update profile
  profile.response_to_pressure = response_to_pressure
  profile.pressure_history.append(current_response)
```

## Fatigue Detection Integration

### Tracking Fatigue Points

```
# Integrate with mock-exam-evaluator fatigue detection

For mock exam with pressure simulation:
  # Calculate accuracy by 10-question blocks
  block_accuracies = calculate_block_accuracies(answers)

  # Detect fatigue onset
  fatigue_detected_at = null
  For i in range(len(blocks) - 2):
    If blocks[i+1] < blocks[i] - 5 AND blocks[i+2] < blocks[i+1] - 5:
      fatigue_detected_at = (i + 1) × 10 + 1
      break

  # Compare fatigue points across pressure levels
  fatigue_comparison = {
    "standard_fatigue_point": from standard mocks,
    "pressured_fatigue_point": fatigue_detected_at,
    "fatigue_acceleration": standard_point - pressured_point
  }

  # Fatigue acceleration indicates how much sooner fatigue sets in under pressure
  If fatigue_acceleration > 20:
    fatigue_sensitivity = "high"  # Fatigues much faster under pressure
  Elif fatigue_acceleration > 10:
    fatigue_sensitivity = "moderate"
  Else:
    fatigue_sensitivity = "low"  # Resilient to pressure-induced fatigue
```

### Fatigue-Pressure Correlation

```
# Track relationship between pressure and fatigue

correlation_data = {
  "pressure_level": level,
  "fatigue_point": question number,
  "post_fatigue_accuracy": accuracy after fatigue point,
  "pre_fatigue_accuracy": accuracy before fatigue point,
  "fatigue_impact": pre - post
}

# Use for recommendations
If fatigue_sensitivity == "high" AND response_to_pressure == "low":
  recommendation = "Consider breaking study into shorter sessions and practice pacing strategies"
```

## Execution Steps

1. **Load student context**
   ```
   profile = read_file(memory/students/{student_id}/profile.json)
   learning_profile = read_file(memory/students/{student_id}/learning-profile.json)
   mock_history = read_file(memory/students/{student_id}/mock-exams/*.json)
   ```

2. **Configure pressure settings**
   ```
   pressure_config = get_pressure_config(pressure_level)
   adjusted_time = calculate_adjusted_time(pressure_config)
   ```

3. **Generate pressure parameters for mock**
   ```
   exam_config = {
     "total_time_seconds": adjusted_time × total_questions,
     "time_per_question_seconds": adjusted_time,
     "review_settings": pressure_config.review_settings,
     "skip_settings": pressure_config.skip_settings,
     "ui_elements": pressure_config.stress_elements
   }
   ```

4. **Track performance during exam** (called by mock-exam-conductor)
   ```
   For each answer:
     Record time_taken
     Record review_attempts
     Record if changed
   ```

5. **Calculate pressure response metrics** (post-exam)
   ```
   metrics = calculate_pressure_metrics(exam_result, baseline_data)
   response_classification = classify_response(metrics)
   ```

6. **Update pressure profile**
   ```
   Update learning_profile.response_to_pressure
   Append to pressure_history
   ```

7. **Integrate fatigue data**
   ```
   fatigue_data = get_fatigue_from_evaluator(exam_result)
   fatigue_correlation = calculate_fatigue_pressure_correlation(fatigue_data, pressure_level)
   ```

8. **Generate recommendations**

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "action": {
    "type": "string",
    "enum": ["configure", "track_response", "update_profile", "get_recommendations"],
    "required": true
  },
  "pressure_level": {
    "type": "string",
    "enum": ["standard", "high", "extreme"],
    "required": false,
    "description": "Required for configure action"
  },
  "mock_exam_result": {
    "type": "object",
    "required": false,
    "description": "Required for track_response action"
  }
}
```

## Output Schema

### Configure Action Output

```json
{
  "student_id": "string",
  "pressure_level": "standard | high | extreme",
  "exam_config": {
    "total_time_minutes": "integer",
    "time_per_question_seconds": "integer",
    "review_allowed": "boolean",
    "review_limit": "integer | null",
    "skip_allowed": "boolean",
    "skip_limit": "integer | null",
    "timer_warnings_at": ["number percentages"],
    "stress_elements": ["string elements"]
  },
  "recommendations_for_level": "string"
}
```

### Track Response Output

```json
{
  "student_id": "string",
  "mock_session_id": "string",
  "pressure_level": "string",
  "performance_metrics": {
    "baseline_accuracy": "number 0-100",
    "pressured_accuracy": "number 0-100",
    "accuracy_delta": "number",
    "completion_rate": "number 0-1",
    "time_management": {
      "avg_time_per_question": "number seconds",
      "rushed_answers": "integer",
      "timeout_answers": "integer"
    }
  },
  "response_classification": {
    "response_to_pressure": "low | moderate | high",
    "confidence": "number 0-1",
    "trend": "improving | stable | declining"
  },
  "fatigue_analysis": {
    "fatigue_detected_at_question": "integer | null",
    "fatigue_acceleration": "integer (vs standard)",
    "fatigue_sensitivity": "low | moderate | high"
  },
  "recommendations": ["string recommendations"]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/profile.json` |
| Read | `memory/students/{student_id}/learning-profile.json` |
| Read | `memory/students/{student_id}/mock-exams/*.json` |
| Write | `memory/students/{student_id}/learning-profile.json` (update response_to_pressure) |

## Pressure Response History Schema

Added to learning-profile.json:

```json
{
  "pressure_response_history": [
    {
      "mock_session_id": "string",
      "date": "string ISO 8601",
      "pressure_level": "standard | high | extreme",
      "baseline_accuracy": "number",
      "pressured_accuracy": "number",
      "accuracy_delta": "number",
      "fatigue_point": "integer | null",
      "classification": "low | moderate | high"
    }
  ]
}
```

## Recommendations by Profile

```
If response_to_pressure == "high":
  recommendations = [
    "Ready for real exam conditions",
    "Continue mock exams at high/extreme pressure to maintain readiness",
    "Focus on content gaps rather than test-taking strategy"
  ]

Elif response_to_pressure == "moderate":
  recommendations = [
    "Schedule regular timed practice sessions",
    "Practice with timer visible to build time awareness",
    "Use gradual pressure increase: standard → high → extreme",
    "Focus on pacing strategy for longer sections"
  ]

Else:  # low
  recommendations = [
    "Start with standard pressure to build confidence",
    "Practice breathing techniques before timed sessions",
    "Break practice into shorter timed segments (20-30 questions)",
    "Focus on process over outcome during practice",
    "Consider studying stress management techniques"
  ]
```

## Constraints

- Must have at least one standard mock for baseline comparison
- Pressure level should match student's current readiness
- Extreme pressure only recommended for students with moderate+ response
- Fatigue tracking requires full mock exam completion
- Profile updates use weighted moving average (recent = 40%, historical = 60%)

## Usage Notes

- Use before real exam to assess pressure readiness
- Combine with mock-exam-evaluator for comprehensive analysis
- Track improvement over multiple pressure sessions
- Adjust study recommendations based on pressure response
- Consider fatigue sensitivity when planning study session length
