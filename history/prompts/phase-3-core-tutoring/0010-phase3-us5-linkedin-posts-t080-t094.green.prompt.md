---
id: "0010"
title: "phase3-us5-linkedin-posts-t080-t094"
stage: green
date: 2026-01-31
surface: cli
model: claude-opus-4-5-20251101
feature: phase-3-core-tutoring
branch: master
user: human
command: /sp.implement
labels: [green, phase-3, us5, linkedin, social-media]
links:
  spec: specs/phase-3-core-tutoring/spec.md
  plan: specs/phase-3-core-tutoring/plan.md
  tasks: specs/phase-3-core-tutoring/tasks.md
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - .claude/skills/exam-tutor/social-post-generator/SKILL.md
  - .claude/skills/exam-tutor/approval-workflow/SKILL.md
  - .claude/subagents/social-media-coordinator/AGENT.md
  - schedules/linkedin-posts.json
  - schedules/linkedin-rotation.json
tests:
  - Manual test via post generation for PPSC
  - Verify approval workflow moves to done/
---

## Prompt

```text
implement T080-T094
```

## Response snapshot

Completed 15 tasks for User Story 5 (Daily LinkedIn Question Posts):

**social-post-generator Skill (T080-T087, T094)**:
- Created comprehensive SKILL.md with:
  - Input: exam_type, excluded_question_ids, target_topic, scheduled_for
  - Output: SocialPost JSON per data-model.md
  - Question selection via daily-question-selector with subject rotation
  - Post formatting per contracts/linkedin-post-template.json
  - Hashtag selection: exam-specific (2) + topic (1) + general (2) = max 5
  - 3000 character limit validation
  - Draft saved to needs_action/social-posts/
  - Subject rotation tracking implementation

**approval-workflow Extension (T088-T090)**:
- Enhanced social_post handling with full implementation code
- handleSocialPostApproval function with approve/reject flows
- LinkedIn MCP integration for publishing
- Examples for both approval and rejection scenarios

**social-media-coordinator Subagent (T091-T092)**:
- Created AGENT.md with complete workflow
- Orchestrates: daily-question-selector → social-post-generator → approval-workflow
- Exam type rotation: PPSC → SPSC → KPPSC → PPSC
- Topic cooldown (3 days), question cooldown (30 days)
- ASCII workflow diagram

**Schedule Configuration (T093)**:
- Created schedules/linkedin-posts.json
- Daily at 9 AM Asia/Karachi
- Global scope with exam rotation config

**Rotation Tracking (T094)**:
- Created schedules/linkedin-rotation.json
- Tracks last_topics, last_questions, last_exam_types
- Statistics tracking for analytics

## Outcome

- ✅ Impact: User Story 5 COMPLETE - 15/15 tasks done (T080-T094)
- 🧪 Tests: Manual testing instructions documented
- 📁 Files: 5 files created/updated
- 🔁 Next prompts: Continue with US6 (WhatsApp Tests) T095-T107 or Phase 9 (Polish)
- 🧠 Reflection: LinkedIn integration complete with human-in-the-loop approval

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Skill structure follows template PASS
- Prompt variant (if applicable): Simple task range request
- Next experiment: Test actual LinkedIn MCP integration when credentials available
