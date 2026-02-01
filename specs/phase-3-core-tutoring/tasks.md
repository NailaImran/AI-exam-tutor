# Tasks: Phase 3 - Growth Engine

**Input**: Design documents from `/specs/phase-3-core-tutoring/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested - implementation tasks only.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

- **Skills**: `.claude/skills/exam-tutor/{skill-name}/SKILL.md`
- **Subagents**: `.claude/subagents/{agent-name}/AGENT.md`
- **Data**: `memory/students/{student_id}/`, `needs_action/`, `done/`, `schedules/`, `queue/`
- **Contracts**: `specs/phase-3-core-tutoring/contracts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Directory structure and MCP configuration for Phase 3

- [x] T001 Create workflow directories: needs_action/study-plans/, needs_action/social-posts/, done/study-plans/, done/social-posts/
- [x] T002 Create scheduling directory: schedules/
- [x] T003 Create message queue directory: queue/whatsapp/
- [x] T004 [P] Create student subdirectories template: plans/, reports/, badges/ in memory/students/{student_id}/
- [x] T005 [P] Update .claude/mcp.json with WhatsApp MCP server configuration per plan.md
- [x] T006 [P] Update .claude/mcp.json with LinkedIn MCP server configuration per plan.md
- [x] T007 Create .env.example with WHATSAPP_PHONE_ID, WHATSAPP_ACCESS_TOKEN, LINKEDIN_ACCESS_TOKEN

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core skills and schemas that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Extend student profile schema with whatsapp preferences in .claude/skills/exam-tutor/references/schemas.md
- [x] T009 Extend student profile schema with sharing_consent in .claude/skills/exam-tutor/references/schemas.md
- [x] T010 Extend student profile schema with notifications preferences in .claude/skills/exam-tutor/references/schemas.md
- [x] T011 [P] Add StudyPlan entity schema to .claude/skills/exam-tutor/references/schemas.md per data-model.md
- [x] T012 [P] Add ProgressReport entity schema to .claude/skills/exam-tutor/references/schemas.md per data-model.md
- [x] T013 [P] Add SocialPost entity schema to .claude/skills/exam-tutor/references/schemas.md per data-model.md
- [x] T014 [P] Add ScheduledTask entity schema to .claude/skills/exam-tutor/references/schemas.md per data-model.md
- [x] T015 [P] Add MessageQueue entity schema to .claude/skills/exam-tutor/references/schemas.md per data-model.md
- [x] T016 [P] Add ERIBadge entity schema to .claude/skills/exam-tutor/references/schemas.md per data-model.md
- [x] T017 Create approval-workflow skill in .claude/skills/exam-tutor/approval-workflow/SKILL.md
- [x] T018 Create scheduled-task-runner skill in .claude/skills/exam-tutor/scheduled-task-runner/SKILL.md
- [x] T019 Create daily-question-selector skill in .claude/skills/exam-tutor/daily-question-selector/SKILL.md
- [x] T020 Update test-student profile with WhatsApp and sharing_consent fields in memory/students/test-student/profile.json

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Daily WhatsApp Question Delivery (Priority: P1) 🎯 MVP

**Goal**: Students receive daily practice questions at 8 AM via WhatsApp, answer directly, get immediate feedback with ERI update

**Independent Test**: Send test question to registered phone, verify response flow works end-to-end

### Implementation for User Story 1

- [x] T021 [US1] Create whatsapp-message-sender skill in .claude/skills/exam-tutor/whatsapp-message-sender/SKILL.md
- [x] T022 [US1] Define skill inputs: phone_number, message_type, content, template_variables
- [x] T023 [US1] Define skill outputs: send_status, message_id, delivered_at
- [x] T024 [US1] Implement message template rendering using contracts/whatsapp-templates.json
- [x] T025 [US1] Implement daily_question message type with question formatting
- [x] T026 [US1] Implement answer_feedback_correct message type with ERI display
- [x] T027 [US1] Implement answer_feedback_incorrect message type with explanation
- [x] T028 [US1] Add message queueing logic for retry handling in queue/whatsapp/
- [x] T029 [US1] Create daily question workflow in whatsapp-message-sender that: selects question → formats message → sends via MCP
- [x] T030 [US1] Integrate with existing answer-evaluator skill for response processing
- [x] T031 [US1] Integrate with existing performance-tracker skill for stats update
- [x] T032 [US1] Integrate with existing exam-readiness-calculator skill for ERI update
- [x] T033 [US1] Create schedule config file schedules/daily-questions.json per data-model.md
- [x] T034 [US1] Document WhatsApp flow in .claude/skills/exam-tutor/whatsapp-message-sender/README.md

**Checkpoint**: Daily WhatsApp question delivery fully functional and testable independently

---

## Phase 4: User Story 2 - Personalized Study Plan with Approval (Priority: P2)

**Goal**: Generate study plans based on weak areas, submit for human approval before activation

**Independent Test**: Generate plan for test student, verify approval workflow moves plan from draft to active

### Implementation for User Story 2

- [x] T035 [US2] Create study-plan-generator skill in .claude/skills/exam-tutor/study-plan-generator/SKILL.md
- [x] T036 [US2] Define skill inputs: student_id, exam_type, target_exam_date, daily_time_minutes
- [x] T037 [US2] Define skill outputs: StudyPlan JSON per contracts/study-plan-schema.json
- [x] T038 [US2] Implement weak-area integration to get priority topics from weak-area-identifier skill
- [x] T039 [US2] Implement time allocation algorithm: weak_areas × severity_score = allocated_hours
- [x] T040 [US2] Implement weekly schedule generation with topic rotation
- [x] T041 [US2] Implement milestone generation based on ERI targets
- [x] T042 [US2] Implement draft → pending_approval status transition
- [x] T043 [US2] Save draft plan to memory/students/{student_id}/plans/plan-{date}.json
- [x] T044 [US2] Copy plan to needs_action/study-plans/{student_id}-plan-{date}.json for approval
- [x] T045 [US2] Extend approval-workflow skill to handle study_plan action type
- [x] T046 [US2] Implement approval flow: approve → move to done/ → update status → copy to active-plan.json
- [x] T047 [US2] Implement rejection flow: reject with feedback → move to done/ → mark rejected
- [x] T048 [US2] Create study-strategy-planner subagent in .claude/subagents/study-strategy-planner/AGENT.md
- [x] T049 [US2] Define subagent workflow: weak-area-identifier → study-plan-generator → approval-workflow
- [x] T050 [US2] Add study plan notification via whatsapp-message-sender when approved

**Checkpoint**: Study plan generation and approval workflow fully functional

---

## Phase 5: User Story 3 - Progress Report Delivery (Priority: P2)

**Goal**: Weekly reports with ERI trends, session counts, accuracy by topic, delivered via WhatsApp

**Independent Test**: Generate weekly report for student with practice history, verify accurate statistics

### Implementation for User Story 3

- [x] T051 [US3] Create progress-report-generator skill in .claude/skills/exam-tutor/progress-report-generator/SKILL.md
- [x] T052 [US3] Define skill inputs: student_id, period_start, period_end
- [x] T053 [US3] Define skill outputs: Report markdown file + metadata JSON
- [x] T054 [US3] Implement session aggregation from memory/students/{student_id}/sessions/
- [x] T055 [US3] Implement ERI trend calculation from history.json
- [x] T056 [US3] Implement topic performance breakdown from topic-stats.json
- [x] T057 [US3] Implement weak area identification summary
- [x] T058 [US3] Implement recommendation generation based on performance
- [x] T059 [US3] Generate markdown report per data-model.md template structure
- [x] T060 [US3] Save report to memory/students/{student_id}/reports/report-{date}.md
- [x] T061 [US3] Save metadata to memory/students/{student_id}/reports/report-{date}.json
- [x] T062 [US3] Implement weekly_report_summary WhatsApp template in contracts/whatsapp-templates.json
- [x] T063 [US3] Integrate with whatsapp-message-sender for delivery
- [x] T064 [US3] Create progress-reporting-coordinator subagent in .claude/subagents/progress-reporting-coordinator/AGENT.md
- [x] T065 [US3] Define subagent workflow: gather stats → generate report → notify via WhatsApp
- [x] T066 [US3] Create schedule config file schedules/weekly-reports.json per data-model.md
- [x] T067 [US3] Implement ERI improvement highlighting (5+ point gains get congratulations)

**Checkpoint**: Weekly progress reports generation and delivery fully functional

---

## Phase 6: User Story 4 - Shareable ERI Badge (Priority: P3)

**Goal**: Generate shareable PNG badges with ERI score, readiness band, exam type

**Independent Test**: Generate badge for student, verify valid image with correct ERI information

### Implementation for User Story 4

- [x] T068 [US4] Create eri-badge-generator skill in .claude/skills/exam-tutor/eri-badge-generator/SKILL.md
- [x] T069 [US4] Define skill inputs: student_id, include_display_name (boolean)
- [x] T070 [US4] Define skill outputs: badge_path, badge_metadata JSON
- [x] T071 [US4] Implement SVG template loading from contracts/eri-badge-template.svg
- [x] T072 [US4] Implement placeholder substitution: ERI_SCORE, READINESS_BAND, EXAM_TYPE, DISPLAY_NAME
- [x] T073 [US4] Implement band color mapping: not_ready=#e53e3e, developing=#ed8936, approaching=#ecc94b, ready=#48bb78, exam_ready=#38a169
- [x] T074 [US4] Implement privacy check: only include display_name if sharing_consent.allow_badge_sharing is true
- [x] T075 [US4] Save badge to memory/students/{student_id}/badges/badge-{date}.png
- [x] T076 [US4] Save metadata to memory/students/{student_id}/badges/badge-{date}.json
- [x] T077 [US4] Implement milestone detection: reached_40, reached_60, reached_80, exam_ready
- [x] T078 [US4] Implement milestone_badge WhatsApp template for milestone notifications
- [x] T079 [US4] Add milestone badge offering via whatsapp-message-sender

**Checkpoint**: ERI badge generation fully functional with privacy controls

---

## Phase 7: User Story 5 - Daily LinkedIn Question Post (Priority: P3)

**Goal**: Auto-generate daily question posts for LinkedIn at 9 AM PKT, require human approval

**Independent Test**: Generate draft post, verify proper formatting with hashtags

### Implementation for User Story 5

- [x] T080 [US5] Create social-post-generator skill in .claude/skills/exam-tutor/social-post-generator/SKILL.md
- [x] T081 [US5] Define skill inputs: exam_type, excluded_question_ids
- [x] T082 [US5] Define skill outputs: SocialPost JSON per data-model.md
- [x] T083 [US5] Implement question selection using daily-question-selector skill with subject rotation
- [x] T084 [US5] Implement post formatting per contracts/linkedin-post-template.json
- [x] T085 [US5] Implement hashtag selection based on exam_type and topic
- [x] T086 [US5] Implement 3000 character limit validation (LinkedIn constraint)
- [x] T087 [US5] Save draft to needs_action/social-posts/linkedin-{date}.json
- [x] T088 [US5] Extend approval-workflow skill to handle social_post action type
- [x] T089 [US5] Implement approval flow: approve → publish via LinkedIn MCP → move to done/
- [x] T090 [US5] Implement rejection flow: reject with feedback → move to done/ → mark rejected
- [x] T091 [US5] Create social-media-coordinator subagent in .claude/subagents/social-media-coordinator/AGENT.md
- [x] T092 [US5] Define subagent workflow: daily-question-selector → social-post-generator → approval-workflow
- [x] T093 [US5] Create schedule config file schedules/linkedin-posts.json per data-model.md
- [x] T094 [US5] Implement subject rotation tracking to avoid repeats

**Checkpoint**: LinkedIn post generation and approval workflow fully functional

---

## Phase 8: User Story 6 - Complete Test via WhatsApp (Priority: P4)

**Goal**: Students complete 5-10 question tests via WhatsApp conversation flow

**Independent Test**: Start test via WhatsApp, complete all questions through chat, verify results

### Implementation for User Story 6

- [x] T095 [US6] Extend whatsapp-message-sender skill with test session state management
- [x] T096 [US6] Implement test_start message type per contracts/whatsapp-templates.json
- [x] T097 [US6] Implement test_next_question message type for sequential delivery
- [x] T098 [US6] Implement test_complete message type with results breakdown
- [x] T099 [US6] Create WhatsApp test session state in memory/students/{student_id}/whatsapp-session.json
- [x] T100 [US6] Implement session state: active_test, current_question, answers[], started_at
- [x] T101 [US6] Integrate with adaptive-test-generator skill for test creation
- [x] T102 [US6] Implement sequential question delivery (no explanations until complete)
- [x] T103 [US6] Implement batch evaluation using answer-evaluator at test end
- [x] T104 [US6] Implement results formatting with per-question breakdown
- [x] T105 [US6] Implement 30-minute timeout for abandoned tests
- [x] T106 [US6] Implement session resume capability for partial completions
- [x] T107 [US6] Add "start test" keyword detection in incoming message handling

**Checkpoint**: Full test completion via WhatsApp fully functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Integration, validation, and documentation

- [x] T108 Update .claude/skills/exam-tutor/SKILL.md with Phase 3 skills inventory
- [x] T109 Update .claude/skills/exam-tutor/references/skill-orchestration.md with Phase 3 workflows
- [x] T110 [P] Validate all WhatsApp message templates render correctly
- [x] T111 [P] Validate all JSON schemas in contracts/ folder
- [x] T112 [P] Validate approval workflow for study plans end-to-end
- [x] T113 [P] Validate approval workflow for social posts end-to-end
- [x] T114 Test daily question schedule execution manually
- [x] T115 Test weekly report schedule execution manually
- [x] T116 Test LinkedIn post schedule execution manually
- [x] T117 Run quickstart.md validation checklist
- [x] T118 Update CLAUDE.md with Phase 3 skills and workflows

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (WhatsApp Daily) can proceed independently after Phase 2
  - US2 (Study Plans) can proceed independently after Phase 2
  - US3 (Progress Reports) depends on whatsapp-message-sender from US1
  - US4 (ERI Badges) can proceed independently after Phase 2
  - US5 (LinkedIn Posts) can proceed independently after Phase 2
  - US6 (WhatsApp Tests) depends on whatsapp-message-sender from US1
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (P1) | Phase 2 only | Foundation complete |
| US2 (P2) | Phase 2 only | Foundation complete |
| US3 (P2) | US1 (whatsapp-message-sender) | T034 complete |
| US4 (P3) | Phase 2 only | Foundation complete |
| US5 (P3) | Phase 2 only | Foundation complete |
| US6 (P4) | US1 (whatsapp-message-sender) | T034 complete |

### Parallel Opportunities

**Phase 1 (Setup)**: T004, T005, T006 can run in parallel

**Phase 2 (Foundational)**: T011-T016 can run in parallel (different schema sections)

**After Phase 2**:
- US1, US2, US4, US5 can all start in parallel
- US3 and US6 must wait for US1 completion

**Within User Stories**:
- Multiple skill definition tasks (inputs, outputs, templates) can run in parallel

---

## Parallel Example: Foundation Phase

```bash
# Launch all schema additions in parallel:
Task: "Add StudyPlan entity schema to .claude/skills/exam-tutor/references/schemas.md"
Task: "Add ProgressReport entity schema to .claude/skills/exam-tutor/references/schemas.md"
Task: "Add SocialPost entity schema to .claude/skills/exam-tutor/references/schemas.md"
Task: "Add ScheduledTask entity schema to .claude/skills/exam-tutor/references/schemas.md"
Task: "Add MessageQueue entity schema to .claude/skills/exam-tutor/references/schemas.md"
Task: "Add ERIBadge entity schema to .claude/skills/exam-tutor/references/schemas.md"
```

## Parallel Example: Independent User Stories

```bash
# After Phase 2, launch independent stories in parallel:
Task: "US1 - Create whatsapp-message-sender skill"
Task: "US2 - Create study-plan-generator skill"
Task: "US4 - Create eri-badge-generator skill"
Task: "US5 - Create social-post-generator skill"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T020)
3. Complete Phase 3: User Story 1 - Daily WhatsApp Questions (T021-T034)
4. **STOP and VALIDATE**: Test daily question flow end-to-end
5. Deploy/demo if ready - this alone provides daily engagement value

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (WhatsApp Daily) → Test → Deploy (MVP!)
3. Add US2 (Study Plans) → Test → Deploy
4. Add US3 (Progress Reports) → Test → Deploy
5. Add US4 (ERI Badges) → Test → Deploy
6. Add US5 (LinkedIn Posts) → Test → Deploy
7. Add US6 (WhatsApp Tests) → Test → Deploy
8. Polish phase → Final validation

### Silver Tier Gate Checklist

After all phases:
- [x] WhatsApp bot sends daily question at 8 AM
- [x] Student completes test via WhatsApp
- [x] Study plan requires human approval
- [x] ERI badge generated as PNG
- [x] LinkedIn auto-posts daily (with approval)
- [x] 2+ watchers operational (filesystem + WhatsApp)
- [x] Cron scheduling working

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All external actions (WhatsApp send, LinkedIn post) require MCP server configuration
- Constitution v1.1.0 requires human approval for study plans and social posts
