# Quickstart: Phase 3 - Growth Engine

**Feature**: phase-3-core-tutoring
**Prerequisites**: Phase 1 + Phase 2 complete, Constitution v1.1.0

## Setup

### 1. Environment Variables

Create or update `.env` file with external API credentials:

```bash
# WhatsApp Business API
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_ACCESS_TOKEN=your_access_token

# LinkedIn API
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
```

### 2. MCP Server Configuration

Update `.claude/mcp.json` to add new servers:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "E:/AI-exam-tutor"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "whatsapp": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-whatsapp"],
      "env": {
        "WHATSAPP_PHONE_ID": "${WHATSAPP_PHONE_ID}",
        "WHATSAPP_ACCESS_TOKEN": "${WHATSAPP_ACCESS_TOKEN}"
      }
    },
    "linkedin": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-linkedin"],
      "env": {
        "LINKEDIN_ACCESS_TOKEN": "${LINKEDIN_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 3. Directory Structure

Ensure required directories exist:

```bash
mkdir -p needs_action/study-plans
mkdir -p needs_action/social-posts
mkdir -p done/study-plans
mkdir -p done/social-posts
mkdir -p schedules
mkdir -p queue/whatsapp
```

### 4. Student Profile Update

Add WhatsApp and sharing preferences to test student:

```json
// memory/students/test-student/profile.json - add these fields
{
  "whatsapp": {
    "phone_number": "+92300XXXXXXX",
    "verified": true,
    "opted_in_daily_questions": true,
    "opted_in_reports": true,
    "preferred_time": "08:00",
    "timezone": "Asia/Karachi"
  },
  "sharing_consent": {
    "display_name": "Test Student",
    "show_full_name": false,
    "allow_badge_sharing": true
  }
}
```

## Testing Workflows

### Stage 3A: Study Plans & Reports

#### Generate Study Plan

```
/exam-tutor generate study plan for test-student
```

Expected output:
- Plan saved to `memory/students/test-student/plans/plan-{date}.json`
- Copy placed in `needs_action/study-plans/{student}-plan-{date}.json`
- Status: `pending_approval`

#### Approve Study Plan

```
/exam-tutor approve study plan for test-student
```

Expected output:
- Plan moved from `needs_action/` to `done/`
- Active plan updated in `memory/students/test-student/active-plan.json`
- Status: `active`

#### Generate Progress Report

```
/exam-tutor generate weekly report for test-student
```

Expected output:
- Report saved to `memory/students/test-student/reports/report-{date}.md`
- Metadata saved to `memory/students/test-student/reports/report-{date}.json`

### Stage 3B: WhatsApp Integration

#### Send Daily Question (Manual Test)

```
/exam-tutor send daily question to test-student
```

Expected output:
- Question selected from question bank
- Message queued in `queue/whatsapp/`
- WhatsApp message sent via MCP

#### Simulate Answer Reception

```
/exam-tutor process whatsapp reply from test-student answer B
```

Expected output:
- Answer evaluated
- Feedback message sent
- Progress updated

### Stage 3C: Social Media & Viral

#### Generate ERI Badge

```
/exam-tutor generate eri badge for test-student
```

Expected output:
- Badge saved to `memory/students/test-student/badges/badge-{date}.png`
- Metadata saved to `memory/students/test-student/badges/badge-{date}.json`

#### Generate LinkedIn Post

```
/exam-tutor generate linkedin post for SPSC
```

Expected output:
- Post draft saved to `needs_action/social-posts/linkedin-{date}.json`
- Status: `pending_approval`

### Stage 3D: Human-in-the-Loop

#### Check Pending Approvals

```
/exam-tutor list pending approvals
```

Expected output:
- List of items in `needs_action/study-plans/` and `needs_action/social-posts/`

#### Approve Social Post

```
/exam-tutor approve linkedin post linkedin-{date}
```

Expected output:
- Post moved to `done/social-posts/`
- If LinkedIn MCP configured: Post published
- Status: `published`

## Schedule Configuration

### Daily Questions Schedule

Create `schedules/daily-questions.json`:

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
  },
  "last_run": null,
  "next_run": "2026-01-31T08:00:00+05:00"
}
```

### Weekly Reports Schedule

Create `schedules/weekly-reports.json`:

```json
{
  "task_type": "weekly_report",
  "enabled": true,
  "schedule": {
    "frequency": "weekly",
    "day_of_week": 0,
    "hour": 18,
    "minute": 0,
    "timezone": "Asia/Karachi"
  },
  "target": {
    "scope": "all_opted_in"
  },
  "last_run": null,
  "next_run": "2026-02-02T18:00:00+05:00"
}
```

### LinkedIn Posts Schedule

Create `schedules/linkedin-posts.json`:

```json
{
  "task_type": "linkedin_post",
  "enabled": true,
  "schedule": {
    "frequency": "daily",
    "hour": 9,
    "minute": 0,
    "timezone": "Asia/Karachi"
  },
  "target": {
    "scope": "global"
  },
  "last_run": null,
  "next_run": "2026-01-31T09:00:00+05:00"
}
```

## Validation Checklist

### Phase Gate Criteria

- [ ] WhatsApp bot sends daily question at 8 AM
- [ ] Student can complete test via WhatsApp
- [ ] Study plan requires human approval before activation
- [ ] ERI badge generated as shareable image
- [ ] LinkedIn auto-posts daily (with approval)
- [ ] 2+ watchers operational (filesystem + WhatsApp)
- [ ] Cron scheduling working

### End-to-End Test

1. Create test student with WhatsApp preferences
2. Generate and approve study plan
3. Send daily question via WhatsApp
4. Process answer and verify feedback
5. Generate weekly progress report
6. Generate ERI badge
7. Generate and approve LinkedIn post
8. Verify all files created correctly

## Troubleshooting

### WhatsApp Messages Not Sending

1. Check `WHATSAPP_PHONE_ID` and `WHATSAPP_ACCESS_TOKEN` are set
2. Verify MCP server is running: Check Claude Code logs
3. Check message queue: `queue/whatsapp/`
4. Check for failed messages with `status: "failed"`

### LinkedIn Posts Failing

1. Verify `LINKEDIN_ACCESS_TOKEN` is valid (tokens expire)
2. Check LinkedIn API rate limits (100 posts/day)
3. Verify post content is under 3000 characters

### Badge Generation Issues

1. Ensure SVG template exists: `specs/phase-3-core-tutoring/contracts/eri-badge-template.svg`
2. Check student has ERI calculated in `memory/students/{id}/eri.json`
3. Verify PNG conversion is working

### Approval Workflow Stuck

1. Check `needs_action/` for pending items
2. Verify reviewer has access to approve
3. Check approval decision is recorded in file
