# Skill Orchestration Reference

This document describes how the parent agent should orchestrate the exam tutor skills.

## Skill Dependency Graph

```
                    ┌─────────────────────────┐
                    │  student-profile-loader │
                    └───────────┬─────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
┌───────────────────┐  ┌───────────────┐  ┌─────────────────┐
│ syllabus-mapper   │  │ weak-area-    │  │ exam-readiness- │
│ (optional)        │  │ identifier    │  │ calculator      │
└───────────────────┘  └───────┬───────┘  └────────┬────────┘
                               │                   │
                ┌──────────────┴──────────────┐    │
                │                             │    │
                ▼                             ▼    ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │ adaptive-test-      │      │ study-plan-         │
    │ generator           │      │ generator           │
    └──────────┬──────────┘      └─────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ question-bank-      │
    │ querier             │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ answer-evaluator    │
    │ (pure computation)  │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ performance-tracker │
    └──────────┬──────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌─────────────┐  ┌───────────────────┐
│ session-    │  │ progress-report-  │
│ logger      │  │ generator         │
└─────────────┘  └───────────────────┘
```

## Workflow Templates

### 1. New Student Onboarding

```yaml
workflow: new_student_onboarding
trigger: New student registration

steps:
  1. Create student profile
     - Write profile.json with initial data
     - Initialize empty history.json
     - Initialize empty topic-stats.json

  2. student-profile-loader
     - Verify profile was created correctly
     - Load for downstream skills

  3. diagnostic-assessment-generator
     - Generate initial diagnostic test
     - Cover full syllabus
     - assessment_type: "initial"

  4. [Student completes assessment]

  5. answer-evaluator
     - Evaluate diagnostic results
     - Generate topic_breakdown

  6. performance-tracker
     - Save first session data
     - Initialize topic-stats from results

  7. exam-readiness-calculator
     - Calculate initial ERI (baseline)

  8. weak-area-identifier
     - Identify initial weak areas
     - All untested topics will be flagged

  9. study-plan-generator
     - Generate personalized study plan
     - Based on weak areas and daily time

  10. session-logger (optional)
      - Log onboarding session

output: Student ready for daily practice
```

### 2. Daily Practice Session

```yaml
workflow: daily_practice_session
trigger: Student starts practice

steps:
  1. student-profile-loader
     - Load student context
     - Get exam_target, preferences

  2. weak-area-identifier
     - Get current weak areas
     - Prioritize by severity

  3. exam-readiness-calculator
     - Get current ERI
     - Determine session intensity

  4. adaptive-test-generator
     - Generate personalized test
     - Focus on weak areas (60%)
     - Include balanced coverage (40%)

  5. [Student completes test]

  6. answer-evaluator
     - Evaluate all answers
     - Calculate topic breakdown

  7. performance-tracker
     - Save session results
     - Update topic-stats
     - Update history

  8. exam-readiness-calculator
     - Recalculate ERI
     - Show improvement/decline

  9. weak-area-identifier
     - Update weak area list
     - Check for improvements

  10. session-logger (optional)
      - Log session events

output: Session complete, stats updated
```

### 3. Weekly Review

```yaml
workflow: weekly_review
trigger: End of week or on-demand

steps:
  1. student-profile-loader
     - Load student context

  2. exam-readiness-calculator
     - Get current ERI with components

  3. weak-area-identifier
     - Get current weak/strong/untested lists

  4. progress-report-generator
     - Generate weekly report
     - report_period_days: 7
     - include_recommendations: true

  5. study-plan-generator (if needed)
     - Regenerate plan if significant changes
     - Adjust based on progress

output: Weekly report generated
```

### 4. Exam Target Change

```yaml
workflow: exam_target_change
trigger: Student changes target exam (e.g., PPSC to SPSC)

steps:
  1. student-profile-loader
     - Load current profile

  2. syllabus-mapper
     - query_type: "cross_exam_map"
     - Map existing progress to new exam

  3. Update profile.json
     - Change exam_target
     - Note mapping confidence

  4. weak-area-identifier
     - Recalculate against new syllabus
     - Some topics may become untested

  5. exam-readiness-calculator
     - Recalculate ERI for new exam

  6. study-plan-generator
     - Generate new plan for new exam

output: Transition complete
```

### 5. Inbox Processing (Phase 1 On-Demand Polling)

```yaml
workflow: inbox_processor
trigger: On-demand polling of /inbox folder

steps:
  1. List inbox contents
     - Use mcp__filesystem__list_directory("inbox/")
     - Filter for .md files with test-request frontmatter

  2. For each request file:
     a. Parse frontmatter
        - Extract: student_id, exam_type, subject, question_count, difficulty

     b. Validate request
        - Check student_id exists in /students/{student_id}/
        - Check exam_type is valid (PPSC | SPSC | KPPSC)
        - Check question_count is reasonable (1-100)

     c. If INVALID:
        - Move file to /needs_action/
        - Create error companion file: {filename}.error.md
        - Log to logs/watcher/{date}.log
        - Continue to next file

     d. If VALID:
        - student-profile-loader: Load student context
        - question-bank-querier: Get questions matching criteria
        - Return questions to user for answering

  3. After answers received:
     - answer-evaluator: Score answers
     - performance-tracker: Save results
     - exam-readiness-calculator: Update ERI
     - Move original request to /done/
     - Create results companion file: {filename}.results.md
     - Log to logs/watcher/{date}.log

validation_rules:
  - student_id: must exist as directory
  - exam_type: PPSC | SPSC | KPPSC
  - subject: must match question-bank structure
  - question_count: integer 1-100, default 5
  - difficulty: easy | medium | hard | adaptive, default adaptive

error_handling:
  - Missing student_id: Move to needs_action, suggest creation
  - Invalid exam_type: Move to needs_action with valid options
  - No questions available: Move to needs_action, report availability
  - Parse error: Move to needs_action with format example

output: Processed files in /done/ or /needs_action/
```

## Error Handling Strategies

### Skill Failure Recovery

| Skill | Failure Impact | Recovery Strategy |
|-------|----------------|-------------------|
| student-profile-loader | Critical | Abort session, alert user |
| question-bank-querier | High | Reduce question count, warn |
| answer-evaluator | High | Retry, manual calculation fallback |
| performance-tracker | Medium | Queue for retry, continue session |
| exam-readiness-calculator | Low | Use last known ERI |
| weak-area-identifier | Low | Use previous weak areas |
| study-plan-generator | Low | Keep existing plan |
| progress-report-generator | Low | Skip report, notify user |
| session-logger | Very Low | Silent fail, log locally |
| syllabus-mapper | Low | Use direct syllabus query |

### Data Integrity Checks

Before each session:
1. Verify student profile exists and is valid
2. Verify history.json is parseable
3. Verify topic-stats.json is consistent
4. Verify question bank has sufficient questions

### Rollback Procedures

For failed writes:
1. Keep backup of previous state
2. Attempt atomic write
3. On failure, restore from backup
4. Log failure for debugging

## Parallelization Opportunities

### Safe to Run in Parallel

```
Group 1 (after profile load):
  - weak-area-identifier
  - exam-readiness-calculator
  - syllabus-mapper (if needed)

Group 2 (post-session):
  - session-logger
  - progress-report-generator (if scheduled)
```

### Must Run Sequentially

```
1. student-profile-loader (always first)
2. adaptive-test-generator (needs weak areas)
3. question-bank-querier (called by generator)
4. answer-evaluator (needs test completion)
5. performance-tracker (needs evaluation results)
```

## Caching Recommendations

### Cache Always (rarely changes)
- Syllabus structure
- Topic weights
- Cross-exam mappings

### Cache Per Session (changes per session)
- Student profile
- Recent question IDs (for exclusion)

### Never Cache (always fresh)
- History data
- Topic stats
- ERI calculations

---

# Phase 2: Question Bank Automation Workflows

## Skill Dependency Graph (Phase 2)

```
┌─────────────────────┐
│ past-paper-scraper  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ question-extractor  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ question-validator  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ question-bank-      │
│ manager             │
└─────────────────────┘
```

## Workflow Templates (Phase 2)

### 6. Mass Paper Import Pipeline

```yaml
workflow: mass_paper_import
trigger: Batch import of past papers to expand question bank

steps:
  1. past-paper-scraper
     input:
       exam_type: "PPSC"
       year_range: "2020-2023"
       subjects: ["Pakistan Studies", "General Knowledge", "Current Affairs", "English"]
     output:
       downloaded_files: List of paper paths in Raw-Papers/

  2. For each downloaded paper:
     a. question-extractor
        input:
          raw_paper_path: "Raw-Papers/PPSC/2023/pakistan-studies.pdf"
          exam_type: "PPSC"
          year: 2023
          subject: "Pakistan Studies"
        output:
          extracted_questions: Array of MCQ objects
          flagged_questions: Low-confidence extractions

     b. For each extracted_question:
        i. question-validator
           input:
             extracted_question: {...}
             exam_type: "PPSC"
             subject: "Pakistan Studies"
             year: 2023
           output:
             validation_result: VALID | REJECTED | FLAGGED
             validated_question: Enriched question object

        ii. If VALID:
            question-bank-manager
            input:
              action: "ADD"
              validated_question: {...}
              exam_type: "PPSC"
              subject: "Pakistan Studies"
            output:
              operation_result: Success confirmation with ID

        iii. If REJECTED:
             - Log rejection reason
             - Continue to next question

        iv. If FLAGGED:
            - Write to Needs-Review/
            - Optionally add to bank with flag
            - Log for manual review

  3. Log pipeline summary
     - Total papers processed
     - Total questions extracted
     - Total validated and added
     - Total flagged for review
     - Total rejected

output: Question bank expanded with validated questions
```

### 7. Single Paper Processing

```yaml
workflow: single_paper_import
trigger: Import questions from one past paper

steps:
  1. question-extractor
     input:
       raw_paper_path: "Raw-Papers/SPSC/2022/general-knowledge.pdf"
       exam_type: "SPSC"
       year: 2022
       subject: "General Knowledge"

  2. question-validator (batch)
     input:
       extracted_questions: Array from step 1
       exam_type: "SPSC"
       subject: "General Knowledge"
       year: 2022

  3. question-bank-manager (batch ADD)
     input:
       action: "ADD"
       validated_questions: Array from step 2
       exam_type: "SPSC"
       subject: "General Knowledge"

  4. Return summary
     - Questions added: count
     - Questions flagged: count
     - Questions rejected: count

output: Paper processed, questions imported
```

### 8. Manual Review Workflow

```yaml
workflow: manual_review_flagged
trigger: Review low-confidence questions in Needs-Review/

steps:
  1. List flagged questions
     - Read Needs-Review/{exam}/{date}/*.json
     - Sort by confidence_score (lowest first)

  2. For each flagged question:
     a. Display question with flagging reason
     b. Human reviewer corrects or confirms
     c. If corrected:
        - Update question object
        - Re-run question-validator
        - If now VALID, add via question-bank-manager
     d. If invalid:
        - Mark as permanently rejected
        - Move to /Needs-Review/rejected/

  3. Log review session
     - Questions reviewed: count
     - Questions added: count
     - Questions rejected: count

output: Flagged questions resolved
```

### 9. Duplicate Resolution

```yaml
workflow: resolve_cross_exam_duplicates
trigger: Same question appears across multiple exams

steps:
  1. question-validator detects duplicate
     - Question from SPSC matches existing PPSC question
     - Similarity score: 0.96

  2. question-bank-manager handles duplicate
     - Add question to SPSC bank (keep both)
     - Create cross-exam link in cross-exam-links.json
     - Link structure:
       {
         "link_id": "link-042",
         "question_ids": ["PPSC-PK-00124", "SPSC-PK-00089"],
         "similarity_score": 0.96
       }

  3. Update statistics
     - Increment both exam counters
     - Track cross-exam link

output: Duplicate tracked, both instances linked
```

## Error Handling Strategies (Phase 2)

### Skill Failure Recovery

| Skill | Failure Impact | Recovery Strategy |
|-------|----------------|-------------------|
| past-paper-scraper | Medium | Retry with exponential backoff, skip failed papers, continue |
| question-extractor | Medium | Log extraction failure, flag paper for manual extraction |
| question-validator | High | Log validation failure, reject question, continue pipeline |
| question-bank-manager | Critical | Rollback transaction, log error, halt pipeline |

### Rate Limiting Handling

```yaml
scenario: HTTP 429 (Too Many Requests)
response:
  1. Detect 429 status from past-paper-scraper
  2. Log rate limit event
  3. Wait for extended period (60 seconds)
  4. Retry with exponential backoff
  5. If persistent, switch to next source in priority list
```

### Extraction Failures

```yaml
scenario: PDF extraction returns 0 questions
response:
  1. Log extraction failure with file path
  2. Check if PDF is scanned image (OCR required)
  3. Flag paper for manual extraction
  4. Write to Needs-Review/{exam}/extraction-failed/
  5. Continue pipeline with next paper
```

### Validation Failures

```yaml
scenario: 30% of questions from paper are rejected
response:
  1. Log high rejection rate
  2. Flag paper for manual review
  3. Add successfully validated questions
  4. Create summary report of rejection reasons
  5. Write report to Needs-Review/{exam}/high-rejection/
```

## Parallelization Opportunities (Phase 2)

### Safe to Run in Parallel

```
Scraping (different exams):
  - past-paper-scraper(SPSC)
  - past-paper-scraper(PPSC)
  - past-paper-scraper(KPPSC)

Extraction (different papers):
  - question-extractor(paper1)
  - question-extractor(paper2)
  - question-extractor(paper3)

Validation (different questions):
  - question-validator(question1)
  - question-validator(question2)
  - question-validator(question3)
```

### Must Run Sequentially

```
1. past-paper-scraper (must complete before extraction)
2. question-extractor (must complete before validation)
3. question-validator (must complete before adding)
4. question-bank-manager (writes must be atomic)
```

## Data Integrity Checks (Phase 2)

### Pre-Pipeline Validation

```yaml
before_pipeline:
  1. Verify sources-registry.json exists and is valid
  2. Verify master-index.json exists and is writable
  3. Verify statistics.json exists and is consistent
  4. Verify Raw-Papers/ directories exist
  5. Verify Needs-Review/ directories exist
  6. Verify sufficient disk space (minimum 1GB recommended)
```

### Post-Pipeline Validation

```yaml
after_pipeline:
  1. Verify all questions have unique IDs
  2. Verify master-index.json matches question files
  3. Verify statistics.json counts match actual counts (within 1%)
  4. Verify all cross-exam links are bidirectional
  5. Verify no corrupt JSON files
  6. Generate pipeline completion report
```

## Rollback Procedures (Phase 2)

### Failed Question Import

```yaml
scenario: question-bank-manager write fails mid-batch
response:
  1. Identify last successful question ID
  2. Read master-index.json backup (pre-batch)
  3. Read statistics.json backup (pre-batch)
  4. Restore backups
  5. Remove partial question files
  6. Log rollback event
  7. Return error to caller
```

### Corrupted Index

```yaml
scenario: master-index.json becomes corrupted
response:
  1. Detect corruption (JSON parse error)
  2. Backup corrupted file with timestamp
  3. Rebuild master-index.json from question files
  4. Scan all topic files in question-bank/
  5. Collect all question IDs and metadata
  6. Generate new master-index.json
  7. Verify consistency
  8. Log rebuild event
```

## Logging Strategy (Phase 2)

### Scraper Logs

```
Location: Logs/scraper/{YYYY-MM-DD}.log
Format: Timestamp | Exam | Year | Subject | Source | Status | Details
Example: 2026-01-20T10:30:45Z | SPSC | 2023 | Pakistan Studies | spsc-official | SUCCESS | 2.4MB
```

### Pipeline Logs

```
Location: Logs/pipeline/{YYYY-MM-DD}.log
Format: Timestamp | Stage | Paper | Status | Questions | Details
Example: 2026-01-20T10:32:15Z | EXTRACT | PPSC-2023-PK | SUCCESS | 35 extracted | 32 high-conf, 3 flagged
```

### Validation Logs

```
Location: Logs/pipeline/{YYYY-MM-DD}.log
Format: Timestamp | VALIDATE | Question | Status | Reason
Example: 2026-01-20T10:35:22Z | VALIDATE | Q-042 | REJECTED | MISSING_OPTION_D
```

## Performance Targets (Phase 2)

| Operation | Target Performance |
|-----------|-------------------|
| Scrape 1 paper | < 10 seconds (including rate limit) |
| Extract from 1 PDF | < 30 seconds |
| Validate 1 question | < 100 milliseconds |
| Add 1 question to bank | < 200 milliseconds |
| Full pipeline (100 papers) | < 30 minutes |
| Rebuild master index | < 2 minutes (for 1500 questions) |

---

# Phase 3: Growth Engine Workflows

## Skill Dependency Graph (Phase 3)

```
                    ┌─────────────────────────┐
                    │  scheduled-task-runner  │
                    └───────────┬─────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
┌───────────────────┐  ┌───────────────────┐  ┌─────────────────────┐
│ daily-question-   │  │ progress-report-  │  │ social-post-        │
│ selector          │  │ generator         │  │ generator           │
└─────────┬─────────┘  └─────────┬─────────┘  └──────────┬──────────┘
          │                      │                        │
          ▼                      ▼                        ▼
┌───────────────────┐  ┌───────────────────┐  ┌─────────────────────┐
│ whatsapp-message- │  │ whatsapp-message- │  │ approval-workflow   │
│ sender            │  │ sender            │  │                     │
└─────────┬─────────┘  └───────────────────┘  └──────────┬──────────┘
          │                                              │
          ▼                                              ▼
┌───────────────────┐                        ┌─────────────────────┐
│ answer-evaluator  │                        │ LinkedIn MCP        │
└─────────┬─────────┘                        └─────────────────────┘
          │
          ▼
┌───────────────────┐
│ performance-      │
│ tracker           │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐      ┌───────────────────┐
│ exam-readiness-   │─────►│ eri-badge-        │
│ calculator        │      │ generator         │
└───────────────────┘      └───────────────────┘
```

## Workflow Templates (Phase 3)

### 10. Daily WhatsApp Question Delivery

```yaml
workflow: daily_whatsapp_question
trigger: Scheduled task at 8 AM PKT (schedules/daily-questions.json)

steps:
  1. scheduled-task-runner
     - Check if enabled
     - Check if current time matches schedule
     - Get list of opted-in students

  2. For each opted-in student:
     a. student-profile-loader
        - Load student context
        - Verify WhatsApp opt-in

     b. daily-question-selector
        input:
          exam_type: student.exam_target
          mode: "student"
          student_id: student.student_id
        output:
          question: Selected question with rotation

     c. whatsapp-message-sender
        input:
          phone_number: student.whatsapp.phone_number
          message_type: "daily_question"
          content:
            question: {...}
            student: {current_eri: ...}
        output:
          message_id: Sent message ID

  3. [Student replies with A/B/C/D]

  4. answer-evaluator
     input:
       question_id: sent_question.id
       student_answer: reply.text
     output:
       is_correct: boolean
       explanation: string

  5. performance-tracker
     input:
       student_id: student.student_id
       session_type: "daily_question"
       results: [evaluation_result]

  6. exam-readiness-calculator
     input:
       student_id: student.student_id
     output:
       previous_score: number
       current_score: number
       milestone_crossed: boolean

  7. whatsapp-message-sender
     - Send feedback (correct or incorrect)
     - Include updated ERI

  8. If milestone_crossed:
     - Send milestone_badge notification
     - Offer shareable badge

output: Daily question delivered, answered, and tracked
```

### 11. WhatsApp Test Session

```yaml
workflow: whatsapp_test_session
trigger: Student sends "start test" via WhatsApp

steps:
  1. whatsapp-message-sender (incoming handler)
     - Detect "start test" intent
     - Load/create session state

  2. Check for active test
     - If exists and not timed out: resume
     - If exists and timed out: abandon
     - If none: create new

  3. adaptive-test-generator
     input:
       student_id: student.student_id
       exam_type: student.exam_target
       question_count: 5
       difficulty: "adaptive"
     output:
       test_id: string
       questions: array

  4. Initialize session state
     - Save to whatsapp-session.json
     - Set timeout_at (30 minutes)

  5. whatsapp-message-sender
     - Send test_start with first question

  6. Answer loop (5 iterations):
     a. [Student replies A/B/C/D]
     b. Record answer in session state
     c. If more questions: send test_next_question
     d. If complete: proceed to step 7

  7. Batch evaluation
     - answer-evaluator for all questions
     - Calculate correct count and accuracy

  8. performance-tracker
     - Save complete session

  9. exam-readiness-calculator
     - Update ERI

  10. whatsapp-message-sender
      - Send test_complete with results
      - Include per-question breakdown

  11. Clear session state

  12. If milestone crossed:
      - Offer badge

output: Test completed via WhatsApp conversation
```

### 12. Study Plan Generation with Approval

```yaml
workflow: study_plan_with_approval
trigger: study-strategy-planner subagent invoked

steps:
  1. student-profile-loader
     - Load student context

  2. weak-area-identifier
     input:
       student_id: student.student_id
     output:
       weak_areas: [{topic, severity_score, accuracy}]

  3. study-plan-generator
     input:
       student_id: student.student_id
       exam_type: student.exam_target
       target_exam_date: student.target_exam_date
       daily_time_minutes: student.preferences.daily_time_minutes
       weak_areas: from step 2
     output:
       plan: StudyPlan JSON
       draft_path: memory path

  4. Copy plan to approval queue
     - Write to needs_action/study-plans/{student_id}-plan-{date}.json
     - Set status: "pending_approval"

  5. [Human reviews plan in needs_action/]

  6. If approved:
     a. approval-workflow
        input:
          action_type: "study_plan"
          item_id: plan filename
          decision: "approve"
          reviewer: reviewer ID
        output:
          - Move to done/
          - Copy to active-plan.json
          - status: "active"

     b. whatsapp-message-sender
        - Send study_plan_approved notification

  7. If rejected:
     a. approval-workflow
        input:
          action_type: "study_plan"
          decision: "reject"
          feedback: "reason for rejection"
        output:
          - Move to done/
          - status: "rejected"

output: Study plan approved and activated, or rejected with feedback
```

### 13. LinkedIn Post Generation with Approval

```yaml
workflow: linkedin_post_generation
trigger: Scheduled task at 9 AM PKT (schedules/linkedin-posts.json)

steps:
  1. scheduled-task-runner
     - Check if enabled
     - Check if post already exists for today

  2. Load rotation tracking
     - Read schedules/linkedin-rotation.json
     - Get last_topics, last_questions, last_exam_types

  3. daily-question-selector
     input:
       exam_type: rotate_exam_type()
       mode: "linkedin"
       excluded_topics: last_topics[0:3]
       excluded_ids: last_questions[0:30]
     output:
       question: Selected question

  4. social-post-generator
     input:
       exam_type: selected exam
       excluded_question_ids: last_questions
     output:
       post: SocialPost JSON
       character_count: number

  5. Validate post
     - Ensure <= 3000 characters
     - Ensure <= 5 hashtags

  6. Save to approval queue
     - Write to needs_action/social-posts/linkedin-{date}.json
     - Set status: "pending_approval"

  7. [Human reviews post in needs_action/]

  8. If approved:
     a. approval-workflow
        input:
          action_type: "social_post"
          item_id: post filename
          decision: "approve"
        output:
          - Publish via LinkedIn MCP
          - Set published_at
          - Move to done/

  9. If rejected:
     a. approval-workflow
        input:
          decision: "reject"
          feedback: "reason"
        output:
          - Move to done/
          - status: "rejected"

  10. Update rotation tracking
      - Add topic to last_topics
      - Add question_id to last_questions

output: Post published to LinkedIn, or rejected with feedback
```

### 14. Weekly Progress Report

```yaml
workflow: weekly_progress_report
trigger: Scheduled task on Sundays (schedules/weekly-reports.json)

steps:
  1. scheduled-task-runner
     - Get list of active students

  2. For each student with opted_in_reports:
     a. progress-report-generator
        input:
          student_id: student.student_id
          period_start: 7 days ago
          period_end: today
        output:
          report_path: markdown file
          metadata_path: JSON file
          summary: {eri_start, eri_end, eri_change, ...}

     b. If eri_change >= 5:
        - Add congratulations to report

     c. whatsapp-message-sender
        input:
          message_type: "weekly_report_summary"
          content:
            report: summary data
            report_link: path to full report

output: Weekly reports generated and delivered
```

### 15. ERI Badge Generation

```yaml
workflow: eri_badge_generation
trigger: Student requests badge OR milestone reached

steps:
  1. student-profile-loader
     - Load profile with sharing_consent

  2. Check consent
     - If !allow_badge_sharing: return error

  3. Load ERI data
     - Read eri.json
     - Get current_score, band

  4. eri-badge-generator
     input:
       student_id: student.student_id
       include_display_name: true
     output:
       badge_path: SVG file
       badge_metadata: JSON with milestone info

  5. If milestone detected:
     - Set is_milestone: true
     - Set milestone_type

  6. whatsapp-message-sender (if triggered by badge request)
     - Send badge image
     - Include sharing instructions

output: Badge generated and optionally delivered
```

## Error Handling Strategies (Phase 3)

### Skill Failure Recovery

| Skill | Failure Impact | Recovery Strategy |
|-------|----------------|-------------------|
| scheduled-task-runner | Medium | Log, retry next interval |
| daily-question-selector | Low | Use random question |
| whatsapp-message-sender | High | Queue for retry (3 attempts) |
| approval-workflow | Medium | Leave in needs_action, alert |
| social-post-generator | Low | Skip today's post |
| eri-badge-generator | Low | Notify user of failure |

### WhatsApp Delivery Failures

```yaml
scenario: WhatsApp API unavailable
response:
  1. Queue message in queue/whatsapp/
  2. Set status: "pending"
  3. Retry with exponential backoff (5m, 15m, 60m)
  4. After 3 failures: mark as failed, notify admin
```

### Approval Queue Stuck

```yaml
scenario: Items in needs_action/ for > 24 hours
response:
  1. Detect aged items
  2. Send reminder notification
  3. If social post: skip (post was time-sensitive)
  4. If study plan: keep waiting
```

## Subagent Authority Matrix

Per Constitution v1.1.0:

| Subagent | Autonomous Actions | Requires Approval |
|----------|-------------------|-------------------|
| study-strategy-planner | Load data, generate plans | Activate study plan |
| progress-reporting-coordinator | Generate reports, send notifications | None |
| social-media-coordinator | Select questions, format posts | Publish to LinkedIn |

## Performance Targets (Phase 3)

| Operation | Target Performance |
|-----------|-------------------|
| Daily question delivery | < 5 seconds per student |
| WhatsApp test session | < 2 seconds per question |
| Study plan generation | < 10 seconds |
| Progress report generation | < 5 seconds |
| Badge generation | < 2 seconds |
| LinkedIn post generation | < 3 seconds |
