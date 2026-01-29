---
name: file-watcher
description: Monitors the inbox/ folder for new test requests and processes them automatically. Use this skill to enable automated request handling. Parses markdown test requests, validates inputs, executes skill chains, and logs all activity.
---

# File Watcher

Monitors inbox folder and automatically processes test requests.

## MCP Integration

This skill uses the **filesystem MCP server** for all file operations.

### Required MCP Tools
- `mcp__filesystem__list_directory` - Monitor inbox for new files
- `mcp__filesystem__read_file` - Read request content
- `mcp__filesystem__write_file` - Write logs
- `mcp__filesystem__create_directory` - Create log directories

## Execution Steps

### 1. Monitor Inbox

```
Use: mcp__filesystem__list_directory
Path: inbox/

Check for new .md files every 5 seconds
Filter: *.md files not previously processed
```

### 2. Parse Request

When a new file is detected:

```
Use: mcp__filesystem__read_file
Path: inbox/{filename}.md

Extract fields using markdown parser:
  - Student ID (required)
  - Name (optional)
  - Exam Type (required: SPSC|PPSC|KPPSC)
  - Test Type (required: diagnostic|adaptive|timed)
  - Question Count (optional, default: 25)
  - Subject Focus (optional, default: All)
  - Difficulty (optional, default: mixed)
  - Time Limit (optional, default: none)
  - Focus on Weak Areas (optional, default: yes)
```

### 3. Validate Request

```
Required field checks:
  - student_id must be non-empty string
  - exam_type must be SPSC, PPSC, or KPPSC
  - test_type must be diagnostic, adaptive, or timed

If validation fails:
  → Move to needs_action/
  → Log error with specific reason
  → Exit processing
```

### 4. Process Request

Based on test_type:

**diagnostic**:
```
1. student-profile-loader (create if new)
2. diagnostic-assessment-generator
3. Output test to student folder
```

**adaptive**:
```
1. student-profile-loader
2. weak-area-identifier
3. adaptive-test-generator
4. Output test to student folder
```

**timed**:
```
1. student-profile-loader
2. question-bank-querier (with time_limit)
3. Output test to student folder
```

### 5. Move File

**On success**:
```
Move: inbox/{filename}.md → done/{filename}.md
```

**On failure**:
```
Move: inbox/{filename}.md → needs_action/{filename}.md
Add error details to file header
```

### 6. Log Activity

```
Use: mcp__filesystem__write_file
Path: logs/watcher/{YYYY-MM-DD}.log

Log format:
[{timestamp}] {LEVEL}: {message}

Levels: INFO, WARNING, ERROR, SUCCESS
```

## Input Schema

The file watcher reads markdown files with this structure:

```markdown
# Test Request

## Student Information
- **Student ID**: string (required)
- **Name**: string (optional)

## Test Configuration
- **Exam Type**: SPSC | PPSC | KPPSC (required)
- **Test Type**: diagnostic | adaptive | timed (required)
- **Question Count**: integer 10-100 (optional)
- **Subject Focus**: string (optional)

## Additional Options
- **Difficulty**: easy | medium | hard | mixed (optional)
- **Time Limit**: none | 30min | 60min | 90min (optional)
- **Focus on Weak Areas**: yes | no (optional)

## Notes
Free text (optional)
```

## Output Schema

### Processed Request (success)

File moved to `done/` with processing metadata added:

```markdown
---
processed_at: "2026-01-29T10:30:05Z"
status: success
test_id: "PPSC-ADAPT-student-001-20260129"
questions_generated: 25
---

# Test Request
[original content]
```

### Failed Request (error)

File moved to `needs_action/` with error details:

```markdown
---
attempted_at: "2026-01-29T10:30:05Z"
status: failed
error: "Missing required field: exam_type"
---

# Test Request
[original content]
```

## File Paths

| Path | Purpose |
|------|---------|
| `inbox/` | Monitored for new requests |
| `done/` | Successfully processed requests |
| `needs_action/` | Failed requests requiring attention |
| `logs/watcher/{date}.log` | Processing logs |

## Log Format

```
[2026-01-29T10:30:00Z] INFO: Watcher started
[2026-01-29T10:30:05Z] INFO: File detected: test-request-001.md
[2026-01-29T10:30:05Z] INFO: Parsing request...
[2026-01-29T10:30:06Z] INFO: Validation passed
[2026-01-29T10:30:06Z] INFO: Processing adaptive test for student-001
[2026-01-29T10:30:08Z] INFO: Test generated: 25 questions
[2026-01-29T10:30:08Z] INFO: Moving to done/
[2026-01-29T10:30:08Z] SUCCESS: Request processed successfully

[2026-01-29T10:35:00Z] INFO: File detected: test-request-002.md
[2026-01-29T10:35:01Z] ERROR: Missing required field: exam_type
[2026-01-29T10:35:01Z] INFO: Moving to needs_action/
[2026-01-29T10:35:01Z] WARNING: Request failed - manual review required
```

## Constraints

- Poll interval: 5 seconds (configurable)
- Only process .md files
- Never delete original files (move only)
- Log all operations
- Create directories if missing
- Handle concurrent requests sequentially

## Error Handling

| Error | Action | Log Level |
|-------|--------|-----------|
| Missing required field | Move to needs_action | ERROR |
| Invalid enum value | Move to needs_action | ERROR |
| Student not found | Create profile, continue | WARNING |
| Question bank insufficient | Generate partial, continue | WARNING |
| File system error | Retry 3 times, then fail | ERROR |
| Skill execution error | Move to needs_action | ERROR |

## Configuration

Default settings (can be overridden):

```json
{
  "poll_interval_seconds": 5,
  "max_retries": 3,
  "default_question_count": 25,
  "default_difficulty": "mixed",
  "default_focus_weak_areas": true,
  "log_retention_days": 30
}
```
