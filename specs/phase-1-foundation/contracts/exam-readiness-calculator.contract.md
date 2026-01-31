# Skill Contract: exam-readiness-calculator

**Version**: 1.0
**Category**: CORE
**MCP Tools**: read_file

## Purpose

Calculates the Exam Readiness Index (ERI) based on student performance history.

## Input Schema

```json
{
  "student_id": {
    "type": "string",
    "required": true,
    "description": "Student identifier"
  },
  "exam_type": {
    "type": "string",
    "required": true,
    "enum": ["SPSC", "PPSC", "KPPSC"],
    "description": "Target exam for coverage calculation"
  }
}
```

## Output Schema

```json
{
  "eri_score": {
    "type": "number",
    "range": "0-100",
    "precision": 2,
    "description": "Calculated ERI score"
  },
  "eri_band": {
    "type": "string",
    "enum": ["not_ready", "developing", "approaching", "ready", "exam_ready"],
    "description": "Readiness band classification"
  },
  "components": {
    "accuracy": {
      "raw": "number 0-100",
      "weighted": "number (raw * 0.40)"
    },
    "coverage": {
      "topics_practiced": "integer",
      "total_topics": "integer",
      "raw": "number 0-100",
      "weighted": "number (raw * 0.25)"
    },
    "recency": {
      "days_since_practice": "integer",
      "raw": "number 0-100",
      "weighted": "number (raw * 0.20)"
    },
    "consistency": {
      "session_count": "integer",
      "score_std_dev": "number",
      "raw": "number 0-100",
      "weighted": "number (raw * 0.15)"
    }
  },
  "calculation_notes": ["string"],
  "calc_status": "success | insufficient_data"
}
```

## ERI Formula

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

### Component Calculations

**Accuracy (40%)**:
- Source: `history.json` → `overall_accuracy`
- Raw value: 0-100

**Coverage (25%)**:
- Source: `topic-stats.json` → count of topics with attempts > 0
- Reference: `Syllabus/{exam}/syllabus-structure.json` → total topics
- Raw value: (practiced / total) × 100

**Recency (20%)**:
- Source: `history.json` → `last_session_date`
- Decay table:
  | Days | Score |
  |------|-------|
  | 0-3 | 100 |
  | 4-7 | 80 |
  | 8-14 | 60 |
  | 15-30 | 40 |
  | 31+ | 20 |

**Consistency (15%)**:
- Source: `history.json` → `sessions[].accuracy` (last 10 sessions)
- Calculate standard deviation
- Score table:
  | SD | Score |
  |----|-------|
  | <5 | 100 |
  | 5-10 | 80 |
  | 10-15 | 60 |
  | 15-20 | 40 |
  | >20 | 20 |
- Special case: 1 session = 100 (no variance)

### Band Thresholds

| Band | Score Range |
|------|-------------|
| not_ready | 0-20 |
| developing | 21-40 |
| approaching | 41-60 |
| ready | 61-80 |
| exam_ready | 81-100 |

## MCP Operations

1. `mcp__filesystem__read_file` → `Students/{student_id}/history.json`
2. `mcp__filesystem__read_file` → `Students/{student_id}/topic-stats.json`
3. `mcp__filesystem__read_file` → `Syllabus/{exam_type}/syllabus-structure.json`

## Example

**Input**:
```json
{
  "student_id": "STU001",
  "exam_type": "PPSC"
}
```

**Output**:
```json
{
  "eri_score": 52.0,
  "eri_band": "approaching",
  "components": {
    "accuracy": {
      "raw": 75.0,
      "weighted": 30.0
    },
    "coverage": {
      "topics_practiced": 4,
      "total_topics": 20,
      "raw": 20.0,
      "weighted": 5.0
    },
    "recency": {
      "days_since_practice": 1,
      "raw": 100.0,
      "weighted": 20.0
    },
    "consistency": {
      "session_count": 3,
      "score_std_dev": 8.5,
      "raw": 80.0,
      "weighted": 12.0
    }
  },
  "calculation_notes": [
    "Based on 3 practice sessions",
    "Coverage limited to 4/20 topics"
  ],
  "calc_status": "success"
}
```
