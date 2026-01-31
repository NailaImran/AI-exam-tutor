# Implementation Plan: Phase 3 - Growth Engine

**Branch**: `003-phase3-growth-engine` | **Date**: 2026-01-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/phase-3-core-tutoring/spec.md`

## Summary

Phase 3 extends the Exam Tutor with multi-channel engagement (WhatsApp, LinkedIn), personalized study plans with human-in-the-loop approval, progress reports, and viral ERI badges. The implementation uses Claude Code Skills (markdown-based), MCP servers for external APIs, and file-based scheduling.

## Technical Context

**Language/Version**: Claude Code Skills (Markdown prompts), JSON (data), Markdown (documents)
**Primary Dependencies**: MCP Filesystem Server, WhatsApp Business API (via MCP), LinkedIn API (via MCP)
**Storage**: Local filesystem (JSON files in memory/, needs_action/, done/)
**Testing**: Manual validation via skill execution, end-to-end workflow tests
**Target Platform**: Claude Code CLI with MCP server ecosystem
**Project Type**: Skills bundle with subagent orchestration
**Performance Goals**: Message delivery within 5 minutes of schedule, badge generation under 5 seconds
**Constraints**: Human approval required for study plans and social posts per Constitution v1.1.0
**Scale/Scope**: Single-tenant (one student at a time), file-based persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Phase 3 Compliance |
|-----------|-------------|-------------------|
| I. Accuracy First | Questions from verified sources | ✅ Uses existing Phase 2 question bank |
| II. Student Encouragement | Constructive feedback | ✅ Positive messaging in templates |
| III. Data-Driven | Recommendations from performance data | ✅ Study plans based on weak-area-identifier |
| IV. Transparency | ERI formula visible | ✅ Reports include component breakdown |
| V. Respect Context | Honor preferences | ✅ Timezone, notification opt-in respected |
| VI. Bounded Autonomy | Human approval for external actions | ✅ Study plans & posts go to needs_action/ |
| VII. Privacy-First | Consent for public sharing | ✅ Badges exclude PII without consent |

**Subagent Authority** (Constitution v1.1.0):

| Subagent | Autonomous | Requires Approval |
|----------|------------|-------------------|
| study-strategy-planner | Generate drafts | Activate plans |
| progress-reporting-coordinator | Generate reports | Send via external channels |
| social-media-coordinator | Draft posts | Publish to LinkedIn |

**Scheduled Actions** (Constitution v1.1.0):
- Daily question delivery: 8 AM local (auto after content pre-approved)
- Weekly progress report: Sunday 6 PM (auto-generate, manual send)
- Daily LinkedIn post: 9 AM PKT (requires approval)

**Gate Status**: ✅ PASS - All principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/phase-3-core-tutoring/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research
├── data-model.md        # Entity schemas
├── quickstart.md        # Getting started guide
├── contracts/           # Message/file format contracts
└── checklists/          # Quality validation
```

### Skills & Subagents

```text
.claude/skills/exam-tutor/
├── study-plan-generator/SKILL.md        # Generate personalized plans
├── progress-report-generator/SKILL.md   # Weekly progress reports
├── whatsapp-message-sender/SKILL.md     # Send messages via WhatsApp
├── social-post-generator/SKILL.md       # LinkedIn post drafts
├── eri-badge-generator/SKILL.md         # Shareable badge images
├── daily-question-selector/SKILL.md     # Question rotation logic
├── scheduled-task-runner/SKILL.md       # Cron-like execution
└── approval-workflow/SKILL.md           # Human-in-the-loop processing

.claude/subagents/
├── study-strategy-planner/AGENT.md
├── progress-reporting-coordinator/AGENT.md
└── social-media-coordinator/AGENT.md
```

### Data Storage

```text
memory/
└── students/{student_id}/
    ├── profile.json           # Existing - add whatsapp, preferences
    ├── active-plan.json       # Current study plan
    ├── plans/                 # Plan history
    │   └── plan-{date}.json
    └── reports/               # Progress reports
        └── report-{date}.md

needs_action/
├── study-plans/              # Pending approval
│   └── {student_id}-plan-{date}.json
└── social-posts/             # Pending approval
    └── linkedin-{date}.json

done/
├── study-plans/              # Approved/rejected
└── social-posts/             # Published/rejected

schedules/
├── daily-questions.json      # Student schedule config
├── weekly-reports.json       # Report schedule config
└── linkedin-posts.json       # Post schedule config
```

**Structure Decision**: Skill-based architecture with file-based workflow (inbox → needs_action → done pattern from Phase 2). MCP servers handle external API communication.

## Complexity Tracking

No constitution violations requiring justification. Architecture follows established Phase 1/2 patterns.

## Phase 0: Research Summary

See [research.md](./research.md) for full details.

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| WhatsApp Integration | WhatsApp Business API via MCP | Official API, reliable delivery, supports templates |
| LinkedIn Integration | LinkedIn API via MCP | Direct posting, professional audience |
| Image Generation | SVG template → PNG conversion | Simple, no external dependencies |
| Scheduling | File-based with manual trigger | Simpler than daemon, Claude Code can poll |
| Approval Workflow | needs_action/ folder pattern | Consistent with Phase 2 file watcher |

### MCP Server Configuration

```json
{
  "mcpServers": {
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

## Phase 1: Design

### Data Model

See [data-model.md](./data-model.md) for complete schemas.

#### New Entities

| Entity | Purpose | Storage |
|--------|---------|---------|
| StudyPlan | Personalized schedule | memory/students/{id}/plans/*.json |
| ProgressReport | Weekly summary | memory/students/{id}/reports/*.md |
| ERIBadge | Shareable image | memory/students/{id}/badges/*.png |
| SocialPost | LinkedIn draft | needs_action/social-posts/*.json |
| ScheduledTask | Cron config | schedules/*.json |
| MessageQueue | Outbound messages | queue/whatsapp/*.json |

#### Profile Extensions

```json
{
  "whatsapp": {
    "phone_number": "+92300XXXXXXX",
    "verified": true,
    "opted_in_daily_questions": true,
    "preferred_time": "08:00",
    "timezone": "Asia/Karachi"
  },
  "sharing_consent": {
    "display_name": "Fatima A.",
    "show_full_name": false,
    "allow_badge_sharing": true
  }
}
```

### Contracts

See [contracts/](./contracts/) folder for detailed specifications.

| Contract | Format | Purpose |
|----------|--------|---------|
| whatsapp-question.json | JSON | Daily question message template |
| whatsapp-feedback.json | JSON | Answer feedback message template |
| whatsapp-report.json | JSON | Weekly report summary template |
| linkedin-post.json | JSON | Daily question post template |
| study-plan.json | JSON | Plan structure |
| eri-badge.svg | SVG | Badge template |

### Skill Specifications

| Skill | Input | Output | MCP Tools |
|-------|-------|--------|-----------|
| study-plan-generator | student_id, exam_type | StudyPlan JSON | read_file, write_file |
| progress-report-generator | student_id | Report MD + summary | read_file, write_file |
| whatsapp-message-sender | phone, message_type, content | send_status | whatsapp.send_message |
| social-post-generator | question, exam_type | SocialPost JSON | read_file, write_file |
| eri-badge-generator | student_id | badge_path | read_file, write_file |
| daily-question-selector | exam_type, excluded_subjects | question | read_file, list_directory |
| scheduled-task-runner | task_type | execution_log | read_file, write_file |
| approval-workflow | action_type, item_id, decision | updated_status | read_file, write_file |

### Subagent Specifications

| Subagent | Skills Used | Workflow |
|----------|-------------|----------|
| study-strategy-planner | weak-area-identifier, study-plan-generator, approval-workflow | Analyze → Generate → Submit for approval |
| progress-reporting-coordinator | performance-tracker, progress-report-generator, whatsapp-message-sender | Gather stats → Generate → Notify |
| social-media-coordinator | daily-question-selector, social-post-generator, approval-workflow | Select → Generate → Submit for approval |

## Implementation Stages

### Stage 3A: Study Plans & Reports
1. Implement study-plan-generator skill
2. Implement progress-report-generator skill
3. Create study-strategy-planner subagent
4. Create progress-reporting-coordinator subagent
5. Add profile extensions for preferences

### Stage 3B: WhatsApp Integration
1. Configure whatsapp-mcp server
2. Implement whatsapp-message-sender skill
3. Implement daily-question-selector skill
4. Create daily question workflow
5. Create test-via-whatsapp workflow

### Stage 3C: Social Media & Viral
1. Configure linkedin-mcp server
2. Implement social-post-generator skill
3. Implement eri-badge-generator skill
4. Create social-media-coordinator subagent

### Stage 3D: Human-in-the-Loop
1. Implement approval-workflow skill
2. Implement scheduled-task-runner skill
3. Create schedule configuration files
4. End-to-end workflow testing

## Quickstart

See [quickstart.md](./quickstart.md) for setup and testing instructions.
