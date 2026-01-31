# Past Paper Collection Guide

**Purpose**: Collect 48+ past papers from SPSC, PPSC, and KPPSC for Phase 2 mass processing
**Target**: 1500+ questions across 3 exams
**Timeline**: 1-2 hours (manual download) or automated with web scraping

---

## Collection Strategy

### Priority 1: Official PSC Websites (Reliability: 5/5)

These are the most authoritative sources. Always check here first.

#### SPSC (Sindh Public Service Commission)

**Primary URLs**:
- Main website: https://www.spsc.gov.pk
- Past papers section: https://www.spsc.gov.pk/past-papers
- Downloads: https://online.spsc.gov.pk/downloads

**What to Download**:
- Pakistan Studies (2020-2023): 4 papers
- General Knowledge (2020-2023): 4 papers
- Current Affairs (2020-2023): 4 papers
- English (2020-2023): 4 papers
- **Target**: 16 papers

**Download Instructions**:
1. Navigate to past papers section
2. Select year (2020, 2021, 2022, 2023)
3. Select subject (Pakistan Studies, GK, Current Affairs, English)
4. Download PDF to: `Raw-Papers/SPSC/{Year}/{Subject}.pdf`

---

#### PPSC (Punjab Public Service Commission)

**Primary URLs**:
- Main website: https://www.ppsc.gop.pk
- Past papers: https://www.ppsc.gop.pk/past_papers
- Online portal: https://online.ppsc.gop.pk

**What to Download**:
- Pakistan Studies (2020-2023): 4 papers
- General Knowledge (2020-2023): 4 papers
- Current Affairs (2020-2023): 4 papers
- English (2020-2023): 4 papers
- **Target**: 16 papers

**Download Instructions**:
1. Go to ppsc.gop.pk
2. Navigate to "Past Papers" or "Downloads"
3. Filter by year and subject
4. Save to: `Raw-Papers/PPSC/{Year}/{Subject}.pdf`

---

#### KPPSC (Khyber Pakhtunkhwa Public Service Commission)

**Primary URLs**:
- Main website: https://www.kppsc.gov.pk
- Past papers: https://www.kppsc.gov.pk/past-papers
- Downloads: https://online.kppsc.gov.pk

**What to Download**:
- Pakistan Studies (2020-2023): 4 papers
- General Knowledge (2020-2023): 4 papers
- Current Affairs (2020-2023): 4 papers
- English (2020-2023): 4 papers
- **Target**: 16 papers

**Download Instructions**:
1. Visit kppsc.gov.pk
2. Find past papers archive
3. Download by year and subject
4. Save to: `Raw-Papers/KPPSC/{Year}/{Subject}.pdf`

---

### Priority 2: Verified Secondary Sources (Reliability: 4/5)

If official sources are incomplete, use these trusted secondary sources:

#### IlmKiDunya

**URLs**:
- SPSC: https://ilmkidunya.com/spsc/past-papers
- PPSC: https://ilmkidunya.com/ppsc/past-papers
- KPPSC: https://ilmkidunya.com/kppsc/past-papers

**Advantages**:
- Well-organized by year and subject
- Often includes answer keys
- Good HTML formatting (easier to extract)
- Verified by educational community

**Download Method**:
- Papers available as HTML or PDF
- Can save HTML page directly
- Save to same folder structure: `Raw-Papers/{Exam}/{Year}/{Subject}.html`

---

#### ETEST Pakistan

**URLs**:
- SPSC: https://etest.net.pk/spsc-past-papers
- PPSC: https://etest.net.pk/ppsc-past-papers
- KPPSC: https://etest.net.pk/kppsc-past-papers

**Advantages**:
- Searchable PDFs (good for extraction)
- Community-verified content
- Regular updates

---

#### PakStudyPortal / BeEducated

**URLs**:
- https://pakstudyportal.com
- https://beeducated.pk

**Use Case**: Backup if official sources missing specific years/subjects

---

## Manual Download Procedure (Recommended for First Time)

### Step-by-Step Process

1. **Create download checklist**
   ```
   [ ] SPSC Pakistan Studies 2020
   [ ] SPSC Pakistan Studies 2021
   [ ] SPSC Pakistan Studies 2022
   [ ] SPSC Pakistan Studies 2023
   ... (continue for all 48 papers)
   ```

2. **Open browser in incognito mode** (avoid rate limiting issues)

3. **Download systematically**:
   - Start with SPSC 2023, work backward to 2020
   - Complete all subjects for one year before moving to next
   - Verify each download (check file size > 0)

4. **Save with consistent naming**:
   ```
   Raw-Papers/SPSC/2023/pakistan-studies.pdf
   Raw-Papers/SPSC/2023/general-knowledge.pdf
   Raw-Papers/SPSC/2023/current-affairs.pdf
   Raw-Papers/SPSC/2023/english.pdf
   ```

5. **Check each file**:
   - Open PDF to verify it's readable
   - Check it contains MCQ questions
   - Verify answer key is present (if available)

6. **Log your progress** in `Logs/scraper/manual-download.log`:
   ```
   2026-01-21 | SPSC | 2023 | Pakistan Studies | SUCCESS | ppsc.gop.pk | 2.4MB
   2026-01-21 | SPSC | 2023 | General Knowledge | SUCCESS | ppsc.gop.pk | 1.8MB
   ```

---

## Automated Download (Future Enhancement)

### Using Python + Selenium

Create a script: `scripts/download-papers.py`

```python
import time
import requests
from selenium import webdriver
from pathlib import Path

# Configuration
BASE_DIR = Path("Raw-Papers")
DELAY = 3  # seconds between requests
USER_AGENT = "ExamTutor-Bot/1.0 (Educational)"

sources = {
    "SPSC": "https://www.spsc.gov.pk/past-papers",
    "PPSC": "https://www.ppsc.gop.pk/past_papers",
    "KPPSC": "https://www.kppsc.gov.pk/past-papers"
}

def download_paper(exam, year, subject, url):
    """Download a single past paper with rate limiting"""
    output_dir = BASE_DIR / exam / str(year)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{subject.lower().replace(' ', '-')}.pdf"

    # Download with proper headers
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded: {exam} {year} {subject}")
        return True
    else:
        print(f"❌ Failed: {exam} {year} {subject} (HTTP {response.status_code})")
        return False

    time.sleep(DELAY)  # Rate limiting

# Usage
# download_paper("SPSC", 2023, "Pakistan Studies", "https://...")
```

**Note**: This requires:
- Python 3.8+
- `pip install requests selenium`
- Actual paper URLs (need to scrape website first)

---

## Alternative: Contact PSC Directly

If website download is difficult:

### Email Requests

**SPSC**: info@spsc.gov.pk
**PPSC**: info@ppsc.gop.pk
**KPPSC**: info@kppsc.gov.pk

**Email Template**:
```
Subject: Request for Past Examination Papers (2020-2023)

Dear Sir/Madam,

I am developing an educational resource for competitive exam preparation and
would like to request digital copies of past examination papers from your
commission for the following:

Years: 2020, 2021, 2022, 2023
Subjects: Pakistan Studies, General Knowledge, Current Affairs, English

These papers will be used for educational purposes only, with proper attribution
to [SPSC/PPSC/KPPSC] as the source.

If these are available on your website, please direct me to the appropriate
download section. Otherwise, I would greatly appreciate if you could provide
these papers via email or share a download link.

Thank you for your assistance.

Best regards,
[Your Name]
```

---

## Quality Checklist (Per Paper)

Before accepting a downloaded paper, verify:

- [ ] File is readable (not corrupted)
- [ ] Contains MCQ questions (not essay-type)
- [ ] Has at least 15-20 questions
- [ ] Questions are in English or Urdu (readable)
- [ ] Options A, B, C, D are clearly marked
- [ ] Answer key is present (or can be obtained separately)
- [ ] File size is reasonable (>100KB for PDF, >10KB for HTML)
- [ ] Paper matches the claimed year and subject

**Reject if**:
- File is corrupt or password-protected
- Contains only images (scanned without OCR)
- Questions are incomplete or cut off
- Answer key is completely missing
- Wrong subject or year

---

## Expected Outcomes

### Ideal Scenario (100% success)
```
48 papers × ~35 questions each = ~1,680 questions
After validation (80% pass rate) = ~1,344 questions
✅ Exceeds 1500 target
```

### Realistic Scenario (70% success)
```
34 papers × ~35 questions each = ~1,190 questions
After validation (75% pass rate) = ~893 questions
⚠️ Below 1500 target, need more papers
```

### Minimum Acceptable
```
30 papers × ~40 questions each = ~1,200 questions
After validation (80% pass rate) = ~960 questions
✅ Acceptable for Phase 2 completion (can add more later)
```

---

## Tracking Progress

Use this table to track downloads:

| Exam | Year | Subject | Source | Status | File Size | Notes |
|------|------|---------|--------|--------|-----------|-------|
| SPSC | 2023 | Pakistan Studies | Official | ✅ | 2.4MB | |
| SPSC | 2023 | General Knowledge | Official | ✅ | 1.8MB | |
| SPSC | 2023 | Current Affairs | IlmKiDunya | ✅ | HTML | Official unavailable |
| ... | ... | ... | ... | ... | ... | ... |

**Track in**: `Logs/scraper/download-tracker.md`

---

## Next Steps After Collection

Once you have 30+ papers:

1. **Run question-extractor** on all downloaded papers
   - Expected: 70-85% extraction rate (lower than 100% for sample papers)
   - Flagged questions will go to Needs-Review/

2. **Run question-validator** on extracted questions
   - Expected: 70-80% validation rate
   - Rejected questions logged with reasons

3. **Run question-bank-manager** on validated questions
   - Import to question bank
   - Update statistics
   - Verify 1500+ target met

4. **Manual review** of flagged questions in Needs-Review/
   - Correct OCR errors
   - Add missing answers
   - Re-validate and import

---

## Troubleshooting

### Problem: Official website is down
**Solution**: Use IlmKiDunya or ETEST as fallback

### Problem: Papers are scanned images (no text)
**Solution**:
- Use OCR tool (Adobe Acrobat, Tesseract)
- Extract text, save as new PDF
- Expect lower extraction accuracy

### Problem: Answer keys are missing
**Solution**:
- Search for answer keys separately on education forums
- Cross-reference with secondary sources
- Flag questions for manual verification

### Problem: Rate limited or blocked
**Solution**:
- Wait 24 hours before retrying
- Use different IP (VPN, different network)
- Contact website admin to whitelist

### Problem: PDFs are password-protected
**Solution**:
- Search for unprotected versions
- Contact PSC for official copy
- Skip and find alternative papers

---

## Estimated Time Required

**Manual Download** (48 papers):
- Finding papers: 30-60 minutes
- Downloading: 20-30 minutes
- Verification: 10-20 minutes
- **Total**: 1-2 hours

**Automated Download** (setup + run):
- Script setup: 1-2 hours (first time)
- Running script: 10-20 minutes
- Verification: 10-20 minutes
- **Total**: ~2-3 hours (but reusable for future updates)

---

## Legal & Ethical Considerations

### ✅ Acceptable Use
- Educational and research purposes
- Non-commercial use
- Proper attribution to source
- Respecting robots.txt and rate limits

### ❌ Not Acceptable
- Commercial sale of papers
- Removing source attribution
- Aggressive scraping (DDOS)
- Circumventing access controls

**Our Approach**: Educational, respectful, attributed, rate-limited ✅

---

## Support Resources

If you need help:
1. Check PSC website FAQs
2. Contact PSC info emails
3. Visit education forums (PakStudyPortal, EduKids)
4. Ask in Pakistani education Facebook groups

---

**Ready to start?** Begin with PPSC 2023 papers (most likely to be available online).

**Questions?** Document any issues in `Logs/scraper/issues.log` for future reference.
