# Feature Specification: Phase 3 - Growth Engine

**Feature Branch**: `003-phase3-growth-engine`
**Created**: 2026-01-30
**Status**: Draft
**Tier**: Silver
**Dependencies**: Phase 1 (Foundation) + Phase 2 (Core Product) complete
**Constitution**: v1.1.0 (includes Phase 3 governance)

## Overview

Phase 3 transforms the Exam Tutor from a local practice tool into a multi-channel engagement platform with viral features. Students receive daily questions via WhatsApp, share achievements on LinkedIn, and follow personalized study plans with human oversight.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Daily WhatsApp Question Delivery (Priority: P1)

A student receives a daily practice question at 8 AM via WhatsApp, answers directly in the chat, receives immediate feedback with explanation, and sees their updated ERI score.

**Why this priority**: WhatsApp is the primary communication channel in Pakistan. Daily engagement via familiar messaging dramatically increases practice consistency and retention.

**Independent Test**: Can be fully tested by sending a test question to a registered phone number and verifying the response flow works end-to-end.

**Acceptance Scenarios**:

1. **Given** a student is registered with a valid WhatsApp number and has opted in to daily questions, **When** 8 AM local time arrives, **Then** the student receives a single MCQ question via WhatsApp with options A, B, C, D.

2. **Given** a student received a daily question, **When** they reply with their answer (e.g., "B"), **Then** the system evaluates the answer, sends feedback (correct/incorrect + explanation), and updates topic-stats.

3. **Given** a student answers the daily question, **When** the answer is processed, **Then** the student receives their updated ERI score in the response message.

4. **Given** a student has not responded to the daily question, **When** 24 hours pass, **Then** the question expires and the next day's question is sent (no queue buildup).

---

### User Story 2 - Personalized Study Plan with Approval (Priority: P2)

A student requests a study plan based on their weak areas. The system generates a draft plan, submits it for human review, and upon approval, the student receives their personalized schedule.

**Why this priority**: Study plans provide structured guidance that transforms sporadic practice into systematic preparation. Human approval ensures quality and prevents automated mistakes.

**Independent Test**: Can be tested by generating a study plan for a test student and verifying the approval workflow moves the plan from draft to active state.

**Acceptance Scenarios**:

1. **Given** a student has completed at least one diagnostic or 3 practice sessions, **When** they request a study plan, **Then** the system generates a draft plan based on weak areas and syllabus coverage.

2. **Given** a draft study plan is generated, **When** the system saves it, **Then** the plan is placed in needs_action/ folder with status "pending_approval".

3. **Given** a human reviewer approves the study plan, **When** approval is recorded, **Then** the plan status changes to "active" and the student is notified.

4. **Given** a human reviewer rejects the study plan, **When** rejection is recorded with feedback, **Then** the system generates a revised plan incorporating the feedback.

---

### User Story 3 - Progress Report Delivery (Priority: P2)

A student receives weekly progress reports summarizing their practice activity, ERI trends, weak areas, and recommendations for the coming week.

**Why this priority**: Regular progress visibility motivates continued engagement and helps students understand their preparation trajectory.

**Independent Test**: Can be tested by generating a weekly report for a student with practice history and verifying the report contains accurate statistics.

**Acceptance Scenarios**:

1. **Given** a student has practice history, **When** Sunday 6 PM arrives (or report is manually triggered), **Then** a progress report is generated with session count, accuracy trends, and ERI change.

2. **Given** a progress report is generated, **When** the student has opted into notifications, **Then** the report summary is sent via WhatsApp with a link to the full report.

3. **Given** a student's ERI has improved by 5+ points, **When** the report is generated, **Then** the improvement is highlighted with congratulations.

---

### User Story 4 - Shareable ERI Badge (Priority: P3)

A student generates a shareable badge displaying their ERI score and readiness band, which they can share on social media to showcase their preparation progress.

**Why this priority**: Viral sharing creates organic marketing and builds community among exam aspirants. Badges gamify progress and encourage continued practice.

**Independent Test**: Can be tested by generating a badge for a student and verifying the output is a valid image file with correct ERI information.

**Acceptance Scenarios**:

1. **Given** a student requests an ERI badge, **When** the badge is generated, **Then** it displays their current ERI score, readiness band, target exam type, and optional display name.

2. **Given** a badge is generated, **When** the student shares it, **Then** no personally identifiable information (email, phone, full name) is visible unless student explicitly consented.

3. **Given** a student's ERI reaches a milestone (e.g., 60, 80), **When** they achieve this, **Then** the system offers to generate a special milestone badge.

---

### User Story 5 - Daily LinkedIn Question Post (Priority: P3)

The system automatically posts a daily exam question to LinkedIn at 9 AM PKT, engaging the broader community and driving traffic to the platform.

**Why this priority**: LinkedIn posts establish thought leadership, attract new students, and create a daily touchpoint with the professional community preparing for government exams.

**Independent Test**: Can be tested by generating a draft LinkedIn post and verifying it contains a properly formatted question with hashtags.

**Acceptance Scenarios**:

1. **Given** it is 9 AM PKT, **When** the daily post scheduler runs, **Then** a draft post is created with today's question, 4 options, relevant hashtags, and submitted for approval.

2. **Given** a draft LinkedIn post is approved, **When** approval is recorded, **Then** the post is published to the configured LinkedIn page/profile.

3. **Given** a question was posted yesterday, **When** selecting today's question, **Then** a different subject is chosen (rotation to maintain variety).

4. **Given** the LinkedIn post requires approval, **When** 9 AM arrives, **Then** the draft is placed in needs_action/ with type "social_post" for human review.

---

### User Story 6 - Complete Test via WhatsApp (Priority: P4)

A student completes an entire practice test (5-10 questions) via WhatsApp conversation, receiving each question sequentially after answering the previous one.

**Why this priority**: Full test completion via WhatsApp enables practice without opening a separate app, meeting students where they already spend time.

**Independent Test**: Can be tested by starting a test session via WhatsApp and completing all questions through the chat interface.

**Acceptance Scenarios**:

1. **Given** a student sends "start test" to WhatsApp, **When** the message is received, **Then** an adaptive test is generated and the first question is sent.

2. **Given** a student answers a test question, **When** the answer is received, **Then** the next question is sent immediately (no explanation until test complete).

3. **Given** a student completes all test questions, **When** the final answer is received, **Then** the complete results are sent with per-question breakdown and updated ERI.

4. **Given** a student abandons a test mid-way, **When** 30 minutes of inactivity pass, **Then** the partial session is saved and can be resumed or discarded.

---

### Edge Cases

- What happens when WhatsApp API is unavailable? → Queue messages for retry with exponential backoff; notify admin after 3 failures
- What happens when a student's phone number changes? → Require re-verification via profile update
- What happens when LinkedIn API rate limits are hit? → Queue posts and retry; never post more than 1/day
- What happens when a study plan generation fails? → Return error to student with option to retry or contact support
- What happens when ERI badge generation fails? → Return text-based ERI summary as fallback
- What happens when scheduled messages overlap with student's quiet hours? → Respect student timezone and do-not-disturb preferences

## Requirements *(mandatory)*

### Functional Requirements

#### Stage 3A: Study Plans & Reports

- **FR-001**: System MUST generate personalized study plans based on weak areas, syllabus coverage, and target exam date
- **FR-002**: Study plans MUST include daily/weekly topic recommendations with estimated time per topic
- **FR-003**: Study plans MUST have status lifecycle: draft → pending_approval → active → completed
- **FR-004**: System MUST generate weekly progress reports with ERI trends, session counts, and accuracy by topic
- **FR-005**: Progress reports MUST be deliverable via WhatsApp summary and full markdown file

#### Stage 3B: WhatsApp Integration

- **FR-006**: System MUST send daily questions to opted-in students at their preferred time (default 8 AM local)
- **FR-007**: System MUST receive and process student answers via WhatsApp reply
- **FR-008**: System MUST send immediate feedback with correct answer explanation after each response
- **FR-009**: System MUST support full test sessions (5-10 questions) via WhatsApp conversation
- **FR-010**: System MUST update student progress data after each WhatsApp interaction

#### Stage 3C: Social Media & Viral Features

- **FR-011**: System MUST generate shareable ERI badges as image files with score, band, and exam type
- **FR-012**: ERI badges MUST NOT contain PII unless student explicitly consents
- **FR-013**: System MUST generate LinkedIn post drafts with questions, options, and relevant hashtags
- **FR-014**: System MUST rotate question subjects daily to maintain variety
- **FR-015**: Social media posts MUST require human approval before publication

#### Stage 3D: Human-in-the-Loop

- **FR-016**: Study plans MUST be placed in needs_action/ folder for human review before activation
- **FR-017**: LinkedIn posts MUST be placed in needs_action/ folder for human review before posting
- **FR-018**: System MUST log all approval/rejection decisions with reviewer identity and timestamp
- **FR-019**: System MUST support scheduled execution of daily tasks (questions, reports, posts)
- **FR-020**: Scheduled tasks MUST respect student timezone preferences

### Key Entities

- **StudyPlan**: Personalized preparation schedule with topics, dates, estimated times, and status (draft/pending/active/completed)
- **ProgressReport**: Weekly summary document with ERI history, session stats, topic breakdown, and recommendations
- **ERIBadge**: Shareable image with ERI score, readiness band, exam type, and optional display name
- **SocialPost**: LinkedIn post draft with question content, hashtags, scheduled time, and approval status
- **ScheduledTask**: Cron-like task definition with type, schedule, target student/global, and last execution time
- **MessageQueue**: Outbound messages pending delivery via WhatsApp with retry tracking

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Daily WhatsApp questions are delivered within 5 minutes of scheduled time for 95% of opted-in students
- **SC-002**: 80% of daily WhatsApp questions receive a response within 24 hours
- **SC-003**: Students can complete a full 10-question test via WhatsApp in under 15 minutes
- **SC-004**: Study plans are generated within 30 seconds of request
- **SC-005**: 90% of study plans pass human review on first submission
- **SC-006**: Weekly progress reports accurately reflect all practice sessions from the past 7 days
- **SC-007**: ERI badges are generated within 5 seconds of request
- **SC-008**: LinkedIn posts maintain daily schedule with 95% uptime (allowing for weekends/holidays skip)
- **SC-009**: All human approval requests are processed within 4 hours during business hours
- **SC-010**: Student engagement (sessions per week) increases by 30% after WhatsApp integration

## Assumptions

- Students have access to WhatsApp on their phones (>95% smartphone penetration in target demographic)
- WhatsApp Business API is available and configured with valid credentials
- LinkedIn API access is available for posting (personal or company page)
- Human reviewers are available during Pakistan business hours for approvals
- Students have provided valid phone numbers during registration
- Timezone information is available for each student (default: PKT)

## Dependencies

- Phase 1: Student profile system, question bank structure
- Phase 2: ERI calculator, weak area identifier, adaptive test generator, answer evaluator
- Constitution v1.1.0: Subagent authority, scheduled actions, privacy-first sharing rules
- External: WhatsApp Business API, LinkedIn API

## Out of Scope

- Voice messages or audio questions via WhatsApp
- Group WhatsApp chats or broadcast lists
- Twitter/X, Facebook, or Instagram integration
- Paid premium features or subscription management
- Multi-language support (Urdu localization deferred)
- Video content or explanatory lectures
- Real-time chat with human tutors
