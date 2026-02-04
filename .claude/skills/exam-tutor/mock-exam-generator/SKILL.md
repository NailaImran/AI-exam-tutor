---
name: mock-exam-generator
description: Generates a full-length mock exam matching the real SPSC/PPSC/KPPSC format (100 questions, 180 minutes, 5 sections). Use this skill when a student needs realistic exam practice under authentic conditions. Creates a complete exam session with proper section distribution.
phase: 4
category: MASTERY
priority: P0
---

# Mock Exam Generator

Generates full-length mock exams matching real provincial public service commission exam formats.

## MCP Integration

This skill uses the **filesystem MCP server** for reading question bank and writing exam sessions.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read question bank files
- `mcp__filesystem__list_directory` - List available questions per topic
- `mcp__filesystem__write_file` - Save generated mock exam session

## Exam Format Configuration

### Standard Format (All Exams)
| Parameter | Value |
|-----------|-------|
| Total Questions | 100 |
| Duration | 180 minutes (3 hours) |
| Sections | 5 |
| Questions per Section | 20 |

### Section Distribution

| Section | Subject Code | Questions | Topics |
|---------|--------------|-----------|--------|
| 1 | pakistan_studies | 20 | History, Geography, Constitution, Culture |
| 2 | general_knowledge | 20 | Science, World Affairs, Organizations, Sports |
| 3 | current_affairs | 20 | Pakistan Current, World Current, Economy, Politics |
| 4 | english | 20 | Grammar, Vocabulary, Comprehension, Idioms |
| 5 | math_reasoning | 20 | Arithmetic, Algebra, Reasoning, Data Interpretation |

## Execution Steps

1. **Validate inputs**
   - student_id must be valid
   - exam_type must be SPSC, PPSC, or KPPSC
   - duration_minutes defaults to 180

2. **Generate session ID**
   ```
   session_id = "mock-{YYYY-MM-DD}-{sequence}"
   ```

3. **For each section, select questions**
   ```
   For section in [pakistan_studies, general_knowledge, current_affairs, english, math_reasoning]:
     questions = query_question_bank(
       exam_type: exam_type,
       subject: section,
       count: 20,
       exclude: previously_used_in_recent_mocks,
       difficulty_distribution: {easy: 6, medium: 10, hard: 4}
     )

     Shuffle questions within section
     Add to exam_questions[]
   ```

4. **Build mock exam session**
   ```json
   {
     "session_id": "{session_id}",
     "student_id": "{student_id}",
     "exam_type": "{exam_type}",
     "exam_format": {
       "total_questions": 100,
       "duration_minutes": 180,
       "sections": ["pakistan_studies", "general_knowledge", "current_affairs", "english", "math_reasoning"]
     },
     "questions": [
       {
         "question_number": 1,
         "section": "pakistan_studies",
         "question_id": "PPSC-PK-042",
         "text": "...",
         "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
         "topic": "Constitutional Amendments",
         "difficulty": "medium"
       }
     ],
     "timing": {
       "recommended_time_per_question_seconds": 108,
       "section_time_allocation_minutes": 36
     },
     "status": "generated",
     "created_at": "{ISO 8601}"
   }
   ```

5. **Save mock exam session**
   ```
   Use: mcp__filesystem__write_file
   Path: memory/students/{student_id}/mock-exams/{session_id}.json
   Content: mock_exam_session (without answers - those come from question bank)
   ```

6. **Return session details**

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
  "duration_minutes": {
    "type": "integer",
    "required": false,
    "default": 180,
    "description": "Total exam duration in minutes"
  },
  "difficulty_distribution": {
    "type": "object",
    "required": false,
    "default": {"easy": 30, "medium": 50, "hard": 20},
    "description": "Percentage distribution of difficulty levels"
  },
  "exclude_question_ids": {
    "type": "array",
    "required": false,
    "default": [],
    "description": "Question IDs to exclude (e.g., from recent mocks)"
  }
}
```

## Output Schema

```json
{
  "session_id": {
    "type": "string",
    "description": "Unique identifier for the mock exam session"
  },
  "exam_type": {
    "type": "string"
  },
  "total_questions": {
    "type": "integer",
    "value": 100
  },
  "duration_minutes": {
    "type": "integer",
    "value": 180
  },
  "sections": {
    "type": "array",
    "items": {
      "name": "string",
      "question_count": "integer",
      "question_range": "[start, end]"
    }
  },
  "session_path": {
    "type": "string",
    "description": "Path where mock exam was saved"
  },
  "status": {
    "type": "enum",
    "values": ["generated", "error"]
  }
}
```

## File Paths

| Operation | Path |
|-----------|------|
| Read | `question-bank/{exam_type}/{subject}/*.json` |
| Write | `memory/students/{student_id}/mock-exams/{session_id}.json` |

## Difficulty Distribution

Default per section (20 questions):
- Easy: 6 questions (30%)
- Medium: 10 questions (50%)
- Hard: 4 questions (20%)

This matches the typical distribution in real PSC exams.

## Question Selection Algorithm

```
1. Load all questions for subject from question bank
2. Filter out excluded question IDs
3. Group by difficulty
4. Randomly select required count from each difficulty bucket
5. Shuffle selected questions
6. Assign question numbers (1-100)
```

## Constraints

- Must generate exactly 100 questions
- Must include exactly 20 questions per section
- Must respect difficulty distribution
- Must not include questions from recent mocks (if exclude_question_ids provided)
- Questions must be shuffled within sections
- Session file must not include correct answers (security)
- Must handle insufficient questions in bank gracefully

## Error Handling

| Error | Response |
|-------|----------|
| Insufficient questions in bank | Return partial exam with warning |
| Invalid exam_type | Return error |
| Student not found | Return error |
| File write failure | Return error with details |

## Example Output

```json
{
  "session_id": "mock-2025-02-02-001",
  "exam_type": "PPSC",
  "total_questions": 100,
  "duration_minutes": 180,
  "sections": [
    {"name": "pakistan_studies", "question_count": 20, "question_range": [1, 20]},
    {"name": "general_knowledge", "question_count": 20, "question_range": [21, 40]},
    {"name": "current_affairs", "question_count": 20, "question_range": [41, 60]},
    {"name": "english", "question_count": 20, "question_range": [61, 80]},
    {"name": "math_reasoning", "question_count": 20, "question_range": [81, 100]}
  ],
  "session_path": "memory/students/student_123/mock-exams/mock-2025-02-02-001.json",
  "status": "generated"
}
```

## Usage Notes

- Generate mock exams weekly for best results
- Exclude questions from last 3 mocks to ensure variety
- Use with mock-exam-conductor subagent for full workflow
- Follow up with mock-exam-evaluator after completion
