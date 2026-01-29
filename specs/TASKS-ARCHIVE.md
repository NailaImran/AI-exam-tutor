# Implementation Tasks: Exam Tutor

**Project**: Digital FTE Competitive Exam Tutor
**Branch**: `001-phase1-foundation` (active), `002-question-bank-automation`
**Date**: 2026-01-26
**Status**: Phase 1 Complete, Phase 2 In Progress

---

## Overview

This document tracks all implementation tasks organized by MASTER_PLAN phases. Each phase maps to a hackathon tier and builds upon previous phases.

### Phase-to-Tier Mapping

| Phase | Name | Tier | Hours | Status |
|-------|------|------|-------|--------|
| **1** | Foundation | Bronze | 8-12 | ✅ COMPLETE |
| **2** | Core Product | Bronze+ to Silver | 12-20 | ⏳ IN PROGRESS |
| **3** | Growth Engine | Silver | 20-30 | ⏳ NOT STARTED |
| **4** | Full Platform | Gold | 30-40 | ⏳ NOT STARTED |
| **5** | Autonomous Excellence | Gold+ | 40+ | ⏳ NOT STARTED |

---

## Phase 1: Foundation (Bronze Tier) ✅ COMPLETE

**Goal**: Minimal viable tutoring with Obsidian vault - basic Q&A loop, student profiles, performance tracking.

**Skills Built**: student-profile-loader, question-bank-querier, answer-evaluator, performance-tracker

**Spec Folder**: `specs/phase-1-foundation/`

### Stage 1.1: Setup (Shared Infrastructure)

- [x] T001 Create vault root folder structure: inbox/, needs_action/, done/, students/, question-bank/, syllabus/, logs/
- [x] T002 [P] Create Question-Bank subdirectories at question-bank/SPSC/Pakistan-Studies/, question-bank/PPSC/Pakistan-Studies/, question-bank/KPPSC/Pakistan-Studies/
- [x] T003 [P] Create Syllabus subdirectories at syllabus/SPSC/, syllabus/PPSC/, syllabus/KPPSC/
- [x] T004 [P] Create Logs subdirectory at logs/watcher/
- [x] T005 [P] Create sample student sessions directory at students/STU001/sessions/
- [x] T006 Verify MCP filesystem configuration in .claude/mcp.json can read/write vault paths

### Stage 1.2: Foundational Content (Question Bank + Syllabus)

#### Syllabus Structure

- [x] T007 Create PPSC syllabus-structure.json at syllabus/PPSC/syllabus-structure.json with 20 Pakistan Studies topics
- [x] T008 [P] Create PPSC topic-weights.json at syllabus/PPSC/topic-weights.json
- [x] T009 [P] Create SPSC syllabus-structure.json at syllabus/SPSC/syllabus-structure.json
- [x] T010 [P] Create KPPSC syllabus-structure.json at syllabus/KPPSC/syllabus-structure.json
- [x] T011 [P] Create cross-exam-mapping.json at syllabus/cross-exam-mapping.json

#### Question Bank (150+ questions)

- [x] T012 Create PPSC Pakistan Studies questions (10) at question-bank/PPSC/Pakistan-Studies/constitutional-history.json
- [x] T013 [P] Create PPSC Pakistan Studies questions (10) at question-bank/PPSC/Pakistan-Studies/independence-movement.json
- [x] T014 [P] Create PPSC Pakistan Studies questions (10) at question-bank/PPSC/Pakistan-Studies/geography.json
- [x] T015 [P] Create PPSC Pakistan Studies questions (10) at question-bank/PPSC/Pakistan-Studies/economy.json
- [x] T016 [P] Create PPSC Pakistan Studies questions (10) at question-bank/PPSC/Pakistan-Studies/foreign-relations.json
- [x] T017 [P] Create SPSC Pakistan Studies questions (10) at question-bank/SPSC/Pakistan-Studies/constitutional-history.json
- [x] T018 [P] Create SPSC Pakistan Studies questions (10) at question-bank/SPSC/Pakistan-Studies/independence-movement.json
- [x] T019 [P] Create SPSC Pakistan Studies questions (10) at question-bank/SPSC/Pakistan-Studies/geography.json
- [x] T020 [P] Create SPSC Pakistan Studies questions (10) at question-bank/SPSC/Pakistan-Studies/economy.json
- [x] T021 [P] Create SPSC Pakistan Studies questions (10) at question-bank/SPSC/Pakistan-Studies/foreign-relations.json
- [x] T022 [P] Create KPPSC Pakistan Studies questions (10) at question-bank/KPPSC/Pakistan-Studies/constitutional-history.json
- [x] T023 [P] Create KPPSC Pakistan Studies questions (10) at question-bank/KPPSC/Pakistan-Studies/independence-movement.json
- [x] T024 [P] Create KPPSC Pakistan Studies questions (10) at question-bank/KPPSC/Pakistan-Studies/geography.json
- [x] T025 [P] Create KPPSC Pakistan Studies questions (10) at question-bank/KPPSC/Pakistan-Studies/economy.json
- [x] T026 [P] Create KPPSC Pakistan Studies questions (10) at question-bank/KPPSC/Pakistan-Studies/foreign-relations.json

#### Skill Reference Documents

- [x] T027 Update schemas.md at .claude/skills/exam-tutor/references/schemas.md with all data schemas
- [x] T028 [P] Update mcp-integration.md at .claude/skills/exam-tutor/references/mcp-integration.md with vault paths
- [x] T029 [P] Update skill-orchestration.md at .claude/skills/exam-tutor/references/skill-orchestration.md with Phase 1 workflows

### Stage 1.3: Student Registration (US3)

- [x] T030 Create sample profile.json at students/STU001/profile.json
- [x] T031 Create empty history.json at students/STU001/history.json with initial structure
- [x] T032 Create empty topic-stats.json at students/STU001/topic-stats.json with initial structure
- [x] T033 Create baseline eri.json at students/STU001/eri.json with no-data state
- [x] T034 Implement student-profile-loader skill at .claude/skills/exam-tutor/student-profile-loader/SKILL.md
- [x] T035 Validate student-profile-loader skill returns valid profile object for STU001

### Stage 1.4: First Practice Test (US1)

- [x] T036 Implement question-bank-querier skill at .claude/skills/exam-tutor/question-bank-querier/SKILL.md
- [x] T037 Validate question-bank-querier returns 5 PPSC Pakistan Studies questions
- [x] T038 Implement answer-evaluator skill at .claude/skills/exam-tutor/answer-evaluator/SKILL.md
- [x] T039 Validate answer-evaluator scores sample answers correctly
- [x] T040 Implement performance-tracker skill at .claude/skills/exam-tutor/performance-tracker/SKILL.md
- [x] T041 Validate performance-tracker updates history.json and topic-stats.json
- [x] T042 Create sample test-request.md template at inbox/test-request-sample.md
- [x] T043 End-to-end test: Process test request and verify session saved

### Phase 1 Completion Gate ✅ PASSED

- [x] All vault folders exist per structure
- [x] 150+ questions in question bank (actual: 200+)
- [x] Syllabus files for all 3 exams
- [x] MCP configuration verified
- [x] Sample student profile created
- [x] 4 core skills operational (profile-loader, question-querier, answer-evaluator, performance-tracker)
- [x] End-to-end test: request → questions → answers → results → saved

**Phase 1 Summary**: 43/43 tasks complete (100%)

---

## Phase 2: Core Product (Bronze+ to Silver) ⏳ IN PROGRESS

**Goal**: Complete tutoring loop with ERI calculation, weak area identification, adaptive tests, and engagement features.

**Skills to Build**: exam-readiness-calculator, weak-area-identifier, diagnostic-assessment-generator, adaptive-test-generator, streak-tracker

**Spec Folders**: `specs/phase-2-question-bank/` (2A), `specs/phase-3-core-tutoring/` (2B)

### Stage 2A: Question Bank Automation

> Note: Basic question bank was created in Phase 1. This stage focuses on scaling to 1500+ questions.

- [x] T044 Create question bank pipeline documentation at specs/phase-2-question-bank/PAPER-COLLECTION-GUIDE.md
- [x] T045 [P] Set up Raw-Papers folder structure for source PDFs
- [x] T046 [P] Create sources-registry.json to track question origins
- [x] T047 [P] Create master-index.json for question bank indexing
- [x] T048 [P] Create cross-exam-links.json for topic equivalence
- [x] T049 Implement web scraping for pakmcqs.com (batch extraction)
- [x] T050 Add 100+ questions from web sources (PPSC History, Islamic Studies, Computer Science)
- [x] T051 Implement PDF extraction pipeline for scanned papers
- [x] T052 Add 500+ questions from PPSC solved papers
- [x] T053 Add 500+ questions from SPSC solved papers
- [x] T054 Add 500+ questions from KPPSC solved papers
- [x] T055 Update statistics.json to reflect 1500+ total questions

### Stage 2B: ERI Calculator & Dashboard (US2)

- [x] T056 Implement exam-readiness-calculator skill at .claude/skills/exam-tutor/exam-readiness-calculator/SKILL.md
- [x] T057 Validate ERI calculation matches formula: (Accuracy×0.40)+(Coverage×0.25)+(Recency×0.20)+(Consistency×0.15)
- [x] T058 Validate ERI band assignment: not_ready (0-20), developing (21-40), approaching (41-60), ready (61-80), exam_ready (81-100)
- [x] T059 Update performance-tracker to trigger ERI recalculation after each session
- [x] T060 Create Dashboard.md template at vault root with ERI display section
- [x] T061 Update Dashboard.md to show student name, target exam, and recent activity
- [x] T062 Validate Dashboard displays correct ERI for test-student after practice session

### Stage 2C: Weak Area Identification

- [x] T063 Implement weak-area-identifier skill at .claude/skills/exam-tutor/weak-area-identifier/SKILL.md
- [x] T064 Validate weak-area-identifier returns topics sorted by severity
- [x] T065 Add weak area display to Dashboard.md

### Stage 2D: Diagnostic & Adaptive Tests

- [x] T066 Implement diagnostic-assessment-generator skill
- [x] T067 Implement adaptive-test-generator skill
- [x] T068 Validate adaptive tests focus on weak topics

### Stage 2E: Documentation & Automation (US4, US5)

- [x] T069 Create Company_Handbook.md at vault root with system overview
- [x] T070 Add test request instructions to Company_Handbook.md
- [x] T071 Add ERI calculation documentation to Company_Handbook.md
- [x] T072 Add Constitution behavioral rules to Company_Handbook.md
- [x] T073 Implement inbox monitoring file watcher
- [x] T074 Implement request parser for test-request.md format
- [x] T075 Implement file movement logic: /inbox → /done or /needs_action
- [x] T076 Implement event logging to logs/watcher/{date}.log

### Stage 2F: Polish & Validation

- [ ] T077 Verify all 6 core skills pass input/output validation
- [ ] T078 Verify ERI calculation accuracy with manual calculation
- [ ] T079 Run full end-to-end test: New student → diagnostic → practice → ERI → Dashboard
- [ ] T080 Generate Phase 2 completion report

### Phase 2 Completion Gate ⏳ IN PROGRESS

- [x] Question bank expanded beyond 150 questions (currently 200+)
- [x] 1500+ questions in question bank (actual: 1,570)
- [x] exam-readiness-calculator computes ERI correctly (validated: test-student ERI = 37.90)
- [x] weak-area-identifier identifies knowledge gaps (validated: 1 weak, 1 strong, 28 untested)
- [x] Dashboard.md displays ERI with component breakdown
- [x] Company_Handbook.md complete with all sections
- [x] File watcher detects files within 5 seconds

**Phase 2 Summary**: 33/37 tasks complete (89%)

---

## Phase 3: Growth Engine (Silver) ⏳ NOT STARTED

**Goal**: Multi-channel engagement, viral features, monetization hooks.

**Skills to Build**: study-plan-generator, progress-report-generator, whatsapp-message-sender, social-post-generator, eri-badge-generator, daily-question-selector

**Subagents**: study-strategy-planner, progress-reporting-coordinator, social-media-coordinator

**Spec Folder**: `specs/phase-4-integrations/`

### Stage 3A: Study Plans & Reports

- [ ] T081 Implement study-plan-generator skill
- [ ] T082 Implement progress-report-generator skill
- [ ] T083 Create study-strategy-planner subagent
- [ ] T084 Create progress-reporting-coordinator subagent

### Stage 3B: WhatsApp Integration

- [ ] T085 Set up whatsapp-mcp server
- [ ] T086 Implement whatsapp-message-sender skill
- [ ] T087 Implement daily question delivery via WhatsApp
- [ ] T088 Implement test completion via WhatsApp

### Stage 3C: Social Media & Viral Features

- [ ] T089 Implement social-post-generator skill
- [ ] T090 Implement eri-badge-generator skill
- [ ] T091 Implement daily-question-selector skill
- [ ] T092 Create social-media-coordinator subagent
- [ ] T093 Set up linkedin-mcp server
- [ ] T094 Implement daily question auto-post to LinkedIn

### Stage 3D: Human-in-the-Loop

- [ ] T095 Implement approval workflow for study plans
- [ ] T096 Implement approval workflow for social posts
- [ ] T097 Set up cron scheduling for daily/weekly tasks

### Phase 3 Completion Gate

- [ ] WhatsApp bot sends daily question at 8 AM
- [ ] Student can complete test via WhatsApp
- [ ] Study plan requires human approval before activation
- [ ] ERI badge generated as shareable image
- [ ] Daily question auto-posts to LinkedIn
- [ ] 2+ watchers operational (filesystem + WhatsApp)

**Phase 3 Summary**: 0/17 tasks complete (0%)

---

## Phase 4: Full Platform (Gold) ⏳ NOT STARTED

**Goal**: B2B features, premium upsells, comprehensive logging.

**Skills to Build**: session-logger, syllabus-mapper, batch-test-assigner, performance-comparator, parent-report-generator, challenge-coordinator, mock-exam-generator, deep-dive-analyzer

**Subagent**: academy-operations-coordinator

**Spec Folder**: `specs/phase-5-gold-tier/`

### Stage 4A: B2B Academy Features

- [ ] T098 Implement batch-test-assigner skill
- [ ] T099 Implement performance-comparator skill
- [ ] T100 Implement parent-report-generator skill
- [ ] T101 Create academy-operations-coordinator subagent
- [ ] T102 Create multi-student dashboard view

### Stage 4B: Premium Features

- [ ] T103 Implement mock-exam-generator skill (100+ questions, timed)
- [ ] T104 Implement deep-dive-analyzer skill
- [ ] T105 Implement challenge-coordinator skill

### Stage 4C: Logging & Cross-Exam

- [ ] T106 Implement session-logger skill (audit trail)
- [ ] T107 Implement syllabus-mapper skill (cross-exam topics)

### Phase 4 Completion Gate

- [ ] Academy can view dashboard with 10+ students
- [ ] Batch test assigned to group, results aggregated
- [ ] Performance leaderboard shows rankings
- [ ] Parent receives weekly email/WhatsApp report
- [ ] Full 100-question timed mock exam works
- [ ] All sessions logged with audit trail

**Phase 4 Summary**: 0/10 tasks complete (0%)

---

## Phase 5: Autonomous Excellence (Gold+) ⏳ NOT STARTED

**Goal**: Fully autonomous operations, business integration, scaling.

**Skills to Build**: payment-tracker, subscription-manager, renewal-reminder, business-audit-generator, ceo-briefing-generator, referral-tracker, score-predictor

**Subagent**: business-intelligence-coordinator

### Stage 5A: Odoo Integration

- [ ] T108 Set up odoo-mcp server
- [ ] T109 Implement payment-tracker skill
- [ ] T110 Implement subscription-manager skill
- [ ] T111 Implement renewal-reminder skill

### Stage 5B: Business Intelligence

- [ ] T112 Implement business-audit-generator skill
- [ ] T113 Implement ceo-briefing-generator skill
- [ ] T114 Create business-intelligence-coordinator subagent

### Stage 5C: Ralph Wiggum Autonomous Loop

- [ ] T115 Implement observe-analyze-plan-act cycle
- [ ] T116 Set up 6-hour autonomous loop
- [ ] T117 Implement error recovery (90%+ failures)

### Stage 5D: Extended Social & Referrals

- [ ] T118 Set up twitter-mcp and instagram-mcp servers
- [ ] T119 Implement referral-tracker skill
- [ ] T120 Implement score-predictor skill (ML-based)

### Phase 5 Completion Gate

- [ ] Odoo tracks payments, shows subscription status
- [ ] Auto-renewal reminder sent 7 days before expiry
- [ ] Weekly business audit generated automatically
- [ ] CEO briefing summarizes all operations
- [ ] Ralph Wiggum loop runs autonomously
- [ ] Error recovery handles 90%+ of failures

**Phase 5 Summary**: 0/13 tasks complete (0%)

---

## Overall Progress

| Phase | Tasks | Complete | Remaining | Status |
|-------|-------|----------|-----------|--------|
| Phase 1: Foundation | 43 | 43 | 0 | ✅ COMPLETE |
| Phase 2: Core Product | 37 | 33 | 4 | ⏳ IN PROGRESS |
| Phase 3: Growth Engine | 17 | 0 | 17 | ⏳ NOT STARTED |
| Phase 4: Full Platform | 10 | 0 | 10 | ⏳ NOT STARTED |
| Phase 5: Autonomous | 13 | 0 | 13 | ⏳ NOT STARTED |
| **Total** | **120** | **76** | **44** | **63%** |

---

## Skill Inventory by Phase

| Phase | Skill | Category | Status |
|-------|-------|----------|--------|
| **1** | student-profile-loader | CORE | ✅ |
| **1** | question-bank-querier | CORE | ✅ |
| **1** | answer-evaluator | CORE | ✅ |
| **1** | performance-tracker | CORE | ✅ |
| **2** | exam-readiness-calculator | CORE | ✅ |
| **2** | weak-area-identifier | CORE | ✅ |
| **2** | diagnostic-assessment-generator | SUPPORTING | ✅ |
| **2** | adaptive-test-generator | SUPPORTING | ✅ |
| **3** | study-plan-generator | SUPPORTING | ⏳ |
| **3** | progress-report-generator | SUPPORTING | ⏳ |
| **3** | whatsapp-message-sender | ENGAGEMENT | ⏳ |
| **3** | social-post-generator | ENGAGEMENT | ⏳ |
| **3** | eri-badge-generator | ENGAGEMENT | ⏳ |
| **3** | daily-question-selector | ENGAGEMENT | ⏳ |
| **4** | session-logger | OPTIONAL | ⏳ |
| **4** | syllabus-mapper | OPTIONAL | ⏳ |
| **4** | batch-test-assigner | B2B | ⏳ |
| **4** | performance-comparator | B2B | ⏳ |
| **4** | parent-report-generator | B2B | ⏳ |
| **4** | challenge-coordinator | ENGAGEMENT | ⏳ |
| **4** | mock-exam-generator | PREMIUM | ⏳ |
| **4** | deep-dive-analyzer | PREMIUM | ⏳ |
| **5** | payment-tracker | BUSINESS | ⏳ |
| **5** | subscription-manager | BUSINESS | ⏳ |
| **5** | renewal-reminder | BUSINESS | ⏳ |
| **5** | business-audit-generator | BUSINESS | ⏳ |
| **5** | ceo-briefing-generator | BUSINESS | ⏳ |
| **5** | referral-tracker | ENGAGEMENT | ⏳ |
| **5** | score-predictor | PREMIUM | ⏳ |

**Skills Complete**: 8/29 (28%)

---

## Critical Path

```
Phase 1: Foundation (COMPLETE)
    │
    ├── student-profile-loader ✅
    ├── question-bank-querier ✅
    ├── answer-evaluator ✅
    └── performance-tracker ✅
            │
            ▼
Phase 2: Core Product (IN PROGRESS)
    │
    ├── exam-readiness-calculator ✅
    ├── weak-area-identifier ✅
    ├── diagnostic-assessment-generator ✅
    └── adaptive-test-generator ✅
            │
            ▼
Phase 3: Growth Engine
    │
    ├── study-plan-generator
    ├── whatsapp-message-sender
    └── social-post-generator
            │
            ▼
Phase 4: Full Platform
    │
    ├── batch-test-assigner
    ├── mock-exam-generator
    └── parent-report-generator
            │
            ▼
Phase 5: Autonomous
    │
    ├── payment-tracker
    ├── business-audit-generator
    └── ceo-briefing-generator
```

---

## Notes

- **[P]** marks parallelizable tasks
- Task IDs are globally unique across all phases
- Phase 2 combines "Phase 2A: Question Bank" and "Phase 2B: Core Tutoring" from MASTER_PLAN
- Spec folders follow the phase-X-name convention from MASTER_PLAN

---

**Next Action**: Continue Phase 2 Stage 2F - implement T077 (verify all core skills)

**Last Updated**: 2026-01-29 - Completed Stage 2E (T069-T076: Documentation & File Watcher)
