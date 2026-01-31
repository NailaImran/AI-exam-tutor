# WhatsApp Message Sender - Flow Documentation

## Overview

This document describes the complete WhatsApp integration flow for the AI Exam Tutor, including daily question delivery, answer processing, and feedback loops.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    WhatsApp Integration Flow                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ scheduled-task-  │───>│ daily-question-  │                   │
│  │ runner           │    │ selector         │                   │
│  └──────────────────┘    └────────┬─────────┘                   │
│          │                        │                              │
│          │                        ▼                              │
│          │               ┌──────────────────┐                   │
│          └──────────────>│ whatsapp-message-│                   │
│                          │ sender           │                   │
│                          └────────┬─────────┘                   │
│                                   │                              │
│                                   ▼                              │
│                          ┌──────────────────┐                   │
│                          │ WhatsApp MCP     │                   │
│                          │ Server           │                   │
│                          └────────┬─────────┘                   │
│                                   │                              │
│                                   ▼                              │
│                          ┌──────────────────┐                   │
│                          │ Student's        │                   │
│                          │ WhatsApp         │                   │
│                          └────────┬─────────┘                   │
│                                   │                              │
│                          (Student replies)                       │
│                                   │                              │
│                                   ▼                              │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ answer-evaluator │<───│ Incoming Message │                   │
│  └────────┬─────────┘    │ Handler          │                   │
│           │              └──────────────────┘                   │
│           ▼                                                      │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ performance-     │───>│ exam-readiness-  │                   │
│  │ tracker          │    │ calculator       │                   │
│  └──────────────────┘    └────────┬─────────┘                   │
│                                   │                              │
│                                   ▼                              │
│                          ┌──────────────────┐                   │
│                          │ whatsapp-message-│                   │
│                          │ sender (feedback)│                   │
│                          └──────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Daily Question Flow

### 1. Scheduled Trigger (8:00 AM PKT)

The `scheduled-task-runner` checks `schedules/daily-questions.json`:

```json
{
  "task_type": "daily_question",
  "enabled": true,
  "schedule": {
    "frequency": "daily",
    "hour": 8,
    "minute": 0,
    "timezone": "Asia/Karachi"
  }
}
```

### 2. Student Selection

For each student with `whatsapp.opted_in_daily_questions == true`:

1. Check timezone - only process if within delivery window
2. Check quiet hours - skip if in quiet period
3. Proceed to question selection

### 3. Question Selection

The `daily-question-selector` skill:

1. Loads student's weak areas
2. Checks recently sent questions (avoid repeats)
3. Applies subject rotation
4. Selects appropriate difficulty
5. Returns question with full details

### 4. Message Formatting

Using template from `contracts/whatsapp-templates.json`:

```
📚 Daily Question - PPSC

Good morning! Here's your daily practice question:

**Topic**: Independence Movement

When was the Lahore Resolution passed?

A) March 23, 1939
B) March 23, 1940
C) August 14, 1947
D) March 23, 1956

Reply with A, B, C, or D

Your current ERI: 58
```

### 5. Message Delivery

Via WhatsApp MCP Server:

```javascript
mcp__whatsapp__send_message({
  phone: "+923001234567",
  message: formattedMessage
})
```

### 6. Tracking

Question sent is tracked to:
- Prevent repeat sends
- Enable response matching
- Support analytics

## Answer Processing Flow

### 1. Receive Reply

When student replies (e.g., "B"):

```json
{
  "from": "+923001234567",
  "text": "B",
  "timestamp": "2026-01-30T08:05:23+05:00"
}
```

### 2. Match to Question

Look up the last question sent to this student to get question_id.

### 3. Evaluate Answer

The `answer-evaluator` skill:

```json
Input: {
  "question_id": "PPSC-PK-042",
  "student_answer": "B",
  "student_id": "test-student"
}

Output: {
  "is_correct": true,
  "correct_answer": "B",
  "explanation": "The Lahore Resolution was passed on March 23, 1940..."
}
```

### 4. Update Performance

The `performance-tracker` skill saves the result:

- Updates `topic-stats.json`
- Updates `history.json`
- Creates session record

### 5. Recalculate ERI

The `exam-readiness-calculator` skill:

- Computes new ERI based on updated stats
- Updates `eri.json`
- Returns new score and change

### 6. Send Feedback

Based on correctness:

**Correct Answer**:
```
✅ Correct!

Great job! The answer is **B**.

**Explanation**: The Lahore Resolution (Pakistan Resolution) was passed on March 23, 1940 at Minto Park (now Greater Iqbal Park) in Lahore...

📊 Your updated ERI: 60 (+2)

Keep up the great work! 💪

Topic: Independence Movement
```

**Incorrect Answer**:
```
❌ Not quite

The correct answer is **B**.

You answered: A

**Explanation**: The Lahore Resolution was passed on March 23, 1940, not 1939...

📊 Your updated ERI: 57

Don't worry - every mistake is a learning opportunity! 📖

Topic: Independence Movement
```

## Error Handling

### API Unavailable

If WhatsApp MCP is unavailable:

1. Queue message to `queue/whatsapp/{message_id}.json`
2. Set status to "pending"
3. Retry with exponential backoff (5m, 15m, 60m)
4. After 3 failures, mark as failed and alert admin

### Invalid Phone Number

- Validate E.164 format before send
- Return error immediately, do not queue
- Log invalid number for profile cleanup

### Student Not Found

- Log warning
- Skip this student
- Continue with next student in batch

## Testing

### Manual Test: Send Daily Question

```
/exam-tutor send daily question to test-student
```

Expected:
1. Question selected from PPSC bank
2. Message sent to +923001234567
3. Question tracked in session

### Manual Test: Process Answer

```
/exam-tutor process whatsapp reply from test-student answer B
```

Expected:
1. Answer evaluated
2. Stats updated
3. ERI recalculated
4. Feedback sent

### End-to-End Test

1. Ensure test-student profile has WhatsApp configured
2. Trigger daily question send
3. Simulate student reply
4. Verify feedback received
5. Check ERI updated correctly

## Configuration

### Environment Variables

```bash
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_ACCESS_TOKEN=your_access_token
```

### MCP Server

In `.claude/mcp.json`:

```json
{
  "whatsapp": {
    "command": "npx",
    "args": ["-y", "@anthropic-ai/mcp-server-whatsapp"],
    "env": {
      "WHATSAPP_PHONE_ID": "${WHATSAPP_PHONE_ID}",
      "WHATSAPP_ACCESS_TOKEN": "${WHATSAPP_ACCESS_TOKEN}"
    }
  }
}
```

### Schedule Configuration

In `schedules/daily-questions.json`:

```json
{
  "task_type": "daily_question",
  "enabled": true,
  "schedule": {
    "frequency": "daily",
    "hour": 8,
    "minute": 0,
    "timezone": "Asia/Karachi"
  },
  "target": {
    "scope": "all_opted_in"
  }
}
```

## Metrics

### Success Metrics

- **Delivery Rate**: % of scheduled messages successfully sent
- **Response Rate**: % of daily questions that receive a response
- **Response Time**: Average time between send and reply
- **Accuracy Trend**: Student accuracy over time

### Monitoring

- Check `queue/whatsapp/` for pending messages
- Check schedule `last_run` status
- Monitor failed message count

## Troubleshooting

### Messages Not Sending

1. Verify MCP server is configured
2. Check environment variables are set
3. Verify phone number format (+923001234567)
4. Check `queue/whatsapp/` for queued messages

### Wrong Question Sent

1. Check student's exam_target in profile
2. Verify question bank has questions for that exam
3. Check subject rotation state

### ERI Not Updating

1. Verify answer-evaluator returned result
2. Check performance-tracker executed
3. Verify exam-readiness-calculator ran
4. Check eri.json was updated

## Related Documentation

- [SKILL.md](./SKILL.md) - Skill specification
- [contracts/whatsapp-templates.json](../../../specs/phase-3-core-tutoring/contracts/whatsapp-templates.json) - Message templates
- [schemas.md](../references/schemas.md) - Data schemas
- [daily-question-selector](../daily-question-selector/SKILL.md) - Question selection
