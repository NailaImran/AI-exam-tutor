---
name: syllabus-mapper
description: Maps topics between SPSC, PPSC, and KPPSC exam syllabi. Calculates knowledge transfer when switching exams and identifies gaps that need additional preparation. Use when student changes target exam or wants to prepare for multiple exams.
phase: 4
category: CORE
priority: P4
---

# Syllabus Mapper

Enables seamless exam target switching by mapping topic equivalences across SPSC, PPSC, and KPPSC exams and calculating knowledge transfer.

## MCP Integration

This skill uses the **filesystem MCP server** for reading syllabus data and student progress.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read syllabus structures and cross-exam mapping
- `mcp__filesystem__write_file` - Save transfer calculation results

## Topic Equivalence Mapping

### Mapping Structure

```json
{
  "source_exam": "PPSC",
  "source_topic": "Constitutional History",
  "equivalents": {
    "SPSC": {
      "topic": "Constitutional Development",
      "confidence": 0.95,
      "coverage_overlap": 0.90,
      "notes": "Nearly identical content with Sindh-specific additions"
    },
    "KPPSC": {
      "topic": "Constitutional Background",
      "confidence": 0.90,
      "coverage_overlap": 0.85,
      "notes": "Similar core content, some KPK-specific context"
    }
  }
}
```

### Confidence Levels

| Confidence | Range | Meaning |
|------------|-------|---------|
| `exact` | 0.95-1.0 | Identical topic, same content |
| `high` | 0.80-0.94 | Mostly same content, minor differences |
| `moderate` | 0.60-0.79 | Significant overlap, some unique content |
| `low` | 0.40-0.59 | Partial overlap, substantial differences |
| `none` | < 0.40 | Different topics, minimal transfer |

### Coverage Overlap

```
coverage_overlap = shared_subtopics / total_subtopics

Example:
  PPSC Constitutional History: [amendments, federal_structure, rights, provincial]
  SPSC Constitutional Development: [amendments, federal_structure, rights, sindh_specific]

  shared = [amendments, federal_structure, rights]
  coverage_overlap = 3/4 = 0.75
```

## Knowledge Transfer Calculation

### Transfer Score Algorithm

```
For student switching from source_exam to target_exam:

1. Get all practiced topics in source_exam:
   source_topics = topic_stats.filter(exam_type == source_exam)

2. For each source topic, find equivalent in target:
   For topic in source_topics:
     equivalent = cross_exam_mapping[source_exam][topic][target_exam]

     If equivalent exists:
       transfer_score = (
         topic.accuracy × equivalent.confidence × equivalent.coverage_overlap
       )

       transferred_knowledge.append({
         "source_topic": topic.name,
         "target_topic": equivalent.topic,
         "source_accuracy": topic.accuracy,
         "transferred_accuracy": transfer_score,
         "confidence": equivalent.confidence,
         "gap_percentage": 100 - (equivalent.coverage_overlap × 100)
       })
     Else:
       # No equivalent - knowledge doesn't transfer
       no_transfer_topics.append(topic)

3. Calculate overall transfer:
   total_source_knowledge = sum(topic.accuracy × topic.weight for topic in source_topics)
   total_transferred = sum(t.transferred_accuracy × t.weight for t in transferred_knowledge)

   overall_transfer_rate = total_transferred / total_source_knowledge
```

### Gap Identification

```
For target_exam syllabus:
  target_topics = get_all_topics(target_exam)

  For topic in target_topics:
    transferred = find_in_transferred_knowledge(topic)

    If transferred exists:
      If transferred.gap_percentage > 30:
        gaps.append({
          "topic": topic,
          "gap_type": "partial_coverage",
          "existing_knowledge": transferred.transferred_accuracy,
          "additional_study_needed": estimate_study_hours(transferred.gap_percentage)
        })
    Else:
      # New topic - no transferred knowledge
      gaps.append({
        "topic": topic,
        "gap_type": "new_topic",
        "existing_knowledge": 0,
        "additional_study_needed": estimate_study_hours(100)
      })
```

### Study Hours Estimation

```
estimate_study_hours(gap_percentage):
  # Base hours for full topic mastery
  base_hours = topic.weight × 10  # Weighted by syllabus importance

  # Adjust for existing knowledge
  required_hours = base_hours × (gap_percentage / 100)

  # Minimum hours for any gap
  return max(1, round(required_hours, 1))
```

## Exam-Specific Content Identification

### Provincial Variations

```
provincial_specific = {
  "SPSC": [
    "Sindh Local Government",
    "Sindh Geography",
    "Sindh History Post-1947",
    "Sindh Culture and Heritage"
  ],
  "PPSC": [
    "Punjab Local Government",
    "Punjab Geography",
    "Punjab History",
    "Punjab Development Programs"
  ],
  "KPPSC": [
    "KPK Local Government",
    "KPK Geography",
    "KPK History and Tribal Areas",
    "KPK Development and CPEC"
  ]
}

# These topics have NO equivalent in other exams
# Knowledge must be built from scratch
```

### Common Core Topics

```
common_core = [
  "Pakistan Studies - National History",
  "Constitutional Law - Federal Level",
  "Current Affairs - National",
  "Islamic Studies",
  "General Knowledge",
  "English Language",
  "Mathematics/Quantitative"
]

# These transfer with high confidence (>0.90) across all exams
```

## Execution Steps

1. **Load syllabus data**
   ```
   source_syllabus = read_file(syllabus/{source_exam}/syllabus-structure.json)
   target_syllabus = read_file(syllabus/{target_exam}/syllabus-structure.json)
   cross_mapping = read_file(syllabus/cross-exam-mapping.json)
   ```

2. **Load student progress**
   ```
   topic_stats = read_file(memory/students/{student_id}/topic-stats.json)
   ```

3. **Map source topics to target**
   ```
   For each practiced topic:
     Find equivalent in target exam
     Calculate transfer score
   ```

4. **Identify gaps**
   ```
   For each target topic:
     Determine if covered by transfer
     Calculate gap percentage
     Estimate additional study needed
   ```

5. **Calculate overall transfer**
   ```
   overall_rate = calculate_transfer_rate()
   estimated_readiness = calculate_initial_readiness()
   ```

6. **Generate transition plan**

7. **Save transfer results**
   ```
   write_file(memory/students/{student_id}/exam-transfer-{source}-to-{target}.json)
   ```

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true
  },
  "source_exam": {
    "type": "string",
    "enum": ["SPSC", "PPSC", "KPPSC"],
    "required": true,
    "description": "Current/previous exam target"
  },
  "target_exam": {
    "type": "string",
    "enum": ["SPSC", "PPSC", "KPPSC"],
    "required": true,
    "description": "New exam target"
  },
  "include_transition_plan": {
    "type": "boolean",
    "default": true
  }
}
```

## Output Schema

```json
{
  "student_id": "string",
  "calculated_at": "string ISO 8601",
  "source_exam": "SPSC | PPSC | KPPSC",
  "target_exam": "SPSC | PPSC | KPPSC",
  "transfer_summary": {
    "overall_transfer_rate": "number 0-1",
    "topics_with_transfer": "integer",
    "topics_without_transfer": "integer",
    "estimated_starting_eri": "number 0-100",
    "study_hours_saved": "number",
    "additional_hours_needed": "number"
  },
  "topic_transfer": [
    {
      "source_topic": "string",
      "target_topic": "string",
      "source_accuracy": "number 0-100",
      "transferred_accuracy": "number 0-100",
      "confidence": "number 0-1",
      "confidence_level": "exact | high | moderate | low | none",
      "coverage_overlap": "number 0-1",
      "gap_percentage": "number 0-100",
      "notes": "string"
    }
  ],
  "gaps": {
    "new_topics": [
      {
        "topic_id": "string",
        "topic_name": "string",
        "subject": "string",
        "weight_in_exam": "number 0-1",
        "estimated_study_hours": "number",
        "priority": "high | medium | low"
      }
    ],
    "partial_coverage": [
      {
        "topic_id": "string",
        "topic_name": "string",
        "existing_knowledge": "number 0-100",
        "gap_percentage": "number 0-100",
        "specific_gaps": ["string subtopics"],
        "estimated_study_hours": "number"
      }
    ],
    "provincial_specific": [
      {
        "topic_id": "string",
        "topic_name": "string",
        "description": "string",
        "estimated_study_hours": "number"
      }
    ]
  },
  "transition_plan": {
    "phase_1_foundation": {
      "duration_weeks": "integer",
      "focus": "Fill critical gaps and provincial-specific content",
      "topics": ["string topic_ids"],
      "estimated_hours": "number"
    },
    "phase_2_alignment": {
      "duration_weeks": "integer",
      "focus": "Align partial coverage topics to target exam format",
      "topics": ["string topic_ids"],
      "estimated_hours": "number"
    },
    "phase_3_mastery": {
      "duration_weeks": "integer",
      "focus": "Build on transferred knowledge, mock exams",
      "topics": ["string topic_ids"],
      "estimated_hours": "number"
    },
    "total_transition_weeks": "integer",
    "total_hours": "number"
  },
  "recommendations": [
    {
      "type": "priority | content | strategy",
      "message": "string",
      "priority": "high | medium | low"
    }
  ]
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `syllabus/{exam_type}/syllabus-structure.json` |
| Read | `syllabus/cross-exam-mapping.json` |
| Read | `memory/students/{student_id}/topic-stats.json` |
| Write | `memory/students/{student_id}/exam-transfer-{source}-to-{target}.json` |

## Example Output

```json
{
  "student_id": "student_123",
  "calculated_at": "2025-02-03T17:00:00Z",
  "source_exam": "PPSC",
  "target_exam": "SPSC",
  "transfer_summary": {
    "overall_transfer_rate": 0.78,
    "topics_with_transfer": 18,
    "topics_without_transfer": 4,
    "estimated_starting_eri": 52,
    "study_hours_saved": 45,
    "additional_hours_needed": 28
  },
  "topic_transfer": [
    {
      "source_topic": "Constitutional History",
      "target_topic": "Constitutional Development",
      "source_accuracy": 75,
      "transferred_accuracy": 64,
      "confidence": 0.95,
      "confidence_level": "exact",
      "coverage_overlap": 0.90,
      "gap_percentage": 10,
      "notes": "Nearly identical content with Sindh-specific additions"
    },
    {
      "source_topic": "Punjab Local Government",
      "target_topic": null,
      "source_accuracy": 68,
      "transferred_accuracy": 0,
      "confidence": 0,
      "confidence_level": "none",
      "coverage_overlap": 0,
      "gap_percentage": 100,
      "notes": "Provincial-specific content, no equivalent in SPSC"
    }
  ],
  "gaps": {
    "new_topics": [
      {
        "topic_id": "sindh_local_govt",
        "topic_name": "Sindh Local Government System",
        "subject": "pakistan_studies",
        "weight_in_exam": 0.05,
        "estimated_study_hours": 8,
        "priority": "high"
      }
    ],
    "partial_coverage": [
      {
        "topic_id": "provincial_history",
        "topic_name": "Provincial History",
        "existing_knowledge": 65,
        "gap_percentage": 35,
        "specific_gaps": ["Sindh post-1947 history", "Sindh cultural movements"],
        "estimated_study_hours": 5
      }
    ],
    "provincial_specific": [
      {
        "topic_id": "sindh_geography",
        "topic_name": "Sindh Geography",
        "description": "Physical features, rivers, districts of Sindh",
        "estimated_study_hours": 6
      }
    ]
  },
  "transition_plan": {
    "phase_1_foundation": {
      "duration_weeks": 2,
      "focus": "Fill critical gaps and provincial-specific content",
      "topics": ["sindh_local_govt", "sindh_geography", "sindh_culture"],
      "estimated_hours": 15
    },
    "phase_2_alignment": {
      "duration_weeks": 2,
      "focus": "Align partial coverage topics to target exam format",
      "topics": ["provincial_history", "current_affairs_sindh"],
      "estimated_hours": 8
    },
    "phase_3_mastery": {
      "duration_weeks": 3,
      "focus": "Build on transferred knowledge, mock exams",
      "topics": ["all_topics"],
      "estimated_hours": 20
    },
    "total_transition_weeks": 7,
    "total_hours": 43
  },
  "recommendations": [
    {
      "type": "priority",
      "message": "Start with Sindh-specific content (Local Government, Geography) as these have no transfer",
      "priority": "high"
    },
    {
      "type": "content",
      "message": "Your Pakistan Studies knowledge transfers well (85%) - focus on Sindh-specific angles",
      "priority": "medium"
    },
    {
      "type": "strategy",
      "message": "Take an SPSC mock exam after Phase 1 to calibrate your actual readiness",
      "priority": "medium"
    }
  ]
}
```

## Constraints

- Mapping must exist in cross-exam-mapping.json for transfer calculation
- Provincial-specific topics always have 0% transfer
- Confidence levels must reflect actual content overlap
- Transition plan phases should be achievable (reasonable hours/week)
- Must handle bidirectional mapping (PPSC→SPSC and SPSC→PPSC)

## Usage Notes

- Run when student explicitly changes target exam
- Use to advise students considering multiple exams
- Update cross-exam-mapping.json when syllabi change
- Feed transition plan into study-plan-generator
- Track actual vs estimated transition time for calibration
