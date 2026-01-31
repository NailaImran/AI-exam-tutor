# Skill: whatsapp-message-sender

**Category**: CORE (Phase 3)
**Purpose**: Send messages to students via WhatsApp Business API including daily questions, feedback, reports, and test sessions

## Description

The whatsapp-message-sender skill handles all outbound WhatsApp communication with students. It supports multiple message types, template rendering, message queueing for retry handling, and integrates with the WhatsApp MCP server for delivery.

## Input

```json
{
  "phone_number": "string E.164 format (required)",
  "message_type": "daily_question | answer_feedback_correct | answer_feedback_incorrect | weekly_report_summary | test_start | test_next_question | test_complete | milestone_badge | study_plan_approved (required)",
  "content": {
    "question": {
      "id": "string (for question types)",
      "text": "string",
      "options": {"A": "", "B": "", "C": "", "D": ""},
      "topic": "string",
      "correct_answer": "string",
      "explanation": "string"
    },
    "student": {
      "id": "string",
      "display_name": "string",
      "current_eri": "number"
    },
    "feedback": {
      "student_answer": "string",
      "is_correct": "boolean",
      "new_eri": "number",
      "eri_change": "string (+2 or -1)"
    },
    "report": {
      "eri_start": "number",
      "eri_end": "number",
      "eri_change": "string",
      "sessions_count": "integer",
      "accuracy": "number",
      "weak_topic": "string",
      "recommendation": "string",
      "report_link": "string"
    },
    "test": {
      "question_count": "integer",
      "current": "integer",
      "total": "integer",
      "focus_topic": "string",
      "difficulty": "string",
      "results": {
        "correct": "integer",
        "accuracy": "number",
        "breakdown": "string"
      }
    },
    "milestone": {
      "milestone": "integer (40, 60, 80, 100)",
      "band": "string",
      "exam_type": "string"
    },
    "study_plan": {
      "weeks": "integer",
      "daily_minutes": "integer",
      "priority_topic": "string",
      "first_topic": "string",
      "first_date": "string",
      "exam_type": "string"
    }
  },
  "template_variables": "object (optional, for custom templates)"
}
```

## Output

```json
{
  "success": "boolean",
  "message_id": "string (msg-{uuid})",
  "send_status": "sent | queued | failed",
  "delivered_at": "string ISO 8601 | null",
  "queue_path": "string (if queued)",
  "error": "string | null"
}
```

## Message Types

### 1. daily_question

Sends the daily practice question to a student.

**Template**: `daily_question` from contracts/whatsapp-templates.json

**Required content fields**:
- `question.text`, `question.options`, `question.topic`
- `student.current_eri`
- `student.display_name` (optional)

**Format**:
```
📚 Daily Question - {exam_type}

Good morning! Here's your daily practice question:

**Topic**: {topic}

{question_text}

A) {option_a}
B) {option_b}
C) {option_c}
D) {option_d}

Reply with A, B, C, or D

Your current ERI: {current_eri}
```

### 2. answer_feedback_correct

Sends positive feedback when student answers correctly.

**Template**: `answer_feedback_correct`

**Required content fields**:
- `question.correct_answer`, `question.explanation`, `question.topic`
- `feedback.new_eri`, `feedback.eri_change`

**Format**:
```
✅ Correct!

Great job! The answer is **{correct_answer}**.

**Explanation**: {explanation}

📊 Your updated ERI: {new_eri} ({eri_change})

Keep up the great work! 💪

Topic: {topic}
```

### 3. answer_feedback_incorrect

Sends constructive feedback when student answers incorrectly.

**Template**: `answer_feedback_incorrect`

**Required content fields**:
- `question.correct_answer`, `question.explanation`, `question.topic`
- `feedback.student_answer`, `feedback.new_eri`

**Format**:
```
❌ Not quite

The correct answer is **{correct_answer}**.

You answered: {student_answer}

**Explanation**: {explanation}

📊 Your updated ERI: {new_eri}

Don't worry - every mistake is a learning opportunity! 📖

Topic: {topic}
```

### 4. weekly_report_summary

Sends a summary of the weekly progress report.

**Template**: `weekly_report_summary`

**Required content fields**:
- `student.display_name`
- `report.*` (all report fields)

### 5. test_start

Confirms test start and sends first question.

**Template**: `test_start`

**Required content fields**:
- `test.question_count`, `test.focus_topic`, `test.difficulty`
- `question.*`

### 6. test_next_question

Sends the next question in a test sequence.

**Template**: `test_next_question`

**Required content fields**:
- `test.current`, `test.total`
- `question.*`

### 7. test_complete

Sends test completion results with breakdown.

**Template**: `test_complete`

**Required content fields**:
- `test.results.*`
- `feedback.new_eri`, `feedback.eri_change`

### 8. milestone_badge

Notifies student of ERI milestone achievement.

**Template**: `milestone_badge`

**Required content fields**:
- `student.display_name`
- `milestone.*`

### 9. study_plan_approved

Notifies student their study plan is approved and active.

**Template**: `study_plan_approved`

**Required content fields**:
- `student.display_name`
- `study_plan.*`

## Workflow

### Send Message Flow

1. **Validate input**:
   - Check phone_number is E.164 format
   - Check message_type is supported
   - Validate required content fields for message_type

2. **Load template**:
   - Read template from `specs/phase-3-core-tutoring/contracts/whatsapp-templates.json`
   - Get format for specified message_type

3. **Render message**:
   - Substitute placeholders with content values
   - Apply any template_variables overrides

4. **Send via MCP**:
   - Call `mcp__whatsapp__send_message` with phone and rendered text
   - If MCP unavailable, queue message

5. **Handle response**:
   - On success: Return message_id and delivered_at
   - On failure: Queue for retry, return queue_path

### Daily Question Workflow

Complete workflow for sending daily questions:

1. **Select question** via daily-question-selector skill:
   ```
   daily-question-selector({
     exam_type: student.exam_target,
     mode: "student",
     student_id: student.student_id
   })
   ```

2. **Load student context**:
   - Read profile for current_eri, display_name
   - Read eri.json for latest score

3. **Format message** using daily_question template

4. **Send message** via WhatsApp MCP

5. **Track question** sent to avoid repeats

### Answer Processing Integration

When student replies with answer:

1. **Evaluate answer** via answer-evaluator skill:
   ```
   answer-evaluator({
     question_id: sent_question.id,
     student_answer: reply.text,
     student_id: student.student_id
   })
   ```

2. **Update performance** via performance-tracker skill:
   ```
   performance-tracker({
     student_id: student.student_id,
     session_type: "daily_question",
     results: [evaluation_result]
   })
   ```

3. **Recalculate ERI** via exam-readiness-calculator skill:
   ```
   exam-readiness-calculator({
     student_id: student.student_id
   })
   ```

4. **Send feedback** based on evaluation:
   - Correct: answer_feedback_correct
   - Incorrect: answer_feedback_incorrect

## Message Queueing

For retry handling when WhatsApp API is unavailable:

**Queue Location**: `queue/whatsapp/{message_id}.json`

**Queue Entry Schema**:
```json
{
  "$schema": "exam-tutor/message-queue/v1",
  "message_id": "msg-{uuid}",
  "created_at": "ISO 8601",
  "message_type": "string",
  "recipient": {
    "student_id": "string",
    "phone_number": "string"
  },
  "content": {
    "template": "string",
    "text": "rendered message text",
    "variables": {}
  },
  "status": "pending",
  "attempts": 0,
  "last_attempt": null,
  "error": null,
  "delivered_at": null
}
```

**Retry Logic**:
- Max attempts: 3
- Backoff: 5min, 15min, 60min
- After 3 failures: Mark as failed, notify admin

## MCP Tools Used

- `mcp__whatsapp__send_message` - Send text message
- `mcp__whatsapp__send_template` - Send template message (if supported)
- `mcp__filesystem__read_file` - Load templates, student data
- `mcp__filesystem__write_file` - Queue messages for retry

## Error Handling

| Error | Action |
|-------|--------|
| Invalid phone number | Return error, do not queue |
| Missing content fields | Return error with missing fields |
| WhatsApp API unavailable | Queue message for retry |
| Template not found | Return error |
| MCP server not configured | Queue message, log warning |

## Constitution Compliance

- **Principle II (Student Encouragement)**: Feedback messages use positive, constructive language
- **Principle V (Respect Context)**: Respects student timezone and quiet hours (checked before send)
- **Principle VII (Privacy-First)**: Uses display_name, never exposes full PII in messages

## Example Usage

### Send Daily Question

```json
Input: {
  "phone_number": "+923001234567",
  "message_type": "daily_question",
  "content": {
    "question": {
      "id": "PPSC-PK-042",
      "text": "When was the Lahore Resolution passed?",
      "options": {
        "A": "March 23, 1939",
        "B": "March 23, 1940",
        "C": "August 14, 1947",
        "D": "March 23, 1956"
      },
      "topic": "Independence Movement"
    },
    "student": {
      "id": "test-student",
      "display_name": "Ahmed K.",
      "current_eri": 58
    }
  }
}

Output: {
  "success": true,
  "message_id": "msg-a1b2c3d4",
  "send_status": "sent",
  "delivered_at": "2026-01-30T08:00:05+05:00",
  "queue_path": null,
  "error": null
}
```

### Send Correct Answer Feedback

```json
Input: {
  "phone_number": "+923001234567",
  "message_type": "answer_feedback_correct",
  "content": {
    "question": {
      "correct_answer": "B",
      "explanation": "The Lahore Resolution (Pakistan Resolution) was passed on March 23, 1940...",
      "topic": "Independence Movement"
    },
    "feedback": {
      "new_eri": 60,
      "eri_change": "+2"
    }
  }
}
```

## Milestone Badge Offering Workflow

When a student reaches an ERI milestone (40, 60, 80, or exam_ready), the system offers them a shareable badge:

### Automatic Milestone Detection

After each ERI recalculation, check for new milestones:

```javascript
async function checkAndOfferMilestoneBadge(student_id, new_eri, previous_eri) {
  const milestones = [40, 60, 80]

  for (const threshold of milestones) {
    // Check if just crossed this threshold
    if (new_eri >= threshold && previous_eri < threshold) {
      await sendMilestoneNotification(student_id, threshold, getBandForScore(new_eri))
      return true
    }
  }

  // Special case: reached exam_ready band (81+)
  if (new_eri >= 81 && previous_eri < 81) {
    await sendMilestoneNotification(student_id, new_eri, "exam_ready")
    return true
  }

  return false
}
```

### Send Milestone Notification

```javascript
async function sendMilestoneNotification(student_id, milestone, band) {
  const profile = await loadProfile(student_id)

  // Send milestone_badge message
  await whatsapp_message_sender({
    phone_number: profile.whatsapp.phone_number,
    message_type: "milestone_badge",
    content: {
      student: {
        display_name: profile.sharing_consent.display_name || profile.name
      },
      milestone: {
        milestone: milestone,
        band: formatBandLabel(band),
        exam_type: profile.exam_target
      }
    }
  })
}
```

### Handle Badge Request Reply

When student replies "BADGE" to milestone notification:

```javascript
async function handleBadgeRequest(student_id) {
  // 1. Check if student has badge sharing consent
  const profile = await loadProfile(student_id)

  if (!profile.sharing_consent.allow_badge_sharing) {
    // Send privacy prompt
    return sendPrivacyConsentRequest(student_id)
  }

  // 2. Generate badge via eri-badge-generator
  const badge_result = await eri_badge_generator({
    student_id: student_id,
    include_display_name: true
  })

  if (!badge_result.success) {
    return sendError(student_id, "Unable to generate badge. Please try again later.")
  }

  // 3. Send badge image via WhatsApp
  await sendBadgeImage(student_id, badge_result.badge_path)

  // 4. Send sharing instructions
  await whatsapp_message_sender({
    phone_number: profile.whatsapp.phone_number,
    message_type: "badge_delivery",
    content: {
      badge_path: badge_result.badge_path,
      share_message: `I just reached ERI ${badge_result.badge_metadata.eri_score} in my ${badge_result.badge_metadata.exam_type} preparation! 🎉`
    }
  })
}
```

### Integration with exam-readiness-calculator

The exam-readiness-calculator skill should trigger milestone checking:

```
exam-readiness-calculator output includes:
- previous_score: number
- current_score: number
- milestone_crossed: boolean
- milestone_value: number | null

If milestone_crossed is true:
  → Trigger milestone badge offering via whatsapp-message-sender
```

### Milestone Message Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  Milestone Badge Offering Flow                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                           │
│  │ ERI Recalculated │                                           │
│  │ (after practice) │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ Check Milestone  │──── No milestone crossed ────► (end)      │
│  │ Thresholds       │                                           │
│  └────────┬─────────┘                                           │
│           │ Milestone crossed!                                   │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ Send milestone_  │                                           │
│  │ badge message    │                                           │
│  │ via WhatsApp     │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ Student receives │                                           │
│  │ "Reply BADGE to  │                                           │
│  │ get shareable"   │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │ Student replies  │      │ No reply         │                 │
│  │ "BADGE"          │      │ (reminder later) │                 │
│  └────────┬─────────┘      └──────────────────┘                 │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ Check sharing    │──── No consent ────► Request consent      │
│  │ consent          │                                           │
│  └────────┬─────────┘                                           │
│           │ Has consent                                          │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ Generate badge   │                                           │
│  │ (eri-badge-      │                                           │
│  │ generator)       │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ Send badge image │                                           │
│  │ + share message  │                                           │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Related Skills

- daily-question-selector (selects questions)
- answer-evaluator (evaluates responses)
- performance-tracker (updates stats)
- exam-readiness-calculator (updates ERI, triggers milestone detection)
- progress-report-generator (generates reports for delivery)
- eri-badge-generator (generates shareable badges for milestones)
