# Phase 2: Question Bank Automation - Tasks

⚠️ **SCOPE**: Phase 2 Only
⚠️ **PREREQUISITE**: Phase 1 must be 100% complete before starting
⚠️ **Timeline**: 6-8 hours
⚠️ **Approach**: Incremental skill-by-skill implementation

---

## Task List

### Setup & Research (2.5 hours)

- [X] P2-001: Research and document SPSC past paper sources (URLs, formats, rate limits) - 30 min
- [X] P2-002: Research and document PPSC past paper sources (URLs, formats, rate limits) - 30 min
- [X] P2-003: Research and document KPPSC past paper sources (URLs, formats, rate limits) - 30 min
- [X] P2-004: Create sources.md with all URLs, formats, rate limits, reliability ratings - 30 min
- [X] P2-005: Create /Raw-Papers/{SPSC,PPSC,KPPSC}/ folder structure - 15 min
- [X] P2-006: Create /Needs-Review/ folder with exam subdirectories - 10 min
- [X] P2-007: Create /Logs/pipeline/ folder for pipeline logs - 5 min
- [X] P2-008: Update .gitignore to exclude /Raw-Papers/ (large binary files) - 5 min
- [X] P2-009: Update .claude/mcp.json with filesystem, github, context7 servers - 15 min
- [X] P2-010: Test MCP filesystem operations (read, write, list, create_directory) - 15 min

**Checkpoint**: All folders created, sources documented, MCP operational

---

### Skill: past-paper-scraper (2 hours)

- [X] P2-011: Create .claude/skills/exam-tutor/past-paper-scraper/SKILL.md specification - 30 min
- [X] P2-012: Implement past-paper-scraper skill with rate limiting and logging - 45 min
  - Input: exam_type, year_range, subjects
  - Output: downloaded files in /Raw-Papers/
  - Logic: Read sources-registry.json, fetch PDFs/HTML, respect rate limits (2s delay), log to /Logs/scraper/
- [ ] P2-013: Test scraper on SPSC - download 3 sample papers - 15 min
- [ ] P2-014: Test scraper on PPSC - download 3 sample papers - 15 min
- [ ] P2-015: Test scraper on KPPSC - download 3 sample papers - 15 min

**Checkpoint**: Scraper downloads papers from all 3 exam sources successfully

---

### Skill: question-extractor (2.5 hours)

- [X] P2-016: Create .claude/skills/exam-tutor/question-extractor/SKILL.md specification - 30 min
- [X] P2-017: Implement PDF text extraction and parsing logic - 30 min
  - Extract text from PDF files
  - Detect MCQ format (question, options A-D, answer marker)
- [X] P2-018: Implement HTML content extraction and parsing logic - 30 min
  - Parse HTML structure for question data
  - Handle different HTML formats
- [X] P2-019: Implement MCQ detection and structured extraction - 30 min
  - Extract question text, options, correct answer
  - Assign confidence score (0.0-1.0)
  - Flag low-confidence extractions (< 0.80)
- [ ] P2-020: Test extractor on 5 sample papers (mix of PDF and HTML) - 30 min
  - Verify 80%+ extraction accuracy
  - Verify flagging of low-confidence questions

**Checkpoint**: Extractor parses papers and extracts questions with confidence scoring

---

### Skill: question-validator (2 hours)

- [X] P2-021: Create .claude/skills/exam-tutor/question-validator/SKILL.md specification - 30 min
- [X] P2-022: Implement 4-options completeness check (verify A, B, C, D all present) - 15 min
- [X] P2-023: Implement answer validation (correct_answer must be A, B, C, or D) - 10 min
- [X] P2-024: Implement duplicate detection via text similarity (>90% threshold) - 20 min
  - Check against existing questions in master-index.json
  - Compare question text similarity
- [X] P2-025: Implement auto-tagging for difficulty and topics - 30 min
  - Difficulty: keyword-based or default to "medium"
  - Topics: match against syllabus structure
- [ ] P2-026: Test validator - validate 50 questions, intentionally reject 5 bad ones - 20 min
  - Verify rejection reasons are specific
  - Verify flagging to /Needs-Review/

**Checkpoint**: Validator catches incomplete questions, detects duplicates, provides specific rejection reasons

---

### Skill: question-bank-manager (1.5 hours)

- [X] P2-027: Create .claude/skills/exam-tutor/question-bank-manager/SKILL.md specification - 30 min
- [X] P2-028: Implement add questions logic with unique ID generation - 20 min
  - Format: {EXAM}-{SUBJECT_CODE}-{NNNNN}
  - Add to /Question-Bank/{Exam}/{Subject}/{topic}.json
- [X] P2-029: Implement deduplication logic (check master index before adding) - 20 min
  - Check master-index.json for existing IDs
  - Prevent duplicate imports
- [X] P2-030: Implement organization by exam/subject/topic - 20 min
  - Update master-index.json
  - Update statistics.json
  - Create cross-exam-links.json entries for duplicates
- [ ] P2-031: Test manager - add 100 questions, verify organization and stats - 20 min
  - Verify unique IDs generated
  - Verify correct file organization
  - Verify statistics accuracy

**Checkpoint**: Manager adds questions, generates IDs, updates all indexes and statistics

---

### Batch Pipeline (2 hours)

- [X] P2-032: Document pipeline workflow in .claude/skills/exam-tutor/references/skill-orchestration.md - 20 min
  - Define flow: scrape → extract → validate → add
  - Document orchestration patterns
- [X] P2-033: Create pipeline execution logic that chains all 4 skills - 30 min
  - Invoke skills in sequence
  - Pass data between skills
- [X] P2-034: Implement error handling - log failures, continue processing - 20 min
  - Log all failures with context
  - Continue on individual file failures
  - Retry with exponential backoff
- [X] P2-035: Implement progress logging to /Logs/pipeline/{date}.log - 15 min
  - Log each step (scrape, extract, validate, add)
  - Log success/failure counts
- [ ] P2-036: Test pipeline end-to-end on 10 papers - 30 min
  - Verify full flow works
  - Verify error handling
  - Verify logging

**Checkpoint**: Pipeline processes papers from download to import, handles errors gracefully

---

### Mass Processing (2 hours)

- [ ] P2-037: Run pipeline on all SPSC sources (years 2020-2023, all subjects) - 30 min
  - Monitor progress
  - Handle failures
- [ ] P2-038: Run pipeline on all PPSC sources (years 2020-2023, all subjects) - 30 min
  - Monitor progress
  - Handle failures
- [ ] P2-039: Run pipeline on all KPPSC sources (years 2020-2023, all subjects) - 30 min
  - Monitor progress
  - Handle failures
- [ ] P2-040: Review flagged questions in /Needs-Review/ for manual intervention - 30 min
  - Document flagging patterns
  - Identify extraction challenges

**Checkpoint**: 1500+ questions imported, flagged questions documented

---

### Validation (1.5 hours)

- [ ] P2-041: Verify SPSC has 500+ questions (check statistics.json) - 10 min
- [ ] P2-042: Verify PPSC has 500+ questions (check statistics.json) - 10 min
- [ ] P2-043: Verify KPPSC has 500+ questions (check statistics.json) - 10 min
- [ ] P2-044: Verify all questions have complete metadata - 15 min
  - Check: id, text, options (A-D), correct_answer, explanation
  - Check: source (type, exam, year, url), difficulty, topic
  - Check: created_at, validation_status
  
- [ ] P2-045: Test question-bank-querier (Phase 1 skill) with expanded data - 15 min
  - Verify Phase 1 skills work with new questions
  - Verify backward compatibility
- [ ] P2-046: Document any manual fixes applied and validation results - 15 min
  - Create validation report
  - Document extraction patterns needing improvement

**Checkpoint**: All acceptance criteria met, Phase 2 complete

---

## Progress Tracker

| Category | Total | Done | Remaining |
|----------|-------|------|-----------|
| Setup & Research | 10 | 10 | 0 |
| past-paper-scraper | 5 | 2 | 3 |
| question-extractor | 5 | 4 | 1 |
| question-validator | 6 | 5 | 1 |
| question-bank-manager | 5 | 4 | 1 |
| Batch Pipeline | 5 | 4 | 1 |
| Mass Processing | 4 | 0 | 4 |
| Validation | 6 | 0 | 6 |
| **TOTAL** | **46** | **29** | **17** |

---

## Phase Gate Checklist

Before marking Phase 2 complete, verify:

- [X] sources.md complete with 3+ sources per exam (SPSC, PPSC, KPPSC)
- [X] All 4 skills implemented (.claude/skills/exam-tutor/)
  - [X] past-paper-scraper
  - [X] question-extractor
  - [X] question-validator
  - [X] question-bank-manager
- [ ] All 4 skills tested with sample data
- [ ] Pipeline runs end-to-end successfully
- [ ] SPSC: 500+ questions in /Question-Bank/SPSC/
- [ ] PPSC: 500+ questions in /Question-Bank/PPSC/
- [ ] KPPSC: 500+ questions in /Question-Bank/KPPSC/
- [ ] All questions have complete metadata:
  - [ ] source (url, type, year)
  - [ ] difficulty level
  - [ ] topics/tags
  - [ ] unique ID
- [ ] Flagged questions documented in /Needs-Review/
- [ ] master-index.json accurate and up-to-date
- [ ] statistics.json accurate (within 1% margin)
- [ ] cross-exam-links.json has bidirectional references
- [ ] question-bank-querier (Phase 1) works with expanded bank
- [ ] Phase 1 skills remain operational with new data

**Total Estimated Time**: 8 hours (upper bound of 6-8h range)

---

## Dependencies

```
P2-001, P2-002, P2-003
    ↓
P2-004 (sources.md)
    ↓
P2-005, P2-006, P2-007, P2-008 (folders)
    ↓
P2-009, P2-010 (MCP config)
    ↓
    ├─→ P2-011, P2-012, P2-013, P2-014, P2-015 (scraper)
    ├─→ P2-016, P2-017, P2-018, P2-019, P2-020 (extractor)
    ├─→ P2-021, P2-022, P2-023, P2-024, P2-025, P2-026 (validator)
    └─→ P2-027, P2-028, P2-029, P2-030, P2-031 (manager)
            ↓
    P2-032, P2-033, P2-034, P2-035, P2-036 (pipeline)
            ↓
    P2-037, P2-038, P2-039, P2-040 (mass processing)
            ↓
    P2-041, P2-042, P2-043, P2-044, P2-045, P2-046 (validation)
```

**Critical Path**: Setup → MCP Config → Skills (parallel) → Pipeline → Mass Processing → Validation

**Parallel Opportunities**:
- P2-001, P2-002, P2-003 can run in parallel (different exam sources)
- P2-011-P2-015, P2-016-P2-020, P2-021-P2-026, P2-027-P2-031 can run in parallel (different skills)
- P2-037, P2-038, P2-039 can run in parallel (different exams)

---

## Implementation Strategy

### Sequential Approach (Recommended)

1. **Week 1, Day 1**: Setup & Research (P2-001 through P2-010)
2. **Week 1, Day 2**: Build Skills (P2-011 through P2-031)
   - Implement one skill at a time
   - Test each skill before moving to next
3. **Week 1, Day 3**: Pipeline & Processing (P2-032 through P2-040)
   - Build pipeline
   - Run mass processing
4. **Week 1, Day 4**: Validation & Cleanup (P2-041 through P2-046)

### Parallel Approach (Team)

With multiple developers:
- Developer A: past-paper-scraper (P2-011 through P2-015)
- Developer B: question-extractor (P2-016 through P2-020)
- Developer C: question-validator (P2-021 through P2-026)
- Developer D: question-bank-manager (P2-027 through P2-031)

Then converge for pipeline, processing, and validation.

---

## Next Steps

✅ Phase 2 complete → Proceed to **Phase 3: Core Tutoring Skills**

Phase 3 will implement:
- Diagnostic assessment generation
- Adaptive test generation
- Weak area identification
- Study plan generation
- ERI calculation
- Progress tracking
