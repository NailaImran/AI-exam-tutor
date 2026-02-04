# AI Exam Tutor - Master Plan

> Digital FTE Competitive Exam Tutor for Pakistani Provincial Public Service Commission Exams

## Vision

A fully autonomous, deeply personalized exam coach that proactively manages a student's entire preparation journey for SPSC, PPSC, and KPPSC competitive exams.

---

## Phase Overview

| Phase | Name | Status | Focus |
|-------|------|--------|-------|
| 1 | Foundation | Complete | Vault structure, core skills, basic Q&A |
| 2 | Question Bank | Complete | 1500+ questions, ERI calculation, diagnostics |
| 3 | Growth Engine | Complete | WhatsApp, study plans, social media, engagement |
| 4 | Autonomous Coach | In Progress | Full autonomy, mock exams, predictive coaching |

---

## Phase 1: Foundation (Complete)

### Goal
Establish the foundational infrastructure and core skills for the tutoring system.

### Deliverables
- Project structure with memory/, question-bank/, syllabus/ directories
- MCP filesystem integration
- 4 core skills: student-profile-loader, question-bank-querier, answer-evaluator, performance-tracker
- Basic Q&A loop functionality

### Skills Delivered
| Skill | Category | Purpose |
|-------|----------|---------|
| student-profile-loader | CORE | Load student context from memory |
| question-bank-querier | CORE | Retrieve questions by criteria |
| answer-evaluator | CORE | Evaluate responses (pure computation) |
| performance-tracker | CORE | Persist results to memory |

---

## Phase 2: Question Bank (Complete)

### Goal
Build comprehensive question bank and implement intelligent assessment capabilities.

### Deliverables
- 1500+ questions across SPSC/PPSC/KPPSC
- Exam Readiness Index (ERI) calculation
- Weak area identification
- Diagnostic and adaptive test generation

### Skills Delivered
| Skill | Category | Purpose |
|-------|----------|---------|
| exam-readiness-calculator | CORE | Calculate ERI (0-100) |
| weak-area-identifier | CORE | Find topics needing practice |
| diagnostic-assessment-generator | SUPPORTING | Create baseline tests |
| adaptive-test-generator | SUPPORTING | Generate personalized tests |

### Subagents Delivered
| Subagent | Purpose |
|----------|---------|
| assessment-examiner | Evaluate MCQs, calculate ERI, identify weak areas |

---

## Phase 3: Growth Engine (Complete)

### Goal
Enable student engagement through WhatsApp, study planning, and social media presence.

### Deliverables
- WhatsApp integration for daily questions and test sessions
- Study plan generation with approval workflow
- Progress reporting
- LinkedIn post generation for marketing
- ERI badge generation

### Skills Delivered
| Skill | Category | Purpose |
|-------|----------|---------|
| study-plan-generator | SUPPORTING | Create study schedules |
| progress-report-generator | SUPPORTING | Generate progress reports |
| whatsapp-message-sender | ENGAGEMENT | WhatsApp messaging & test sessions |
| daily-question-selector | ENGAGEMENT | Select daily questions with rotation |
| scheduled-task-runner | ENGAGEMENT | Cron-like task execution |
| approval-workflow | ENGAGEMENT | Human-in-the-loop approvals |
| eri-badge-generator | ENGAGEMENT | Generate shareable ERI badges |
| social-post-generator | ENGAGEMENT | LinkedIn post generation |

### Subagents Delivered
| Subagent | Purpose |
|----------|---------|
| study-strategy-planner | Orchestrate study plan creation with approval |
| progress-reporting-coordinator | Weekly report generation and delivery |
| social-media-coordinator | LinkedIn post workflow with approval |

---

## Phase 4: Autonomous Coach (In Progress)

### Goal
Transform the tutor into a fully autonomous Digital FTE that proactively manages the student's entire preparation journey without manual intervention.

### Design Principles
| Principle | Description |
|-----------|-------------|
| Single Student Focus | All features serve one student's journey |
| Proactive Autonomy | System initiates, not just responds |
| Deep Personalization | Learns and adapts to individual patterns |
| Exam Simulation Fidelity | Authentic practice under real conditions |
| Zero Manual Intervention | Self-managing preparation lifecycle |

### Deliverables
| ID | Deliverable | Status | Purpose |
|----|-------------|--------|---------|
| D4.1 | Mock Exam Engine | Complete | Full-length timed exams matching real format |
| D4.2 | Deep Diagnostic Analyzer | Complete | Root-cause analysis of weak areas |
| D4.3 | Learning Pattern Detector | Complete | Identify optimal study times/methods |
| D4.4 | Autonomous Session Manager | Complete | Proactive session initiation |
| D4.5 | Knowledge Gap Predictor | Complete | Anticipate weaknesses before they manifest |
| D4.6 | Revision Cycle Engine | Complete | Spaced repetition with forgetting curve |
| D4.7 | Exam Countdown Intelligence | Complete | Smart urgency calibration |
| D4.8 | Cross-Exam Syllabus Mapper | Complete | Topic equivalence across SPSC/PPSC/KPPSC |

### Skills Implemented
| Skill | Category | Status | Purpose |
|-------|----------|--------|---------|
| session-logger | CORE | Complete | Audit trail for all interactions |
| syllabus-mapper | CORE | Complete | Cross-exam topic mapping |
| mock-exam-generator | MASTERY | Complete | Full timed mock exams |
| mock-exam-evaluator | MASTERY | Complete | Comprehensive mock scoring |
| exam-pressure-simulator | MASTERY | Complete | Add time pressure simulation |
| deep-dive-analyzer | INTELLIGENCE | Complete | Root-cause weak area analysis |
| learning-pattern-detector | INTELLIGENCE | Complete | Identify optimal study patterns |
| knowledge-gap-predictor | INTELLIGENCE | Complete | Predict future weak areas |
| forgetting-curve-tracker | INTELLIGENCE | Complete | Track knowledge decay |
| autonomous-session-initiator | AUTONOMY | Complete | Proactive session triggers |
| study-pattern-optimizer | AUTONOMY | Complete | Optimize study schedule |
| revision-cycle-manager | AUTONOMY | Complete | Spaced repetition management |
| exam-countdown-calibrator | AUTONOMY | Complete | Smart urgency adjustment |
| motivation-monitor | AUTONOMY | Complete | Engagement tracking |

### Subagents Implemented
| Subagent | Status | Purpose |
|----------|--------|---------|
| autonomous-coach-coordinator | Complete | Master orchestrator for proactive coaching |
| mock-exam-conductor | Complete | End-to-end mock exam management |
| deep-diagnostic-analyst | Complete | Comprehensive weakness analysis |

### Success Metrics
| Metric | Target |
|--------|--------|
| Proactive session acceptance | >60% |
| Prediction accuracy | >75% |
| Mock-to-real correlation | >0.85 |
| Revision compliance | >70% |
| Zero-touch days | >80% |

### Non-Goals (Explicitly Excluded)
- B2B / Academy / Institution features
- Multi-student dashboards
- Payment or subscription management
- Parent/guardian portals
- Business analytics
- SaaS infrastructure
- User authentication systems

---

## Architecture Summary

### Total Skills by Phase
| Phase | CORE | SUPPORTING | ENGAGEMENT | MASTERY | INTELLIGENCE | AUTONOMY | Total |
|-------|------|------------|------------|---------|--------------|----------|-------|
| 1 | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| 2 | 2 | 2 | 0 | 0 | 0 | 0 | 4 |
| 3 | 0 | 2 | 6 | 0 | 0 | 0 | 8 |
| 4 | 2 | 0 | 0 | 3 | 4 | 5 | 14 |
| **Total** | **8** | **4** | **6** | **3** | **4** | **5** | **30** |

### Total Subagents by Phase
| Phase | Count | Subagents |
|-------|-------|-----------|
| 2 | 1 | assessment-examiner |
| 3 | 3 | study-strategy-planner, progress-reporting-coordinator, social-media-coordinator |
| 4 | 3 | autonomous-coach-coordinator, mock-exam-conductor, deep-diagnostic-analyst |
| **Total** | **7** | |

### MCP Integrations
| Server | Phase | Purpose |
|--------|-------|---------|
| filesystem | 1+ | Core data persistence |
| github | 1+ | Version control |
| context7 | 1+ | Documentation lookup |
| whatsapp | 3+ | Student communication |
| linkedin | 3 | Social media posts |

---

## Key Workflows

### Daily Practice (Phase 1-2)
```
student-profile-loader → weak-area-identifier → exam-readiness-calculator →
adaptive-test-generator → [Student] → answer-evaluator → performance-tracker
```

### WhatsApp Engagement (Phase 3)
```
scheduled-task-runner → daily-question-selector → whatsapp-message-sender →
[Student] → answer-evaluator → performance-tracker → whatsapp-message-sender
```

### Autonomous Coaching (Phase 4)
```
autonomous-session-initiator → learning-pattern-detector → motivation-monitor →
revision-cycle-manager → knowledge-gap-predictor → [Personalized Session] →
whatsapp-message-sender
```

### Full Mock Exam (Phase 4)
```
mock-exam-generator → exam-pressure-simulator → [Student] → mock-exam-evaluator →
deep-dive-analyzer → study-plan-generator → exam-countdown-calibrator
```

---

## File References

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project rules and skill inventory |
| `MASTER_PLAN.md` | This file - overall roadmap |
| `TASKS-ARCHIVE.md` | Completed task history |
| `specs/phase-{n}-*/spec.md` | Phase specifications |
| `.claude/skills/exam-tutor/SKILL.md` | Skill bundle documentation |
