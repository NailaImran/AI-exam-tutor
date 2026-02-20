# /approved

Move approval request files here from /pending_approval/ to authorize the action.

The orchestrator watches this folder every 30 seconds.
Once detected, it executes the action via the appropriate MCP and moves the file to /done/.
