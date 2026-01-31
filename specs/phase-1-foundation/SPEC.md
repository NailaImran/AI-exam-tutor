# Feature Specification: Exam Tutor Phase 1 - Foundation (Bronze Tier)

**Feature Branch**: `001-phase1-foundation`
**Created**: 2026-01-17
**Updated**: 2026-01-18
**Status**: Draft
**Input**: User description: "Create minimum viable tutoring system in Obsidian with vault structure, file watcher, question bank (150+ questions), student profiles, ERI calculation, and 5 core skills"

## Overview

Phase 1 establishes the minimum viable tutoring system for Pakistani competitive exam preparation (SPSC, PPSC, KPPSC). The foundation enables a complete question-answer-evaluate loop within an Obsidian vault, providing students with their first practice experience and baseline Exam Readiness Index (ERI) score.

### Scope Boundaries

**In Scope (Phase 1)**:
- Obsidian vault folder structure with Dashboard and Company Handbook
- File system watcher for /Inbox folder monitoring
- Question bank foundation with 150+ questions (50 per exam)
- Student profile system with profile, history, topic-stats, and ERI files
- Core skills: profile loader, question querier, answer evaluator, ERI calculator, performance tracker
- Basic performance tracking with session history

**Out of Scope (Later Phases)**:
- WhatsApp/Gmail/LinkedIn integration
- Adaptive test generation
- Odoo integration
- Leaderboard and gamification
- Payment tracking
- Study plan generator
- Shareable ERI badge
- Multi-student academy features

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete First Practice Test (Priority: P1)

A student new to competitive exam preparation wants to answer practice questions and see how they performed. They drop a test request into the Inbox folder, the file watcher detects it, questions are generated, they submit answers, and receive immediate feedback with their score and updated ERI.

**Why this priority**: This is the core value proposition - without a working question-answer-evaluate loop, the entire tutoring system has no value. Every subsequent feature depends on this foundation.

**Independent Test**: Can be fully tested by creating a test request file in /Inbox, having the watcher trigger question generation, submitting answers, and verifying evaluation results are saved to history.json and topic-stats.json.

**Acceptance Scenarios**:

1. **Given** a student with a valid profile, **When** they create a test-request.md file in /Inbox with exam type "PPSC", subject "Pakistan Studies", and 5 questions, **Then** the file watcher detects the file within 5 seconds and triggers question generation.

2. **Given** a valid test request, **When** the system generates a test file with questions, **Then** each question includes text, 4 options (A-D), and is drawn from the specified exam's question bank.

3. **Given** a test file with 5 questions, **When** the student fills in their answers and saves the file, **Then** the system evaluates the answers and produces a results file showing correct/incorrect for each question with explanations.

4. **Given** completed test evaluation, **When** the results are generated, **Then** the student's history.json and topic-stats.json are updated, and processed files move to /Done.

---

### User Story 2 - View Exam Readiness Score (Priority: P2)

A student wants to know their current readiness level for their target exam. After completing practice tests, they can view their ERI score on their Dashboard, which tells them where they stand on a 0-100 scale with a clear readiness band.

**Why this priority**: The ERI score is the key differentiator - it answers "Am I ready for this exam?" which provides actionable insight beyond raw scores. Requires at least one completed test (P1) to calculate.

**Independent Test**: Can be tested by completing a practice session and verifying Dashboard.md displays an updated ERI score with correct band classification and component breakdown.

**Acceptance Scenarios**:

1. **Given** a student who has completed at least one practice session, **When** they open Dashboard.md, **Then** they see their current ERI score (0-100), readiness band, and breakdown of all four components.

2. **Given** a student with no practice history, **When** they open Dashboard.md, **Then** they see "No ERI available - complete a practice test to calculate your readiness" with instructions.

3. **Given** a student who has completed multiple sessions, **When** the ERI is calculated, **Then** it uses the formula: (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15).

4. **Given** a calculated ERI score, **When** displayed, **Then** it shows the correct band: not_ready (0-20), developing (21-40), approaching (41-60), ready (61-80), or exam_ready (81-100).

---

### User Story 3 - Register as New Student (Priority: P3)

A person preparing for a provincial competitive exam wants to start using the tutoring system. They create their profile with name, email, target exam, and start date so the system can personalize their experience.

**Why this priority**: Student registration is necessary before any tutoring can happen, but it's a one-time setup activity. The system provides a template-based profile creation process.

**Independent Test**: Can be tested by creating a student folder with profile.json containing required fields and verifying the system initializes companion files (history.json, topic-stats.json, eri.json).

**Acceptance Scenarios**:

1. **Given** a new user, **When** they create a profile.json file in /Students/{student_id}/ with name, email, target_exam, and start_date, **Then** the system validates the profile and creates companion files (history.json, topic-stats.json, eri.json).

2. **Given** a profile with missing required fields, **When** the system attempts to load it, **Then** an error message indicates which fields are missing.

3. **Given** a valid student profile, **When** they open Dashboard.md, **Then** their name, target exam, and subscription tier are displayed.

---

### User Story 4 - Review Company Handbook (Priority: P4)

A student or administrator wants to understand how to use the Exam Tutor system. They access the Company Handbook to learn about available commands, folder structure, supported exams, behavioral rules, and ERI calculation methodology.

**Why this priority**: Documentation is essential for usability but has lower priority than core functionality.

**Independent Test**: Can be tested by verifying Company_Handbook.md exists and contains accurate documentation derived from the Constitution.

**Acceptance Scenarios**:

1. **Given** a new user, **When** they open Company_Handbook.md, **Then** they find clear instructions for creating their first test request.

2. **Given** a user curious about the ERI, **When** they read the Company Handbook, **Then** they understand the formula, component weights, and what each band means.

3. **Given** a user, **When** they read the Company Handbook, **Then** they see the behavioral rules from the Constitution (must always, must never).

---

### User Story 5 - File Watcher Processes Requests (Priority: P5)

The system automatically monitors the /Inbox folder and processes student requests without manual intervention. Valid requests trigger appropriate skills; invalid requests are routed to /Needs_Action with error documentation.

**Why this priority**: Automation is key to the "file-based" interaction model. Without the watcher, students would need manual intervention for each request.

**Independent Test**: Can be tested by dropping files into /Inbox and verifying they are processed, logged, and moved to appropriate folders.

**Acceptance Scenarios**:

1. **Given** a running file watcher, **When** a new .md file is created in /Inbox, **Then** the watcher detects it within 5 seconds.

2. **Given** a valid test-request.md file, **When** the watcher processes it, **Then** it parses the request, invokes appropriate skills, and moves the file to /Done.

3. **Given** an invalid or malformed request file, **When** the watcher attempts to process it, **Then** the file is moved to /Needs_Action with an accompanying error file explaining the issue.

4. **Given** any file processing event, **When** the watcher handles it, **Then** the event is logged to /Logs with timestamp, action, and outcome.

---

### Edge Cases

- What happens when a student requests more questions than available in the question bank for that topic?
  - System provides all available questions with a note indicating fewer than requested.

- How does the system handle malformed test request files (wrong format, missing fields)?
  - System moves file to /Needs_Action with an error description file explaining the issue.

- What happens if a student submits answers with invalid options (e.g., "E" instead of A-D)?
  - Invalid answers are marked as incorrect and flagged in the results.

- How does the system handle concurrent test requests from the same student?
  - Requests are queued and processed sequentially to prevent data corruption.

- What happens if the question bank is empty for the requested subject?
  - System returns an error message indicating no questions available for that subject.

- What happens if the file watcher is not running when files are added to /Inbox?
  - Files remain in /Inbox until the watcher starts and processes the backlog.

- How does the system handle a student profile that references a non-existent exam type?
  - System rejects the profile with an error indicating valid exam types: SPSC, PPSC, KPPSC.

---

## Requirements *(mandatory)*

> **Note**: Requirements use phase-prefixed IDs (P1-FR-XXX) to prevent collisions across phases.

### Functional Requirements

#### Vault Structure

- **P1-FR-001**: System MUST create and maintain Obsidian vault folder structure with: /inbox, /needs_action, /done, /students, /question-bank, /syllabus, /logs
- **P1-FR-002**: System MUST provide a Dashboard.md file at vault root displaying student overview, ERI score with component breakdown, and recent activity
- **P1-FR-003**: System MUST provide a Company_Handbook.md file at vault root documenting system usage and behavioral rules from Constitution

#### File Watcher

- **P1-FR-004**: System MUST monitor the /inbox folder for new and modified files
- **P1-FR-005**: System MUST detect new files in /inbox within 5 seconds of creation (polling interval: 2 seconds)
- **P1-FR-006**: System MUST parse test request files and route to appropriate skills
- **P1-FR-007**: System MUST move valid processed requests to /done upon completion
- **P1-FR-008**: System MUST move invalid or failed requests to /needs_action with error documentation
- **P1-FR-009**: System MUST log all watcher events to /logs with timestamp, action, and outcome

#### Question Bank

- **P1-FR-010**: System MUST store questions as JSON files organized by exam type, subject, and topic: /question-bank/{Exam}/{Subject}/{topic}.json
- **P1-FR-011**: System MUST support questions for three exam types: SPSC, PPSC, KPPSC
- **P1-FR-012**: Each question MUST include: unique ID, question text, four options (A-D), correct_answer, explanation, source, year, difficulty
- **P1-FR-013**: System MUST provide an initial question set of at least 50 questions per exam type (150 total minimum)
- **P1-FR-014**: Question IDs MUST follow format: {EXAM}-{SUBJECT_CODE}-{NNNNN} (e.g., PPSC-PK-00001)

#### Student Profile System

- **P1-FR-015**: System MUST store student data in /students/{student_id}/ folder
- **P1-FR-016**: System MUST maintain profile.json with: student_id, name, email, target_exam, start_date, subscription_tier, created_at, updated_at
- **P1-FR-017**: System MUST maintain history.json with: session array containing session_id, date, exam_type, questions_count, correct, accuracy, topics_covered
- **P1-FR-018**: System MUST maintain topic-stats.json with: per-topic accuracy, attempts, last_attempted, difficulty_breakdown, trend
- **P1-FR-019**: System MUST maintain eri.json with: current_score, band, component breakdown (accuracy, coverage, recency, consistency), last_calculated timestamp
- **P1-FR-020**: System MUST create companion files (history.json, topic-stats.json, eri.json) when a new profile is created

#### Core Skills

- **P1-FR-021**: student-profile-loader skill MUST read student profile from /students/{student_id}/profile.json and return profile object
- **P1-FR-022**: question-bank-querier skill MUST retrieve questions by exam type, subject, topic (optional), count, and difficulty and return questions array
- **P1-FR-023**: answer-evaluator skill MUST compare student answers to correct answers and return score with per-question feedback array including explanations (per Constitution MUST Always #2)
- **P1-FR-024**: exam-readiness-calculator skill MUST compute Exam Readiness Index using the formula: (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
- **P1-FR-025**: performance-tracker skill MUST persist session results to history.json, update topic-stats.json, and trigger ERI recalculation

#### ERI Calculation

- **P1-FR-026**: Accuracy component MUST be calculated as (Total Correct / Total Attempted) × 100
- **P1-FR-027**: Coverage component MUST be calculated as (Topics Practiced / Total Syllabus Topics) × 100
- **P1-FR-028**: Recency component MUST use decay function: 100 (0-3 days), 80 (4-7 days), 60 (8-14 days), 40 (15-30 days), 20 (31+ days)
- **P1-FR-029**: Consistency component MUST be based on standard deviation of last 10 session scores (or all if <10): SD<5=100, 5-10=80, 10-15=60, 15-20=40, >20=20
- **P1-FR-030**: ERI MUST be recalculated automatically after each completed session
- **P1-FR-031**: ERI bands MUST be: not_ready (0-20), developing (21-40), approaching (41-60), ready (61-80), exam_ready (81-100)

### Key Entities

- **Student Profile**: Represents a registered user with identification, target exam preference, subscription tier, and learning preferences. Links to all performance data.

- **Question**: A single MCQ item from the question bank. Contains question text, four answer options, correct answer, explanation, source metadata (exam, year), topic, and difficulty level. Questions are immutable once created.

- **Session**: A single practice test instance. Records which questions were presented, student's answers, correctness, and timing. Sessions are the atomic unit of practice.

- **ERI Score**: The Exam Readiness Index computed from cumulative performance. Ranges 0-100 with five interpretive bands. Stored in eri.json and recalculated after each session.

- **Topic Statistics**: Aggregated performance data per topic for a student. Tracks accuracy, attempt count, difficulty breakdown, trend, and last practice date. Used for ERI coverage calculation.

---

## Success Criteria *(mandatory)*

> **Note**: Success criteria use phase-prefixed IDs (P1-SC-XXX) for cross-reference clarity.

### Measurable Outcomes

- **P1-SC-001**: File watcher detects new files in /inbox within 5 seconds of creation
- **P1-SC-002**: Students can complete an end-to-end practice test (request → questions → answers → results) in under 5 minutes for a 5-question test
- **P1-SC-003**: Question bank contains at least 150 verified questions (50 per exam type)
- **P1-SC-004**: ERI calculation produces correct scores matching the documented formula when verified with test data
- **P1-SC-005**: 100% of student session data is persisted without loss or corruption to history.json and topic-stats.json
- **P1-SC-006**: All 5 core skills (student-profile-loader, question-bank-querier, answer-evaluator, exam-readiness-calculator, performance-tracker) pass input/output validation
- **P1-SC-007**: Dashboard.md displays current ERI score with component breakdown and recent activity for students with history
- **P1-SC-008**: System correctly categorizes student readiness into appropriate ERI bands
- **P1-SC-009**: New student onboarding (profile creation to first test completion) achievable in under 10 minutes
- **P1-SC-010**: Company Handbook accurately documents all system features and behavioral rules from Constitution

---

## Assumptions

1. **Obsidian as Primary Interface**: Students interact with the system through Obsidian's file explorer and markdown files. No other UI is required for Phase 1.

2. **Single Student per Vault**: Phase 1 assumes one primary student per vault instance. Multi-student management is deferred to later phases.

3. **Manual Profile Creation**: Students create their own profile.json file following documented templates. Guided wizards are out of scope.

4. **50 Questions Per Exam**: Initial question bank targets 50 questions each for SPSC, PPSC, and KPPSC, primarily in Pakistan Studies and General Knowledge subjects.

5. **Local File System**: All data is stored locally in the Obsidian vault. Cloud sync is handled by Obsidian's native capabilities if the user configures it.

6. **MCP Filesystem Server**: The system uses MCP filesystem tools for all file operations. The MCP server is assumed to be configured and running.

7. **JSON for Data, Markdown for Display**: Structured data uses JSON format. User-facing documents (Dashboard, results) use Markdown for readability.

8. **File Watcher Technology**: Watcher implementation uses Node.js chokidar or Python watchdog for cross-platform compatibility.

9. **Skills Follow SKILL.md Format**: All 5 core skills follow the established SKILL.md template format from the project structure.

---

## Appendix: ERI Calculation Details

### Formula

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

### Component Definitions

| Component   | Weight | Calculation                                          | Range |
| ----------- | ------ | ---------------------------------------------------- | ----- |
| Accuracy    | 40%    | (Total Correct / Total Attempted) × 100              | 0-100 |
| Coverage    | 25%    | (Topics Practiced / Total Syllabus Topics) × 100     | 0-100 |
| Recency     | 20%    | Decay function based on days since last practice     | 0-100 |
| Consistency | 15%    | Based on standard deviation of recent session scores | 0-100 |

### Recency Decay

| Days Since Last Practice | Recency Score |
| ------------------------ | ------------- |
| 0-3 days                 | 100           |
| 4-7 days                 | 80            |
| 8-14 days                | 60            |
| 15-30 days               | 40            |
| 31+ days                 | 20            |

### Consistency Scoring

| Score Standard Deviation | Consistency Score |
| ------------------------ | ----------------- |
| SD < 5                   | 100               |
| SD 5-10                  | 80                |
| SD 10-15                 | 60                |
| SD 15-20                 | 40                |
| SD > 20                  | 20                |

### ERI Bands

| Band        | Score Range | Interpretation                   |
| ----------- | ----------- | -------------------------------- |
| not_ready   | 0-20        | Significant preparation needed   |
| developing  | 21-40       | Building foundational knowledge  |
| approaching | 41-60       | Moderate readiness, gaps remain  |
| ready       | 61-80       | Good preparation level           |
| exam_ready  | 81-100      | Strong readiness for examination |

---

## Appendix: Vault Folder Structure

```
ExamTutor-Vault/
├── Dashboard.md              # Student home: ERI, recent sessions, quick actions
├── Company_Handbook.md       # System documentation and behavioral rules
│
├── Inbox/                    # Drop test requests here (watched folder)
│   └── test-request-{timestamp}.md
│
├── Needs_Action/             # Failed or invalid requests with error info
│
├── Done/                     # Successfully processed requests
│
├── Students/                 # Student data storage
│   └── {student_id}/
│       ├── profile.json      # Student profile
│       ├── history.json      # Session history
│       ├── topic-stats.json  # Topic-level performance
│       ├── eri.json          # ERI score and breakdown
│       └── sessions/         # Individual session details
│           └── {session_id}.json
│
├── Question-Bank/            # Exam questions organized by type
│   ├── SPSC/
│   │   └── {Subject}/
│   │       └── {topic}.json
│   ├── PPSC/
│   │   └── {Subject}/
│   │       └── {topic}.json
│   └── KPPSC/
│       └── {Subject}/
│           └── {topic}.json
│
├── Syllabus/                 # Exam syllabi and topic weights
│   ├── cross-exam-mapping.json
│   ├── SPSC/
│   ├── PPSC/
│   └── KPPSC/
│       ├── syllabus-structure.json
│       └── topic-weights.json
│
└── Logs/                     # Audit logs
    └── watcher/
        └── {date}.log
```

---

## Appendix: Test Request Format

Students create test requests as markdown files with the following structure:

```markdown
# Test Request

**Student ID**: STU-001
**Exam Type**: PPSC
**Subject**: Pakistan Studies
**Topic**: Constitutional Amendments (optional - if omitted, random topics)
**Difficulty**: medium (optional - easy/medium/hard/mixed)
**Question Count**: 5
```

The file watcher detects this file, validates the request, retrieves matching questions, and generates a test file for the student to complete.

---

## Appendix: Core Skills Summary

> **Naming Convention**: All skills use lowercase-with-hyphens format.

| Skill                      | Input                                     | Output                    | MCP Tools             | SKILL.md Location |
| -------------------------- | ----------------------------------------- | ------------------------- | --------------------- | ----------------- |
| student-profile-loader     | student_id                                | profile object            | read_file             | .claude/skills/exam-tutor/student-profile-loader/ |
| question-bank-querier      | exam, subject, count, difficulty          | questions array           | read_file, list_directory | .claude/skills/exam-tutor/question-bank-querier/ |
| answer-evaluator           | questions, student_answers                | score, feedback array with explanations | none (pure compute)   | .claude/skills/exam-tutor/answer-evaluator/ |
| exam-readiness-calculator  | student_id                                | eri object with breakdown | read_file             | .claude/skills/exam-tutor/exam-readiness-calculator/ |
| performance-tracker        | student_id, session_result                | updated stats             | read_file, write_file | .claude/skills/exam-tutor/performance-tracker/ |

**Note**: The skill previously named `eri-calculator` is now standardized to `exam-readiness-calculator` across all documentation.
