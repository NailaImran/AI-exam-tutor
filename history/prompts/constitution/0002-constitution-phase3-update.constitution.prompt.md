---
id: "0002"
title: "constitution-phase3-update"
stage: constitution
date: 2026-01-30
surface: cli
model: claude-opus-4-5-20251101
feature: phase-3-growth-engine
branch: 002-question-bank-automation
user: human
command: /sp.constitution
labels: [constitution, phase-3, subagents, whatsapp, linkedin, privacy]
links:
  spec: specs/phase-3-core-tutoring/
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - .specify/memory/constitution.md
tests:
  - N/A (governance document)
---

## Prompt

Update constitution according to phase 3 requirements. Phase 3 includes:
- Study Plans & Reports (study-plan-generator, progress-report-generator)
- WhatsApp Integration (whatsapp-mcp, daily questions, test delivery)
- Social Media & Viral Features (LinkedIn posts, ERI badges, daily question selector)
- Human-in-the-Loop workflows (approval for study plans, social posts)
- 3 new subagents: study-strategy-planner, progress-reporting-coordinator, social-media-coordinator

## Response snapshot

Updated constitution from v1.0.0 to v1.1.0 with the following changes:

**New Principle Added:**
- VII. Privacy-First Sharing: Governs public sharing of student data with opt-in consent requirements

**New Sections Added:**
- Subagent Authority: Defines autonomous vs approval-required actions for 3 new subagents
- Scheduled Actions: Rules for cron-based automation (daily questions at 8 AM, weekly reports)
- External Integrations: WhatsApp MCP, LinkedIn MCP configuration
- Public Sharing Rules: ERI badge generation, achievement sharing consent requirements
- Channel-Specific Guidelines: WhatsApp, LinkedIn, Email communication styles

**Modified Sections:**
- VI. Bounded Autonomy: Expanded to include study plan drafts, progress reports, daily question selection
- Behavioral Rules: Added rules 8-10 for privacy consent, rate limits, approval workflows
- Self-Audit: Added external API health checks

**Version History Table:** Added to track amendments over time.

## Outcome

- ✅ Impact: Constitution ready for Phase 3 implementation with clear governance for external integrations
- 🧪 Tests: N/A (governance document, no automated tests)
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Phase 3 task implementation can begin
- 🧠 Reflection: Proactive constitution update before Phase 3 work prevents governance gaps

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): Standard /sp.constitution
- Next experiment: Monitor if subagent constraints are sufficient during Phase 3 implementation
