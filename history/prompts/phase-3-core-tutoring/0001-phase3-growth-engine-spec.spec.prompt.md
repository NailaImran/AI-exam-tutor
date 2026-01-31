---
id: "0001"
title: "phase3-growth-engine-spec"
stage: spec
date: 2026-01-30
surface: cli
model: claude-opus-4-5-20251101
feature: phase-3-core-tutoring
branch: 003-phase3-growth-engine
user: human
command: /sp.specify
labels: [spec, phase-3, whatsapp, linkedin, study-plans, viral]
links:
  spec: specs/phase-3-core-tutoring/spec.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - specs/phase-3-core-tutoring/spec.md
  - specs/phase-3-core-tutoring/checklists/requirements.md
tests:
  - N/A (specification document)
---

## Prompt

Create SPEC.md for Exam Tutor Phase 3: Growth Engine (Silver Tier)

Context:
- Location: /specs/phase-3-growth-engine/SPEC.md
- Depends on: Phase 1 + Phase 2 complete
- Goal: Multi-channel engagement, viral features, Silver tier completion

Scope by Stage:
- Stage 3A: Study Plans & Reports (study-plan-generator, progress-report-generator, subagents)
- Stage 3B: WhatsApp Integration (whatsapp-mcp, daily questions, test delivery)
- Stage 3C: Social Media & Viral (LinkedIn posts, ERI badges, daily question selector)
- Stage 3D: Human-in-the-Loop (approval workflows, cron scheduling)

## Response snapshot

Created comprehensive Phase 3 specification with:

**6 User Stories** (prioritized P1-P4):
1. Daily WhatsApp Question Delivery (P1)
2. Personalized Study Plan with Approval (P2)
3. Progress Report Delivery (P2)
4. Shareable ERI Badge (P3)
5. Daily LinkedIn Question Post (P3)
6. Complete Test via WhatsApp (P4)

**20 Functional Requirements** across 4 stages:
- FR-001 to FR-005: Study Plans & Reports
- FR-006 to FR-010: WhatsApp Integration
- FR-011 to FR-015: Social Media & Viral
- FR-016 to FR-020: Human-in-the-Loop

**10 Success Criteria** (all measurable, technology-agnostic):
- SC-001: 95% on-time delivery for WhatsApp questions
- SC-002: 80% response rate within 24 hours
- SC-003: 15-minute test completion via WhatsApp
- SC-004-010: Various performance and quality metrics

**6 Key Entities**: StudyPlan, ProgressReport, ERIBadge, SocialPost, ScheduledTask, MessageQueue

**Quality Checklist**: 16/16 items passed - spec ready for planning

## Outcome

- ✅ Impact: Complete Phase 3 specification ready for implementation planning
- 🧪 Tests: N/A (specification document)
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Comprehensive spec with clear user stories and measurable outcomes

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Quality checklist 16/16 PASS
- Prompt variant (if applicable): Standard /sp.specify
- Next experiment: Monitor if 6 user stories is appropriate scope for Silver tier
