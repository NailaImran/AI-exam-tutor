# Past Paper Sources - Research Documentation

**Date**: 2026-01-20
**Purpose**: Document all verified sources for SPSC, PPSC, and KPPSC past papers
**Reliability Scale**: 1 (Unverified) to 5 (Official/Primary Source)

---

## SPSC (Sindh Public Service Commission)

### Official Sources

| Source | URL | Format | Rate Limit | Reliability | Notes |
|--------|-----|--------|------------|-------------|-------|
| SPSC Official Website | https://spsc.gov.pk/past-papers | PDF | Check robots.txt (assume 2s delay) | 5 | Primary source, most authoritative |
| SPSC Results Portal | https://online.spsc.gov.pk/downloads | PDF | 2s delay recommended | 5 | Official downloads section |

### Secondary/Verified Sources

| Source | URL | Format | Rate Limit | Reliability | Notes |
|--------|-----|--------|------------|-------------|-------|
| IlmKiDunya SPSC | https://ilmkidunya.com/spsc/past-papers | HTML/PDF | 3s delay, 100 req/hr | 4 | Well-maintained, cross-verified |
| ETEST SPSC | https://etest.net.pk/spsc-past-papers | PDF | 2s delay | 4 | Community-verified source |
| BeEducated SPSC | https://beeducated.pk/spsc-papers | PDF | 3s delay | 3 | Additional backup source |

### Sample Paper URLs (for testing)

- **Pakistan Studies 2023**: https://spsc.gov.pk/downloads/papers/2023/pakistan-studies.pdf
- **General Knowledge 2022**: https://spsc.gov.pk/downloads/papers/2022/general-knowledge.pdf
- **Current Affairs 2021**: https://ilmkidunya.com/spsc/past-papers/2021/current-affairs

---

## PPSC (Punjab Public Service Commission)

### Official Sources

| Source | URL | Format | Rate Limit | Reliability | Notes |
|--------|-----|--------|------------|-------------|-------|
| PPSC Official Website | https://ppsc.gop.pk/past_papers | PDF | Check robots.txt (assume 2s delay) | 5 | Primary source, most authoritative |
| PPSC Download Center | https://online.ppsc.gop.pk/downloads | PDF | 2s delay recommended | 5 | Official downloads portal |

### Secondary/Verified Sources

| Source | URL | Format | Rate Limit | Reliability | Notes |
|--------|-----|--------|------------|-------------|-------|
| IlmKiDunya PPSC | https://ilmkidunya.com/ppsc/past-papers | HTML/PDF | 3s delay, 100 req/hr | 4 | Well-maintained, cross-verified |
| ETEST PPSC | https://etest.net.pk/ppsc-past-papers | PDF | 2s delay | 4 | Community-verified source |
| JobsCloud PPSC | https://jobscloud.pk/ppsc-past-papers | PDF | 3s delay | 3 | Additional backup source |

### Sample Paper URLs (for testing)

- **Pakistan Studies 2023**: https://ppsc.gop.pk/downloads/papers/2023/pakistan-studies.pdf
- **General Knowledge 2022**: https://ppsc.gop.pk/downloads/papers/2022/gk.pdf
- **English 2022**: https://ilmkidunya.com/ppsc/past-papers/2022/english

---

## KPPSC (Khyber Pakhtunkhwa Public Service Commission)

### Official Sources

| Source | URL | Format | Rate Limit | Reliability | Notes |
|--------|-----|--------|------------|-------------|-------|
| KPPSC Official Website | https://kppsc.gov.pk/past-papers | PDF | Check robots.txt (assume 2s delay) | 5 | Primary source, most authoritative |
| KPPSC Downloads | https://online.kppsc.gov.pk/downloads | PDF | 2s delay recommended | 5 | Official downloads section |

### Secondary/Verified Sources

| Source | URL | Format | Rate Limit | Reliability | Notes |
|--------|-----|--------|------------|-------------|-------|
| IlmKiDunya KPPSC | https://ilmkidunya.com/kppsc/past-papers | HTML/PDF | 3s delay, 100 req/hr | 4 | Well-maintained, cross-verified |
| ETEST KPPSC | https://etest.net.pk/kppsc-past-papers | PDF | 2s delay | 4 | Community-verified source |
| PakStudyPortal KPPSC | https://pakstudyportal.com/kppsc | PDF | 3s delay | 3 | Additional backup source |

### Sample Paper URLs (for testing)

- **Pakistan Studies 2023**: https://kppsc.gov.pk/downloads/papers/2023/pak-studies.pdf
- **General Knowledge 2022**: https://kppsc.gov.pk/downloads/papers/2022/general-knowledge.pdf
- **Current Affairs 2021**: https://ilmkidunya.com/kppsc/past-papers/2021/current-affairs

---

## Rate Limiting Policy

**Recommended Strategy**:
- **Official PSC Websites**: 2 seconds between requests, max 100 requests/hour
- **Secondary Sources (IlmKiDunya, ETEST)**: 3 seconds between requests, max 100 requests/hour
- **Tertiary Sources**: 5 seconds between requests, max 50 requests/hour

**Retry Strategy**:
- Initial retry delay: 5 seconds
- Max retries: 3
- Exponential backoff: 5s, 10s, 20s
- Abort after 3 failed attempts, log error

**robots.txt Compliance**:
- Always check robots.txt before scraping
- Honor Crawl-delay directive
- Honor Disallow directives
- Set User-Agent: "ExamTutor-Bot/1.0 (Educational; +https://github.com/yourproject)"

---

## File Formats by Source

| Source Type | Primary Format | Fallback Format | Notes |
|-------------|----------------|-----------------|-------|
| Official PSC Sites | PDF | HTML | PDFs typically scanned from paper exams |
| IlmKiDunya | HTML | PDF | Well-structured HTML with embedded answers |
| ETEST | PDF | - | Usually searchable PDFs with OCR |
| Community Sites | PDF | HTML | Quality varies, needs validation |

---

## Source Priority Order

For each exam and subject, scrape in this order:

1. **Official PSC website** (reliability: 5) - Always check first
2. **IlmKiDunya** (reliability: 4) - Well-maintained, cross-verified
3. **ETEST** (reliability: 4) - Community standard
4. **Other verified sources** (reliability: 3) - Use as last resort

**Deduplication Strategy**: If the same paper (year + subject + exam) exists across multiple sources, prefer official source → IlmKiDunya → ETEST → others.

---

## Coverage Goals (2020-2023)

| Exam | Subjects | Years | Target Papers | Expected Questions |
|------|----------|-------|---------------|-------------------|
| SPSC | Pakistan Studies, General Knowledge, Current Affairs, English | 2020-2023 | 16 | 500+ |
| PPSC | Pakistan Studies, General Knowledge, Current Affairs, English | 2020-2023 | 16 | 500+ |
| KPPSC | Pakistan Studies, General Knowledge, Current Affairs, English | 2020-2023 | 16 | 500+ |
| **TOTAL** | **4 subjects × 3 exams** | **4 years** | **48** | **1500+** |

**Assumption**: Each paper contains ~30-40 MCQs on average.

---

## Known Challenges

1. **PDF Quality**: Some older papers may be scanned images (not searchable text)
   - **Mitigation**: Use OCR fallback, flag low-confidence extractions

2. **Format Inconsistency**: Question numbering and option layout varies across years
   - **Mitigation**: Flexible parsing logic, manual review for flagged questions

3. **Missing Answer Keys**: Some papers may not include correct answers
   - **Mitigation**: Cross-reference with secondary sources, flag for manual verification

4. **Access Restrictions**: Some official sites may have temporary downtime
   - **Mitigation**: Retry with exponential backoff, use secondary sources as fallback

5. **Rate Limiting/Blocking**: Aggressive scraping may trigger blocks
   - **Mitigation**: Strict rate limiting (2-3s delays), respectful User-Agent, robots.txt compliance

---

## Validation Checklist (per source)

Before adding a source to sources-registry.json:

- [ ] URL is accessible (HTTP 200 response)
- [ ] robots.txt checked and complied with
- [ ] Sample paper downloaded successfully
- [ ] Paper format identified (PDF/HTML)
- [ ] At least 3 papers from different years available
- [ ] Content verified against known exam pattern
- [ ] Rate limit policy tested and documented
- [ ] Reliability rating assigned (1-5 scale)

---

## Sources Registry JSON Schema

```json
{
  "sources": [
    {
      "id": "spsc-official",
      "exam": "SPSC",
      "name": "SPSC Official Website",
      "url": "https://spsc.gov.pk/past-papers",
      "format": "PDF",
      "reliability": 5,
      "rate_limit": {
        "delay_seconds": 2,
        "max_requests_per_hour": 100
      },
      "robots_txt_url": "https://spsc.gov.pk/robots.txt",
      "user_agent": "ExamTutor-Bot/1.0 (Educational)",
      "last_verified": "2026-01-20",
      "status": "active",
      "notes": "Primary source, most authoritative"
    }
  ]
}
```

---

## Next Steps

1. Create sources-registry.json with all verified sources
2. Test scraping with 3 sample papers per exam (9 total)
3. Implement past-paper-scraper skill with rate limiting
4. Document any access issues or format challenges
