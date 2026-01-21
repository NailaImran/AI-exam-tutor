# Data Model: Phase 2 - Question Bank Automation

**Feature**: Phase 2 - Question Bank Automation
**Date**: 2026-01-19
**Status**: Complete

## Entity Overview

Phase 2 introduces 5 new entities to support the question bank automation pipeline:

| Entity | Purpose | Storage Location |
|--------|---------|------------------|
| Raw Paper | Downloaded past exam paper (PDF/HTML) | `/Raw-Papers/{Exam}/{Year}/{Subject}/` |
| Extracted Question | Parsed question awaiting validation | In-memory or temp storage |
| Flagged Question | Question needing manual review | `/Needs-Review/{Exam}/{date}/` |
| Source Registry | Catalog of paper sources | `/Question-Bank-Index/sources-registry.json` |
| Question Bank Index | Master index and statistics | `/Question-Bank-Index/` |

## Entity Schemas

### 1. Raw Paper Metadata

Tracks downloaded papers for traceability.

**Location**: `/Raw-Papers/{Exam}/{Year}/{Subject}/{filename}.metadata.json`

```json
{
  "file_name": "pakistan-studies-2021.pdf",
  "file_path": "Raw-Papers/PPSC/2021/Pakistan-Studies/pakistan-studies-2021.pdf",
  "exam_type": "PPSC",
  "year": 2021,
  "subject": "Pakistan-Studies",
  "source": {
    "url": "https://ppsc.gop.pk/downloads/papers/2021/pk-studies.pdf",
    "type": "official",
    "accessed_at": "2026-01-19T10:30:00Z"
  },
  "file_info": {
    "size_bytes": 245000,
    "format": "pdf",
    "pages": 12,
    "checksum_md5": "a1b2c3d4e5f6..."
  },
  "extraction_status": "pending | complete | failed",
  "questions_extracted": 0,
  "downloaded_at": "2026-01-19T10:30:00Z"
}
```

### 2. Extracted Question (Extended from Phase 1)

Question schema with additional metadata for automation pipeline.

**Location**: `/Question-Bank/{Exam}/{Subject}/{topic}.json`

```json
{
  "id": "PPSC-PK-00151",
  "text": "Which amendment significantly altered the balance of power between federal and provincial governments in Pakistan?",
  "options": {
    "A": "17th Amendment",
    "B": "18th Amendment",
    "C": "19th Amendment",
    "D": "20th Amendment"
  },
  "correct_answer": "B",
  "explanation": "The 18th Amendment (2010) devolved significant powers to provinces and abolished the concurrent list.",
  "topic": "constitutional-amendments",
  "difficulty": "medium",
  "source": {
    "type": "official",
    "exam": "PPSC",
    "year": 2021,
    "paper": "Pakistan Studies",
    "url": "https://ppsc.gop.pk/papers/2021/pk-studies.pdf",
    "accessed_at": "2026-01-19T10:30:00Z",
    "page_number": 3,
    "question_number": 15
  },
  "metadata": {
    "created_at": "2026-01-19T10:35:00Z",
    "updated_at": "2026-01-19T10:35:00Z",
    "validation_status": "verified",
    "extraction_confidence": 0.95,
    "cross_exam_links": ["SPSC-PK-00089", "KPPSC-PK-00112"],
    "review_history": [],
    "active": true
  }
}
```

### 3. Flagged Question

Question that failed validation and needs manual review.

**Location**: `/Needs-Review/{Exam}/{date}/{question-hash}.json`

```json
{
  "temp_id": "review-ppsc-pk-20260119-001",
  "text": "Which year did Pakistan gain independence?",
  "options": {
    "A": "1945",
    "B": "1947",
    "C": "1948",
    "D": null
  },
  "correct_answer": null,
  "source": {
    "type": "official",
    "exam": "PPSC",
    "year": 2021,
    "paper": "Pakistan Studies",
    "file_path": "Raw-Papers/PPSC/2021/Pakistan-Studies/pk-studies.pdf",
    "page_number": 2,
    "question_number": 8
  },
  "extraction": {
    "confidence": 0.65,
    "raw_text": "8. Which year did Pakistan gain independence?\n   (A) 1945\n   (B) 1947\n   (C) 1948\n   (D) [illegible]",
    "extractor_version": "1.0"
  },
  "review_flags": [
    {
      "code": "MISSING_OPTION_D",
      "severity": "critical",
      "message": "Option D is empty or unreadable",
      "field": "options.D"
    },
    {
      "code": "NO_CORRECT_ANSWER",
      "severity": "critical",
      "message": "Correct answer not found in answer key",
      "field": "correct_answer"
    }
  ],
  "flagged_at": "2026-01-19T10:35:00Z",
  "review_status": "pending | resolved | rejected",
  "resolution": null
}
```

### 4. Source Registry

Catalog of all known past paper sources with reliability ratings.

**Location**: `/Question-Bank-Index/sources-registry.json`

```json
{
  "version": "1.0",
  "last_updated": "2026-01-19T10:00:00Z",
  "sources": [
    {
      "id": "src-001",
      "name": "PPSC Official Website",
      "url": "https://ppsc.gop.pk",
      "past_papers_path": "/downloads/past-papers/",
      "type": "official",
      "reliability": 1.0,
      "exam_types": ["PPSC"],
      "formats_available": ["pdf"],
      "years_available": [2018, 2019, 2020, 2021, 2022, 2023],
      "rate_limit": {
        "requests_per_minute": 10,
        "delay_between_requests_ms": 2000
      },
      "last_scraped": "2026-01-19T09:00:00Z",
      "scrape_success_rate": 0.95,
      "notes": "Requires patience, occasional 503 errors"
    },
    {
      "id": "src-002",
      "name": "SPSC Official Website",
      "url": "https://spsc.gov.pk",
      "past_papers_path": "/past-papers/",
      "type": "official",
      "reliability": 1.0,
      "exam_types": ["SPSC"],
      "formats_available": ["pdf"],
      "years_available": [2019, 2020, 2021, 2022],
      "rate_limit": {
        "requests_per_minute": 15,
        "delay_between_requests_ms": 2000
      },
      "last_scraped": null,
      "scrape_success_rate": null,
      "notes": ""
    },
    {
      "id": "src-003",
      "name": "KPPSC Official Website",
      "url": "https://kppsc.gov.pk",
      "past_papers_path": "/resources/past-papers/",
      "type": "official",
      "reliability": 1.0,
      "exam_types": ["KPPSC"],
      "formats_available": ["pdf"],
      "years_available": [2018, 2019, 2020, 2021, 2022, 2023],
      "rate_limit": {
        "requests_per_minute": 10,
        "delay_between_requests_ms": 2000
      },
      "last_scraped": null,
      "scrape_success_rate": null,
      "notes": ""
    },
    {
      "id": "src-004",
      "name": "IlmKiDunya",
      "url": "https://www.ilmkidunya.com",
      "past_papers_path": "/past-papers/ppsc/",
      "type": "verified",
      "reliability": 0.85,
      "exam_types": ["SPSC", "PPSC", "KPPSC"],
      "formats_available": ["pdf", "html"],
      "years_available": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
      "rate_limit": {
        "requests_per_minute": 20,
        "delay_between_requests_ms": 1000
      },
      "last_scraped": null,
      "scrape_success_rate": null,
      "notes": "Good coverage but verify answers against official sources"
    }
  ]
}
```

### 5. Master Index

Quick lookup index for all questions.

**Location**: `/Question-Bank-Index/master-index.json`

```json
{
  "version": "2.0",
  "last_updated": "2026-01-19T12:00:00Z",
  "total_questions": 1500,
  "active_questions": 1485,
  "questions": [
    {
      "id": "PPSC-PK-00001",
      "exam": "PPSC",
      "subject": "Pakistan-Studies",
      "topic": "constitutional-history",
      "difficulty": "medium",
      "file_path": "Question-Bank/PPSC/Pakistan-Studies/constitutional-history.json",
      "source_type": "official",
      "year": 2021,
      "active": true,
      "cross_exam_links": []
    }
  ]
}
```

### 6. Cross-Exam Links

Tracks questions that appear across multiple exams.

**Location**: `/Question-Bank-Index/cross-exam-links.json`

```json
{
  "version": "1.0",
  "last_updated": "2026-01-19T12:00:00Z",
  "total_link_groups": 50,
  "links": [
    {
      "link_id": "link-001",
      "questions": ["PPSC-PK-00001", "SPSC-PK-00089", "KPPSC-PK-00112"],
      "link_type": "cross_exam_duplicate",
      "similarity_score": 0.98,
      "canonical_id": "PPSC-PK-00001",
      "created_at": "2026-01-19T11:00:00Z"
    }
  ]
}
```

### 7. Statistics

Aggregated question bank metrics.

**Location**: `/Question-Bank-Index/statistics.json`

```json
{
  "version": "1.0",
  "last_updated": "2026-01-19T12:00:00Z",
  "totals": {
    "all_questions": 1500,
    "active_questions": 1485,
    "inactive_questions": 15,
    "pending_review": 25
  },
  "by_exam": {
    "SPSC": {
      "total": 500,
      "active": 495,
      "by_subject": {
        "Pakistan-Studies": 200,
        "General-Knowledge": 150,
        "Current-Affairs": 100,
        "English": 50
      }
    },
    "PPSC": {
      "total": 500,
      "active": 495,
      "by_subject": {}
    },
    "KPPSC": {
      "total": 500,
      "active": 495,
      "by_subject": {}
    }
  },
  "by_difficulty": {
    "easy": 450,
    "medium": 750,
    "hard": 300
  },
  "by_source_type": {
    "official": 1200,
    "verified": 250,
    "unverified": 50
  },
  "by_year": {
    "2018": 150,
    "2019": 200,
    "2020": 250,
    "2021": 300,
    "2022": 350,
    "2023": 250
  },
  "coverage_analysis": {
    "low_coverage_topics": [
      {
        "exam": "SPSC",
        "subject": "Pakistan-Studies",
        "topic": "foreign-policy-2020s",
        "count": 5,
        "status": "low"
      }
    ],
    "adequate_coverage_topics": [],
    "good_coverage_topics": []
  },
  "cross_exam_stats": {
    "total_link_groups": 50,
    "questions_with_links": 150
  }
}
```

## Entity Relationships

```
┌─────────────────┐
│   Raw Paper     │
│  (PDF/HTML)     │
└────────┬────────┘
         │ extracts
         ▼
┌─────────────────┐     fails      ┌─────────────────┐
│   Extracted     │────────────────▶│    Flagged      │
│   Question      │                 │    Question     │
└────────┬────────┘                 └────────┬────────┘
         │ validates                         │ resolves
         ▼                                   │
┌─────────────────┐◀─────────────────────────┘
│   Validated     │
│   Question      │
└────────┬────────┘
         │ imports
         ▼
┌─────────────────┐     links      ┌─────────────────┐
│  Question Bank  │────────────────▶│  Cross-Exam     │
│   (by topic)    │                 │    Links        │
└────────┬────────┘                 └─────────────────┘
         │ indexes
         ▼
┌─────────────────┐
│  Master Index   │
│  & Statistics   │
└─────────────────┘
```

## Validation Rules Summary

| Field | Rule | Error Code |
|-------|------|------------|
| text | Non-empty, >10 chars | EMPTY_TEXT |
| options.A-D | All non-empty | MISSING_OPTION_{X} |
| correct_answer | One of A, B, C, D | INVALID_ANSWER |
| source.url | Valid URL format | INVALID_SOURCE |
| metadata.extraction_confidence | 0.0 to 1.0 | OUT_OF_RANGE |

## Backward Compatibility

Phase 2 question schema extends Phase 1:
- All Phase 1 fields preserved
- New fields added: `source` (detailed), `metadata.cross_exam_links`, `metadata.review_history`
- Phase 1 questions can be migrated by adding default values for new fields
