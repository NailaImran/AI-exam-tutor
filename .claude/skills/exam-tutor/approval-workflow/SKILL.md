# Skill: approval-workflow

**Category**: CORE (Phase 3)
**Purpose**: Process human-in-the-loop approval decisions for study plans and social posts

## Description

The approval-workflow skill handles the human approval process for items that require review before activation or publication. It moves items between needs_action/ and done/ folders, updates their status, and triggers notifications.

## Input

```json
{
  "action_type": "study_plan | social_post",
  "item_id": "string (plan ID or post ID)",
  "decision": "approve | reject",
  "reviewer": "string (reviewer identifier)",
  "feedback": "string (optional, required for rejection)"
}
```

## Output

```json
{
  "success": "boolean",
  "item_id": "string",
  "previous_status": "string",
  "new_status": "string",
  "source_path": "string (original location)",
  "destination_path": "string (new location)",
  "notification_sent": "boolean",
  "error": "string | null"
}
```

## Workflow

### For Study Plans

1. **Load item** from `needs_action/study-plans/{student_id}-plan-{date}.json`
2. **Validate** item exists and has status `pending_approval`
3. **If approved**:
   - Update status to `active`
   - Set approval.reviewed_at, approval.reviewer, approval.decision
   - Move to `done/study-plans/`
   - Copy to `memory/students/{student_id}/active-plan.json`
   - Queue WhatsApp notification (study_plan_approved)
4. **If rejected**:
   - Update status to `rejected`
   - Set approval.reviewed_at, approval.reviewer, approval.decision, approval.feedback
   - Move to `done/study-plans/`
   - Do NOT activate the plan

### For Social Posts

1. **Load item** from `needs_action/social-posts/linkedin-{date}.json`
2. **Validate** item exists and has status `pending_approval`
3. **If approved**:
   - Update status to `approved`
   - Set approval.reviewed_at, approval.reviewer, approval.decision
   - Trigger LinkedIn MCP publish (if available)
   - Update status to `published` after successful post
   - Move to `done/social-posts/`
4. **If rejected**:
   - Update status to `rejected`
   - Set approval.reviewed_at, approval.reviewer, approval.decision, approval.feedback
   - Move to `done/social-posts/`

## MCP Tools Used

- `mcp__filesystem__read_file` - Load pending items
- `mcp__filesystem__write_file` - Update item status, save to done/
- `mcp__linkedin__create_post` - Publish approved social posts (optional)

## Error Handling

- **Item not found**: Return error with item_id
- **Invalid status**: Return error if item not in pending_approval state
- **Rejection without feedback**: Return error requesting feedback
- **LinkedIn API failure**: Mark as approved but not published, log error

## Constitution Compliance

- **Principle VI (Bounded Autonomy)**: This skill enforces human approval before external actions
- **Principle VII (Privacy-First)**: Approval records include reviewer identity for audit

## Example Usage

```
Input: {
  "action_type": "study_plan",
  "item_id": "test-student-plan-2026-01-30",
  "decision": "approve",
  "reviewer": "admin@example.com"
}

Output: {
  "success": true,
  "item_id": "test-student-plan-2026-01-30",
  "previous_status": "pending_approval",
  "new_status": "active",
  "source_path": "needs_action/study-plans/test-student-plan-2026-01-30.json",
  "destination_path": "done/study-plans/test-student-plan-2026-01-30.json",
  "notification_sent": true,
  "error": null
}
```

## Related Skills

- study-plan-generator (creates items for approval)
- social-post-generator (creates items for approval)
- whatsapp-message-sender (sends notifications after approval)
