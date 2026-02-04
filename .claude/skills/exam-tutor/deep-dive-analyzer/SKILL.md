---
name: deep-dive-analyzer
description: Performs root-cause analysis of weak topics with actionable insights. Identifies why a topic is weak (no_practice, historically_difficult, related_weakness), analyzes contributing factors, and generates specific recommended actions. Use when student needs detailed diagnosis of their weak areas.
phase: 4
category: INTELLIGENCE
priority: P2
---

# Deep Dive Analyzer

Provides comprehensive root-cause analysis of weak topics, identifying why performance is poor and generating actionable recommendations for improvement.

## MCP Integration

This skill uses the **filesystem MCP server** for reading student data and writing diagnostic reports.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read topic stats, session history, retention data
- `mcp__filesystem__write_file` - Save diagnostic reports

## Root Cause Identification

### Root Cause Categories

| Root Cause | Code | Detection Criteria |
|------------|------|-------------------|
| No recent practice | `no_practice` | No sessions in last 14 days |
| Insufficient practice | `insufficient_practice` | < 10 questions attempted |
| Historically difficult | `historically_difficult` | Accuracy consistently < 60% over 3+ sessions |
| Related topic weakness | `related_weakness` | Related/prerequisite topics also weak |
| Knowledge decay | `knowledge_decay` | Retention score < 0.50 |
| Concept confusion | `concept_confusion` | Similar topics have inverse performance |
| Time pressure issue | `time_pressure` | Accuracy drops significantly in timed tests |
| Difficulty mismatch | `difficulty_mismatch` | Poor on medium/hard, good on easy |

### Root Cause Detection Algorithm

```
For topic with accuracy < 70%:

1. Check practice recency:
   days_since_last = (today - last_practiced).days
   If days_since_last > 14:
     root_causes.append("no_practice")

2. Check practice volume:
   If total_attempted < 10:
     root_causes.append("insufficient_practice")

3. Check historical difficulty:
   session_accuracies = get_last_n_session_accuracies(topic, n=3)
   If all(acc < 60% for acc in session_accuracies):
     root_causes.append("historically_difficult")

4. Check related topics:
   related_topics = get_related_topics(topic, syllabus)
   weak_related = [t for t in related_topics if t.accuracy < 60%]
   If len(weak_related) > 0:
     root_causes.append("related_weakness")

5. Check knowledge decay:
   If retention_score < 0.50:
     root_causes.append("knowledge_decay")

6. Check concept confusion:
   similar_topics = get_similar_topics(topic)
   For each similar:
     If abs(topic.accuracy - similar.accuracy) > 30:
       root_causes.append("concept_confusion")

7. Check time pressure performance:
   timed_accuracy = get_timed_test_accuracy(topic)
   untimed_accuracy = get_untimed_accuracy(topic)
   If timed_accuracy < untimed_accuracy - 15:
     root_causes.append("time_pressure")

8. Check difficulty breakdown:
   If easy_accuracy > 80 AND medium_accuracy < 60:
     root_causes.append("difficulty_mismatch")

9. Determine primary root cause (most impactful):
   primary = prioritize_root_causes(root_causes)
```

### Root Cause Priority Order

```
priority_order = [
  "no_practice",           # Most actionable
  "insufficient_practice", # Volume issue
  "knowledge_decay",       # Retention issue
  "related_weakness",      # Dependency issue
  "historically_difficult", # Structural issue
  "concept_confusion",     # Understanding issue
  "difficulty_mismatch",   # Progression issue
  "time_pressure"          # Performance issue
]
```

## Contributing Factors Analysis

### Factor Categories

| Factor | Weight | Description |
|--------|--------|-------------|
| Practice recency | 0.20 | Days since last practice |
| Practice volume | 0.15 | Total questions attempted |
| Retention health | 0.20 | Current retention score |
| Trend direction | 0.15 | Improving, stable, or declining |
| Related topic health | 0.15 | Average accuracy of related topics |
| Difficulty progression | 0.15 | Performance across difficulty levels |

### Factor Calculation

```
For each factor:
  factor_score = calculate_factor_score(factor, topic_data)
  contribution = factor_score × factor_weight
  impact = "positive" if factor_score > 0.7 else "negative" if factor_score < 0.4 else "neutral"

Contributing factors list includes only factors with impact != "neutral":
  contributing_factors = [
    {
      "factor": factor_name,
      "impact": "positive" | "negative",
      "value": factor_score,
      "description": human_readable_description
    }
  ]
```

### Factor Score Calculations

```
practice_recency_score:
  If days_since < 3: score = 1.0
  Elif days_since < 7: score = 0.8
  Elif days_since < 14: score = 0.5
  Elif days_since < 30: score = 0.3
  Else: score = 0.1

practice_volume_score:
  If total_attempted >= 50: score = 1.0
  Elif total_attempted >= 30: score = 0.8
  Elif total_attempted >= 15: score = 0.6
  Elif total_attempted >= 10: score = 0.4
  Else: score = total_attempted / 10 × 0.4

retention_health_score:
  score = retention_score  # Direct mapping (0-1)

trend_direction_score:
  recent_3 = last_3_session_accuracies
  If recent_3[2] > recent_3[0] + 10: score = 1.0  # Improving
  Elif recent_3[2] > recent_3[0]: score = 0.7     # Slight improvement
  Elif recent_3[2] < recent_3[0] - 10: score = 0.2  # Declining
  Else: score = 0.5  # Stable

related_topic_score:
  related_accuracies = [t.accuracy for t in related_topics]
  score = average(related_accuracies) / 100

difficulty_progression_score:
  If easy >= 80 AND medium >= 60 AND hard >= 40:
    score = 1.0  # Healthy progression
  Elif easy >= 70 AND medium >= 50:
    score = 0.7  # Acceptable
  Elif easy >= 60:
    score = 0.4  # Struggling
  Else:
    score = 0.2  # Fundamental issue
```

## Recommended Action Generation

### Action Templates

| Root Cause | Recommended Action | Priority |
|------------|-------------------|----------|
| no_practice | Schedule immediate review session | urgent |
| insufficient_practice | Complete 20 more practice questions | high |
| historically_difficult | Start with fundamentals, gradual difficulty | high |
| related_weakness | Practice prerequisite topics first | high |
| knowledge_decay | Intensive revision with spaced repetition | urgent |
| concept_confusion | Review distinguishing features side-by-side | medium |
| time_pressure | Practice timed drills starting at 150% time | medium |
| difficulty_mismatch | Focus on medium difficulty before advancing | high |

### Action Generation Algorithm

```
For primary_root_cause:
  action = action_templates[primary_root_cause]

  # Customize action based on context
  If primary_root_cause == "no_practice":
    action.specific = f"Review {topic_name} - last practiced {days_since} days ago"
    action.questions_recommended = 10
    action.estimated_time = 15

  Elif primary_root_cause == "related_weakness":
    prerequisite = get_weakest_related(topic)
    action.specific = f"First strengthen {prerequisite.name} (current: {prerequisite.accuracy}%)"
    action.questions_recommended = 15
    action.estimated_time = 25

  Elif primary_root_cause == "historically_difficult":
    action.specific = f"Start with easy questions on {topic_name}, aim for 80% before advancing"
    action.questions_recommended = 20
    action.difficulty = "easy"
    action.estimated_time = 30

  # Add secondary actions for other root causes
  secondary_actions = []
  For cause in root_causes[1:3]:  # Top 2 secondary
    secondary_actions.append(generate_secondary_action(cause))
```

### Action Structure

```json
{
  "primary_action": {
    "action_type": "practice | review | prerequisite | drill",
    "description": "Human-readable action description",
    "specific_instruction": "Detailed instruction",
    "topic_focus": "topic_id",
    "difficulty_level": "easy | medium | hard | adaptive",
    "questions_recommended": "integer",
    "estimated_time_minutes": "integer",
    "priority": "urgent | high | medium | low",
    "success_criteria": "What defines completion"
  },
  "secondary_actions": [
    {
      "action_type": "string",
      "description": "string",
      "priority": "string"
    }
  ]
}
```

## Execution Steps

1. **Load student data**
   ```
   topic_stats = read_file(memory/students/{student_id}/topic-stats.json)
   history = read_file(memory/students/{student_id}/history.json)
   retention_data = read_file(memory/students/{student_id}/retention-data.json)
   syllabus = read_file(syllabus/{exam_type}/syllabus-structure.json)
   ```

2. **Identify weak topics (if not specified)**
   ```
   If topic_id not provided:
     weak_topics = [t for t in topic_stats.topics if t.accuracy < 70]
     Sort by accuracy ascending
   Else:
     weak_topics = [topic_stats.topics[topic_id]]
   ```

3. **For each weak topic, analyze root causes**
   ```
   For topic in weak_topics:
     root_causes = detect_root_causes(topic, history, retention_data, syllabus)
     primary_cause = prioritize_root_causes(root_causes)
   ```

4. **Analyze contributing factors**
   ```
   For topic in weak_topics:
     factors = analyze_contributing_factors(topic, history)
     negative_factors = [f for f in factors if f.impact == "negative"]
     positive_factors = [f for f in factors if f.impact == "positive"]
   ```

5. **Generate recommendations**
   ```
   For topic in weak_topics:
     primary_action = generate_primary_action(primary_cause, topic)
     secondary_actions = generate_secondary_actions(root_causes[1:], topic)
   ```

6. **Build diagnostic report**

7. **Save report**
   ```
   write_file(memory/students/{student_id}/diagnostics/{topic_id}-{date}.json)
   ```

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "topic_id": {
    "type": "string",
    "required": false,
    "description": "Specific topic to analyze. If omitted, analyzes all weak topics."
  },
  "depth": {
    "type": "string",
    "enum": ["quick", "standard", "comprehensive"],
    "default": "standard",
    "description": "Analysis depth level"
  },
  "include_related": {
    "type": "boolean",
    "default": true,
    "description": "Include related topic analysis"
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "analyzed_at": "string ISO 8601",
  "depth": "quick | standard | comprehensive",
  "diagnostics": [
    {
      "topic_id": "string",
      "topic_name": "string",
      "subject": "string",
      "current_accuracy": "number 0-100",
      "severity": "critical | severe | moderate | mild",
      "root_causes": {
        "primary": {
          "code": "string root cause code",
          "name": "string human readable",
          "confidence": "number 0-1",
          "evidence": ["string supporting data points"]
        },
        "secondary": [
          {
            "code": "string",
            "name": "string",
            "confidence": "number 0-1"
          }
        ]
      },
      "contributing_factors": {
        "negative": [
          {
            "factor": "string",
            "impact": "negative",
            "value": "number 0-1",
            "description": "string"
          }
        ],
        "positive": [
          {
            "factor": "string",
            "impact": "positive",
            "value": "number 0-1",
            "description": "string"
          }
        ]
      },
      "recommendations": {
        "primary_action": {
          "action_type": "string",
          "description": "string",
          "specific_instruction": "string",
          "topic_focus": "string",
          "difficulty_level": "string",
          "questions_recommended": "integer",
          "estimated_time_minutes": "integer",
          "priority": "string",
          "success_criteria": "string"
        },
        "secondary_actions": [
          {
            "action_type": "string",
            "description": "string",
            "priority": "string"
          }
        ]
      },
      "related_topics": [
        {
          "topic_id": "string",
          "relationship": "prerequisite | related | similar",
          "accuracy": "number 0-100",
          "impact_on_weakness": "high | medium | low"
        }
      ]
    }
  ],
  "summary": {
    "topics_analyzed": "integer",
    "critical_count": "integer",
    "severe_count": "integer",
    "moderate_count": "integer",
    "mild_count": "integer",
    "most_common_root_cause": "string",
    "total_recommended_time_minutes": "integer"
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `memory/students/{student_id}/topic-stats.json` |
| Read | `memory/students/{student_id}/history.json` |
| Read | `memory/students/{student_id}/retention-data.json` |
| Read | `syllabus/{exam_type}/syllabus-structure.json` |
| Write | `memory/students/{student_id}/diagnostics/{topic_id}-{date}.json` |

## Severity Classification

```
If accuracy < 30:
  severity = "critical"
Elif accuracy < 50:
  severity = "severe"
Elif accuracy < 60:
  severity = "moderate"
Else:  # 60-70
  severity = "mild"
```

## Example Output

```json
{
  "student_id": "student_123",
  "analyzed_at": "2025-02-03T11:00:00Z",
  "depth": "standard",
  "diagnostics": [
    {
      "topic_id": "constitutional_amendments",
      "topic_name": "Constitutional Amendments",
      "subject": "pakistan_studies",
      "current_accuracy": 42,
      "severity": "severe",
      "root_causes": {
        "primary": {
          "code": "related_weakness",
          "name": "Related Topic Weakness",
          "confidence": 0.85,
          "evidence": [
            "Constitutional History accuracy: 38%",
            "Federal Structure accuracy: 45%",
            "Both topics share prerequisite concepts"
          ]
        },
        "secondary": [
          {
            "code": "no_practice",
            "name": "No Recent Practice",
            "confidence": 0.75
          },
          {
            "code": "historically_difficult",
            "name": "Historically Difficult Topic",
            "confidence": 0.70
          }
        ]
      },
      "contributing_factors": {
        "negative": [
          {
            "factor": "practice_recency",
            "impact": "negative",
            "value": 0.3,
            "description": "Last practiced 18 days ago"
          },
          {
            "factor": "related_topic_health",
            "impact": "negative",
            "value": 0.35,
            "description": "2 of 3 related topics also weak"
          }
        ],
        "positive": [
          {
            "factor": "trend_direction",
            "impact": "positive",
            "value": 0.7,
            "description": "Slight improvement in last 2 sessions"
          }
        ]
      },
      "recommendations": {
        "primary_action": {
          "action_type": "prerequisite",
          "description": "Strengthen prerequisite topics before continuing",
          "specific_instruction": "First strengthen Constitutional History (current: 38%). This topic provides the foundation for understanding amendments.",
          "topic_focus": "constitutional_history",
          "difficulty_level": "easy",
          "questions_recommended": 15,
          "estimated_time_minutes": 25,
          "priority": "high",
          "success_criteria": "Achieve 70% accuracy on Constitutional History"
        },
        "secondary_actions": [
          {
            "action_type": "review",
            "description": "Schedule immediate review session for Constitutional Amendments",
            "priority": "high"
          },
          {
            "action_type": "practice",
            "description": "Focus on easy difficulty questions to build confidence",
            "priority": "medium"
          }
        ]
      },
      "related_topics": [
        {
          "topic_id": "constitutional_history",
          "relationship": "prerequisite",
          "accuracy": 38,
          "impact_on_weakness": "high"
        },
        {
          "topic_id": "federal_structure",
          "relationship": "related",
          "accuracy": 45,
          "impact_on_weakness": "medium"
        }
      ]
    }
  ],
  "summary": {
    "topics_analyzed": 5,
    "critical_count": 1,
    "severe_count": 2,
    "moderate_count": 2,
    "mild_count": 0,
    "most_common_root_cause": "related_weakness",
    "total_recommended_time_minutes": 85
  }
}
```

## Constraints

- Must identify at least one root cause per weak topic
- Confidence scores must be between 0 and 1
- Must provide actionable recommendations for every diagnosis
- Must consider topic relationships from syllabus
- Severity classification must be consistent with accuracy ranges
- Evidence must reference actual student data
- Actions must include estimated time and question count

## Usage Notes

- Call when student asks "why am I weak at X?"
- Call after weak-area-identifier to get deeper insights
- Use comprehensive depth for exam countdown planning
- Feed recommendations into study-plan-generator
- Track if recommended actions are followed for effectiveness measurement
