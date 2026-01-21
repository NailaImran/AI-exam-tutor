# Implementation Plan: Phase 2 - Question Bank Automation

**Branch**: `002-question-bank-automation` | **Date**: 2026-01-19 | **Updated**: 2026-01-20 | **Spec**: [SPEC.md](./SPEC.md)
**Input**: Feature specification from `/specs/phase-2-question-bank/SPEC.md`
**Depends On**: Phase 1 Foundation (must be 100% complete)
**Timeline**: 6-8 hours
**Approach**: Spec-driven development with Claude Code Skills

## Summary

Automate the collection and processing of past exam papers to expand the question bank from 150 questions (Phase 1) to 1500+ verified questions. The implementation introduces a pipeline of 4 skills: past-paper-scraper, question-extractor, question-validator, and question-bank-manager. All skills use MCP filesystem operations for consistency with Phase 1 architecture.

## Technical Context

**Language/Version**: Claude Code Skills (Markdown-based prompts), JSON (data), Markdown (documents)
**Primary Dependencies**: MCP Filesystem Server (@anthropic-ai/mcp-server-filesystem), HTTP capabilities for scraping
**Storage**: Local file system (JSON files in vault: /Raw-Papers/, /Question-Bank/, /Question-Bank-Index/)
**Testing**: Manual validation via Claude Code skill invocation
**Target Platform**: Obsidian vault on Windows/Mac/Linux
**Project Type**: Agent Skills (no traditional code structure)
**Performance Goals**: Process 50 questions per minute, complete full pipeline in <30 minutes for 100 papers
**Constraints**: Rate limiting (2s between requests), no external APIs except MCP filesystem, respect robots.txt
**Scale/Scope**: 1500+ questions, 4 new skills, 100+ past papers processed

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Plan Compliance |
|-----------|-------------|-----------------|
| I. Accuracy First | Questions from verified sources | PASS: Official PSC websites as primary, verification workflow for secondary |
| II. Student Encouragement | Not directly applicable | N/A: Phase 2 is admin/automation focused |
| III. Data-Driven | Backed by source data | PASS: All questions include source metadata (exam, year, URL) |
| IV. Transparency | Source attribution | PASS: Every question tracks origin, reliability rating, access date |
| V. Respect Context | Exam-specific content | PASS: Questions organized by exam type, cross-exam links explicit |
| VI. Bounded Autonomy | Autonomous decisions defined | PASS: Scraping/extraction autonomous, validation flags for human review |

**Quality Standards Compliance**:
- Question Bank: ID format `{EXAM}-{SUBJ}-{NNNNN}`, verified answers, organized by exam/subject/topic ✓
- Source Attribution: Every question includes source URL, type (official/verified/unverified), year ✓
- Validation Workflow: Multi-level validation, flagging for manual review when uncertain ✓

## Project Structure

### Documentation (this feature)

```text
specs/phase-2-question-bank/
├── SPEC.md              # Feature specification
├── PLAN.md              # This file
├── research.md          # Research decisions (complete)
├── data-model.md        # Entity schemas (complete)
├── contracts/           # Skill contracts (complete)
│   ├── past-paper-scraper.contract.md
│   ├── question-extractor.contract.md
│   ├── question-validator.contract.md
│   └── question-bank-manager.contract.md
├── checklists/
│   └── requirements.md  # Quality checklist
└── skills/              # Phase 2 skill definitions
    ├── past-paper-scraper/SKILL.md
    ├── question-extractor/SKILL.md
    ├── question-validator/SKILL.md
    └── question-bank-manager/SKILL.md
```

### Vault Structure (additions for Phase 2)

```text
ExamTutor-Vault/
├── Raw-Papers/                    # NEW: Downloaded raw papers
│   ├── SPSC/{Year}/{Subject}/
│   ├── PPSC/{Year}/{Subject}/
│   └── KPPSC/{Year}/{Subject}/
│
├── Needs-Review/                  # NEW: Flagged questions
│   ├── SPSC/{date}/
│   ├── PPSC/{date}/
│   └── KPPSC/{date}/
│
├── Question-Bank/                 # EXPANDED: More questions and subjects
│   ├── SPSC/{Subject}/{topic}.json
│   ├── PPSC/{Subject}/{topic}.json
│   └── KPPSC/{Subject}/{topic}.json
│
├── Question-Bank-Index/           # NEW: Master index and statistics
│   ├── master-index.json
│   ├── cross-exam-links.json
│   ├── statistics.json
│   └── sources-registry.json
│
└── Logs/
    └── scraper/{date}.log         # NEW: Scraper activity logs
```

### Agent Skills Structure

```text
.claude/skills/exam-tutor/
├── SKILL.md                              # Bundle overview (update)
├── references/
│   ├── schemas.md                        # Update with Phase 2 schemas
│   ├── mcp-integration.md               # Update with new paths
│   └── skill-orchestration.md           # Add Phase 2 workflows
│
├── [Phase 1 skills...]
│
├── past-paper-scraper/                   # NEW
│   └── SKILL.md
├── question-extractor/                   # NEW
│   └── SKILL.md
├── question-validator/                   # NEW
│   └── SKILL.md
└── question-bank-manager/                # NEW
    └── SKILL.md
```

**Structure Decision**: Extends Phase 1 Agent Skills architecture. All new skills follow same patterns: file-based data storage, MCP filesystem operations, no external dependencies beyond HTTP for scraping.

## Task Breakdown - Phase 2 Only

### 1. Source Research & Documentation (1 hr)

**Objective**: Document all official and secondary past paper sources with metadata

**Tasks**:
- Research official SPSC/PPSC/KPPSC URLs and verify accessibility
- Find 2-3 reliable secondary past paper websites (IlmKiDunya, etc.)
- Document per source:
  - URL and access path to past papers
  - Format (PDF/HTML)
  - Rate limit policy (robots.txt check)
  - Reliability rating (1-5 scale)
  - Sample paper URLs for testing
- Create source registry JSON schema

**Output**: `/specs/phase-2-question-bank/sources.md`

**Done Criteria**: 3+ sources per exam (SPSC, PPSC, KPPSC) documented with complete metadata

---

### 2. Folder Structure Setup (30 min)

**Objective**: Create Phase 2 vault structure

**Tasks**:
- Create `/Raw-Papers/` with subdirectories: SPSC/, PPSC/, KPPSC/
- Create `/Needs-Review/` with subdirectories: SPSC/, PPSC/, KPPSC/
- Create `/Question-Bank-Index/` for master index and statistics
- Create `/Logs/scraper/` for scraping activity logs
- Update .gitignore to exclude /Raw-Papers/ (large binary files)

**Output**: Directory structure in vault

**Done Criteria**: All directories exist, .gitignore updated, folders writable by MCP

---

### 3. MCP Configuration Update (30 min)

**Objective**: Enable web scraping capabilities

**Tasks**:
- Review current `.claude/mcp.json` configuration
- Verify filesystem server configuration
- Ensure github and context7 servers are configured
- Test MCP filesystem operations (read, write, list)
- Test HTTP fetch capability for web scraping

**Output**: Updated `.claude/mcp.json`

**Done Criteria**: All 3 MCP servers operational (filesystem, github, context7), web fetch works

---

### 4. Skill: past-paper-scraper (1.5 hrs)

**Objective**: Download past papers from official PSC sources

**Tasks**:
- Create `/specs/phase-2-question-bank/skills/past-paper-scraper/SKILL.md`
- Define skill contract:
  - Input: exam_type (SPSC/PPSC/KPPSC), year_range (2020-2023), subjects
  - Output: files saved to /Raw-Papers/{Exam}/{Year}/{Subject}/
  - MCP Tools: web_fetch, write_file, create_directory, read_file
- Implement skill logic:
  - Read sources-registry.json for URLs
  - Fetch PDFs/HTML from official sources
  - Respect rate limiting (2s between requests, 100 req/hr max)
  - Honor robots.txt directives
  - Log all scraping activities to /Logs/scraper/{date}.log
  - Handle errors gracefully (retry with exponential backoff)

**Output**: `past-paper-scraper/SKILL.md`

**Testing**: Download 3 papers from each exam (9 total)

**Done Criteria**: Skill downloads papers successfully, respects rate limits, logs all activities

---

### 5. Skill: question-extractor (1.5 hrs)

**Objective**: Extract MCQ questions from raw papers into structured JSON

**Tasks**:
- Create `/specs/phase-2-question-bank/skills/question-extractor/SKILL.md`
- Define skill contract:
  - Input: raw_paper_path, exam_type, year, subject
  - Output: questions array (JSON)
  - MCP Tools: read_file, write_file
- Implement skill logic:
  - Parse PDF files to extract text
  - Parse HTML pages to extract structured data
  - Detect MCQ format (question, options A-D, answer marker)
  - Extract question text, options, correct answer, page/line reference
  - Assign confidence score (0.0-1.0) based on extraction quality
  - Flag unclear questions (confidence < 0.80) for manual review
  - Preserve reference to original source file

**Output**: `question-extractor/SKILL.md`

**Testing**: Extract from 5 sample papers (mix of PDF and HTML)

**Done Criteria**: Extracts 80%+ questions correctly, flags low-confidence extractions

---

### 6. Skill: question-validator (1 hr)

**Objective**: Validate extracted questions for completeness and uniqueness

**Tasks**:
- Create `/specs/phase-2-question-bank/skills/question-validator/SKILL.md`
- Define skill contract:
  - Input: extracted_question, exam_type, subject, year
  - Output: validated question OR rejection reason
  - MCP Tools: read_file, write_file, list_directory
- Implement skill logic:
  - Verify all 4 options (A, B, C, D) are present and non-empty
  - Verify correct_answer is one of A, B, C, or D
  - Check duplicates via text similarity (>90% threshold)
  - Auto-assign difficulty based on keywords or default to "medium"
  - Auto-suggest topics based on keyword matching against syllabus structure
  - Reject questions missing required fields with specific reasons
  - Flag questions for manual review with specific codes (MISSING_OPTION_D, NO_CORRECT_ANSWER, LOW_OCR_CONFIDENCE)

**Output**: `question-validator/SKILL.md`

**Testing**: Validate 50 questions, intentionally reject 5 bad ones

**Done Criteria**: Catches all incomplete questions, detects duplicates, provides specific rejection reasons

---

### 7. Skill: question-bank-manager (1 hr)

**Objective**: Manage question bank operations (add, update, deactivate, stats)

**Tasks**:
- Create `/specs/phase-2-question-bank/skills/question-bank-manager/SKILL.md`
- Define skill contract:
  - Input: action (ADD/UPDATE/DEACTIVATE/STATS), validated_question, question_id
  - Output: confirmation, updated stats
  - MCP Tools: read_file, write_file, list_directory, create_directory
- Implement skill logic:
  - Generate unique IDs following format: {EXAM}-{SUBJECT_CODE}-{NNNNN}
  - Add questions to /Question-Bank/{Exam}/{Subject}/{topic}.json
  - Organize questions by exam/subject/topic
  - Deduplicate (check master index before adding)
  - Maintain master-index.json with all question metadata
  - Create cross-exam links in cross-exam-links.json for duplicates
  - Update statistics.json with counts by exam/subject/topic/difficulty/source
  - Support UPDATE and DEACTIVATE operations (no hard deletes)

**Output**: `question-bank-manager/SKILL.md`

**Testing**: Add 100 questions, verify organization and statistics

**Done Criteria**: Generates unique IDs, organizes correctly, updates all indexes and stats

---

### 8. Batch Pipeline Orchestration (1 hr)

**Objective**: Create end-to-end pipeline workflow

**Tasks**:
- Document pipeline workflow in `.claude/skills/exam-tutor/references/skill-orchestration.md`
- Define pipeline flow: scrape → extract → validate → add
- Implement error handling strategy:
  - Log all failures with context
  - Continue processing on individual file failures
  - Retry failed downloads with exponential backoff
  - Flag problematic questions for manual review
- Create progress logging to /Logs/pipeline/{date}.log
- Document orchestration patterns for invoking skills in sequence

**Output**: Updated `skill-orchestration.md` with Phase 2 workflows

**Testing**: Run pipeline on 10 papers end-to-end

**Done Criteria**: Pipeline processes papers from download to import, handles errors gracefully, logs all activities

---

### 9. Mass Scraping & Processing (1.5 hrs)

**Objective**: Populate question bank with 1500+ questions

**Tasks**:
- Run past-paper-scraper for all sources and years (2020-2023)
  - PPSC: Pakistan Studies, General Knowledge, Current Affairs, English
  - SPSC: Pakistan Studies, General Knowledge, Current Affairs, English
  - KPPSC: Pakistan Studies, General Knowledge, Current Affairs, English
- Monitor scraping progress and handle failures
- Run question-extractor on all downloaded papers
- Run question-validator on all extracted questions
- Run question-bank-manager to import validated questions
- Review /Needs-Review/ for flagged questions requiring manual intervention
- Document flagging patterns and extraction challenges

**Output**: 1500+ questions in /Question-Bank/

**Target**: 500+ questions per exam (SPSC, PPSC, KPPSC)

**Done Criteria**: 1500+ verified questions, all with complete metadata (source, year, difficulty, topic)

---

### 10. Validation & Quality Assurance (30 min)

**Objective**: Verify all Phase 2 success criteria are met

**Tasks**:
- Verify total question count: 1500+ (check statistics.json)
- Verify per-exam counts: 500+ for SPSC, PPSC, KPPSC
- Verify all questions have complete metadata:
  - id, text, options (A-D), correct_answer, explanation
  - source (type, exam, year, url), difficulty, topic
  - created_at, validation_status
- Test question-bank-querier (Phase 1 skill) with new data
- Manually verify a random sample of 50 questions for accuracy
- Check master-index.json for completeness
- Verify cross-exam-links.json has bidirectional references
- Review /Needs-Review/ and document manual fixes needed
- Verify statistics.json accuracy (within 1% margin)
- Document any extraction patterns that need improvement

**Output**: Validation report documenting Phase 2 completion

**Done Criteria**: All acceptance criteria met, Phase 2 ready for Phase 3

---

## Deliverable Format

| Task ID | Task | Time | Dependencies | Output | Done Criteria |
|---------|------|------|--------------|--------|---------------|
| P2-001 | Source Research | 1h | Phase 1 done | sources.md | 3+ sources per exam |
| P2-002 | Folder Structure | 30m | P2-001 | directories | /Raw-Papers/ exists |
| P2-003 | MCP Update | 30m | P2-002 | mcp.json | All 3 servers work |
| P2-004 | past-paper-scraper SKILL.md | 30m | P2-003 | SKILL.md | Spec complete |
| P2-005 | past-paper-scraper implement | 1h | P2-004 | skill | Downloads 9 papers |
| P2-006 | question-extractor SKILL.md | 30m | P2-003 | SKILL.md | Spec complete |
| P2-007 | question-extractor implement | 1h | P2-006 | skill | Extracts from 5 papers |
| P2-008 | question-validator SKILL.md | 30m | P2-003 | SKILL.md | Spec complete |
| P2-009 | question-validator implement | 30m | P2-008 | skill | Validates 50, rejects 5 |
| P2-010 | question-bank-manager SKILL.md | 30m | P2-003 | SKILL.md | Spec complete |
| P2-011 | question-bank-manager implement | 30m | P2-010 | skill | Adds 100 questions |
| P2-012 | Batch Pipeline | 1h | P2-005,07,09,11 | orchestration | End-to-end works |
| P2-013 | Mass Processing | 1.5h | P2-012 | questions | 1500+ questions |
| P2-014 | Validation | 30m | P2-013 | report | All criteria met |

**Total Estimated Time**: 8 hours

## Definition of Done (Phase 2)

- [ ] All vault folders created (/Raw-Papers/, /Needs-Review/, /Question-Bank-Index/)
- [ ] Source registry populated with official and verified sources
- [ ] All 4 skills passing input/output validation
- [ ] End-to-end pipeline processes papers → extracts → validates → imports
- [ ] 1500+ questions in Question-Bank (500 per exam: SPSC, PPSC, KPPSC)
- [ ] Master index accurate and up-to-date
- [ ] Statistics match manual verification
- [ ] Cross-exam duplicates linked
- [ ] All flagged questions reviewed
- [ ] Documentation updated (schemas.md, skill-orchestration.md)

## Research Decisions (from research.md)

| Topic | Decision | Rationale |
|-------|----------|-----------|
| Paper Sources | Official PSC websites primary | Accuracy First principle |
| PDF Parsing | Text extraction + manual review | Handles 90%+ of papers |
| Duplicate Detection | Text similarity (90% threshold) | Simple, deterministic |
| Rate Limiting | 2s delay, 100 req/hr max | Prevents blocking |
| Question IDs | {EXAM}-{SUBJ}-{NNNNN} | Human-readable, sortable |
| Storage | Hierarchical folders | Consistent with Phase 1 |
| Validation | Multi-level (critical/warning/info) | Balances automation with accuracy |

## Data Model Summary (from data-model.md)

| Entity | Location | Purpose |
|--------|----------|---------|
| Raw Paper | /Raw-Papers/{Exam}/{Year}/{Subject}/ | Downloaded papers |
| Extracted Question | In-memory/temp | Parsed but unvalidated |
| Flagged Question | /Needs-Review/{Exam}/{date}/ | Needs manual review |
| Validated Question | /Question-Bank/{Exam}/{Subject}/{topic}.json | Ready for students |
| Source Registry | /Question-Bank-Index/sources-registry.json | Paper sources catalog |
| Master Index | /Question-Bank-Index/master-index.json | Quick lookup |
| Cross-Exam Links | /Question-Bank-Index/cross-exam-links.json | Duplicate links |
| Statistics | /Question-Bank-Index/statistics.json | Aggregated metrics |

## Skill Contracts Summary (from contracts/)

| Skill | Input | Output | MCP Tools |
|-------|-------|--------|-----------|
| past-paper-scraper | exam_type, year_range, subjects | downloaded papers | write_file, create_directory, read_file |
| question-extractor | raw_paper_path | questions array | read_file, write_file |
| question-validator | extracted_question | validated or rejection | read_file, write_file |
| question-bank-manager | action, question/id | confirmation, stats | read_file, write_file, list_directory |

## Complexity Tracking

No violations. This implementation follows all Constitution principles and uses the simplest approach:
- File-based storage (no database)
- Markdown skills (no compiled code)
- Text-based duplicate detection (no ML)
- Sequential processing (no parallel complexity)
- Manual review for uncertain cases (no false automation)

## Dependencies

### Phase 1 Prerequisites

- Vault folder structure operational
- Question-Bank with 150+ questions (baseline)
- Syllabus structure for topic matching
- MCP filesystem configuration verified

### External Dependencies

- Official PSC websites accessible (spsc.gov.pk, ppsc.gop.pk, kppsc.gov.pk)
- HTTP capabilities for web scraping
- PDF text extraction capability

## Dependencies Graph

```
Phase 1 Complete
    ↓
P2-001: Source Research (1h)
    ↓
P2-002: Folder Structure (30m)
    ↓
P2-003: MCP Configuration (30m)
    ↓
    ├─→ P2-004: past-paper-scraper SKILL.md (30m)
    │       ↓
    │   P2-005: past-paper-scraper implement (1h)
    │
    ├─→ P2-006: question-extractor SKILL.md (30m)
    │       ↓
    │   P2-007: question-extractor implement (1h)
    │
    ├─→ P2-008: question-validator SKILL.md (30m)
    │       ↓
    │   P2-009: question-validator implement (30m)
    │
    └─→ P2-010: question-bank-manager SKILL.md (30m)
            ↓
        P2-011: question-bank-manager implement (30m)

P2-005 + P2-007 + P2-009 + P2-011
    ↓
P2-012: Batch Pipeline (1h)
    ↓
P2-013: Mass Processing (1.5h)
    ↓
P2-014: Validation (30m)
    ↓
Phase 2 Complete
```

**Critical Path**: P2-001 → P2-002 → P2-003 → (Skills in parallel) → P2-012 → P2-013 → P2-014

**Parallel Opportunities**:
- All 4 SKILL.md files (P2-004, P2-006, P2-008, P2-010) can be created in parallel after P2-003
- All 4 skill implementations (P2-005, P2-007, P2-009, P2-011) can proceed in parallel once their respective SKILL.md is complete

**Bottlenecks**:
- P2-003 (MCP Configuration) blocks all skill work
- P2-012 (Batch Pipeline) requires all 4 skills to be implemented
- P2-013 (Mass Processing) is the longest single task (1.5h)

## Next Steps

Run `/sp.tasks` to generate the detailed task list (TASKS.md) for implementation.

Alternatively, begin implementation directly by starting with P2-001 (Source Research).
