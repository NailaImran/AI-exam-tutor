# Exam Tutor - Company Handbook

**Version**: 1.0.0
**Last Updated**: 2026-01-29
**System**: Digital FTE Competitive Exam Tutor

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Supported Exams](#supported-exams)
3. [Test Request Instructions](#test-request-instructions)
4. [ERI Calculation Documentation](#eri-calculation-documentation)
5. [Constitution & Behavioral Rules](#constitution--behavioral-rules)
6. [Skill Reference](#skill-reference)
7. [File Watcher & Automation](#file-watcher--automation)
8. [Troubleshooting](#troubleshooting)

---

## System Overview

The Exam Tutor is an AI-powered tutoring system designed to help students prepare for Pakistani provincial public service commission exams. The system provides:

- **Diagnostic Assessments** - Baseline tests to identify starting knowledge level
- **Adaptive Practice Tests** - Personalized tests focusing on weak areas
- **Progress Tracking** - Session-by-session performance monitoring
- **Exam Readiness Index (ERI)** - 0-100 score indicating exam preparedness
- **Weak Area Identification** - Automated detection of topics needing practice
- **Study Plan Generation** - Personalized study schedules

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EXAM TUTOR SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│  CORE SKILLS (6)           │  SUPPORTING SKILLS (4)        │
│  ├── student-profile-loader│  ├── diagnostic-generator     │
│  ├── question-bank-querier │  ├── adaptive-test-generator  │
│  ├── answer-evaluator      │  ├── study-plan-generator     │
│  ├── performance-tracker   │  └── progress-report-generator│
│  ├── exam-readiness-calc   │                               │
│  └── weak-area-identifier  │                               │
├─────────────────────────────────────────────────────────────┤
│  DATA LAYER                                                 │
│  ├── memory/students/      (Student profiles & history)    │
│  ├── question-bank/        (1,500+ MCQ questions)          │
│  ├── syllabus/             (Exam structures & weights)     │
│  └── logs/                 (Session & watcher logs)        │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Questions | 1,570+ |
| Supported Exams | 3 (SPSC, PPSC, KPPSC) |
| Subjects Covered | 7 |
| Core Skills | 6 |
| Supporting Skills | 4 |

---

## Supported Exams

| Exam | Full Name | Province | Question Count |
|------|-----------|----------|----------------|
| **SPSC** | Sindh Public Service Commission | Sindh | 450+ |
| **PPSC** | Punjab Public Service Commission | Punjab | 670+ |
| **KPPSC** | Khyber Pakhtunkhwa Public Service Commission | KPK | 450+ |

### Subjects Covered

1. **Pakistan Studies** - History, Geography, Constitution, Economy, Foreign Relations
2. **General Knowledge** - World Geography, Science, Famous Personalities, Organizations
3. **Current Affairs** - Pakistan events, International events, Sports, Awards
4. **English** - Grammar, Vocabulary, Comprehension, Sentence Correction
5. **Islamic Studies** - Basic Beliefs, Pillars, Prophet's Life, Islamic History
6. **Everyday Science** - Physics, Chemistry, Biology, Environment
7. **Computer Science** - Hardware, Software, Networking, MS Office

---

## Test Request Instructions

### How to Request a Practice Test

1. **Create a test request file** in the `inbox/` folder
2. **Name the file**: `test-request-{date}.md` (e.g., `test-request-2026-01-29.md`)
3. **Use the following format**:

```markdown
# Test Request

## Student Information
- **Student ID**: your-student-id
- **Name**: Your Name

## Test Configuration
- **Exam Type**: PPSC | SPSC | KPPSC
- **Test Type**: diagnostic | adaptive | timed
- **Question Count**: 10-50 (default: 25)
- **Subject Focus**: All | Pakistan Studies | General Knowledge | etc.

## Additional Options
- **Difficulty**: easy | medium | hard | mixed (default: mixed)
- **Time Limit**: none | 30min | 60min | 90min
- **Focus on Weak Areas**: yes | no (default: yes for adaptive)

## Notes
Any additional instructions or preferences.
```

### Test Types Explained

| Type | Purpose | Best For |
|------|---------|----------|
| `diagnostic` | Baseline assessment across all topics | New students, periodic re-assessment |
| `adaptive` | Focuses on weak areas | Daily practice after diagnosis |
| `timed` | Simulates exam conditions | Exam preparation, time management |

### Example Test Request

```markdown
# Test Request

## Student Information
- **Student ID**: ahmed-khan-001
- **Name**: Ahmed Khan

## Test Configuration
- **Exam Type**: PPSC
- **Test Type**: adaptive
- **Question Count**: 25
- **Subject Focus**: Pakistan Studies

## Additional Options
- **Difficulty**: mixed
- **Focus on Weak Areas**: yes
```

### After Submitting

1. The file watcher detects your request in `inbox/`
2. System processes and generates your test
3. File moves to `done/` (success) or `needs_action/` (issues)
4. Check `logs/watcher/` for processing details

---

## ERI Calculation Documentation

### What is ERI?

The **Exam Readiness Index (ERI)** is a composite score from 0-100 that indicates how prepared a student is for their target exam. It combines multiple factors to give a holistic view of readiness.

### ERI Formula

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

### Component Breakdown

#### 1. Accuracy (40% weight)

**What it measures**: How well you answer questions correctly.

**Calculation**:
```
For each practiced topic:
  weighted_accuracy += topic_accuracy × syllabus_weight

accuracy_score = weighted_accuracy / total_practiced_weight
```

**Example**: If you have 70% accuracy in Pakistan Studies (weight 0.20) and 80% in General Knowledge (weight 0.20):
```
weighted_accuracy = (70 × 0.20) + (80 × 0.20) = 14 + 16 = 30
total_weight = 0.40
accuracy_score = 30 / 0.40 = 75
```

#### 2. Coverage (25% weight)

**What it measures**: How much of the syllabus you have practiced.

**Calculation**:
```
coverage_score = (topics_practiced_with_5+_attempts / total_syllabus_topics) × 100
```

**Example**: If you've practiced 15 topics out of 30:
```
coverage_score = (15 / 30) × 100 = 50
```

#### 3. Recency (20% weight)

**What it measures**: How recently you have practiced (knowledge freshness).

**Calculation**:
```
For each session in last 30 days:
  days_ago = today - session_date
  decay_factor = 1 - (days_ago / 30) × 0.5
  recency_contribution += session_accuracy × decay_factor

recency_score = recency_contribution / session_count
```

**Decay factors**:
- Today: 1.0 (full credit)
- 15 days ago: 0.75
- 30 days ago: 0.50
- 30+ days: 0.50 (minimum)

#### 4. Consistency (15% weight)

**What it measures**: How regularly you practice.

**Calculation**:
```
expected_sessions = days_since_first_session / 2  (every other day)
actual_sessions = total_sessions

consistency_ratio = min(actual_sessions / expected_sessions, 1.0)
consistency_score = consistency_ratio × 100
```

### Readiness Bands

| Band | ERI Score | Description | Recommendation |
|------|-----------|-------------|----------------|
| **not_ready** | 0-20 | Significant preparation needed | Start with diagnostic, focus on basics |
| **developing** | 21-40 | Building foundational knowledge | Continue daily practice on weak areas |
| **approaching** | 41-60 | Moderate readiness, gaps remain | Increase coverage, maintain consistency |
| **ready** | 61-80 | Good preparation level | Focus on hard topics, timed practice |
| **exam_ready** | 81-100 | Strong readiness for examination | Review weak spots, maintain momentum |

### ERI Improvement Tips

| To Improve | Action |
|------------|--------|
| Accuracy | Focus on weak topics, review explanations |
| Coverage | Practice new topics, expand beyond comfort zone |
| Recency | Practice daily, don't take long breaks |
| Consistency | Set regular schedule, practice every other day minimum |

---

## Constitution & Behavioral Rules

### Core Principles

The Exam Tutor system operates under these fundamental principles:

#### 1. Accuracy First

> "Never compromise accuracy for speed or convenience. All information provided must be factually correct and verifiable."

- Questions are sourced from official past papers and verified sources
- Answers are validated before entering the question bank
- Explanations cite authoritative references

#### 2. Student-Centric

> "Every feature and decision prioritizes student learning outcomes."

- Adaptive tests focus on individual weak areas
- Progress tracking celebrates improvement
- Recommendations are personalized to learning style

#### 3. Data-Driven Decisions

> "Use performance data to guide recommendations, not assumptions."

- ERI formula uses weighted, measurable components
- Weak areas identified through statistical analysis
- Study plans based on actual performance trends

#### 4. Transparency

> "Students should understand how the system works and why recommendations are made."

- ERI components are fully explained
- Weak area severity scores are visible
- All calculations can be manually verified

#### 5. Continuous Improvement

> "The system and content improve based on feedback and results."

- Question bank regularly expanded
- Algorithm improvements based on outcomes
- User feedback incorporated into updates

### Behavioral Rules

#### DO:

- Provide accurate, verified information
- Explain the reasoning behind recommendations
- Encourage consistent practice habits
- Celebrate progress and improvements
- Respect student time and effort

#### DON'T:

- Guess answers or make up facts
- Provide discouraging feedback
- Overwhelm with too much content at once
- Ignore student preferences
- Share student data inappropriately

### Data Privacy

- Student data stored locally in `memory/students/`
- No external data transmission without consent
- Session logs retained for improvement purposes
- Students can request data deletion

---

## Skill Reference

### Core Skills

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| **student-profile-loader** | Load student context | student_id | Profile, history, stats |
| **question-bank-querier** | Retrieve questions | exam_type, filters | Question array |
| **answer-evaluator** | Grade responses | questions, answers | Score, breakdown |
| **performance-tracker** | Save results | session_data | Updated history |
| **exam-readiness-calculator** | Calculate ERI | student_id, exam_type | ERI score, components |
| **weak-area-identifier** | Find weak topics | student_id, exam_type | Weak/strong/untested lists |

### Supporting Skills

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| **diagnostic-assessment-generator** | Create baseline tests | exam_type | Full syllabus test |
| **adaptive-test-generator** | Create focused tests | student_id, weak_topics | Personalized test |
| **study-plan-generator** | Create study schedule | student_id, target_date | Weekly plan |
| **progress-report-generator** | Generate reports | student_id, date_range | Progress report |

### Skill Orchestration

**Daily Practice Flow**:
```
1. student-profile-loader    → Load context
2. weak-area-identifier      → Get weak areas
3. exam-readiness-calculator → Current ERI
4. adaptive-test-generator   → Generate test
5. [Student completes test]
6. answer-evaluator          → Evaluate
7. performance-tracker       → Save results
8. exam-readiness-calculator → Updated ERI
```

**New Student Onboarding**:
```
1. Create profile files
2. diagnostic-assessment-generator → Baseline test
3. [Student completes diagnostic]
4. answer-evaluator          → Evaluate
5. performance-tracker       → Initialize stats
6. exam-readiness-calculator → Baseline ERI
7. weak-area-identifier      → Initial weak areas
8. study-plan-generator      → Create plan
```

---

## File Watcher & Automation

### Overview

The file watcher monitors the `inbox/` folder for new test requests and processes them automatically.

### Monitored Paths

| Path | Purpose |
|------|---------|
| `inbox/` | Drop test requests here |
| `done/` | Successfully processed requests |
| `needs_action/` | Requests requiring manual intervention |
| `logs/watcher/` | Processing logs |

### File Watcher Behavior

1. **Detection**: Watches `inbox/` for new `.md` files
2. **Parsing**: Extracts request parameters from markdown format
3. **Validation**: Checks required fields and valid values
4. **Processing**: Executes appropriate skill chain
5. **Movement**: Moves file to `done/` or `needs_action/`
6. **Logging**: Records all actions to `logs/watcher/{date}.log`

### Request Parser Format

The parser expects markdown files with specific headers:

```markdown
# Test Request

## Student Information
- **Student ID**: required
- **Name**: optional

## Test Configuration
- **Exam Type**: PPSC | SPSC | KPPSC (required)
- **Test Type**: diagnostic | adaptive | timed (required)
- **Question Count**: integer (optional, default: 25)
```

### Log Format

Logs are written to `logs/watcher/YYYY-MM-DD.log`:

```
[2026-01-29T10:30:00Z] INFO: File detected: test-request-2026-01-29.md
[2026-01-29T10:30:01Z] INFO: Parsing request...
[2026-01-29T10:30:01Z] INFO: Student ID: ahmed-khan-001
[2026-01-29T10:30:01Z] INFO: Exam Type: PPSC
[2026-01-29T10:30:01Z] INFO: Test Type: adaptive
[2026-01-29T10:30:02Z] INFO: Generating test...
[2026-01-29T10:30:05Z] INFO: Test generated: 25 questions
[2026-01-29T10:30:05Z] INFO: Moving to done/
[2026-01-29T10:30:05Z] SUCCESS: Request processed successfully
```

### Error Handling

| Error | Action | Destination |
|-------|--------|-------------|
| Missing required field | Log error, skip processing | `needs_action/` |
| Invalid exam type | Log error, skip processing | `needs_action/` |
| Student not found | Create new profile, continue | `done/` |
| Insufficient questions | Log warning, generate partial | `done/` |
| System error | Log full error, alert | `needs_action/` |

---

## Troubleshooting

### Common Issues

#### "Student not found"

**Cause**: Student ID doesn't exist in `memory/students/`

**Solution**:
1. Check spelling of student_id
2. Create new student profile if needed
3. Ensure profile.json exists in student folder

#### "Insufficient questions for topic"

**Cause**: Question bank doesn't have enough questions for requested topic

**Solution**:
1. Reduce question count
2. Broaden subject focus
3. Request question bank expansion

#### "ERI not calculating"

**Cause**: Missing history or topic-stats files

**Solution**:
1. Complete at least one practice session
2. Ensure performance-tracker ran successfully
3. Check `memory/students/{id}/history.json` exists

#### "Test request stuck in inbox"

**Cause**: File watcher not running or parsing error

**Solution**:
1. Check `logs/watcher/` for errors
2. Verify request format matches template
3. Ensure all required fields present

### Getting Help

1. Check this handbook first
2. Review logs in `logs/` folder
3. Examine skill SKILL.md files for details
4. Contact system administrator

---

*Exam Tutor Company Handbook v1.0.0 - Last updated 2026-01-29*
