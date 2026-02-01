---
name: exam-tutor
description: Digital FTE Competitive Exam Tutor for SPSC, PPSC, and KPPSC provincial public service commission exams. Use this skill bundle when students need exam preparation help including diagnostic assessments, adaptive practice tests, progress tracking, weak area identification, Exam Readiness Index (ERI) calculation, and personalized study plans. Supports the complete exam preparation lifecycle from initial diagnosis to exam readiness.
---

# Exam Tutor Skill Bundle

A comprehensive skill bundle for competitive exam preparation targeting Pakistani provincial public service commissions.

## Supported Exams

| Exam | Full Name | Province |
|------|-----------|----------|
| SPSC | Sindh Public Service Commission | Sindh |
| PPSC | Punjab Public Service Commission | Punjab |
| KPPSC | Khyber Pakhtunkhwa Public Service Commission | KPK |

## Skill Inventory

### CORE Skills (6)

Essential skills for basic tutoring functionality:

| Skill | Purpose | MCP Tools |
|-------|---------|-----------|
| [student-profile-loader](./student-profile-loader/SKILL.md) | Load student context | read_file, list_directory |
| [question-bank-querier](./question-bank-querier/SKILL.md) | Retrieve questions | read_file, list_directory |
| [answer-evaluator](./answer-evaluator/SKILL.md) | Evaluate responses | *None (pure computation)* |
| [performance-tracker](./performance-tracker/SKILL.md) | Persist results | read_file, write_file |
| [exam-readiness-calculator](./exam-readiness-calculator/SKILL.md) | Calculate ERI | read_file |
| [weak-area-identifier](./weak-area-identifier/SKILL.md) | Find weak topics | read_file |

### SUPPORTING Skills (4)

Skills that enhance the tutoring experience:

| Skill | Purpose | MCP Tools |
|-------|---------|-----------|
| [diagnostic-assessment-generator](./diagnostic-assessment-generator/SKILL.md) | Create baseline tests | read_file, list_directory |
| [adaptive-test-generator](./adaptive-test-generator/SKILL.md) | Generate personalized tests | read_file, list_directory |
| [study-plan-generator](./study-plan-generator/SKILL.md) | Create study schedules | read_file, write_file |
| [progress-report-generator](./progress-report-generator/SKILL.md) | Generate reports | read_file, write_file |

### OPTIONAL Skills (2)

Additional capabilities for specific use cases:

| Skill | Purpose | MCP Tools |
|-------|---------|-----------|
| [session-logger](./session-logger/SKILL.md) | Audit logging | write_file, create_directory |
| [syllabus-mapper](./syllabus-mapper/SKILL.md) | Cross-exam mapping | read_file |

### Phase 3: Growth Engine Skills (8)

Skills for engagement, notifications, and social features:

| Skill | Purpose | MCP Tools |
|-------|---------|-----------|
| [whatsapp-message-sender](./whatsapp-message-sender/SKILL.md) | WhatsApp messaging & test sessions | WhatsApp MCP, read_file, write_file |
| [daily-question-selector](./daily-question-selector/SKILL.md) | Select daily questions with rotation | read_file |
| [scheduled-task-runner](./scheduled-task-runner/SKILL.md) | Cron-like task execution | read_file, write_file |
| [approval-workflow](./approval-workflow/SKILL.md) | Human-in-the-loop approvals | read_file, write_file |
| [eri-badge-generator](./eri-badge-generator/SKILL.md) | Generate shareable ERI badges | read_file, write_file |
| [social-post-generator](./social-post-generator/SKILL.md) | LinkedIn post generation | read_file, write_file |

### Phase 3: Subagents (3)

Autonomous agents that orchestrate skill workflows:

| Subagent | Purpose | Skills Used |
|----------|---------|-------------|
| [study-strategy-planner](../../subagents/study-strategy-planner/AGENT.md) | Orchestrate study plan creation | weak-area-identifier, study-plan-generator, approval-workflow |
| [progress-reporting-coordinator](../../subagents/progress-reporting-coordinator/AGENT.md) | Weekly report generation | progress-report-generator, whatsapp-message-sender |
| [social-media-coordinator](../../subagents/social-media-coordinator/AGENT.md) | LinkedIn post workflow | daily-question-selector, social-post-generator, approval-workflow |

## MCP Server Requirements

This skill bundle requires multiple MCP servers:

### Filesystem (Required)
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "E:/AI-exam-tutor"]
  }
}
```

### WhatsApp (Phase 3 - Optional)
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

### LinkedIn (Phase 3 - Optional)
```json
{
  "linkedin": {
    "command": "npx",
    "args": ["-y", "@anthropic-ai/mcp-server-linkedin"],
    "env": {
      "LINKEDIN_ACCESS_TOKEN": "${LINKEDIN_ACCESS_TOKEN}"
    }
  }
}
```

See [references/mcp-integration.md](./references/mcp-integration.md) for detailed MCP configuration.

## Data Directory Structure

```
project-root/
├── memory/
│   └── students/
│       └── {student_id}/
│           ├── profile.json
│           ├── history.json
│           ├── topic-stats.json
│           ├── eri.json
│           ├── weak-areas.json
│           ├── active-plan.json
│           ├── whatsapp-session.json     # Phase 3: WhatsApp test state
│           ├── sessions/
│           │   └── {session_id}.json
│           ├── plans/                     # Phase 3: Study plan history
│           │   └── plan-{date}.json
│           ├── reports/
│           │   └── {date}.md
│           └── badges/                    # Phase 3: ERI badges
│               ├── badge-{date}.svg
│               └── badge-{date}.json
├── question-bank/
│   ├── SPSC/
│   ├── PPSC/
│   └── KPPSC/
│       └── {Subject}/
│           └── {questions}.json
├── syllabus/
│   ├── SPSC/
│   ├── PPSC/
│   └── KPPSC/
│       ├── syllabus-structure.json
│       └── topic-weights.json
├── schedules/                             # Phase 3: Schedule configs
│   ├── daily-questions.json
│   ├── weekly-reports.json
│   ├── linkedin-posts.json
│   └── linkedin-rotation.json
├── needs_action/                          # Phase 3: Approval queues
│   ├── study-plans/
│   └── social-posts/
├── done/                                  # Phase 3: Completed approvals
│   ├── study-plans/
│   └── social-posts/
├── queue/                                 # Phase 3: Message queues
│   └── whatsapp/
└── logs/
    └── sessions/
        └── {student_id}/
            └── {session_id}.json
```

## Exam Readiness Index (ERI)

The ERI is a 0-100 score indicating exam preparedness:

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

### Readiness Bands

| Band | Score | Meaning |
|------|-------|---------|
| `not_ready` | 0-20 | Significant preparation needed |
| `developing` | 21-40 | Building foundational knowledge |
| `approaching` | 41-60 | Moderate readiness, gaps remain |
| `ready` | 61-80 | Good preparation level |
| `exam_ready` | 81-100 | Strong readiness for examination |

## Standard Workflows

### Daily Practice Session

```
1. student-profile-loader    → Load context
2. weak-area-identifier      → Get weak areas
3. exam-readiness-calculator → Current ERI
4. adaptive-test-generator   → Generate test
5. [Student completes test]
6. answer-evaluator          → Evaluate
7. performance-tracker       → Save results
8. exam-readiness-calculator → Updated ERI
```

### New Student Onboarding

```
1. Create profile files
2. diagnostic-assessment-generator → Baseline test
3. [Student completes diagnostic]
4. answer-evaluator          → Evaluate
5. performance-tracker       → Initialize stats
6. exam-readiness-calculator → Baseline ERI
7. weak-area-identifier      → Initial weak areas
8. study-plan-generator      → Create plan
```

### Phase 3: WhatsApp Daily Question

```
1. scheduled-task-runner      → Trigger at 8 AM PKT
2. daily-question-selector    → Select question with rotation
3. student-profile-loader     → Load student context
4. whatsapp-message-sender    → Send daily_question message
5. [Student replies A/B/C/D]
6. answer-evaluator           → Evaluate response
7. performance-tracker        → Update stats
8. exam-readiness-calculator  → Recalculate ERI
9. whatsapp-message-sender    → Send feedback message
```

### Phase 3: WhatsApp Test Session

```
1. [Student sends "start test"]
2. whatsapp-message-sender    → Detect intent, start session
3. adaptive-test-generator    → Create 5-question test
4. whatsapp-message-sender    → Send test_start with Q1
5. [Student answers each question]
6. whatsapp-message-sender    → Send test_next_question
7. [After all questions]
8. answer-evaluator           → Batch evaluate
9. performance-tracker        → Save session
10. exam-readiness-calculator → Update ERI
11. whatsapp-message-sender   → Send test_complete
```

### Phase 3: Study Plan Approval

```
1. study-strategy-planner     → Orchestrate workflow
2. weak-area-identifier       → Get priority topics
3. study-plan-generator       → Create plan draft
4. approval-workflow          → Save to needs_action/
5. [Human reviews and approves]
6. approval-workflow          → Move to done/, activate
7. whatsapp-message-sender    → Notify student
```

### Phase 3: LinkedIn Post Generation

```
1. scheduled-task-runner      → Trigger at 9 AM PKT
2. social-media-coordinator   → Orchestrate workflow
3. daily-question-selector    → Select with rotation
4. social-post-generator      → Create formatted post
5. approval-workflow          → Save to needs_action/
6. [Human reviews and approves]
7. approval-workflow          → Publish via LinkedIn MCP
```

See [references/skill-orchestration.md](./references/skill-orchestration.md) for complete workflow documentation.

## Reference Documentation

- [schemas.md](./references/schemas.md) - All data structure schemas
- [mcp-integration.md](./references/mcp-integration.md) - MCP server configuration
- [skill-orchestration.md](./references/skill-orchestration.md) - Workflow patterns

## Key Principles

1. **File-based memory** - All state persisted as JSON/Markdown files
2. **Atomic skills** - Each skill has single responsibility
3. **Deterministic** - Same inputs produce same outputs
4. **Composable** - Skills can be orchestrated by parent agent
5. **No user interaction** - Skills execute, parent agent communicates
