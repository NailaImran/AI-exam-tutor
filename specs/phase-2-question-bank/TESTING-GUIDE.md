# Phase 2 Testing Guide

**Purpose**: Test all 4 Phase 2 skills with sample data
**Sample Papers**: 3 papers with 47 total questions
**Estimated Time**: 1-2 hours

---

## Sample Papers Available

```
Raw-Papers/
├── PPSC/2023/pakistan-studies-sample.txt (20 questions)
├── SPSC/2023/general-knowledge-sample.txt (15 questions)
└── KPPSC/2023/current-affairs-sample.txt (12 questions)
```

---

## Test 1: Question Extractor (P2-020)

**Objective**: Extract MCQs from the 3 sample papers

### Test Steps:

1. **Invoke question-extractor skill** for PPSC paper:
   ```
   "Use the question-extractor skill to extract questions from
   Raw-Papers/PPSC/2023/pakistan-studies-sample.txt

   Input:
   - raw_paper_path: Raw-Papers/PPSC/2023/pakistan-studies-sample.txt
   - exam_type: PPSC
   - year: 2023
   - subject: Pakistan Studies

   Follow the skill specification in .claude/skills/exam-tutor/question-extractor/SKILL.md"
   ```

2. **Expected Output**:
   - 20 questions extracted
   - All with confidence score 1.0 (clean formatting)
   - Question text, 4 options (A-D), correct answer identified
   - Source reference to the file

3. **Repeat for other papers**:
   - SPSC General Knowledge (expect 15 questions)
   - KPPSC Current Affairs (expect 12 questions)

4. **Success Criteria**:
   - ✅ 80%+ extraction accuracy (all 47 should extract cleanly)
   - ✅ Confidence scores assigned correctly
   - ✅ All 4 options (A, B, C, D) extracted for each question

---

## Test 2: Question Validator (P2-026)

**Objective**: Validate the 47 extracted questions

### Test Steps:

1. **Invoke question-validator skill** on extracted questions:
   ```
   "Use the question-validator skill to validate the extracted questions.

   For each question:
   - Verify all 4 options present
   - Verify correct_answer is A, B, C, or D
   - Check for duplicates against master-index.json
   - Auto-tag difficulty level
   - Auto-tag topics

   Follow the skill specification in .claude/skills/exam-tutor/question-validator/SKILL.md"
   ```

2. **Expected Output**:
   - All 47 questions should be VALID (complete, no duplicates)
   - Difficulty tags assigned (easy/medium/hard)
   - Topic tags assigned based on question content

3. **Test with intentionally bad questions**:

   Create 5 bad questions to test rejection:
   - Question with missing option D
   - Question with invalid answer "E"
   - Question with duplicate text
   - Question with too short text
   - Question with malformed options

4. **Success Criteria**:
   - ✅ All 47 valid questions pass validation
   - ✅ All 5 bad questions rejected with specific reasons
   - ✅ Rejection codes are specific (MISSING_OPTION_D, NO_CORRECT_ANSWER, etc.)

---

## Test 3: Question Bank Manager (P2-031)

**Objective**: Add validated questions to the question bank

### Test Steps:

1. **Invoke question-bank-manager skill** to add questions:
   ```
   "Use the question-bank-manager skill to add the validated questions to the bank.

   For each validated question:
   - action: ADD
   - Generate unique ID (format: {EXAM}-{SUBJECT_CODE}-{NNNNN})
   - Add to appropriate file: question-bank/{Exam}/{Subject}/{topic}.json
   - Update master-index.json
   - Update statistics.json

   Follow the skill specification in .claude/skills/exam-tutor/question-bank-manager/SKILL.md"
   ```

2. **Expected Output**:
   - 47 unique IDs generated:
     - PPSC-PK-00001 through PPSC-PK-00020 (Pakistan Studies)
     - SPSC-GK-00001 through SPSC-GK-00015 (General Knowledge)
     - KPPSC-CA-00001 through KPPSC-CA-00012 (Current Affairs)
   - Questions organized in topic files
   - master-index.json updated with 47 entries
   - statistics.json showing correct counts

3. **Verify Statistics**:
   ```json
   {
     "total_questions": 47,
     "by_exam": {
       "PPSC": 20,
       "SPSC": 15,
       "KPPSC": 12
     },
     "by_subject": {
       "Pakistan Studies": 20,
       "General Knowledge": 15,
       "Current Affairs": 12
     }
   }
   ```

4. **Success Criteria**:
   - ✅ All 47 questions added successfully
   - ✅ Unique IDs generated (no collisions)
   - ✅ Files organized correctly by exam/subject/topic
   - ✅ Statistics accurate (within 1%)

---

## Test 4: End-to-End Pipeline (P2-036)

**Objective**: Test full workflow from raw paper to question bank

### Test Steps:

1. **Run complete pipeline** on one paper:
   ```
   "Execute the complete Phase 2 pipeline on the PPSC Pakistan Studies paper:

   Step 1: question-extractor
     - Extract from Raw-Papers/PPSC/2023/pakistan-studies-sample.txt

   Step 2: question-validator
     - Validate all extracted questions

   Step 3: question-bank-manager
     - Add validated questions to bank

   Track progress and log any errors.
   Follow the Mass Paper Import Pipeline workflow in
   .claude/skills/exam-tutor/references/skill-orchestration.md"
   ```

2. **Monitor Progress**:
   - Extraction: 20 questions found
   - Validation: 20 passed, 0 rejected, 0 flagged
   - Addition: 20 added, IDs PPSC-PK-00001 to PPSC-PK-00020

3. **Verify Results**:
   - Check `question-bank/PPSC/Pakistan-Studies/*.json`
   - Check `question-bank/master-index.json` has 20 entries
   - Check `question-bank/statistics.json` shows correct counts

4. **Success Criteria**:
   - ✅ Full pipeline executes without errors
   - ✅ All questions flow through: extract → validate → add
   - ✅ Logging tracks each step
   - ✅ Final state is consistent (indexes match question files)

---

## Test Results Template

After completing tests, document results:

```markdown
# Phase 2 Testing Results

**Date**: [DATE]
**Tester**: [NAME]

## Test 1: Question Extractor
- Papers processed: 3
- Questions extracted: X / 47
- Confidence scores: [High/Medium/Low]
- Issues: [None or list issues]
- Status: [PASS/FAIL]

## Test 2: Question Validator
- Questions validated: X / 47
- Valid: X
- Rejected: X (expected 5 bad questions)
- Flagged: X
- Rejection codes: [List codes]
- Status: [PASS/FAIL]

## Test 3: Question Bank Manager
- Questions added: X / 47
- Unique IDs generated: [Yes/No]
- Statistics accurate: [Yes/No]
- Index consistency: [Yes/No]
- Status: [PASS/FAIL]

## Test 4: End-to-End Pipeline
- Pipeline completed: [Yes/No]
- Errors encountered: [None or list]
- Final question count: X
- Status: [PASS/FAIL]

## Overall Result: [PASS/FAIL]

## Issues Found:
1. [Issue description]
2. [Issue description]

## Recommendations:
1. [Recommendation]
2. [Recommendation]
```

---

## Next Steps After Testing

Once all tests pass:

1. ✅ Mark tasks P2-013 to P2-036 as complete in TASKS.md
2. ✅ Update progress tracker (Testing phase complete)
3. ✅ Commit test results and sample data
4. Move to **Mass Processing** phase (P2-037 to P2-040)

---

## Notes for Real Papers

When you have access to real PSC past papers:

1. **Download papers** to Raw-Papers/ directories
2. **Run same tests** with real PDFs/HTML
3. **Expect lower extraction accuracy** (~80-90% vs 100% with clean text)
4. **More questions will be flagged** for manual review
5. **OCR errors** may reduce confidence scores for scanned PDFs

The sample papers simulate ideal conditions. Real papers will have:
- Formatting variations
- Scanned images requiring OCR
- Answer keys in different formats
- Potential missing answers

This is expected and why we have the Needs-Review/ workflow.
