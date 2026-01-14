---
name: syllabus-mapper
description: Maps topics between different exam syllabi and provides syllabus structure information. Use this skill when students switch exam targets, when cross-referencing content, or when loading syllabus data. Enables cross-exam topic correlation and weight lookup. Optional skill for multi-exam support.
---

# Syllabus Mapper

Provides syllabus structure data and cross-exam topic mapping capabilities.

## MCP Integration

This skill uses the **filesystem MCP server** for reading syllabus files.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read syllabus structure and mapping files

## Execution Steps

### Query Type: full_structure

1. **Load syllabus structure**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/{exam_type}/syllabus-structure.json
   ```

2. **Load topic weights**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/{exam_type}/topic-weights.json
   ```

3. **Build complete structure**
   ```
   For each subject:
     Include all topics with weights
     Calculate subject total weight
   ```

4. **Return full syllabus data**

### Query Type: topic_lookup

1. **Load syllabus structure**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/{exam_type}/syllabus-structure.json
   ```

2. **Search for topic**
   ```
   Find topic by exact name or partial match
   Return topic details including:
     - subject
     - weight
     - related topics
     - description
   ```

3. **Return topic data or not_found**

### Query Type: cross_exam_map

1. **Load cross-exam mapping**
   ```
   Use: mcp__filesystem__read_file
   Path: syllabus/cross-exam-mapping.json
   ```

2. **Find topic in source exam**
   ```
   source_topic = mapping[source_exam][topic_name]
   ```

3. **Find equivalent in target exam**
   ```
   equivalent = source_topic.equivalents[exam_type]
   confidence = equivalent.confidence_score
   ```

4. **Return mapping with confidence**

## Input Schema

```json
{
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true,
    "description": "Target examination board"
  },
  "query_type": {
    "type": "enum",
    "values": ["full_structure", "topic_lookup", "cross_exam_map"],
    "required": true
  },
  "topic_name": {
    "type": "string",
    "required": false,
    "description": "Required if query_type is topic_lookup or cross_exam_map"
  },
  "source_exam": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": false,
    "description": "Required if query_type is cross_exam_map"
  }
}
```

## Output Schema

### full_structure

```json
{
  "result": {
    "exam_type": "SPSC | PPSC | KPPSC",
    "total_subjects": "integer",
    "total_topics": "integer",
    "structure": [
      {
        "subject": "string",
        "weight": "number",
        "topics": [
          {
            "name": "string",
            "weight": "number",
            "description": "string"
          }
        ]
      }
    ]
  },
  "subjects": ["array of subject objects"]
}
```

### topic_lookup

```json
{
  "result": {
    "found": "boolean",
    "topic": {
      "name": "string",
      "subject": "string",
      "weight": "number",
      "description": "string",
      "related_topics": ["string"]
    }
  }
}
```

### cross_exam_map

```json
{
  "result": {
    "source_exam": "string",
    "source_topic": "string",
    "target_exam": "string",
    "equivalent_topic": "string | null",
    "confidence": "number (0-1)",
    "mapping_notes": "string"
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `syllabus/{exam_type}/syllabus-structure.json` |
| Read | `syllabus/{exam_type}/topic-weights.json` |
| Read | `syllabus/cross-exam-mapping.json` |

## Syllabus Structure Schema

```json
{
  "exam_type": "SPSC",
  "version": "2024",
  "subjects": [
    {
      "name": "Pakistan Studies",
      "weight": 0.20,
      "topics": [
        {
          "name": "Independence Movement",
          "weight": 0.25,
          "description": "Events leading to Pakistan's creation"
        },
        {
          "name": "Constitutional History",
          "weight": 0.20,
          "description": "Evolution of Pakistan's constitution"
        }
      ]
    }
  ]
}
```

## Cross-Exam Mapping Schema

```json
{
  "SPSC": {
    "Independence Movement": {
      "equivalents": {
        "PPSC": {
          "topic": "Pakistan Movement",
          "confidence": 0.95,
          "notes": "Nearly identical coverage"
        },
        "KPPSC": {
          "topic": "Creation of Pakistan",
          "confidence": 0.85,
          "notes": "Similar scope, different emphasis"
        }
      }
    }
  }
}
```

## Confidence Levels

| Score | Interpretation |
|-------|----------------|
| 0.9 - 1.0 | Exact or near-exact equivalent |
| 0.7 - 0.89 | Strong overlap, minor differences |
| 0.5 - 0.69 | Partial overlap, significant differences |
| < 0.5 | Weak match, use with caution |

## Constraints

- Must return complete syllabus for full_structure query
- Cross-exam mapping must indicate confidence level
- Must handle topics not in syllabus gracefully (return not_found)
- Must not create or modify syllabus files
- Partial matches should use fuzzy matching algorithm

## Usage Notes

This skill is optional but useful for:
- Students switching between exam targets
- Transferring progress from one exam to another
- Understanding which topics are common across exams
- Building cross-exam practice tests
