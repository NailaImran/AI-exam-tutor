---
name: learning-pattern-detector
description: Analyzes student session history to identify optimal study times, learning velocity per topic, engagement patterns, and preferred difficulty progression. Outputs a learning profile that informs autonomous session scheduling and personalized recommendations.
phase: 4
category: INTELLIGENCE
priority: P2
---

# Learning Pattern Detector

Analyzes historical session data to identify when and how a student learns best, enabling personalized scheduling and content delivery.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and writing learning profiles.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read session history and topic stats
- `mcp__filesystem__write_file` - Save learning profile

## Optimal Study Times Detection

### Time Period Classification

| Period | Hours | Label |
|--------|-------|-------|
| Early Morning | 05:00 - 08:00 | `early_morning` |
| Morning | 08:00 - 12:00 | `morning` |
| Afternoon | 12:00 - 17:00 | `afternoon` |
| Evening | 17:00 - 21:00 | `evening` |
| Night | 21:00 - 24:00 | `night` |
| Late Night | 00:00 - 05:00 | `late_night` |

### Detection Algorithm

```
1. Extract session start times from history:
   sessions = history.sessions
   session_times = [parse_time(s.start_time) for s in sessions]

2. Calculate performance by time period:
   For each time_period:
     period_sessions = sessions where start_time in period
     If len(period_sessions) >= 3:  # Minimum sample size
       avg_accuracy = average(s.accuracy for s in period_sessions)
       avg_duration = average(s.duration for s in period_sessions)
       completion_rate = count(completed) / len(period_sessions)

       period_score = (
         avg_accuracy × 0.50 +        # Performance weight
         completion_rate × 0.30 +      # Engagement weight
         duration_factor × 0.20        # Focus weight
       )

3. Rank time periods by score:
   ranked_periods = sort(periods, key=period_score, descending=True)

4. Select optimal times:
   optimal_study_times = ranked_periods[:2]  # Top 2 periods

   # Require minimum score of 0.60 to be considered "optimal"
   optimal_study_times = [p for p in optimal_study_times if p.score >= 0.60]
```

### Duration Factor Calculation

```
# Longer focused sessions indicate better concentration
avg_session_duration = average(session durations in period)

If avg_session_duration >= 45:
  duration_factor = 1.0  # Excellent focus
Elif avg_session_duration >= 30:
  duration_factor = 0.8  # Good focus
Elif avg_session_duration >= 20:
  duration_factor = 0.6  # Moderate focus
Elif avg_session_duration >= 10:
  duration_factor = 0.4  # Short sessions
Else:
  duration_factor = 0.2  # Very brief
```

## Learning Velocity Calculation

### Velocity Metrics

Learning velocity measures how quickly a student improves on a topic.

```
For each topic:
  sessions_with_topic = get_sessions_containing(topic)

  If len(sessions_with_topic) >= 3:
    # Calculate improvement rate
    first_accuracy = sessions_with_topic[0].topic_accuracy
    last_accuracy = sessions_with_topic[-1].topic_accuracy
    sessions_count = len(sessions_with_topic)

    improvement = last_accuracy - first_accuracy
    improvement_per_session = improvement / (sessions_count - 1)

    # Calculate questions to proficiency (70% accuracy)
    If last_accuracy >= 70:
      questions_to_proficiency = total_questions_until_70
    Else:
      # Extrapolate based on current trajectory
      remaining_improvement = 70 - last_accuracy
      estimated_sessions = remaining_improvement / improvement_per_session
      questions_to_proficiency = estimated_sessions × avg_questions_per_session

    velocity = {
      "topic_id": topic.id,
      "improvement_per_session": improvement_per_session,
      "questions_to_proficiency": questions_to_proficiency,
      "current_accuracy": last_accuracy,
      "sessions_analyzed": sessions_count
    }
```

### Topic Classification

```
# Classify topics by learning velocity
all_velocities = calculate_velocities(all_topics)
median_velocity = median(v.improvement_per_session for v in all_velocities)

fast_topics = [t for t in all_velocities
               if t.improvement_per_session > median_velocity × 1.3]

slow_topics = [t for t in all_velocities
               if t.improvement_per_session < median_velocity × 0.7]

# Also consider absolute performance
naturally_strong = [t for t in all_velocities
                    if t.first_session_accuracy >= 70]  # Good from start

naturally_weak = [t for t in all_velocities
                  if t.sessions_analyzed >= 5 AND t.current_accuracy < 50]
```

## Engagement Patterns Analysis

### Day-of-Week Analysis

```
1. Group sessions by day of week:
   day_groups = group_by(sessions, day_of_week)

2. Calculate engagement score per day:
   For each day in [Monday, Tuesday, ..., Sunday]:
     day_sessions = day_groups[day]

     engagement_score = (
       session_count × 0.40 +           # Frequency
       avg_accuracy × 0.30 +            # Quality
       avg_completion_rate × 0.30       # Commitment
     )

     # Normalize by dividing by max possible
     normalized_score = engagement_score / max_engagement_score

3. Classify days:
   day_scores = [(day, score) for day, score in engagement_scores]
   sorted_days = sort(day_scores, key=score, descending=True)

   peak_days = [d for d, s in sorted_days[:3] if s >= 0.60]
   low_engagement_days = [d for d, s in sorted_days[-2:] if s < 0.40]
```

### Weekly Session Patterns

```
# Calculate average sessions per week
total_weeks = (last_session_date - first_session_date).days / 7
average_sessions_per_week = total_sessions / total_weeks

# Identify consistency
session_counts_by_week = group_by(sessions, week_number)
weekly_variance = variance(session_counts_by_week.values())

If weekly_variance < 1.0:
  consistency = "highly_consistent"
Elif weekly_variance < 2.0:
  consistency = "moderately_consistent"
Else:
  consistency = "inconsistent"
```

### Dropout Risk Indicators

```
dropout_risk_indicators = []

# Check for declining engagement
recent_4_weeks = sessions from last 28 days
previous_4_weeks = sessions from 28-56 days ago

If len(recent_4_weeks) < len(previous_4_weeks) × 0.5:
  dropout_risk_indicators.append("declining_frequency")

# Check for declining performance
recent_accuracy = average(s.accuracy for s in recent_4_weeks)
previous_accuracy = average(s.accuracy for s in previous_4_weeks)

If recent_accuracy < previous_accuracy - 10:
  dropout_risk_indicators.append("declining_performance")

# Check for session gaps
max_gap = max(gaps between consecutive sessions)
If max_gap > 7:
  dropout_risk_indicators.append("long_gaps_detected")

# Check for incomplete sessions
incomplete_rate = count(incomplete sessions) / total_sessions
If incomplete_rate > 0.30:
  dropout_risk_indicators.append("high_abandonment_rate")
```

## Preferred Difficulty Ramp Detection

### Difficulty Progression Patterns

```
# Analyze how accuracy changes as difficulty increases within sessions

For each session with mixed difficulties:
  easy_accuracy = accuracy on easy questions
  medium_accuracy = accuracy on medium questions
  hard_accuracy = accuracy on hard questions

  # Calculate performance drop between levels
  easy_to_medium_drop = easy_accuracy - medium_accuracy
  medium_to_hard_drop = medium_accuracy - hard_accuracy

  progression_scores.append({
    "session_id": session.id,
    "easy_to_medium_drop": easy_to_medium_drop,
    "medium_to_hard_drop": medium_to_hard_drop,
    "total_drop": easy_accuracy - hard_accuracy
  })
```

### Ramp Classification

```
avg_easy_to_medium_drop = average(p.easy_to_medium_drop for p in progression_scores)
avg_medium_to_hard_drop = average(p.medium_to_hard_drop for p in progression_scores)
avg_total_drop = average(p.total_drop for p in progression_scores)

# Gradual learner: Small drops, consistent across levels
# Aggressive learner: Can handle big jumps, thrives on challenge
# Mixed learner: Inconsistent pattern

If avg_total_drop < 15:
  # Handles difficulty well
  If avg_easy_to_medium_drop < 10 AND avg_medium_to_hard_drop < 10:
    preferred_difficulty_ramp = "aggressive"
  Else:
    preferred_difficulty_ramp = "gradual"

Elif avg_total_drop < 30:
  # Moderate difficulty handling
  If variance(progression_scores.total_drop) > 100:
    preferred_difficulty_ramp = "mixed"  # Inconsistent
  Else:
    preferred_difficulty_ramp = "gradual"

Else:
  # Struggles with difficulty increases
  preferred_difficulty_ramp = "gradual"
```

### Confidence Scoring

```
# Calculate confidence in the ramp assessment
sample_size = len(progression_scores)

If sample_size >= 20:
  confidence = 0.90
Elif sample_size >= 10:
  confidence = 0.75
Elif sample_size >= 5:
  confidence = 0.60
Else:
  confidence = 0.40  # Low confidence

# Adjust for consistency
If variance(progression_scores.total_drop) < 50:
  confidence = min(1.0, confidence + 0.10)  # Consistent pattern
Elif variance(progression_scores.total_drop) > 150:
  confidence = max(0.30, confidence - 0.15)  # Inconsistent
```

## Execution Steps

1. **Load session history**
   ```
   history = read_file(memory/students/{student_id}/history.json)
   topic_stats = read_file(memory/students/{student_id}/topic-stats.json)
   sessions = read_file(memory/students/{student_id}/sessions/*.json)
   ```

2. **Calculate optimal study times**
   ```
   time_analysis = analyze_session_times(history.sessions)
   optimal_study_times = extract_optimal_times(time_analysis)
   ```

3. **Calculate learning velocity per topic**
   ```
   velocities = calculate_learning_velocities(topic_stats, sessions)
   fast_topics = extract_fast_topics(velocities)
   slow_topics = extract_slow_topics(velocities)
   ```

4. **Analyze engagement patterns**
   ```
   day_analysis = analyze_by_day(history.sessions)
   peak_days = extract_peak_days(day_analysis)
   low_engagement_days = extract_low_days(day_analysis)
   average_sessions_per_week = calculate_weekly_average(history)
   dropout_risk_indicators = detect_dropout_risks(history)
   ```

5. **Detect preferred difficulty ramp**
   ```
   progression_analysis = analyze_difficulty_progression(sessions)
   preferred_difficulty_ramp = classify_ramp_preference(progression_analysis)
   ```

6. **Build learning profile**

7. **Save learning profile**
   ```
   write_file(memory/students/{student_id}/learning-profile.json)
   ```

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "analysis_depth": {
    "type": "string",
    "enum": ["quick", "standard", "comprehensive"],
    "default": "standard",
    "description": "Depth of pattern analysis"
  },
  "minimum_sessions": {
    "type": "integer",
    "default": 5,
    "description": "Minimum sessions required for reliable analysis"
  },
  "lookback_days": {
    "type": "integer",
    "default": 90,
    "description": "Number of days of history to analyze"
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "analyzed_at": "string ISO 8601",
  "analysis_depth": "quick | standard | comprehensive",
  "sessions_analyzed": "integer",
  "date_range": {
    "from": "string ISO 8601",
    "to": "string ISO 8601"
  },
  "optimal_study_times": {
    "primary": "string time period",
    "secondary": "string time period | null",
    "scores": {
      "<period>": {
        "score": "number 0-1",
        "avg_accuracy": "number 0-100",
        "session_count": "integer",
        "avg_duration_minutes": "number"
      }
    },
    "confidence": "number 0-1"
  },
  "learning_velocity": {
    "fast_topics": [
      {
        "topic_id": "string",
        "topic_name": "string",
        "improvement_per_session": "number",
        "sessions_to_proficiency": "integer",
        "current_accuracy": "number 0-100"
      }
    ],
    "slow_topics": [
      {
        "topic_id": "string",
        "topic_name": "string",
        "improvement_per_session": "number",
        "sessions_to_proficiency": "integer",
        "current_accuracy": "number 0-100"
      }
    ],
    "average_velocity": "number",
    "confidence": "number 0-1"
  },
  "engagement_patterns": {
    "peak_days": ["string day names"],
    "low_engagement_days": ["string day names"],
    "average_sessions_per_week": "number",
    "consistency": "highly_consistent | moderately_consistent | inconsistent",
    "dropout_risk_indicators": ["string indicators"],
    "dropout_risk_level": "low | medium | high",
    "day_scores": {
      "<day>": {
        "score": "number 0-1",
        "session_count": "integer",
        "avg_accuracy": "number 0-100"
      }
    },
    "confidence": "number 0-1"
  },
  "preferred_difficulty_ramp": {
    "type": "gradual | aggressive | mixed",
    "avg_easy_to_medium_drop": "number percentage points",
    "avg_medium_to_hard_drop": "number percentage points",
    "recommended_progression": "string description",
    "confidence": "number 0-1"
  },
  "session_duration_preference": {
    "optimal_minutes": "integer",
    "tolerance_range": [min, max],
    "based_on_sessions": "integer"
  },
  "recommendations": [
    {
      "category": "scheduling | content | difficulty | engagement",
      "recommendation": "string",
      "priority": "high | medium | low"
    }
  ]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/history.json` |
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `memory/students/{student_id}/sessions/*.json` |
| Write | `memory/students/{student_id}/learning-profile.json` |

## Dropout Risk Level

```
risk_count = len(dropout_risk_indicators)

If risk_count == 0:
  dropout_risk_level = "low"
Elif risk_count <= 2:
  dropout_risk_level = "medium"
Else:
  dropout_risk_level = "high"
```

## Recommendations Generation

```
recommendations = []

# Scheduling recommendations
If optimal_study_times.primary:
  recommendations.append({
    "category": "scheduling",
    "recommendation": f"Schedule sessions during {primary} for best performance",
    "priority": "high"
  })

# Content recommendations
If len(slow_topics) > 0:
  recommendations.append({
    "category": "content",
    "recommendation": f"Allocate extra time for {slow_topics[0].name} - learning slower than average",
    "priority": "high"
  })

# Difficulty recommendations
If preferred_difficulty_ramp == "gradual":
  recommendations.append({
    "category": "difficulty",
    "recommendation": "Use gradual difficulty progression - start easy, slowly increase",
    "priority": "medium"
  })

# Engagement recommendations
If dropout_risk_level == "high":
  recommendations.append({
    "category": "engagement",
    "recommendation": "Engagement declining - consider shorter, more frequent sessions",
    "priority": "high"
  })
```

## Example Output

```json
{
  "student_id": "student_123",
  "analyzed_at": "2025-02-03T12:00:00Z",
  "analysis_depth": "standard",
  "sessions_analyzed": 45,
  "date_range": {
    "from": "2024-11-05T00:00:00Z",
    "to": "2025-02-03T00:00:00Z"
  },
  "optimal_study_times": {
    "primary": "evening",
    "secondary": "morning",
    "scores": {
      "evening": {"score": 0.82, "avg_accuracy": 78, "session_count": 18, "avg_duration_minutes": 35},
      "morning": {"score": 0.71, "avg_accuracy": 72, "session_count": 12, "avg_duration_minutes": 28},
      "afternoon": {"score": 0.55, "avg_accuracy": 65, "session_count": 10, "avg_duration_minutes": 22}
    },
    "confidence": 0.85
  },
  "learning_velocity": {
    "fast_topics": [
      {"topic_id": "current_affairs", "topic_name": "Current Affairs", "improvement_per_session": 8.5, "sessions_to_proficiency": 4, "current_accuracy": 82},
      {"topic_id": "general_knowledge", "topic_name": "General Knowledge", "improvement_per_session": 6.2, "sessions_to_proficiency": 5, "current_accuracy": 75}
    ],
    "slow_topics": [
      {"topic_id": "constitutional_law", "topic_name": "Constitutional Law", "improvement_per_session": 2.1, "sessions_to_proficiency": 15, "current_accuracy": 48},
      {"topic_id": "islamic_studies", "topic_name": "Islamic Studies", "improvement_per_session": 2.8, "sessions_to_proficiency": 12, "current_accuracy": 52}
    ],
    "average_velocity": 4.5,
    "confidence": 0.78
  },
  "engagement_patterns": {
    "peak_days": ["wednesday", "saturday", "sunday"],
    "low_engagement_days": ["friday"],
    "average_sessions_per_week": 4.2,
    "consistency": "moderately_consistent",
    "dropout_risk_indicators": [],
    "dropout_risk_level": "low",
    "day_scores": {
      "monday": {"score": 0.58, "session_count": 6, "avg_accuracy": 70},
      "tuesday": {"score": 0.52, "session_count": 5, "avg_accuracy": 68},
      "wednesday": {"score": 0.75, "session_count": 8, "avg_accuracy": 76},
      "thursday": {"score": 0.48, "session_count": 4, "avg_accuracy": 65},
      "friday": {"score": 0.32, "session_count": 2, "avg_accuracy": 62},
      "saturday": {"score": 0.78, "session_count": 10, "avg_accuracy": 79},
      "sunday": {"score": 0.72, "session_count": 10, "avg_accuracy": 74}
    },
    "confidence": 0.82
  },
  "preferred_difficulty_ramp": {
    "type": "gradual",
    "avg_easy_to_medium_drop": 12,
    "avg_medium_to_hard_drop": 18,
    "recommended_progression": "Start with easy questions (3-5), then medium (5-7), introduce hard questions gradually",
    "confidence": 0.75
  },
  "session_duration_preference": {
    "optimal_minutes": 30,
    "tolerance_range": [20, 45],
    "based_on_sessions": 45
  },
  "recommendations": [
    {
      "category": "scheduling",
      "recommendation": "Schedule sessions during evening (5-9 PM) for best performance - 82% engagement score",
      "priority": "high"
    },
    {
      "category": "content",
      "recommendation": "Allocate extra time for Constitutional Law - learning 53% slower than average",
      "priority": "high"
    },
    {
      "category": "difficulty",
      "recommendation": "Use gradual difficulty progression - performance drops 30% from easy to hard",
      "priority": "medium"
    },
    {
      "category": "scheduling",
      "recommendation": "Avoid scheduling on Fridays - lowest engagement day",
      "priority": "medium"
    }
  ]
}
```

## Constraints

- Require minimum 5 sessions for reliable pattern detection
- Time period analysis requires at least 3 sessions per period
- Learning velocity requires at least 3 sessions per topic
- Confidence scores must reflect sample size limitations
- Must handle missing or incomplete session data gracefully
- Must not overfit to small samples - prefer "insufficient_data" over low-confidence predictions

## Usage Notes

- Call periodically (weekly) to update learning profile
- Use optimal_study_times to inform autonomous-session-initiator
- Use learning_velocity to adjust study plan time allocations
- Use engagement_patterns to prevent scheduling on low-engagement days
- Use preferred_difficulty_ramp to configure adaptive-test-generator
- Monitor dropout_risk_indicators for proactive intervention
