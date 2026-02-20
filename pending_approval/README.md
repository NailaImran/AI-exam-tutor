# /pending_approval

Claude places approval requests here when a sensitive action requires human review.

## File Naming
`APPROVAL_{action_type}_{description}_{YYYY-MM-DD}.md`

## To Approve
Move the file to /approved/ — the orchestrator will detect it and execute the action.

## To Reject
Move the file to /rejected/ — Claude will log the rejection and skip the action.

## Action Types That Require Approval
- Sending WhatsApp messages to students
- Publishing LinkedIn posts
- Generating and sending weekly reports
- Activating or modifying study plans
