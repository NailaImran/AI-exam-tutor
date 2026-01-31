# Skill: daily-question-selector

**Category**: CORE (Phase 3)
**Purpose**: Select appropriate questions for daily delivery with subject rotation and duplicate avoidance

## Description

The daily-question-selector skill chooses questions for daily WhatsApp delivery and LinkedIn posts. It ensures variety by rotating subjects, avoiding recently used questions, and prioritizing weak areas for personalized delivery.

## Input

```json
{
  "exam_type": "SPSC | PPSC | KPPSC",
  "mode": "student | global",
  "student_id": "string (required if mode is student)",
  "excluded_question_ids": ["string (optional, questions to exclude)"],
  "excluded_subjects": ["string (optional, subjects used recently)"],
  "difficulty": "easy | medium | hard | adaptive (optional, default: adaptive)"
}
```

## Output

```json
{
  "question": {
    "id": "string",
    "text": "string",
    "options": {
      "A": "string",
      "B": "string",
      "C": "string",
      "D": "string"
    },
    "correct_answer": "A | B | C | D",
    "topic": "string",
    "subject": "string",
    "difficulty": "easy | medium | hard",
    "explanation": "string"
  },
  "selection_reason": "string",
  "subject_rotation": {
    "previous_subjects": ["string"],
    "selected_subject": "string"
  }
}
```

## Workflow

### For Student Mode (Daily Questions)

1. **Load student context**:
   - Read `memory/students/{student_id}/topic-stats.json`
   - Read `memory/students/{student_id}/weak-areas.json`
   - Read `memory/students/{student_id}/history.json` (recent questions)

2. **Determine subject rotation**:
   - Get subjects from last 3 daily questions
   - Exclude those subjects from selection pool
   - If all subjects used, reset rotation

3. **Prioritize by weak areas**:
   - 70% chance: Select from weak area topics
   - 30% chance: Select randomly for variety

4. **Select question**:
   - Filter questions by exam_type, subject, difficulty
   - Exclude recently used questions (last 30 days)
   - Select one question randomly from filtered pool

5. **Return with context**

### For Global Mode (LinkedIn Posts)

1. **Track global rotation**:
   - Read `schedules/linkedin-posts.json` for last posted subjects

2. **Select different subject**:
   - Choose subject not posted in last 3 days
   - Prioritize high-engagement subjects

3. **Select engaging question**:
   - Prefer questions with clear, interesting facts
   - Avoid overly technical or niche topics
   - Medium difficulty for broad appeal

## MCP Tools Used

- `mcp__filesystem__read_file` - Load student stats, question bank
- `mcp__filesystem__list_directory` - List available question files

## Subject Rotation Logic

```
Day 1: Pakistan Studies
Day 2: General Knowledge
Day 3: Current Affairs
Day 4: English
Day 5: Islamic Studies
Day 6: Mathematics
Day 7: (reset or review)
```

## Difficulty Selection (Adaptive Mode)

Based on student's recent performance:
- Accuracy > 80%: Select harder questions
- Accuracy 50-80%: Select medium questions
- Accuracy < 50%: Select easier questions

## Error Handling

- **No questions available**: Return error with reason (empty bank, all excluded)
- **Subject exhausted**: Fall back to any available subject
- **Student not found**: Use global mode defaults

## Constitution Compliance

- **Principle I (Accuracy First)**: Only selects verified questions from bank
- **Principle III (Data-Driven)**: Uses weak areas for personalization

## Example Usage

```
Input: {
  "exam_type": "SPSC",
  "mode": "student",
  "student_id": "test-student",
  "excluded_subjects": ["Pakistan Studies", "General Knowledge"]
}

Output: {
  "question": {
    "id": "SPSC-CA-042",
    "text": "Which organization is responsible for Pakistan's monetary policy?",
    "options": {
      "A": "Ministry of Finance",
      "B": "State Bank of Pakistan",
      "C": "Securities and Exchange Commission",
      "D": "Federal Board of Revenue"
    },
    "correct_answer": "B",
    "topic": "Economic Institutions",
    "subject": "Current Affairs",
    "difficulty": "medium",
    "explanation": "The State Bank of Pakistan (SBP) is the central bank responsible for monetary policy..."
  },
  "selection_reason": "Selected from weak area 'Economic Institutions' with subject rotation",
  "subject_rotation": {
    "previous_subjects": ["Pakistan Studies", "General Knowledge"],
    "selected_subject": "Current Affairs"
  }
}
```

## Question Tracking

To avoid repeats, the skill checks:
1. `memory/students/{student_id}/sessions/*.json` - Questions from practice sessions
2. `schedules/daily-questions.json` - Global daily question history
3. `schedules/linkedin-posts.json` - Posted question IDs

## Related Skills

- question-bank-querier (underlying question retrieval)
- weak-area-identifier (prioritization source)
- whatsapp-message-sender (delivery of selected question)
- social-post-generator (uses global mode selection)
