# Implementation Plan: Exam Tutor Phase 1 - Foundation (Bronze Tier)

**Branch**: `001-phase1-foundation` | **Date**: 2026-01-18 | **Spec**: [SPEC.md](./SPEC.md)
**Input**: Feature specification from `/specs/phase-1-foundation/SPEC.md`

## Summary

Build a minimum viable tutoring system for Pakistani competitive exam preparation (SPSC, PPSC, KPPSC) within an Obsidian vault. The foundation includes:
- Vault folder structure with Dashboard and Company Handbook
- File system monitoring via on-demand polling (MCP-based)
- Question bank with 150+ verified questions (50 per exam)
- Student profile system with profile, history, topic-stats, and ERI files
- 5 core agent skills: profile loader, question querier, answer evaluator, ERI calculator, performance tracker

## Technical Context

**Language/Version**: Claude Code Skills (Markdown-based prompts), JSON (data), Markdown (documents)
**Primary Dependencies**: MCP Filesystem Server (@anthropic-ai/mcp-server-filesystem)
**Storage**: Local file system (JSON files in vault)
**Testing**: Manual validation via Claude Code skill invocation
**Target Platform**: Obsidian vault on Windows/Mac/Linux
**Project Type**: Agent Skills (no traditional code structure)
**Performance Goals**: File detection within 5 seconds, full test cycle under 5 minutes
**Constraints**: No external APIs except MCP filesystem, all skills must be independently testable
**Scale/Scope**: Single student per vault, 150+ questions, 5 core skills

## Constitution Check

*GATE: Must pass before implementation. All principles verified.*

| Principle | Requirement | Plan Compliance |
|-----------|-------------|-----------------|
| I. Accuracy First | Questions from verified sources | PASS: Manual curation from past papers, explanations required |
| II. Student Encouragement | Constructive feedback | PASS: Results include explanations, no criticism |
| III. Data-Driven | Backed by performance data | PASS: ERI formula fixed, topic-stats tracked |
| IV. Transparency | ERI visible with breakdown | PASS: Dashboard shows components, Company Handbook documents formula |
| V. Respect Context | Target exam drives content | PASS: Questions filtered by exam_target |
| VI. Bounded Autonomy | Autonomous decisions defined | PASS: Skills operate within defined scope |

**Quality Standards Compliance**:
- Question Bank: ID format, verified answers, organized by exam/subject/topic ✓
- ERI Calculation: Fixed formula, no manipulation ✓
- Session Logging: All interactions persisted ✓

## Project Structure

### Documentation (this feature)

```text
specs/phase-1-foundation/
├── SPEC.md              # Feature specification
├── PLAN.md              # This file
├── BUILD.md             # Implementation tasks
├── research.md          # Research output (complete)
├── data-model.md        # Data model (complete)
├── quickstart.md        # Quick start guide (complete)
├── contracts/           # Skill contracts (complete)
│   ├── student-profile-loader.contract.md
│   ├── question-bank-querier.contract.md
│   ├── answer-evaluator.contract.md
│   ├── exam-readiness-calculator.contract.md
│   └── performance-tracker.contract.md
└── skills/              # Phase 1 skill definitions
    ├── student-profile-loader/SKILL.md
    ├── question-bank-querier/SKILL.md
    ├── answer-evaluator/SKILL.md
    ├── eri-calculator/SKILL.md
    └── performance-tracker/SKILL.md
```

### Vault Structure (implementation target)

```text
ExamTutor-Vault/
├── Dashboard.md                  # Student home: ERI, recent sessions
├── Company_Handbook.md           # System documentation, behavioral rules
├── README.md                     # Project overview
│
├── Inbox/                        # Watched folder for test requests
├── Needs_Action/                 # Invalid/failed requests
├── Done/                         # Processed requests
│
├── Students/
│   └── {student_id}/
│       ├── profile.json
│       ├── history.json
│       ├── topic-stats.json
│       ├── eri.json
│       └── sessions/
│           └── {session_id}.json
│
├── Question-Bank/
│   ├── SPSC/
│   │   └── Pakistan-Studies/
│   │       └── {topic}.json
│   ├── PPSC/
│   │   └── Pakistan-Studies/
│   │       └── {topic}.json
│   └── KPPSC/
│       └── Pakistan-Studies/
│           └── {topic}.json
│
├── Syllabus/
│   ├── cross-exam-mapping.json
│   ├── SPSC/
│   ├── PPSC/
│   │   ├── syllabus-structure.json
│   │   └── topic-weights.json
│   └── KPPSC/
│
└── Logs/
    └── watcher/
        └── {date}.log
```

### Agent Skills Structure

```text
.claude/skills/exam-tutor/
├── SKILL.md                              # Bundle overview
├── references/
│   ├── schemas.md                        # All data schemas
│   ├── mcp-integration.md               # MCP configuration
│   └── skill-orchestration.md           # Workflow patterns
│
├── student-profile-loader/
│   └── SKILL.md
├── question-bank-querier/
│   └── SKILL.md
├── answer-evaluator/
│   └── SKILL.md
├── exam-readiness-calculator/
│   └── SKILL.md
└── performance-tracker/
    └── SKILL.md
```

**Structure Decision**: Agent Skills architecture with file-based data storage. No traditional src/ structure - all logic is in markdown-based skill definitions executed by Claude Code.

## Task Summary

### Phase 1: Project Setup

| ID | Task | Dependencies | Files | Acceptance Criteria |
|----|------|--------------|-------|---------------------|
| P1-001 | Create vault folder structure | None | directories | All folders exist |
| P1-002 | Create Dashboard.md template | P1-001 | Dashboard.md | Template with ERI placeholders |
| P1-003 | Create Company_Handbook.md | P1-001 | Company_Handbook.md | Constitution rules documented |
| P1-004 | Verify MCP filesystem config | P1-001 | .claude/mcp.json | Claude Code can read/write vault |

### Phase 2: Question Bank

| ID | Task | Dependencies | Files | Acceptance Criteria |
|----|------|--------------|-------|---------------------|
| P1-005 | Create syllabus structure | P1-001 | Syllabus/PPSC/*.json | 20 topics defined |
| P1-006 | Create PPSC Pakistan Studies questions | P1-005 | Question-Bank/PPSC/*.json | 50 questions verified |
| P1-007 | Create SPSC Pakistan Studies questions | P1-005 | Question-Bank/SPSC/*.json | 50 questions verified |
| P1-008 | Create KPPSC Pakistan Studies questions | P1-005 | Question-Bank/KPPSC/*.json | 50 questions verified |

### Phase 3: Student Profile System

| ID | Task | Dependencies | Files | Acceptance Criteria |
|----|------|--------------|-------|---------------------|
| P1-009 | Create sample student profile | P1-001 | Students/STU001/profile.json | Valid profile.json |
| P1-010 | Initialize history.json | P1-009 | Students/STU001/history.json | Empty sessions array |
| P1-011 | Initialize topic-stats.json | P1-009 | Students/STU001/topic-stats.json | Zero values |
| P1-012 | Initialize eri.json | P1-009 | Students/STU001/eri.json | Baseline score |

### Phase 4: Core Skills

| ID | Task | Dependencies | Files | Acceptance Criteria |
|----|------|--------------|-------|---------------------|
| P1-013 | Implement student-profile-loader | P1-009 | skill SKILL.md | Returns valid profile |
| P1-014 | Implement question-bank-querier | P1-006 | skill SKILL.md | Returns filtered questions |
| P1-015 | Implement answer-evaluator | P1-014 | skill SKILL.md | Correct scoring |
| P1-016 | Implement eri-calculator | P1-012 | skill SKILL.md | Formula matches spec |
| P1-017 | Implement performance-tracker | P1-010, P1-011 | skill SKILL.md | Updates all files |

### Phase 5: Integration

| ID | Task | Dependencies | Files | Acceptance Criteria |
|----|------|--------------|-------|---------------------|
| P1-018 | End-to-end test: practice session | P1-013 to P1-017 | session files | Full workflow passes |
| P1-019 | Verify ERI calculation | P1-018 | eri.json | Score matches manual calc |
| P1-020 | Verify Dashboard display | P1-019 | Dashboard.md | Shows real data |
| P1-021 | Documentation finalization | P1-020 | README.md | Setup instructions complete |

## Definition of Done (Phase 1)

- [ ] All vault folders created (/Inbox, /Needs_Action, /Done, /Students, /Question-Bank, /Syllabus, /Logs)
- [ ] 150+ questions in Question-Bank (50 per exam: SPSC, PPSC, KPPSC)
- [ ] All 5 skills passing input/output validation
- [ ] Inbox processing works via on-demand polling
- [ ] Sample student (STU001) with calculated ERI
- [ ] Dashboard.md displays real ERI data
- [ ] Company_Handbook.md contains Constitution behavioral rules
- [ ] All session events logged to /Logs

## Research Decisions (from research.md)

| Topic | Decision | Rationale |
|-------|----------|-----------|
| Question Sources | Manual curation | Quality control, verified answers |
| File Watcher | On-demand MCP polling | Simple, no background process |
| First-session ERI | Use defaults (Recency=100, Consistency=100) | Immediate value delivery |
| Syllabus Topics | 20 topics for PPSC | Matches official syllabus |
| Question ID Format | EXAM-SUBJ-NNNNN | Unique, sortable, human-readable |
| Session ID Format | STUID-YYYYMMDD-HHmmss | Unique per student, chronological |

## Data Model Summary (from data-model.md)

| Entity | Location | Purpose |
|--------|----------|---------|
| Student Profile | Students/{id}/profile.json | Identity, preferences |
| Session History | Students/{id}/history.json | All sessions summary |
| Topic Stats | Students/{id}/topic-stats.json | Per-topic performance |
| ERI Score | Students/{id}/eri.json | Current ERI with breakdown |
| Session Detail | Students/{id}/sessions/{sid}.json | Single session record |
| Question Bank | Question-Bank/{exam}/{subject}/{topic}.json | MCQ content |
| Syllabus | Syllabus/{exam}/syllabus-structure.json | Topic organization |

## Skill Contracts Summary (from contracts/)

| Skill | Input | Output | MCP Tools |
|-------|-------|--------|-----------|
| student-profile-loader | student_id | profile object | read_file |
| question-bank-querier | exam, subject, count, difficulty | questions array | read_file, list_directory |
| answer-evaluator | questions, student_answers | score, feedback | none (pure compute) |
| eri-calculator | student_id | eri object with breakdown | read_file |
| performance-tracker | student_id, session_result | confirmation | read_file, write_file |

## Complexity Tracking

No violations. This implementation follows all Constitution principles and uses the simplest approach:
- File-based storage (no database)
- Markdown skills (no compiled code)
- On-demand polling (no background daemon)
- Single student per vault (no multi-tenancy complexity)

## Next Steps

Run `/sp.tasks` to generate the detailed task list for implementation.
