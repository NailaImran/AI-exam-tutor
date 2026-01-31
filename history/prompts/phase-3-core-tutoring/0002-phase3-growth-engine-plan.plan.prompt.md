---
id: "0002"
title: "phase3-growth-engine-plan"
stage: plan
date: 2026-01-30
surface: cli
model: claude-opus-4-5-20251101
feature: phase-3-core-tutoring
branch: 003-phase3-growth-engine
user: human
command: /sp.plan
labels: [plan, phase-3, whatsapp, linkedin, mcp, skills, subagents]
links:
  spec: specs/phase-3-core-tutoring/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - specs/phase-3-core-tutoring/plan.md
  - specs/phase-3-core-tutoring/research.md
  - specs/phase-3-core-tutoring/data-model.md
  - specs/phase-3-core-tutoring/quickstart.md
  - specs/phase-3-core-tutoring/contracts/whatsapp-templates.json
  - specs/phase-3-core-tutoring/contracts/linkedin-post-template.json
  - specs/phase-3-core-tutoring/contracts/eri-badge-template.svg
  - specs/phase-3-core-tutoring/contracts/study-plan-schema.json
tests:
  - Manual validation via quickstart workflows
---

## Prompt

Execute /sp.plan to create implementation plan for Phase 3 Growth Engine specification.

## Response snapshot

Created comprehensive implementation plan with:

**Technical Context**:
- Language: Claude Code Skills (Markdown prompts), JSON, Markdown
- Dependencies: MCP Filesystem, WhatsApp Business API (MCP), LinkedIn API (MCP)
- Storage: Local filesystem (JSON/MD files)
- Architecture: Skills bundle with subagent orchestration

**Constitution Check**: ✅ PASS (all 7 principles satisfied)
- Accuracy First: Uses existing verified question bank
- Student Encouragement: Positive messaging templates
- Data-Driven: Study plans from weak-area-identifier
- Transparency: Reports include ERI breakdown
- Respect Context: Timezone/notification preferences honored
- Bounded Autonomy: Human approval for external actions
- Privacy-First: Badges exclude PII without consent

**Phase 0 Research** (research.md):
- WhatsApp: Business API via MCP
- LinkedIn: Share API via MCP
- Badges: SVG template → PNG
- Scheduling: File-based with manual trigger
- Approval: needs_action/ folder pattern

**Phase 1 Design**:
- 6 new entities: StudyPlan, ProgressReport, ERIBadge, SocialPost, ScheduledTask, MessageQueue
- 8 new skills defined with I/O contracts
- 3 subagents with workflow definitions
- Profile extensions for WhatsApp and sharing consent

**Contracts Created**:
- whatsapp-templates.json (9 message templates)
- linkedin-post-template.json (post format)
- eri-badge-template.svg (badge design)
- study-plan-schema.json (JSON Schema)

**Quickstart Guide**: Setup, testing workflows, validation checklist

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation
- 🧪 Tests: Manual validation workflows in quickstart.md
- 📁 Files: 8 files created (plan, research, data-model, quickstart, 4 contracts)
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Constitution check ensures governance compliance before implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check 7/7 PASS
- Prompt variant (if applicable): Standard /sp.plan
- Next experiment: Verify MCP server availability for WhatsApp/LinkedIn
