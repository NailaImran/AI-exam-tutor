# Feature Specification: Exam Tutor Phase 2 - Question Bank Automation

**Feature Branch**: `002-question-bank-automation`
**Created**: 2026-01-19
**Updated**: 2026-01-20
**Status**: Draft
**Input**: User description: "Automate past paper collection and expand question bank to 1500+ with 4 core skills: past-paper-scraper, question-extractor, question-validator, question-bank-manager"
**Depends On**: Phase 1 Foundation (must be 100% complete)
**Timeline**: 6-8 hours
**Goal**: Automate past paper collection and expand question bank to 1500+

## Overview

Phase 2 automates the collection and processing of past exam papers to rapidly expand the question bank from 150 questions (Phase 1) to 1500+ verified questions. This phase introduces a pipeline of 4 skills that scrape official sources, extract questions from PDFs/HTML, validate quality, and organize the expanded question bank.

## Phase 2 Folder Structure

```
/specs/phase-2-question-bank/
├── SPEC.md (this file)
├── PLAN.md
├── TASKS.md
├── data-model.md
├── research.md
├── sources.md (documented URLs)
├── contracts/
│   ├── past-paper-scraper.contract.md
│   ├── question-extractor.contract.md
│   ├── question-validator.contract.md
│   └── question-bank-manager.contract.md
├── checklists/
│   └── requirements.md
└── skills/
    ├── past-paper-scraper/SKILL.md
    ├── question-extractor/SKILL.md
    ├── question-validator/SKILL.md
    └── question-bank-manager/SKILL.md
```

## Scope - Phase 2 Only

### Must Build

#### 1. Source Documentation
- **File**: `/specs/phase-2-question-bank/sources.md`
- **Official sources**:
  - SPSC: spsc.gov.pk
  - PPSC: ppsc.gop.pk
  - KPPSC: kppsc.gov.pk
- **Secondary sources**: 2-3 reputable past paper websites
- **Per source**: URL, format (PDF/HTML), rate limit, reliability rating

#### 2. Raw Papers Storage
- **New folder**: `/Raw-Papers/`
- **Structure**: `/Raw-Papers/{Exam}/{Year}/{Subject}/{filename}`
- **Purpose**: Store original downloaded files
- **Note**: Add to .gitignore (large files)

#### 3. Review Queue
- **New folder**: `/Needs-Review/`
- **Purpose**: Holds flagged questions needing manual check
- **Format**: `{exam}_{subject}_{timestamp}.json`
- **Structure**: `/Needs-Review/{Exam}/{date}/{question-id}.json`

#### 4. Phase 2 Skills

##### past-paper-scraper

| Field | Value |
|-------|-------|
| **Input** | exam_type, year_range, subjects, source_priority |
| **Output** | downloaded files in /Raw-Papers/ |
| **MCP Tools** | web_fetch, write_file, create_directory, read_file |
| **Logic** | Fetch PDFs/HTML from official sources, respect rate limits (2s delay, 100 req/hr max), honor robots.txt, log downloads to /Logs/scraper/ |

##### question-extractor

| Field | Value |
|-------|-------|
| **Input** | raw_paper_path, exam_type, year, subject |
| **Output** | questions array (JSON) |
| **MCP Tools** | read_file, write_file |
| **Logic** | Parse PDF/HTML, detect MCQ format, extract question+options+answer, assign confidence score (0.0-1.0), flag unclear questions (confidence < 0.80) |

##### question-validator

| Field | Value |
|-------|-------|
| **Input** | extracted_question, exam_type, subject, year |
| **Output** | validated question OR rejection reason |
| **MCP Tools** | read_file, write_file, list_directory |
| **Logic** | Verify all 4 options present, valid answer A-D, check duplicates via text similarity (>90%), auto-tag difficulty/topic using syllabus matching |

##### question-bank-manager

| Field | Value |
|-------|-------|
| **Input** | action (ADD/UPDATE/DEACTIVATE/STATS), validated_question, question_id |
| **Output** | confirmation, updated stats |
| **MCP Tools** | read_file, write_file, list_directory, create_directory |
| **Logic** | Generate unique IDs ({EXAM}-{SUBJECT_CODE}-{NNNNN}), add to /Question-Bank/, organize by exam/subject/topic, deduplicate, maintain master-index.json and statistics.json, create cross-exam links |

#### 5. Batch Pipeline
- **Workflow**: scrape → extract → validate → add
- **Error handling**: Continue on failure (log and move to next file)
- **Logging**: Progress tracking to /Logs/pipeline/
- **Documentation**: Pipeline orchestration in skill-orchestration.md

#### 6. Question Bank Expansion
- **Target**: 500+ questions per exam (1500+ total)
- **Required fields**: question, options (A-D), correct_answer, explanation, source, year, difficulty, topics
- **Schema**: Use question.schema.json from Phase 1 (extended with metadata)
- **Subjects**: Pakistan Studies, General Knowledge, Current Affairs, English, Math (where applicable)

### Integration with Phase 1
- **Uses**: question.schema.json, /Question-Bank/ structure, syllabus files for topic matching
- **Feeds**: question-bank-querier skill (more questions to query)
- **No changes**: Phase 1 skills remain unchanged

### MCP Configuration Update

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "E:/AI-exam-tutor"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### Out of Scope (Later Phases)
- **Phase 3**: Adaptive test generation, study plans, ERI-based recommendations, WhatsApp integration, LinkedIn posts
- **Phase 4**: B2B features, Odoo integration, payment/subscription features, multi-student academy features

## Technical Requirements

**Note**: These are high-level technology considerations, not implementation mandates. The planning phase will determine specific approaches.

- **PDF Parsing**: Text extraction from PDF files (official papers are typically text-based PDFs)
- **HTML Parsing**: Structured data extraction from web pages
- **Duplicate Detection**: Text similarity comparison for identifying duplicate questions
- **Rate Limiting**: Respectful scraping (1 request per 2 seconds minimum)
- **Error Handling**: Robust logging and graceful failure handling (log and continue)
- **OCR Confidence**: Threshold-based flagging for low-quality extractions (< 80%)

## Deliverables

1. **sources.md** - Documented URLs for all past paper sources with reliability ratings
2. **4 Skill SKILL.md files** - Complete skill definitions for all Phase 2 skills
3. **Batch pipeline workflow** - Orchestration specification in skill-orchestration.md
4. **Updated mcp.json** - Configuration with filesystem, github, and context7 servers
5. **Folder structure** - Created /Raw-Papers/, /Needs-Review/, /Question-Bank-Index/
6. **Master index and statistics** - Automated question bank organization and tracking

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Bulk Import Past Papers (Priority: P1)

An administrator wants to quickly populate the question bank with verified past papers from official PSC sources. They provide a year range and exam type, and the system automatically downloads, processes, and adds validated questions to the question bank.

**Why this priority**: This is the core value proposition of Phase 2 - without bulk import capability, expanding the question bank remains a manual process. Every other feature depends on having a populated question bank.

**Independent Test**: Can be fully tested by running the scraper with exam_type="PPSC", years="2020-2023", and verifying that questions appear in the question bank with proper metadata.

**Acceptance Scenarios**:

1. **Given** valid PSC website access, **When** the administrator requests papers for PPSC 2020-2023 Pakistan Studies, **Then** raw papers are downloaded to /Raw-Papers/PPSC/2020/ through /Raw-Papers/PPSC/2023/.

2. **Given** downloaded raw papers (PDF or HTML), **When** the question extractor processes them, **Then** structured JSON files with questions, options, and correct answers are generated.

3. **Given** extracted questions, **When** the validator processes them, **Then** complete questions are added to the question bank and incomplete questions are flagged for manual review.

4. **Given** validated questions, **When** the question bank manager imports them, **Then** duplicates are detected and rejected, and new questions receive unique IDs following the {EXAM}-{SUBJECT_CODE}-{NNNNN} format.

---

### User Story 2 - Validate and Fix Extracted Questions (Priority: P2)

An administrator reviews questions that were flagged during extraction as needing manual review. They can see what's missing, provide corrections, and re-submit for validation.

**Why this priority**: Automated extraction won't be 100% accurate. A review workflow ensures quality while maximizing automation benefits. This enables the "Accuracy First" constitution principle.

**Independent Test**: Can be tested by manually creating a question with missing options, running it through the validator, and verifying it's flagged for review with specific issues identified.

**Acceptance Scenarios**:

1. **Given** an extracted question missing option D, **When** the validator processes it, **Then** it's flagged with reason "missing_option_D" and saved to /Needs-Review/{exam}/{date}/.

2. **Given** a flagged question, **When** the administrator provides the missing option, **Then** re-validation succeeds and the question is added to the question bank.

3. **Given** a question with ambiguous correct answer, **When** flagged for review, **Then** the original paper source and context are referenced for administrator decision.

---

### User Story 3 - Deduplicate Across Exam Types (Priority: P3)

The system identifies questions that appear across multiple exams (SPSC, PPSC, KPPSC) and links them while maintaining separate question bank entries, enabling cross-exam practice recommendations.

**Why this priority**: Many PSC exams share common questions. Deduplication prevents redundant storage and enables cross-exam coverage analysis. This supports the Constitution's data-driven recommendations principle.

**Independent Test**: Can be tested by importing the same question for two different exams and verifying they are linked but maintain separate entries with cross-references.

**Acceptance Scenarios**:

1. **Given** a question already exists for PPSC, **When** an identical question is extracted from SPSC papers, **Then** the system creates a linked entry rather than a duplicate, with cross-exam reference.

2. **Given** linked questions across exams, **When** querying the question bank, **Then** the link is visible in the question metadata showing which exams share this question.

3. **Given** a student practicing for PPSC, **When** they answer a cross-exam question, **Then** coverage is counted for PPSC only (not for exams they're not targeting).

---

### User Story 4 - Track Question Bank Statistics (Priority: P4)

Administrators and the system can view question bank health metrics: total questions by exam/subject/topic, coverage gaps, source distribution, and validation status.

**Why this priority**: Visibility into question bank composition enables strategic expansion and identifies gaps before students encounter them. This supports constitution principles of transparency and data-driven decisions.

**Independent Test**: Can be tested by running the statistics report and verifying counts match manual verification of question files.

**Acceptance Scenarios**:

1. **Given** a populated question bank, **When** statistics are requested, **Then** a report shows total questions per exam, subject, and topic.

2. **Given** question bank statistics, **When** coverage gaps are identified, **Then** topics with fewer than 10 questions are flagged as "low coverage".

3. **Given** source tracking enabled, **When** statistics are requested, **Then** the report shows questions per source (official vs secondary) and per year.

---

### Edge Cases

- What happens when the official PSC website is unavailable or blocks scraping?
  - System logs the failure, retries with exponential backoff, and falls back to cached data if available. Administrator is notified of persistent failures.

- How does the system handle PDFs with poor OCR quality or scanned images?
  - Questions with low OCR confidence (<80%) are flagged for manual review with the original PDF attached for reference.

- What happens if a past paper has no answer key provided?
  - Questions are extracted but marked as "unverified_answer" and excluded from student practice until an administrator provides verification.

- How does the system handle questions in Urdu or mixed language?
  - Phase 2 focuses on English questions. Urdu questions are flagged as "language_unsupported" for future phase handling.

- What happens if the same question appears multiple times in the same paper (e.g., repeated by mistake)?
  - Within-paper duplicates are detected and only one instance is extracted.

- How does the system handle questions where all options appear correct or none appear correct?
  - These are flagged as "ambiguous_options" for manual review with suggested resolution.

---

## Requirements *(mandatory)*

> **Note**: Requirements use phase-prefixed IDs (P2-FR-XXX) to prevent collisions across phases.

### Functional Requirements

#### Past Paper Sources

- **P2-FR-001**: System MUST document official sources for each exam type: SPSC (spsc.gov.pk), PPSC (ppsc.gop.pk), KPPSC (kppsc.gov.pk)
- **P2-FR-002**: System MUST assign reliability ratings to sources: "official" (PSC websites), "verified" (reputable educational sites), "unverified" (other sources)
- **P2-FR-003**: System MUST track source URL, access date, and reliability rating for every question

#### past-paper-scraper Skill

- **P2-FR-004**: System MUST accept inputs: exam_type (SPSC/PPSC/KPPSC), year_range (start-end), subjects list
- **P2-FR-005**: System MUST handle PDF downloads and HTML page scraping
- **P2-FR-006**: System MUST store raw papers in /Raw-Papers/{Exam}/{Year}/{Subject}/ with original filename preserved
- **P2-FR-007**: System MUST respect rate limiting (2s delay between requests) and robots.txt directives when scraping
- **P2-FR-008**: System MUST log all scraping activities including successes, failures, and retries

#### question-extractor Skill

- **P2-FR-009**: System MUST parse PDF files to extract question text, options A-D, and correct answer markers
- **P2-FR-010**: System MUST parse HTML pages to extract structured question data
- **P2-FR-011**: System MUST output structured JSON matching the question schema: id, text, options, correct_answer, explanation, source, year, difficulty, topic
- **P2-FR-012**: System MUST flag questions needing manual review with specific reasons: missing_option, no_correct_answer, low_ocr_confidence (<80%), ambiguous_format
- **P2-FR-013**: System MUST preserve reference to original source file for each extracted question

#### question-validator Skill

- **P2-FR-014**: System MUST verify all four options (A, B, C, D) are present and non-empty
- **P2-FR-015**: System MUST verify correct_answer is one of A, B, C, or D
- **P2-FR-016**: System MUST detect duplicates by comparing question text similarity (>90% match using Levenshtein distance or similar)
- **P2-FR-017**: System MUST auto-assign difficulty based on historical accuracy data when available, defaulting to "medium"
- **P2-FR-018**: System MUST auto-suggest topics based on keyword matching against syllabus structure
- **P2-FR-019**: System MUST reject questions missing required fields and provide specific rejection reasons

#### question-bank-manager Skill

- **P2-FR-020**: System MUST generate unique question IDs following format: {EXAM}-{SUBJECT_CODE}-{NNNNN}
- **P2-FR-021**: System MUST organize questions into /question-bank/{Exam}/{Subject}/{topic}.json structure
- **P2-FR-022**: System MUST maintain a master index of all questions with metadata for quick lookup
- **P2-FR-023**: System MUST support add, update, and deactivate operations (no hard deletes)
- **P2-FR-024**: System MUST link cross-exam duplicate questions with bidirectional references
- **P2-FR-025**: System MUST track question count per exam/subject/topic and update statistics on changes

#### Expanded Question Bank

- **P2-FR-026**: System MUST support minimum 500 questions per exam type (1500 total)
- **P2-FR-027**: Each question MUST include: id, text, options (A-D), correct_answer, explanation, source, year, difficulty, topic, created_at, validation_status
- **P2-FR-028**: System MUST maintain backward compatibility with Phase 1 question format
- **P2-FR-029**: System MUST support multiple subjects per exam: Pakistan Studies, General Knowledge, Current Affairs, English, Math (where applicable)

### Key Entities

- **Raw Paper**: An unprocessed past exam paper (PDF or HTML) downloaded from a source. Contains metadata: exam_type, year, subject, source_url, download_date, file_path.

- **Extracted Question**: A question parsed from a raw paper but not yet validated. Contains all question fields plus extraction_confidence and review_flags.

- **Validated Question**: A question that has passed all validation checks and is ready for the question bank. Contains complete metadata including unique ID and validation timestamp.

- **Question Link**: A relationship between questions that are duplicates across different exam types. Contains source_question_id, linked_question_id, link_type ("cross_exam_duplicate").

- **Source Registry**: A catalog of all known past paper sources with reliability ratings, last access dates, and extraction statistics.

---

## Success Criteria *(mandatory)*

### Timeline

**Phase 2 Duration**: 6-8 hours (as specified in header)
**Milestone Targets**:
- Hour 0-2: Sources documented, scraper skill operational
- Hour 2-4: Extractor and validator skills operational
- Hour 4-6: Question bank manager operational, 500+ questions imported
- Hour 6-8: 1500+ questions imported, statistics verified

### Measurable Outcomes

- **P2-SC-001**: Question bank expands from 150 to 1500+ verified questions within 8 hours
- **P2-SC-002**: Each exam type (SPSC, PPSC, KPPSC) has minimum 500 questions covering all major subjects
- **P2-SC-003**: 95% of extracted questions pass validation without manual intervention
- **P2-SC-004**: Question extraction accuracy achieves 90%+ when compared to manual extraction of sample papers
- **P2-SC-005**: Duplicate detection identifies 99%+ of cross-exam duplicates based on test set
- **P2-SC-006**: All questions include source attribution (exam type, year, official/secondary)
- **P2-SC-007**: Question bank statistics are accurate within 1% margin when verified manually
- **P2-SC-008**: Raw paper storage organized such that any paper can be located within 30 seconds
- **P2-SC-009**: The full pipeline (scrape → extract → validate → import) processes 50 questions per minute average
- **P2-SC-010**: Zero questions with unverified answers enter student-facing practice sessions

## Acceptance Criteria

- [ ] sources.md documents 3+ sources per exam (SPSC, PPSC, KPPSC)
- [ ] past-paper-scraper downloads from 2+ sources successfully
- [ ] question-extractor parses 80%+ questions correctly from sample papers
- [ ] question-validator catches duplicate questions across exams
- [ ] question-bank-manager organizes questions correctly by exam/subject/topic
- [ ] 1500+ questions in question bank (500+ per exam: SPSC, PPSC, KPPSC)
- [ ] All questions have complete metadata (source, year, difficulty, topic)
- [ ] Flagged questions stored in /Needs-Review/ with specific reasons
- [ ] Pipeline runs end-to-end with comprehensive logging
- [ ] Master index and statistics files accurate and up-to-date
- [ ] Cross-exam links created for duplicate questions
- [ ] No questions with unverified answers in active status

---

## Assumptions

1. **Official Websites Accessible**: PSC official websites (spsc.gov.pk, ppsc.gop.pk, kppsc.gov.pk) remain accessible and don't block automated access during reasonable scraping.

2. **PDF Quality**: Most official past papers are text-based PDFs or have reasonable OCR quality. Purely image-based PDFs may require manual processing.

3. **Answer Keys Available**: Official past papers include answer keys or correct answers can be verified from official sources.

4. **English Language Focus**: Phase 2 focuses on English-language questions. Urdu language support is deferred.

5. **Phase 1 Complete**: The vault structure, question bank format, and core skills from Phase 1 are operational and stable.

6. **MCP Filesystem Available**: All file operations use MCP filesystem server as established in Phase 1.

7. **Manual Review Acceptable**: Some percentage (estimated 5-10%) of questions require human review, and administrator time is available for this.

8. **Syllabus Structure Stable**: Topic taxonomy from Phase 1 syllabus files is used for auto-tagging and remains unchanged during Phase 2.

---

## Appendix: Folder Structure Addition

```
ExamTutor-Vault/
├── Raw-Papers/                    # NEW: Downloaded raw papers
│   ├── SPSC/
│   │   └── {Year}/
│   │       └── {Subject}/
│   │           └── {original-filename}.pdf
│   ├── PPSC/
│   │   └── {Year}/
│   │       └── {Subject}/
│   │           └── {original-filename}.pdf
│   └── KPPSC/
│       └── {Year}/
│           └── {Subject}/
│               └── {original-filename}.pdf
│
├── Needs-Review/                  # NEW: Questions flagged for manual review
│   ├── SPSC/
│   │   └── {date}/
│   │       └── {question-id}.json
│   ├── PPSC/
│   └── KPPSC/
│
├── Question-Bank/                 # EXPANDED: More questions and subjects
│   ├── SPSC/
│   │   ├── Pakistan-Studies/
│   │   ├── General-Knowledge/
│   │   ├── Current-Affairs/
│   │   └── English/
│   ├── PPSC/
│   │   ├── Pakistan-Studies/
│   │   ├── General-Knowledge/
│   │   ├── Current-Affairs/
│   │   └── English/
│   └── KPPSC/
│       ├── Pakistan-Studies/
│       ├── General-Knowledge/
│       ├── Current-Affairs/
│       └── English/
│
├── Question-Bank-Index/           # NEW: Master index and statistics
│   ├── master-index.json          # All question IDs with metadata
│   ├── cross-exam-links.json      # Duplicate links across exams
│   ├── statistics.json            # Counts by exam/subject/topic
│   └── sources-registry.json      # All sources with reliability ratings
│
└── Logs/
    └── scraper/                   # NEW: Scraper activity logs
        └── {date}.log
```

---

## Appendix: Phase 2 Skills Summary

| Skill                  | Input                                    | Output                         | MCP Tools                   |
| ---------------------- | ---------------------------------------- | ------------------------------ | --------------------------- |
| past-paper-scraper     | exam_type, year_range, subjects          | raw papers in /Raw-Papers/     | read_file, write_file, HTTP |
| question-extractor     | raw_paper_path                           | extracted questions JSON       | read_file, write_file       |
| question-validator     | extracted_question                       | validated question or rejection| read_file, write_file       |
| question-bank-manager  | validated_questions, action              | updated question bank          | read_file, write_file, list_directory |

---

## Appendix: Question Schema (Extended)

```json
{
  "id": "PPSC-PK-00151",
  "text": "Which amendment introduced the 18th Amendment in Pakistan?",
  "options": {
    "A": "17th Amendment",
    "B": "18th Amendment",
    "C": "19th Amendment",
    "D": "20th Amendment"
  },
  "correct_answer": "B",
  "explanation": "The 18th Amendment was passed in 2010 and significantly altered the constitution.",
  "topic": "constitutional-amendments",
  "difficulty": "easy",
  "source": {
    "type": "official",
    "exam": "PPSC",
    "year": 2021,
    "paper": "Pakistan Studies",
    "url": "https://ppsc.gop.pk/papers/2021/pk-studies.pdf",
    "accessed": "2026-01-15"
  },
  "metadata": {
    "created_at": "2026-01-19T10:30:00Z",
    "validation_status": "verified",
    "extraction_confidence": 0.95,
    "cross_exam_links": ["SPSC-PK-00089", "KPPSC-PK-00112"]
  }
}
```
