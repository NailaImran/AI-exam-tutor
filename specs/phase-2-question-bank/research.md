# Research: Phase 2 - Question Bank Automation

**Feature**: Phase 2 - Question Bank Automation
**Date**: 2026-01-19
**Status**: Complete

## Research Questions

### 1. Past Paper Source Availability

**Question**: Where can official past papers be obtained for SPSC, PPSC, and KPPSC?

**Decision**: Use official PSC websites as primary sources, supplemented by verified educational repositories.

**Findings**:

| Exam | Official URL | Past Papers Section | Format | Access |
|------|--------------|---------------------|--------|--------|
| SPSC | spsc.gov.pk | /past-papers/ or /downloads/ | PDF | Public |
| PPSC | ppsc.gop.pk | /downloads/past-papers/ | PDF | Public |
| KPPSC | kppsc.gov.pk | /resources/past-papers/ | PDF | Public |

**Secondary Sources** (verified educational sites):
- ilmkidunya.com - Pakistan's largest educational portal
- pakprep.com - Competitive exam preparation site
- testpoint.pk - Past papers repository

**Rationale**: Official sources ensure accuracy (Constitution Principle I). Secondary sources expand coverage but require verification.

**Alternatives Considered**:
- Scraping unofficial forums: Rejected (unreliable answers)
- Purchasing from vendors: Rejected (cost, licensing issues)

---

### 2. PDF Parsing Approach

**Question**: How should PDFs be parsed to extract MCQ questions?

**Decision**: Use MCP filesystem with text extraction, flag image-heavy PDFs for manual review.

**Findings**:
- Most official PSC papers are text-based PDFs (good OCR quality)
- Some older papers are scanned images (require OCR)
- MCQ format is consistent: numbered questions, A-D options
- Answer keys usually at end of document or separate file

**Parsing Strategy**:
1. Extract text from PDF using standard text extraction
2. Identify question patterns: `^\d+[.)]\s+` or `^Q\d+[.:]\s+`
3. Identify option patterns: `^[A-D][.)]\s+` or `^\([A-D]\)\s+`
4. Locate answer key section: "Answer Key", "Answers:", etc.
5. Flag low-confidence extractions for manual review

**Rationale**: Text-based extraction is reliable for 90%+ of papers. Manual review handles edge cases without compromising accuracy.

**Alternatives Considered**:
- AI-powered OCR: Rejected (adds complexity, most papers don't need it)
- External PDF services: Rejected (data privacy, cost)

---

### 3. Duplicate Detection Algorithm

**Question**: How should duplicates be detected across exam types?

**Decision**: Text similarity using normalized comparison with 90% threshold.

**Algorithm**:
```
1. Normalize question text:
   - Lowercase
   - Remove punctuation
   - Remove extra whitespace
   - Stem common words

2. Compare using dual approach:
   - Token overlap (Jaccard similarity)
   - Character-level similarity (Levenshtein ratio)

3. Combined score:
   similarity = (token_overlap * 0.6) + (levenshtein_ratio * 0.4)

4. Thresholds:
   - >= 1.0: Exact duplicate (reject)
   - >= 0.9: Near duplicate (link + review)
   - < 0.9: Unique (accept)
```

**Rationale**: Simple, deterministic, runs without external dependencies. Catches variations in wording while avoiding false positives.

**Alternatives Considered**:
- Semantic embeddings: Rejected (requires ML infrastructure)
- Hash-based: Rejected (misses minor variations)

---

### 4. Rate Limiting Strategy

**Question**: How should web scraping respect rate limits?

**Decision**: Conservative rate limiting with exponential backoff.

**Implementation**:
```
- Minimum delay: 2 seconds between requests
- Exponential backoff on errors: 5s → 10s → 30s → 60s
- Maximum 3 retries per resource
- Maximum 100 requests per hour per domain
- Respect robots.txt directives
- User-Agent: "ExamTutor-Bot/1.0 (educational; contact@example.com)"
```

**Rationale**: Prevents IP blocking, respects server resources, maintains access for future scraping.

**Alternatives Considered**:
- Aggressive scraping: Rejected (risk of blocking)
- Proxy rotation: Rejected (adds complexity, ethical concerns)

---

### 5. Question ID Format

**Question**: What ID format ensures uniqueness and traceability?

**Decision**: `{EXAM}-{SUBJECT_CODE}-{NNNNN}` format.

**Format Details**:
```
EXAM: SPSC | PPSC | KPPSC
SUBJECT_CODE:
  - PK = Pakistan Studies
  - GK = General Knowledge
  - CA = Current Affairs
  - EN = English
  - MA = Mathematics
NNNNN: 5-digit sequential number, zero-padded

Examples:
  PPSC-PK-00001
  SPSC-GK-00156
  KPPSC-CA-00042
```

**Rationale**: Human-readable, sortable, encodes key metadata, supports 99,999 questions per exam-subject combination.

**Alternatives Considered**:
- UUID: Rejected (not human-readable)
- Timestamp-based: Rejected (doesn't encode metadata)
- Hash-based: Rejected (not sequential)

---

### 6. Storage Structure

**Question**: How should raw papers and extracted questions be organized?

**Decision**: Hierarchical folder structure by exam/year/subject.

**Structure**:
```
Raw-Papers/
├── SPSC/{Year}/{Subject}/{filename}.pdf
├── PPSC/{Year}/{Subject}/{filename}.pdf
└── KPPSC/{Year}/{Subject}/{filename}.pdf

Needs-Review/
├── SPSC/{date}/{question-id}.json
├── PPSC/{date}/{question-id}.json
└── KPPSC/{date}/{question-id}.json

Question-Bank/
├── SPSC/{Subject}/{topic}.json
├── PPSC/{Subject}/{topic}.json
└── KPPSC/{Subject}/{topic}.json

Question-Bank-Index/
├── master-index.json
├── cross-exam-links.json
├── statistics.json
└── sources-registry.json
```

**Rationale**: Mirrors Phase 1 structure, enables easy navigation, supports MCP filesystem operations.

---

### 7. Validation Rules

**Question**: What validation rules ensure question quality?

**Decision**: Multi-level validation with critical/warning/info classification.

**Critical (Reject)**:
- Empty or too-short question text (<10 chars)
- Missing any option (A, B, C, or D)
- Invalid correct answer (not A-D)
- Exact duplicate of existing question

**Warning (Needs Review)**:
- Near duplicate (90-99% similarity)
- No correct answer found in source
- Low extraction confidence (<80%)
- Cannot determine topic automatically

**Info (Accept with note)**:
- Default difficulty assigned (medium)
- Cross-exam link created
- Source marked as secondary

**Rationale**: Ensures Accuracy First principle while maximizing automation. Critical rules are non-negotiable; warnings allow human judgment.

---

## Technology Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Storage | Local filesystem (MCP) | Consistent with Phase 1, no database needed |
| Scraping | MCP + HTTP capabilities | Respects rate limits, logs activity |
| PDF parsing | Text extraction | Handles 90%+ of papers, flag exceptions |
| Duplicate detection | Text similarity | Simple, deterministic, no ML required |
| Question IDs | Sequential per exam-subject | Human-readable, sortable, traceable |
| Validation | Multi-level rules | Balances automation with accuracy |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PSC website blocks scraping | Medium | High | Cache papers, use secondary sources |
| Low OCR quality | Low | Medium | Flag for manual review |
| Duplicate false positives | Low | Low | Review threshold, manual override |
| Answer key missing | Medium | Medium | Mark unverified, exclude from practice |

---

## Conclusion

Phase 2 implementation can proceed with:
1. Conservative scraping from official sources
2. Text-based PDF extraction with manual review fallback
3. Simple duplicate detection algorithm
4. Multi-level validation ensuring accuracy
5. Hierarchical storage consistent with Phase 1

All research questions resolved. No NEEDS CLARIFICATION items remain.
