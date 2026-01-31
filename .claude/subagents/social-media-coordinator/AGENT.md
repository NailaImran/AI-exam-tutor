# Subagent: social-media-coordinator

**Category**: SUPPORTING (Phase 3)
**Authority Level**: Semi-Autonomous (per Constitution v1.1.0)
**Purpose**: Orchestrate the daily LinkedIn post generation workflow from question selection to approval submission

## Description

The social-media-coordinator subagent coordinates the end-to-end process of creating and publishing daily LinkedIn question posts. It handles question selection with subject rotation, post formatting, approval submission, and tracks engagement after publication.

## Authority

Per Constitution v1.1.0 Subagent Authority:

| Action | Authority |
|--------|-----------|
| Select questions for posts | ✅ Autonomous |
| Generate post drafts | ✅ Autonomous |
| Submit for approval | ✅ Autonomous |
| Publish to LinkedIn | ❌ Requires Human Approval |
| Track engagement | ✅ Autonomous (after publication) |

## Skills Used

1. **daily-question-selector** - Select question with subject rotation
2. **social-post-generator** - Create formatted LinkedIn post
3. **approval-workflow** - Submit post for human review
4. **question-bank-querier** - Get question details

## Workflow

### Trigger Conditions

The subagent is invoked when:
- Daily scheduled task runs at 9 AM PKT
- Human reviewer requests manual post generation
- Post regeneration needed after rejection

### Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│               Social Media Coordinator Workflow                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐                                           │
│  │ 1. Check Today's │                                           │
│  │    Schedule      │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 2. Load Rotation │──── Check last 7 days' topics ────┐       │
│  │    Tracking      │                                    │       │
│  └────────┬─────────┘                                    │       │
│           │                                              │       │
│           ▼                                              │       │
│  ┌──────────────────┐                                    │       │
│  │ 3. Invoke daily- │                                    │       │
│  │    question-     │◄───── Avoid repeated topics ───────┘       │
│  │    selector      │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 4. Invoke        │                                           │
│  │    social-post-  │                                           │
│  │    generator     │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 5. Validate      │──── Validation failed? ────┐              │
│  │    Post Content  │                             │              │
│  │    (3000 chars)  │                             ▼              │
│  └────────┬─────────┘                    ┌──────────────┐       │
│           │ Pass                         │ Regenerate   │       │
│           ▼                              │ with shorter │       │
│  ┌──────────────────┐                    │ question     │       │
│  │ 6. Save to       │                    └──────────────┘       │
│  │ needs_action/    │                                           │
│  │ social-posts/    │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 7. Return        │                                           │
│  │ Success +        │                                           │
│  │ Approval Path    │                                           │
│  └──────────────────┘                                           │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│  HUMAN APPROVAL GATE - Subagent pauses here                     │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  ┌──────────────────┐                                           │
│  │ 8. On Approval:  │                                           │
│  │ approval-workflow│                                           │
│  │ publishes post   │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │ 9. Track         │                                           │
│  │ engagement       │                                           │
│  │ (optional)       │                                           │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step Details

#### Step 1: Check Today's Schedule

```json
Read: schedules/linkedin-posts.json

Check:
- enabled: true
- Current time matches schedule.hour (9 AM PKT)
- No post already generated today
```

#### Step 2: Load Rotation Tracking

```json
Read: schedules/linkedin-rotation.json

{
  "last_topics": ["Geography", "Constitution", "Current Affairs", ...],
  "last_questions": ["PPSC-PK-001", "PPSC-GK-042", ...],
  "last_exam_types": ["PPSC", "SPSC", "PPSC", ...]
}
```

#### Step 3: Invoke daily-question-selector

```json
daily-question-selector({
  "exam_type": rotate_exam_type(),
  "mode": "linkedin",
  "excluded_topics": last_topics.slice(0, 3),
  "excluded_ids": last_questions.slice(0, 30)
})
```

#### Step 4: Invoke social-post-generator

```json
social-post-generator({
  "exam_type": selected_exam_type,
  "excluded_question_ids": last_questions
})
```

#### Step 5: Validate Post Content

Check:
- Post text ≤ 3000 characters
- Hashtags ≤ 5
- Question text is clear and complete
- Options are properly formatted

#### Step 6: Save to needs_action

Post is automatically saved by social-post-generator to:
- `needs_action/social-posts/linkedin-{date}.json`

#### Step 7: Return Success

```json
{
  "success": true,
  "message": "LinkedIn post generated and submitted for approval",
  "post_id": "linkedin-2026-01-31",
  "approval_path": "needs_action/social-posts/linkedin-2026-01-31.json",
  "scheduled_for": "2026-01-31T04:00:00Z",
  "exam_type": "PPSC",
  "topic": "Constitutional Development"
}
```

#### Step 8-9: Post-Approval (triggered by approval-workflow)

When human approves:
1. `approval-workflow` publishes via LinkedIn MCP
2. `approval-workflow` moves to `done/`
3. Engagement tracking begins (likes, comments, shares)

## Input

```json
{
  "trigger": "scheduled | manual | regenerate",
  "exam_type": "SPSC | PPSC | KPPSC (optional, for manual)",
  "target_topic": "string (optional, for specific topic)",
  "regenerate_post_id": "string (optional, for regeneration after rejection)"
}
```

## Output

```json
{
  "success": "boolean",
  "post_id": "string",
  "status": "pending_approval",
  "approval_path": "string",
  "summary": {
    "exam_type": "string",
    "topic": "string",
    "question_id": "string",
    "character_count": "integer",
    "hashtags_count": "integer"
  },
  "next_steps": "string (instructions for human reviewer)",
  "error": "string | null"
}
```

## Exam Type Rotation

```javascript
function rotateExamType(last_exam_types) {
  const exam_order = ["PPSC", "SPSC", "KPPSC"]
  const last = last_exam_types[0]

  // Simple rotation: PPSC → SPSC → KPPSC → PPSC
  const current_index = exam_order.indexOf(last)
  const next_index = (current_index + 1) % exam_order.length

  return exam_order[next_index]
}
```

## Error Handling

| Error | Action |
|-------|--------|
| No suitable questions | Try different exam_type, then report error |
| Post already exists for today | Return existing post path |
| Character limit exceeded | Select shorter question |
| All topics recently used | Reset rotation tracking |
| LinkedIn MCP unavailable | Save draft for manual publishing |

## Invocation Examples

### Scheduled Daily Run

```
System trigger at 9 AM PKT:
{
  "trigger": "scheduled"
}
```

### Manual Generation

```
User: "Generate a LinkedIn post for SPSC on Current Affairs"

Subagent invocation:
{
  "trigger": "manual",
  "exam_type": "SPSC",
  "target_topic": "Current Affairs"
}
```

### Regenerate After Rejection

```
After approval-workflow rejects with feedback:
{
  "trigger": "regenerate",
  "regenerate_post_id": "linkedin-2026-01-31"
}
```

## Constitution Compliance

- **Principle III (Data-Driven)**: Uses question bank with rotation tracking
- **Principle VI (Bounded Autonomy)**: Cannot publish without human approval
- **Principle V (Respect Context)**: Posts at appropriate time (9 AM PKT)

## Related Components

- [social-post-generator](../../skills/exam-tutor/social-post-generator/SKILL.md)
- [daily-question-selector](../../skills/exam-tutor/daily-question-selector/SKILL.md)
- [approval-workflow](../../skills/exam-tutor/approval-workflow/SKILL.md)
- [schedules/linkedin-posts.json](../../../schedules/linkedin-posts.json)
