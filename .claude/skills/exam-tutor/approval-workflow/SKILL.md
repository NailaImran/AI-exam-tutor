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
   - Set published_at timestamp
   - Move to `done/social-posts/`
4. **If rejected**:
   - Update status to `rejected`
   - Set approval.reviewed_at, approval.reviewer, approval.decision, approval.feedback
   - Move to `done/social-posts/`
   - Do NOT publish the post

### Social Post Approval Implementation

```javascript
async function handleSocialPostApproval(item_id, decision, reviewer, feedback) {
  // 1. Load the pending post
  const post_path = `needs_action/social-posts/${item_id}.json`
  const post = await read_file(post_path)

  if (!post) {
    return { success: false, error: `Post not found: ${item_id}` }
  }

  if (post.status !== "pending_approval") {
    return { success: false, error: `Post not in pending_approval status: ${post.status}` }
  }

  const previous_status = post.status
  const now = new Date().toISOString()

  // 2. Update approval fields
  post.approval.reviewed_at = now
  post.approval.reviewer = reviewer
  post.approval.decision = decision

  if (decision === "approve") {
    // 3a. Approve flow
    post.status = "approved"

    // Try to publish via LinkedIn MCP
    try {
      const publish_result = await mcp__linkedin__create_post({
        text: post.content.text
      })

      if (publish_result.success) {
        post.status = "published"
        post.published_at = now
        post.engagement = {
          likes: 0,
          comments: 0,
          shares: 0
        }
      }
    } catch (error) {
      // MCP not available, leave as approved for manual publishing
      console.log("LinkedIn MCP unavailable, marking as approved only")
    }

  } else if (decision === "reject") {
    // 3b. Reject flow
    if (!feedback) {
      return { success: false, error: "Feedback required for rejection" }
    }

    post.status = "rejected"
    post.approval.feedback = feedback
  }

  // 4. Move to done/ folder
  const done_path = `done/social-posts/${item_id}.json`
  await write_file(done_path, JSON.stringify(post, null, 2))

  // 5. Remove from needs_action/
  await delete_file(post_path)

  return {
    success: true,
    item_id: item_id,
    previous_status: previous_status,
    new_status: post.status,
    source_path: post_path,
    destination_path: done_path,
    notification_sent: false, // No notification for social posts
    error: null
  }
}
```

### Social Post Rejection Example

```json
Input: {
  "action_type": "social_post",
  "item_id": "linkedin-2026-01-31",
  "decision": "reject",
  "reviewer": "social-media-manager@example.com",
  "feedback": "Question text is too long. Please shorten the options."
}

Output: {
  "success": true,
  "item_id": "linkedin-2026-01-31",
  "previous_status": "pending_approval",
  "new_status": "rejected",
  "source_path": "needs_action/social-posts/linkedin-2026-01-31.json",
  "destination_path": "done/social-posts/linkedin-2026-01-31.json",
  "notification_sent": false,
  "error": null
}
```

### Social Post Approval Example

```json
Input: {
  "action_type": "social_post",
  "item_id": "linkedin-2026-01-31",
  "decision": "approve",
  "reviewer": "social-media-manager@example.com"
}

Output: {
  "success": true,
  "item_id": "linkedin-2026-01-31",
  "previous_status": "pending_approval",
  "new_status": "published",
  "source_path": "needs_action/social-posts/linkedin-2026-01-31.json",
  "destination_path": "done/social-posts/linkedin-2026-01-31.json",
  "notification_sent": false,
  "error": null
}
```

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
