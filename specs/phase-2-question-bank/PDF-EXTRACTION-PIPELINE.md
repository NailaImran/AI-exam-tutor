# PDF Extraction Pipeline for Scanned Papers

## Overview

This document describes the process for extracting MCQ questions from scanned PDF past papers and converting them to the question bank JSON format.

## Challenge

Most PPSC/SPSC/KPPSC solved papers are available as:
- Scanned image PDFs (not text-searchable)
- Low-resolution scans
- Mixed formats (some text, some images)

## Pipeline Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Source PDFs    │───▶│  OCR Engine     │───▶│  Text Cleanup   │
│  (scanned)      │    │  (Tesseract/    │    │  (regex/manual) │
└─────────────────┘    │   Adobe/Google) │    └────────┬────────┘
                       └─────────────────┘             │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Question Bank  │◀───│  JSON Generator │◀───│  MCQ Parser     │
│  (.json files)  │    │  (structured)   │    │  (Q/A extract)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Step 1: Source Acquisition

### Recommended Sources
1. **Official websites**: ppsc.gop.pk, spsc.gos.pk, kppsc.gov.pk
2. **Book stores**: Jahangir's, Dogar Brothers solved papers
3. **Online repositories**: testpoint.pk, pakmcqs.com (often have typed versions)

### File Organization
```
Raw-Papers/
├── PPSC/
│   ├── 2023/
│   │   ├── junior-clerk-2023.pdf
│   │   └── assistant-2023.pdf
│   ├── 2022/
│   └── 2021/
├── SPSC/
└── KPPSC/
```

## Step 2: OCR Processing

### Option A: Google Cloud Vision (Recommended for accuracy)
```bash
# Install Google Cloud SDK
gcloud auth login
gcloud ml vision detect-text ./input.pdf --output=output.txt
```

### Option B: Tesseract (Free, local)
```bash
# Install Tesseract
# Windows: choco install tesseract
# Linux: apt install tesseract-ocr

# Convert PDF to images first
pdftoppm -png input.pdf output

# Run OCR on each page
tesseract output-01.png page1 -l eng
```

### Option C: Adobe Acrobat Pro
1. Open scanned PDF
2. Tools → Enhance Scans → Recognize Text
3. Export as Word/Text

### Option D: Manual Transcription
For low-quality scans, manual typing may be fastest:
1. Open PDF in viewer
2. Type questions into template
3. Use autocomplete for common options

## Step 3: Text Cleanup

### Common OCR Errors to Fix
| OCR Output | Correct |
|------------|---------|
| `0` (zero) | `O` (letter) |
| `1` (one) | `l` (letter L) or `I` |
| `rn` | `m` |
| Missing spaces | Add spaces |
| `?` instead of `2` | Context-dependent |

### Cleanup Script (Python)
```python
import re

def clean_ocr_text(text):
    # Fix common OCR errors
    text = re.sub(r'\b0(?=[a-zA-Z])', 'O', text)  # 0 before letter -> O
    text = re.sub(r'(?<=[a-zA-Z])0\b', 'O', text)  # 0 after letter -> O
    text = re.sub(r'\brn\b', 'm', text)            # rn -> m

    # Normalize question markers
    text = re.sub(r'Q[\.\s]*(\d+)', r'Q\1.', text)

    # Normalize answer markers
    text = re.sub(r'\(([A-D])\)', r'\1)', text)

    return text
```

## Step 4: MCQ Parsing

### Expected Input Format
```
Q1. When was Pakistan founded?
A) 1945
B) 1947
C) 1948
D) 1950
Answer: B

Q2. Who was the first Prime Minister?
...
```

### Parser Script (Python)
```python
import re
import json

def parse_mcqs(text):
    questions = []

    # Pattern for MCQ extraction
    pattern = r'Q(\d+)\.\s*(.*?)\n\s*A\)\s*(.*?)\n\s*B\)\s*(.*?)\n\s*C\)\s*(.*?)\n\s*D\)\s*(.*?)\n\s*(?:Answer|Ans):\s*([A-D])'

    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        q_num, q_text, opt_a, opt_b, opt_c, opt_d, answer = match
        questions.append({
            "id": f"PPSC-XX-{q_num.zfill(5)}",
            "text": q_text.strip(),
            "options": {
                "A": opt_a.strip(),
                "B": opt_b.strip(),
                "C": opt_c.strip(),
                "D": opt_d.strip()
            },
            "correct_answer": answer.strip(),
            "topic": "TBD",  # Manually categorize
            "difficulty": "medium",
            "source": "pdf-extraction"
        })

    return questions
```

## Step 5: Topic Classification

### Manual Classification Guide
| Keywords in Question | Topic |
|---------------------|-------|
| constitution, amendment, article | Constitutional History |
| 1947, independence, partition, Jinnah | Independence Movement |
| river, mountain, province, city | Geography |
| GDP, economy, budget, trade | Economy |
| foreign, treaty, UN, relations | Foreign Relations |
| Quran, Hadith, Islam, Prophet | Islamic Studies |

### Semi-Automated Classification
```python
TOPIC_KEYWORDS = {
    "Constitutional History": ["constitution", "amendment", "article", "president"],
    "Independence Movement": ["1947", "independence", "partition", "jinnah", "iqbal"],
    "Geography": ["river", "mountain", "province", "district", "area"],
    "Economy": ["gdp", "budget", "trade", "export", "import"],
    "Foreign Relations": ["treaty", "agreement", "foreign", "bilateral"],
    "Islamic Studies": ["quran", "hadith", "prophet", "islam", "namaz"]
}

def classify_topic(question_text):
    text_lower = question_text.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return topic
    return "General Knowledge"
```

## Step 6: JSON Generation

### Output Format
```json
{
  "$schema": "exam-tutor/question-bank/v1",
  "metadata": {
    "exam_type": "PPSC",
    "subject": "Pakistan Studies",
    "topic": "Constitutional History",
    "source": "Junior Clerk Paper 2023",
    "created_at": "2026-01-26T00:00:00Z",
    "question_count": 50
  },
  "questions": [
    {
      "id": "PPSC-PK-00201",
      "text": "When was the first constitution enacted?",
      "options": {"A": "1947", "B": "1956", "C": "1962", "D": "1973"},
      "correct_answer": "B",
      "topic": "Constitutional History",
      "difficulty": "easy",
      "explanation": "The first constitution was enacted on March 23, 1956."
    }
  ]
}
```

## Step 7: Validation

### Pre-Import Checklist
- [ ] All questions have unique IDs
- [ ] All questions have 4 options (A, B, C, D)
- [ ] All correct_answer values are A, B, C, or D
- [ ] No duplicate questions (check against master-index.json)
- [ ] Topics assigned to all questions
- [ ] Difficulty levels assigned (easy/medium/hard)

### Validation Script
```python
def validate_questions(questions):
    errors = []
    ids_seen = set()

    for i, q in enumerate(questions):
        # Check required fields
        required = ['id', 'text', 'options', 'correct_answer', 'topic', 'difficulty']
        for field in required:
            if field not in q:
                errors.append(f"Q{i}: Missing field '{field}'")

        # Check unique ID
        if q.get('id') in ids_seen:
            errors.append(f"Q{i}: Duplicate ID '{q.get('id')}'")
        ids_seen.add(q.get('id'))

        # Check options
        if 'options' in q:
            for opt in ['A', 'B', 'C', 'D']:
                if opt not in q['options']:
                    errors.append(f"Q{i}: Missing option {opt}")

        # Check answer validity
        if q.get('correct_answer') not in ['A', 'B', 'C', 'D']:
            errors.append(f"Q{i}: Invalid correct_answer '{q.get('correct_answer')}'")

    return errors
```

## Batch Processing Workflow

For processing multiple papers:

```bash
# 1. Place PDFs in Raw-Papers/{EXAM}/{YEAR}/
# 2. Run OCR on batch
for file in Raw-Papers/PPSC/2023/*.pdf; do
    tesseract "$file" "${file%.pdf}" -l eng
done

# 3. Run parser on all text files
python parse_all.py Raw-Papers/PPSC/2023/

# 4. Review and validate
python validate.py output/

# 5. Import to question bank
python import.py output/ question-bank/PPSC/
```

## Quality Metrics

| Metric | Target | Current |
|--------|--------|---------|
| OCR Accuracy | >95% | Manual review needed |
| Topic Classification | >90% | Semi-automated |
| Duplicate Detection | 100% | Via master-index.json |
| Answer Verification | 100% | Manual spot-check |

## Notes

- Scanned PDFs require significant manual review
- Budget 5-10 minutes per 50 questions for cleanup
- Consider typed web sources (pakmcqs.com) as faster alternative
- Always verify answers against authoritative sources

## Alternative: Web Scraping

For faster question acquisition, see [PAPER-COLLECTION-GUIDE.md](./PAPER-COLLECTION-GUIDE.md) for web scraping approach using sites with already-typed questions.
