# MASTER PLAN: Exam Tutor

> **Digital FTE for Pakistani Competitive Exam Preparation**
>
> **Hackathon:** Dec 7, 2025 - Jan 18, 2026
> **Stack:** Obsidian Vault + Claude Code + MCP Servers
> **Approach:** Spec-driven development, all AI as Agent Skills

---

## 1. Vision & Value Proposition

### The Problem

**For Students:**
- 500,000+ candidates compete for ~5,000 government jobs annually in Pakistan
- Scattered preparation resources, no personalized feedback
- No objective measure of "Am I ready for this exam?"
- Inconsistent practice, cramming before exams

**For Academies:**
- Manual test creation and grading
- No visibility into individual student progress
- High instructor-to-student ratios
- Paper-based systems don't scale

**For the Market:**
- No dominant digital platform for provincial PSC exams
- Existing solutions focus on CSS/PMS, ignore SPSC/PPSC/KPPSC
- WhatsApp groups are chaotic, not structured learning

### The Solution: Exam Tutor

A **Digital Full-Time Employee** that serves as personal exam coach, academy assistant, and business operator.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            EXAM TUTOR                                   │
│              "Your AI-Powered Competitive Exam Coach"                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   STUDENTS              ACADEMIES              BUSINESS                 │
│   ────────              ─────────              ────────                 │
│   • ERI Score           • Multi-Student        • Payment Tracking      │
│   • Adaptive Tests        Dashboard            • Subscriptions         │
│   • Study Plans         • Batch Testing        • Auto-Renewals         │
│   • WhatsApp Bot        • Performance          • Weekly Reports        │
│   • Leaderboards          Comparison           • Growth Analytics      │
│   • Social Badges       • Parent Reports                               │
│                         • White-Label                                  │
│                                                                         │
│                    ┌─────────────────────┐                             │
│                    │  EXAM READINESS     │                             │
│                    │  INDEX (ERI)        │                             │
│                    │  ═══════════════    │                             │
│                    │       78/100        │                             │
│                    │      "READY"        │                             │
│                    └─────────────────────┘                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Exam Readiness Index (ERI)

The core metric that answers: **"Am I ready for this exam?"**

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

| Band | Score | Meaning | Predicted Outcome |
|------|-------|---------|-------------------|
| `not_ready` | 0-20 | Significant prep needed | Unlikely to pass |
| `developing` | 21-40 | Building foundations | Below cutoff |
| `approaching` | 41-60 | Moderate readiness | Borderline |
| `ready` | 61-80 | Good preparation | Likely to pass |
| `exam_ready` | 81-100 | Strong readiness | Top percentile |

### Unique Value Propositions

| Stakeholder | Value |
|-------------|-------|
| **Students** | Know exactly where you stand, what to study, when you're ready |
| **Working Professionals** | Efficient plans for limited time |
| **Academies** | Scale instruction without hiring, track every student |
| **Parents** | Automatic progress reports, no more guessing |

---

## 2. Target Market & Pricing Tiers

### Market Sizing

| Exam | Annual Candidates | Digital Adoption | Target Market |
|------|-------------------|------------------|---------------|
| PPSC | 300,000+ | 40% | 120,000 |
| SPSC | 100,000+ | 30% | 30,000 |
| KPPSC | 80,000+ | 35% | 28,000 |
| **Total** | **480,000+** | - | **178,000** |

### Customer Segments

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       CUSTOMER SEGMENTS                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  B2C STUDENTS                          B2B ACADEMIES                    │
│  ─────────────                         ─────────────                    │
│                                                                         │
│  ┌───────────┐  ┌───────────┐         ┌───────────────────────────┐   │
│  │   FREE    │  │  PREMIUM  │         │      ACADEMY PLANS        │   │
│  │           │  │           │         │                           │   │
│  │ • 5 Q/day │  │ • Unlim Q │         │ Starter   Pro    Enterprise│   │
│  │ • ERI     │  │ • Full    │         │ 50 std   200 std  Unlimited│   │
│  │ • Basic   │  │   Mocks   │         │                           │   │
│  │   Stats   │  │ • AI Plan │         │ Multi-student dashboard   │   │
│  │           │  │ • Deep    │         │ Batch testing             │   │
│  │ ───────── │  │   Dive    │         │ Performance comparison    │   │
│  │ WhatsApp  │  │           │         │ Parent reports            │   │
│  │ hook for  │  │ Rs 499/mo │         │ White-label (Enterprise)  │   │
│  │ upgrade   │  │           │         │                           │   │
│  └───────────┘  └───────────┘         └───────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Pricing Structure

#### B2C - Individual Students

| Tier | Price | Features |
|------|-------|----------|
| **Free** | Rs 0 | 5 questions/day, ERI tracking, basic stats, WhatsApp daily question |
| **Basic** | Rs 199/mo | 50 questions/day, weekly reports, study plan suggestions |
| **Premium** | Rs 499/mo | Unlimited questions, full mock exams, AI study plans, weak area deep dive |
| **Exam Pack** | Rs 999 one-time | Previous 5 years papers, topic-wise breakdown, unlimited for 3 months |

#### B2B - Academies

| Tier | Price | Students | Features |
|------|-------|----------|----------|
| **Starter** | Rs 4,999/mo | Up to 50 | Dashboard, batch tests, basic reports |
| **Pro** | Rs 9,999/mo | Up to 200 | + Performance comparison, parent reports, API access |
| **Enterprise** | Custom | Unlimited | + White-label, dedicated support, custom integrations |

### Revenue Model

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        REVENUE STREAMS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PRIMARY                           SECONDARY                            │
│  ───────                           ─────────                            │
│  • B2C Subscriptions (60%)         • Referral commissions              │
│  • B2B Academy Plans (30%)         • Sponsored questions               │
│  • Exam Packs (10%)                • Academy partnerships              │
│                                    • Job board affiliate               │
│                                                                         │
│  GROWTH LEVERS                                                          │
│  ─────────────                                                          │
│  • Free tier → Premium conversion (target: 5%)                         │
│  • WhatsApp viral loop (shareable ERI badges)                          │
│  • Academy → Student referrals                                         │
│  • Daily free question on social (lead gen)                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Phase Breakdown

### Overview: 5 Phases Mapped to Hackathon Tiers

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           HACKATHON TIMELINE                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Week 1-2          Week 2-3          Week 3-4          Week 4-6           │
│  ─────────         ─────────         ─────────         ─────────          │
│  Phase 1           Phase 2           Phase 3           Phase 4            │
│  Foundation        Core Product      Growth Engine     Full Platform      │
│                                                                            │
│  ├── BRONZE ──────────────────┤                                           │
│  │   8-12 hrs                 │                                           │
│  │   Vault + Dashboard +      │                                           │
│  │   Basic Q&A + 1 Watcher    │                                           │
│  │                            │                                           │
│  ├────────────── SILVER ──────────────────────┤                           │
│  │               20-30 hrs                    │                           │
│  │               + ERI + Study Plans +        │                           │
│  │               WhatsApp Bot + Human Approval│                           │
│  │                                            │                           │
│  ├──────────────────────── GOLD ──────────────────────────────────────┤   │
│                            40+ hrs                                        │
│                            + B2B Dashboard + Odoo + Social Media +        │
│                            Autonomous Operations + Full Monetization      │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Phase Documentation Links

| Phase | Folder | Status | Key Documents |
|-------|--------|--------|---------------|
| **Phase 1** | [phase-1-foundation/](./phase-1-foundation/) | Complete | [SPEC.md](./phase-1-foundation/SPEC.md), [PLAN.md](./phase-1-foundation/PLAN.md), [BUILD.md](./phase-1-foundation/BUILD.md) |
| **Phase 2** | [phase-2-question-bank/](./phase-2-question-bank/) | Complete | [SPEC.md](./phase-2-question-bank/SPEC.md), [PLAN.md](./phase-2-question-bank/PLAN.md) |
| **Phase 3** | [phase-3-core-tutoring/](./phase-3-core-tutoring/) | Complete | ERI, Adaptive Tests, WhatsApp, Social Media |
| **Phase 4** | [phase-4-gold-tier/](./phase-4-gold-tier/) | Planned | B2B, Odoo, Autonomous, Full Platform |

### Phase Mapping Clarification

> **Note**: The project uses sequential phase numbering (1 → 2 → 3 → 4). Phase 4 combines B2B features, premium features, and autonomous operations.

| Conceptual Phase | Implementation Spec | Scope |
|------------------|---------------------|-------|
| Phase 1: Foundation | `specs/phase-1-foundation/` | Vault structure, 4 core skills, basic Q&A loop |
| Phase 2: Question Bank | `specs/phase-2-question-bank/` | Question bank automation, 1500+ questions |
| Phase 3: Growth Engine | `specs/phase-3-core-tutoring/` | ERI, adaptive tests, WhatsApp, study plans, social media |
| Phase 4: Full Platform | `specs/phase-4-gold-tier/` | B2B dashboard, Odoo, autonomous ops, premium features |

**Phase 4 Scope:** All enterprise/premium features bundled together:
1. B2B: Multi-student dashboard, batch testing, parent reports
2. Premium: Mock exams, deep analysis, challenge mode
3. Business: Odoo integration, payments, autonomous operations

---

### Phase 1: Foundation (Bronze - 8-12 hrs)

**Goal:** Minimal viable tutoring with Obsidian vault

#### Deliverables

| Component | Description |
|-----------|-------------|
| **Dashboard.md** | Student home: ERI score, recent sessions, quick actions |
| **Company_Handbook.md** | How to use Exam Tutor, exam info, commands |
| **Vault Structure** | /Inbox, /Needs_Action, /Done, /Students, /Questions |
| **File Watcher** | Monitor `/Inbox` for test requests |
| **Basic Q&A Loop** | Request → Questions → Answer → Evaluate → Save |

#### Skills Built

| Skill | Category | Purpose |
|-------|----------|---------|
| student-profile-loader | CORE | Load student context from memory |
| question-bank-querier | CORE | Retrieve questions by criteria |
| answer-evaluator | CORE | Evaluate MCQ responses |
| performance-tracker | CORE | Save results to vault |

#### Success Criteria

- [ ] Dashboard.md shows student name, target exam, basic stats
- [ ] Company_Handbook.md documents system usage
- [ ] File watcher detects `/Inbox/test-request.md`
- [ ] 5-question test can be completed end-to-end
- [ ] Results saved to `/Students/{id}/sessions/`

---

### Phase 2: Core Product (Bronze+ to Silver - 12-20 hrs)

**Goal:** Complete tutoring loop with ERI, adaptive tests, and basic engagement

#### Deliverables

| Component | Description |
|-----------|-------------|
| **ERI Calculator** | Compute and display Exam Readiness Index |
| **Weak Area Identifier** | Analyze performance to find gaps |
| **Diagnostic Generator** | Baseline assessment for new students |
| **Adaptive Test Generator** | Tests targeting weak areas |
| **Progress Streaks** | Track consecutive practice days |
| **Plan.md Reasoning** | Document AI decision-making |

#### Skills Built

| Skill | Category | Purpose |
|-------|----------|---------|
| exam-readiness-calculator | CORE | Calculate ERI score (0-100) |
| weak-area-identifier | CORE | Find knowledge gaps |
| diagnostic-assessment-generator | SUPPORTING | Create baseline tests |
| adaptive-test-generator | SUPPORTING | Personalized tests |
| streak-tracker | ENGAGEMENT | Track practice consistency |

#### Subagents Activated

| Subagent | Purpose |
|----------|---------|
| assessment-examiner | Orchestrates evaluation, metrics, weak areas |

#### Success Criteria

- [ ] ERI calculated and displayed correctly
- [ ] Weak areas identified with severity levels
- [ ] New student completes diagnostic, gets baseline ERI
- [ ] Adaptive test focuses on weak topics
- [ ] Streak counter increments on daily practice

---

### Phase 3: Growth Engine (Silver - 20-30 hrs)

**Goal:** Multi-channel engagement, viral features, monetization hooks

#### Deliverables

| Component | Description |
|-----------|-------------|
| **WhatsApp Bot** | Daily questions, test delivery, ERI updates |
| **Study Plan Generator** | AI-created personalized study schedules |
| **Progress Reports** | Weekly/monthly performance summaries |
| **Shareable ERI Badge** | "I'm 78% ready for SPSC!" social card |
| **Daily Free Question** | Auto-post to LinkedIn/Facebook |
| **Human-in-the-Loop** | Approval workflow for plans/posts |
| **Cron Scheduling** | Daily reminders, weekly reports |

#### Skills Built

| Skill | Category | Purpose |
|-------|----------|---------|
| study-plan-generator | SUPPORTING | Create study schedules |
| progress-report-generator | SUPPORTING | Generate reports |
| whatsapp-message-sender | ENGAGEMENT | Send WhatsApp messages |
| social-post-generator | ENGAGEMENT | Create social media content |
| eri-badge-generator | ENGAGEMENT | Create shareable badges |
| daily-question-selector | ENGAGEMENT | Pick viral-worthy questions |

#### Subagents Activated

| Subagent | Purpose |
|----------|---------|
| study-strategy-planner | Creates learning paths, difficulty progression |
| progress-reporting-coordinator | Generates progress reports |
| social-media-coordinator | Manages social posting schedule |

#### MCP Integrations

| Server | Purpose |
|--------|---------|
| whatsapp-mcp | Send/receive WhatsApp messages |
| linkedin-mcp | Post daily questions, milestones |
| scheduler-mcp | Cron job management |

#### Success Criteria

- [ ] WhatsApp bot sends daily question at 8 AM
- [ ] Student can complete test via WhatsApp
- [ ] Study plan requires human approval before activation
- [ ] ERI badge generated as shareable image
- [ ] Daily question auto-posts to LinkedIn
- [ ] 2+ watchers operational (filesystem + WhatsApp)

---

### Phase 4: Full Platform & Autonomous Excellence (Gold - 40+ hrs)

**Goal:** B2B features, premium upsells, autonomous operations, business integration

#### Deliverables

| Component | Description |
|-----------|-------------|
| **Multi-Student Dashboard** | Academy view of all students |
| **Batch Test Assignment** | Assign same test to multiple students |
| **Performance Comparison** | Rank students, identify strugglers |
| **Parent Reports** | Auto-send progress to parents |
| **Challenge a Friend** | Head-to-head test battles |
| **Full Mock Exams** | Timed, full-length practice exams |
| **Weak Area Deep Dive** | Detailed analysis with recommendations |
| **Session Logger** | Complete audit trail |
| **Odoo Integration** | Payment tracking, subscription management |
| **Auto-Renewal Reminders** | Notify before subscription expires |
| **Weekly Business Audit** | Revenue, churn, growth metrics |
| **CEO Briefing** | Executive summary of operations |
| **Ralph Wiggum Loop** | Continuous autonomous improvement |
| **Error Recovery** | Graceful handling of failures |
| **Twitter/Instagram** | Extended social media presence |
| **Referral System** | Track and reward referrals |
| **Predicted Score** | ML-based exam score prediction |

#### Skills Built

| Skill | Category | Purpose |
|-------|----------|---------|
| session-logger | OPTIONAL | Audit logging |
| syllabus-mapper | OPTIONAL | Cross-exam mapping |
| batch-test-assigner | B2B | Assign tests to groups |
| performance-comparator | B2B | Compare student performance |
| parent-report-generator | B2B | Create parent-friendly reports |
| challenge-coordinator | ENGAGEMENT | Manage head-to-head tests |
| mock-exam-generator | PREMIUM | Full timed mock exams |
| deep-dive-analyzer | PREMIUM | Detailed weak area analysis |
| payment-tracker | BUSINESS | Track payments via Odoo |
| subscription-manager | BUSINESS | Manage subscription lifecycle |
| renewal-reminder | BUSINESS | Send renewal notifications |
| business-audit-generator | BUSINESS | Weekly business metrics |
| ceo-briefing-generator | BUSINESS | Executive summary |
| referral-tracker | ENGAGEMENT | Track referral rewards |
| score-predictor | PREMIUM | Predict exam score |

#### MCP Integrations

| Server | Purpose |
|--------|---------|
| email-mcp | Send parent reports, notifications |
| facebook-mcp | Daily questions, milestone sharing |
| odoo-mcp | Accounting, payments, subscriptions |
| twitter-mcp | Daily questions, engagement |
| instagram-mcp | Visual content, stories |

#### Ralph Wiggum Autonomous Loop

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      RALPH WIGGUM LOOP                                  │
│                (Continuous Autonomous Operation)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐       │
│    │  OBSERVE │───→│  ANALYZE │───→│   PLAN   │───→│   ACT    │       │
│    └──────────┘    └──────────┘    └──────────┘    └──────────┘       │
│         ↑                                                ↓             │
│         └────────────────────────────────────────────────┘             │
│                                                                         │
│  OBSERVE:                                                               │
│  • Student activity (practice frequency, ERI changes)                  │
│  • Business metrics (signups, conversions, churn)                      │
│  • Content performance (which questions get shared)                    │
│                                                                         │
│  ANALYZE:                                                               │
│  • Identify at-risk students (ERI declining, inactive)                 │
│  • Spot conversion opportunities (engaged free users)                  │
│  • Detect viral content patterns                                       │
│                                                                         │
│  PLAN:                                                                  │
│  • Re-engagement campaigns for inactive students                       │
│  • Upsell sequences for high-engagement free users                     │
│  • Content calendar based on performance                               │
│                                                                         │
│  ACT:                                                                   │
│  • Send targeted WhatsApp messages                                     │
│  • Post high-performing content                                        │
│  • Adjust study plans automatically                                    │
│  • Generate weekly reports                                             │
│                                                                         │
│  Loop runs every 6 hours | Human override available                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Success Criteria

**B2B Features:**
- [ ] Academy can view dashboard with 10+ students
- [ ] Batch test assigned to group, results aggregated
- [ ] Performance leaderboard shows rankings
- [ ] Parent receives weekly email/WhatsApp report
- [ ] Challenge completed between two students
- [ ] Full 100-question timed mock exam works
- [ ] All sessions logged with audit trail

**Business Operations:**
- [ ] Odoo tracks payments, shows subscription status
- [ ] Auto-renewal reminder sent 7 days before expiry
- [ ] Weekly business audit generated automatically
- [ ] CEO briefing summarizes all operations
- [ ] Ralph Wiggum loop runs autonomously
- [ ] Error recovery handles 90%+ of failures
- [ ] Social media posts to Twitter/Instagram
- [ ] Referral codes generated and tracked

---

## 4. Feature-to-Phase Mapping

### Student-Facing Features

| Feature | Phase | Tier | Notes |
|---------|-------|------|-------|
| Student Dashboard | 1 | Bronze | Core Obsidian view |
| Basic Q&A Loop | 1 | Bronze | Request → Answer → Evaluate |
| ERI Score | 2 | Bronze+ | Core metric |
| Weak Area Reports | 2 | Bronze+ | Topic-level analysis |
| Progress Streaks | 2 | Bronze+ | Gamification |
| Diagnostic Test | 2 | Bronze+ | Baseline assessment |
| Adaptive Practice Tests | 2 | Silver | Personalized questions |
| Study Plan Generator | 3 | Silver | AI-created schedules |
| Daily Reminders | 3 | Silver | Cron-based notifications |
| Predicted Score | 4 | Gold+ | ML-based prediction |

### Engagement & Growth Features

| Feature | Phase | Tier | Notes |
|---------|-------|------|-------|
| WhatsApp Bot | 3 | Silver | Daily questions, test delivery |
| Shareable ERI Badge | 3 | Silver | Social proof, viral loop |
| Daily Free Question (Social) | 3 | Silver | LinkedIn/Facebook lead gen |
| Challenge a Friend | 4 | Gold | Head-to-head tests |
| Leaderboard | 4 | Gold | Competitive ranking |
| Referral Rewards | 4 | Gold | Growth engine |

### Premium/Upsell Features

| Feature | Phase | Tier | Notes |
|---------|-------|------|-------|
| 1-on-1 AI Study Plan | 3 | Silver | Premium personalization |
| Full Timed Mock Exams | 4 | Gold | 100+ questions, timer |
| Weak Area Deep Dive | 4 | Gold | Detailed recommendations |
| Previous Year Paper Packs | 4 | Gold | Content bundle |

### B2B / Academy Features

| Feature | Phase | Tier | Notes |
|---------|-------|------|-------|
| Multi-Student Dashboard | 4 | Gold | Academy admin view |
| Batch Test Assignment | 4 | Gold | Group testing |
| Performance Comparison | 4 | Gold | Student rankings |
| Auto Parent Reports | 4 | Gold | Email/WhatsApp delivery |
| White-Label Branding | 4 | Gold | Enterprise only |

### Business Operations

| Feature | Phase | Tier | Notes |
|---------|-------|------|-------|
| Plan.md Reasoning | 2 | Bronze+ | Decision documentation |
| Human-in-the-Loop | 3 | Silver | Approval workflows |
| Session Logging | 4 | Gold | Audit trail |
| Payment Tracking (Odoo) | 4 | Gold | Subscription management |
| Auto-Renewal Reminders | 4 | Gold | Retention |
| Weekly Business Audit | 4 | Gold | Metrics dashboard |
| CEO Briefing | 4 | Gold | Executive summary |

---

## 5. Skill Inventory Per Phase

### Complete Skill Matrix

| Skill | Category | Phase | Dependencies | MCP Tools |
|-------|----------|-------|--------------|-----------|
| **PHASE 1 - Foundation** |||||
| student-profile-loader | CORE | 1 | None | read_file |
| question-bank-querier | CORE | 1 | None | read_file, list_directory |
| answer-evaluator | CORE | 1 | question-bank-querier | None |
| performance-tracker | CORE | 1 | student-profile-loader | write_file |
| **PHASE 2 - Core Product** |||||
| exam-readiness-calculator | CORE | 2 | performance-tracker | read_file |
| weak-area-identifier | CORE | 2 | performance-tracker | read_file |
| diagnostic-assessment-generator | SUPPORTING | 2 | question-bank-querier | read_file |
| adaptive-test-generator | SUPPORTING | 2 | weak-area-identifier | read_file |
| streak-tracker | ENGAGEMENT | 2 | performance-tracker | read_file, write_file |
| **PHASE 3 - Growth Engine** |||||
| study-plan-generator | SUPPORTING | 3 | weak-area-identifier | write_file |
| progress-report-generator | SUPPORTING | 3 | performance-tracker | write_file |
| whatsapp-message-sender | ENGAGEMENT | 3 | None | whatsapp-mcp |
| social-post-generator | ENGAGEMENT | 3 | question-bank-querier | linkedin-mcp |
| eri-badge-generator | ENGAGEMENT | 3 | exam-readiness-calculator | image generation |
| daily-question-selector | ENGAGEMENT | 3 | question-bank-querier | scheduler-mcp |
| **PHASE 4 - Full Platform & Autonomous** |||||
| session-logger | OPTIONAL | 4 | None | write_file |
| syllabus-mapper | OPTIONAL | 4 | None | read_file |
| batch-test-assigner | B2B | 4 | question-bank-querier | write_file |
| performance-comparator | B2B | 4 | performance-tracker | read_file |
| parent-report-generator | B2B | 4 | progress-report-generator | email-mcp |
| challenge-coordinator | ENGAGEMENT | 4 | adaptive-test-generator | whatsapp-mcp |
| mock-exam-generator | PREMIUM | 4 | question-bank-querier | None |
| deep-dive-analyzer | PREMIUM | 4 | weak-area-identifier | None |
| payment-tracker | BUSINESS | 4 | None | odoo-mcp |
| subscription-manager | BUSINESS | 4 | payment-tracker | odoo-mcp |
| renewal-reminder | BUSINESS | 4 | subscription-manager | whatsapp-mcp |
| business-audit-generator | BUSINESS | 4 | payment-tracker | read_file |
| ceo-briefing-generator | BUSINESS | 4 | business-audit-generator | write_file |
| referral-tracker | ENGAGEMENT | 4 | student-profile-loader | write_file |
| score-predictor | PREMIUM | 4 | performance-tracker | None |

### Subagent Schedule

| Subagent | Phase | Skills Used | Trigger |
|----------|-------|-------------|---------|
| assessment-examiner | 2 | answer-evaluator, weak-area-identifier, exam-readiness-calculator | Test completion |
| study-strategy-planner | 3 | study-plan-generator, syllabus-mapper, weak-area-identifier | Plan request |
| progress-reporting-coordinator | 3 | progress-report-generator, exam-readiness-calculator | Weekly/on-demand |
| social-media-coordinator | 3 | social-post-generator, daily-question-selector, eri-badge-generator | Daily schedule |
| academy-operations-coordinator | 4 | batch-test-assigner, performance-comparator, parent-report-generator | Academy requests |
| business-intelligence-coordinator | 4 | payment-tracker, business-audit-generator, ceo-briefing-generator | Weekly schedule |

---

## 6. Integration Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXAM TUTOR ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         OBSIDIAN VAULT                                 │ │
│  │  Dashboard.md | Company_Handbook.md | Plan.md | Students/ | Questions/│ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                      │                                      │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         CLAUDE CODE                                    │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │                      PARENT AGENT                                │  │ │
│  │  │  User Communication | Session Management | Workflow Orchestration│  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                  │                                     │ │
│  │  ┌───────────────────────────────┼───────────────────────────────┐    │ │
│  │  ▼               ▼               ▼               ▼               ▼    │ │
│  │  assessment-   study-        progress-      social-        academy-   │ │
│  │  examiner      strategy-     reporting-     media-         operations-│ │
│  │               planner       coordinator    coordinator    coordinator │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │                      30+ SKILLS                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                      │                                      │
│          ┌───────────────────────────┼───────────────────────────┐         │
│          ▼                           ▼                           ▼         │
│  ┌──────────────┐           ┌──────────────┐           ┌──────────────┐   │
│  │  FILESYSTEM  │           │   MESSAGING  │           │    SOCIAL    │   │
│  │     MCP      │           │     MCP      │           │     MCP      │   │
│  │              │           │              │           │              │   │
│  │ • read_file  │           │ • WhatsApp   │           │ • LinkedIn   │   │
│  │ • write_file │           │ • Email      │           │ • Facebook   │   │
│  │ • watch      │           │ • SMS        │           │ • Twitter    │   │
│  └──────────────┘           └──────────────┘           │ • Instagram  │   │
│                                                        └──────────────┘   │
│          ┌───────────────────────────┼───────────────────────────┐         │
│          ▼                           ▼                           ▼         │
│  ┌──────────────┐           ┌──────────────┐           ┌──────────────┐   │
│  │    GITHUB    │           │     ODOO     │           │  SCHEDULER   │   │
│  │     MCP      │           │     MCP      │           │     MCP      │   │
│  │              │           │              │           │              │   │
│  │ • Q-Bank     │           │ • Payments   │           │ • Cron jobs  │   │
│  │   versioning │           │ • Invoices   │           │ • Reminders  │   │
│  │ • Issues     │           │ • Customers  │           │ • Reports    │   │
│  └──────────────┘           └──────────────┘           └──────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### WhatsApp Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      WHATSAPP INTEGRATION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INBOUND (Student → Tutor)                                             │
│  ─────────────────────────                                             │
│  • "Start test" → Triggers adaptive-test-generator                     │
│  • "My ERI" → Triggers exam-readiness-calculator                       │
│  • "A, B, C, D, A" → Triggers answer-evaluator                         │
│  • "Challenge @friend" → Triggers challenge-coordinator                │
│                                                                         │
│  OUTBOUND (Tutor → Student)                                            │
│  ─────────────────────────                                             │
│  • 8:00 AM: Daily question (daily-question-selector)                   │
│  • After test: Results + ERI update                                    │
│  • Weekly: Progress report summary                                     │
│  • 7 days before expiry: Renewal reminder                              │
│                                                                         │
│  MESSAGE TEMPLATES                                                      │
│  ─────────────────                                                     │
│  • daily_question: "Your daily PPSC question is ready! 📚"            │
│  • test_result: "Test complete! Score: 8/10. ERI: 72 (+3) 📈"         │
│  • eri_badge: [Image] "Share your progress!"                           │
│  • renewal: "Your Premium expires in 7 days. Renew now: [link]"       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### LinkedIn Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      LINKEDIN INTEGRATION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DAILY FREE QUESTION (Lead Generation)                                 │
│  ────────────────────────────────────                                  │
│  Post at: 9:00 AM daily                                                │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │  📚 PPSC Daily Question                                        │     │
│  │                                                                │     │
│  │  Q: Which constitutional amendment introduced the              │     │
│  │     18th Amendment in Pakistan?                                │     │
│  │                                                                │     │
│  │  A) 17th Amendment                                             │     │
│  │  B) 18th Amendment                                             │     │
│  │  C) 19th Amendment                                             │     │
│  │  D) 20th Amendment                                             │     │
│  │                                                                │     │
│  │  Answer in comments! Full explanation tomorrow.                │     │
│  │                                                                │     │
│  │  Want more? Try Exam Tutor FREE: [link]                       │     │
│  │                                                                │     │
│  │  #PPSC #SPSC #KPPSC #GovtJobs #Pakistan                       │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  MILESTONE SHARING (Viral Loop)                                        │
│  ─────────────────────────────                                         │
│  Triggered when: Student reaches new ERI band                          │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │  🎉 Ahmed just reached "READY" status for SPSC!               │     │
│  │                                                                │     │
│  │  [ERI Badge Image: 78/100 - READY]                            │     │
│  │                                                                │     │
│  │  After 45 days of practice with Exam Tutor.                   │     │
│  │  Start your journey: [link]                                   │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Odoo Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ODOO INTEGRATION                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SYNC POINTS                                                           │
│  ───────────                                                           │
│                                                                         │
│  Exam Tutor → Odoo                    Odoo → Exam Tutor                │
│  ─────────────────                    ─────────────────                │
│  • New signup → Create contact        • Payment received → Activate    │
│  • Upgrade request → Create invoice     subscription                   │
│  • Usage metrics → Update contact     • Invoice overdue → Send         │
│                                         reminder                        │
│                                       • Subscription cancelled →       │
│                                         Downgrade to free              │
│                                                                         │
│  DATA MAPPING                                                          │
│  ────────────                                                          │
│                                                                         │
│  Exam Tutor Field      Odoo Field                                      │
│  ─────────────────     ──────────                                      │
│  student_id            partner_ref                                     │
│  email                 email                                           │
│  phone                 mobile                                          │
│  subscription_tier     product_category                                │
│  subscription_start    subscription_start_date                         │
│  subscription_end      subscription_end_date                           │
│  total_paid            total_invoiced                                  │
│                                                                         │
│  AUTOMATED WORKFLOWS                                                   │
│  ───────────────────                                                   │
│  • 7 days before expiry: Auto-renewal reminder                        │
│  • On payment: Send receipt + activate features                       │
│  • On expiry: Downgrade + send win-back offer                         │
│  • Monthly: Generate revenue report for CEO briefing                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Data & Folder Structure

### Obsidian Vault Structure

```
ExamTutor-Vault/
│
├── Dashboard.md                      # Home view (student or admin)
├── Company_Handbook.md               # System documentation
├── Plan.md                           # Reasoning/decision log
│
├── Inbox/                            # Incoming requests (watched)
│   ├── test-request-{timestamp}.md
│   ├── challenge-{challenger}-{challenged}.md
│   └── support-{timestamp}.md
│
├── Needs_Action/                     # Awaiting human approval
│   ├── study-plan-{student}-{date}.md
│   ├── social-post-{date}.md
│   └── renewal-campaign-{date}.md
│
├── Done/                             # Completed/approved items
│   └── {archived items by date}
│
├── Students/                         # Student memory
│   └── {student_id}/
│       ├── profile.json              # Student profile
│       ├── profile.md                # Human-readable profile
│       ├── history.json              # Session history
│       ├── topic-stats.json          # Performance by topic
│       ├── active-plan.json          # Current study plan
│       ├── subscription.json         # Payment/tier info
│       ├── streaks.json              # Practice streaks
│       ├── referrals.json            # Referral tracking
│       ├── sessions/
│       │   └── {session_id}.json
│       ├── reports/
│       │   ├── weekly-{date}.md
│       │   └── monthly-{date}.md
│       └── badges/
│           └── eri-{score}-{date}.png
│
├── Academies/                        # B2B academy data
│   └── {academy_id}/
│       ├── profile.json
│       ├── students.json             # List of student IDs
│       ├── batch-tests/
│       │   └── {test_id}.json
│       ├── reports/
│       │   └── {date}.md
│       └── branding/                 # White-label assets
│
├── Questions/                        # Question bank
│   ├── SPSC/
│   │   ├── PakistanStudies/
│   │   │   ├── constitutional-amendments.json
│   │   │   ├── geography.json
│   │   │   └── history.json
│   │   ├── GeneralKnowledge/
│   │   ├── CurrentAffairs/
│   │   └── English/
│   ├── PPSC/
│   │   └── {subjects}/
│   └── KPPSC/
│       └── {subjects}/
│
├── Syllabus/                         # Exam syllabi
│   ├── cross-exam-mapping.json
│   ├── SPSC/
│   │   ├── syllabus-structure.json
│   │   └── topic-weights.json
│   ├── PPSC/
│   └── KPPSC/
│
├── Content/                          # Marketing content
│   ├── daily-questions/
│   │   └── {date}.md
│   ├── social-posts/
│   │   └── {platform}-{date}.md
│   └── templates/
│       ├── eri-badge-template.html
│       └── parent-report-template.md
│
├── Business/                         # Business operations
│   ├── subscriptions/
│   │   └── {date}.json
│   ├── revenue/
│   │   └── {month}.json
│   ├── audits/
│   │   └── weekly-{date}.md
│   └── ceo-briefings/
│       └── {date}.md
│
├── Logs/                             # Audit logs
│   ├── sessions/
│   │   └── {student_id}/
│   ├── errors/
│   │   └── {date}.json
│   └── api-calls/
│       └── {date}.json
│
└── .claude/                          # Claude Code configuration
    ├── mcp.json
    ├── agents/
    │   ├── assessment-examiner.md
    │   ├── study-strategy-planner.md
    │   ├── progress-reporting-coordinator.md
    │   ├── social-media-coordinator.md
    │   ├── academy-operations-coordinator.md
    │   └── business-intelligence-coordinator.md
    └── skills/
        └── exam-tutor/
            ├── SKILL.md
            └── {individual skills}/
```

### Key JSON Schemas

#### Student Profile (`Students/{id}/profile.json`)

```json
{
  "student_id": "STU-001",
  "name": "Ahmed Khan",
  "email": "ahmed@example.com",
  "phone": "+923001234567",
  "target_exam": "PPSC",
  "target_date": "2026-03-15",
  "subjects": ["Pakistan Studies", "General Knowledge", "Current Affairs"],
  "created_at": "2025-12-10T10:00:00Z",
  "subscription": {
    "tier": "premium",
    "started": "2025-12-10",
    "expires": "2026-01-10",
    "auto_renew": true
  },
  "referral_code": "AHMED2025",
  "referred_by": null,
  "preferences": {
    "daily_question_time": "08:00",
    "weekly_report_day": "Sunday",
    "notification_channels": ["whatsapp", "email"]
  }
}
```

#### Subscription (`Students/{id}/subscription.json`)

```json
{
  "student_id": "STU-001",
  "tier": "premium",
  "price_paid": 499,
  "currency": "PKR",
  "payment_method": "jazzcash",
  "payment_reference": "JC-12345",
  "started": "2025-12-10",
  "expires": "2026-01-10",
  "auto_renew": true,
  "odoo_invoice_id": "INV-2025-001",
  "features_enabled": [
    "unlimited_questions",
    "full_mock_exams",
    "ai_study_plan",
    "weak_area_deep_dive"
  ],
  "usage": {
    "questions_this_month": 245,
    "mock_exams_taken": 3,
    "study_plans_generated": 2
  }
}
```

#### Academy Profile (`Academies/{id}/profile.json`)

```json
{
  "academy_id": "ACD-001",
  "name": "Karachi Test Prep Academy",
  "admin_email": "admin@ktpa.pk",
  "phone": "+922134567890",
  "subscription": {
    "tier": "pro",
    "max_students": 200,
    "current_students": 87,
    "expires": "2026-06-30"
  },
  "branding": {
    "white_label": false,
    "logo_url": null,
    "primary_color": null
  },
  "settings": {
    "auto_parent_reports": true,
    "report_frequency": "weekly",
    "default_exam": "SPSC"
  }
}
```

---

## 8. Dependencies Between Phases

### Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE DEPENDENCIES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: Foundation (Bronze)                                               │
│  ───────────────────────────                                               │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐       │
│  │student-profile-  │   │question-bank-    │   │                  │       │
│  │loader            │──→│querier           │──→│answer-evaluator  │       │
│  └────────┬─────────┘   └──────────────────┘   └────────┬─────────┘       │
│           │                                             │                  │
│           └──────────────────┬──────────────────────────┘                  │
│                              ▼                                              │
│                    ┌──────────────────┐                                    │
│                    │performance-      │                                    │
│                    │tracker           │                                    │
│                    └────────┬─────────┘                                    │
│                             │                                               │
│  ═══════════════════════════╪═══════════════════════════════════════════   │
│                             ▼                                               │
│  PHASE 2: Core Product (Bronze+)                                           │
│  ──────────────────────────────                                            │
│           ┌─────────────────┴─────────────────┐                            │
│           ▼                                   ▼                            │
│  ┌──────────────────┐               ┌──────────────────┐                  │
│  │exam-readiness-   │               │weak-area-        │                  │
│  │calculator        │               │identifier        │                  │
│  └──────────────────┘               └────────┬─────────┘                  │
│           │                                  │                             │
│           │         ┌────────────────────────┤                             │
│           │         ▼                        ▼                             │
│           │  ┌──────────────────┐   ┌──────────────────┐                  │
│           │  │diagnostic-       │   │adaptive-test-    │                  │
│           │  │assessment-gen    │   │generator         │                  │
│           │  └──────────────────┘   └──────────────────┘                  │
│           │                                                                │
│  ═════════╪════════════════════════════════════════════════════════════   │
│           ▼                                                                │
│  PHASE 3: Growth Engine (Silver)                                          │
│  ──────────────────────────────                                           │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐      │
│  │study-plan-       │   │progress-report-  │   │whatsapp-message- │      │
│  │generator         │   │generator         │   │sender            │      │
│  └──────────────────┘   └──────────────────┘   └──────────────────┘      │
│           │                     │                      │                  │
│           │                     │                      │                  │
│  ┌────────┴────────┐   ┌───────┴────────┐   ┌────────┴────────┐         │
│  │eri-badge-       │   │social-post-    │   │daily-question-  │         │
│  │generator        │   │generator       │   │selector         │         │
│  └─────────────────┘   └────────────────┘   └─────────────────┘         │
│                                                                           │
│  ═════════════════════════════════════════════════════════════════════   │
│                                                                           │
│  PHASE 4: Full Platform & Autonomous (Gold)                             │
│  ──────────────────────────────────────────                              │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐      │
│  │batch-test-       │   │performance-      │   │challenge-        │      │
│  │assigner          │   │comparator        │   │coordinator       │      │
│  └──────────────────┘   └──────────────────┘   └──────────────────┘      │
│           │                     │                                         │
│           └──────────┬──────────┘                                         │
│                      ▼                                                    │
│           ┌──────────────────┐                                           │
│           │parent-report-    │                                           │
│           │generator         │                                           │
│           └──────────────────┘                                           │
│                                                                           │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐      │
│  │payment-tracker   │──→│subscription-     │──→│renewal-reminder  │      │
│  │                  │   │manager           │   │                  │      │
│  └──────────────────┘   └────────┬─────────┘   └──────────────────┘      │
│                                  │                                        │
│                                  ▼                                        │
│           ┌──────────────────────┴──────────────────────┐                │
│           ▼                                             ▼                │
│  ┌──────────────────┐                        ┌──────────────────┐        │
│  │business-audit-   │                        │ceo-briefing-     │        │
│  │generator         │───────────────────────→│generator         │        │
│  └──────────────────┘                        └──────────────────┘        │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Critical Path

```
student-profile-loader
        │
        ▼
question-bank-querier ──→ answer-evaluator
        │                        │
        └───────────┬────────────┘
                    ▼
           performance-tracker
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
exam-readiness-calc    weak-area-identifier
        │                       │
        └───────────┬───────────┘
                    ▼
         adaptive-test-generator
                    │
                    ▼
         study-plan-generator
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 whatsapp-bot          social-integration
        │                       │
        └───────────┬───────────┘
                    ▼
           b2b-dashboard
                    │
                    ▼
           odoo-integration
                    │
                    ▼
         ralph-wiggum-loop
```

---

## 9. Monetization Integration Points

### Conversion Funnels

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MONETIZATION TOUCHPOINTS                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FREE → BASIC (Rs 199/mo)                                                  │
│  ────────────────────────                                                  │
│  Trigger: Daily limit hit (5 questions)                                    │
│  Message: "You've reached your daily limit! Upgrade to Basic for           │
│            50 questions/day. Only Rs 199/month. [Upgrade Now]"             │
│  Channel: In-app + WhatsApp                                                │
│  Phase: 3 (Silver)                                                         │
│                                                                             │
│  BASIC → PREMIUM (Rs 499/mo)                                               │
│  ───────────────────────────                                               │
│  Trigger: Request for AI study plan or mock exam                           │
│  Message: "AI Study Plans are a Premium feature. Upgrade to unlock         │
│            personalized plans, mock exams, and deep analysis."             │
│  Channel: In-app + WhatsApp                                                │
│  Phase: 3 (Silver)                                                         │
│                                                                             │
│  PREMIUM → EXAM PACK (Rs 999 one-time)                                     │
│  ─────────────────────────────────────                                     │
│  Trigger: Student practicing > 30 days, exam date set                      │
│  Message: "30 days until your exam! Get Previous 5 Years Papers with       │
│            topic-wise analysis. One-time Rs 999. [Get Papers]"             │
│  Channel: Email + WhatsApp                                                 │
│  Phase: 5 (Gold)                                                           │
│                                                                             │
│  INDIVIDUAL → ACADEMY REFERRAL                                             │
│  ────────────────────────────                                              │
│  Trigger: High-engagement user, teacher/instructor detected                │
│  Message: "Managing students? Exam Tutor for Academies lets you track      │
│            all your students in one dashboard. [Learn More]"               │
│  Channel: Email                                                            │
│  Phase: 5 (Gold)                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Revenue Tracking Schema

```json
{
  "revenue_daily": {
    "date": "2025-12-15",
    "new_subscriptions": {
      "free_to_basic": 12,
      "basic_to_premium": 5,
      "new_premium": 3
    },
    "renewals": {
      "basic": 8,
      "premium": 4
    },
    "one_time": {
      "exam_packs": 2
    },
    "academy": {
      "new": 0,
      "renewals": 1
    },
    "total_revenue": 15492,
    "currency": "PKR"
  }
}
```

### Upsell Automation Rules

| Trigger | Segment | Action | Phase |
|---------|---------|--------|-------|
| 5 questions reached | Free user | Show upgrade CTA | 3 |
| ERI > 60 | Free/Basic | Suggest mock exam (Premium) | 3 |
| 7 days of streaks | Free user | Offer Basic trial | 3 |
| Exam date < 30 days | Basic/Premium | Offer Exam Pack | 4 |
| Multiple students asked | Individual | Suggest Academy plan | 4 |
| Subscription expiring | Basic/Premium | Send renewal reminder | 4 |
| Churned user | Ex-Premium | Win-back campaign | 4 |

---

## 10. Success Criteria Per Tier

### Bronze Tier Checklist (8-12 hrs)

**Vault Structure**
- [ ] Obsidian vault with correct folder structure
- [ ] Dashboard.md showing student info
- [ ] Company_Handbook.md with documentation

**Core Functionality**
- [ ] Student profile loads from JSON
- [ ] Questions retrieved by exam/subject
- [ ] MCQ answers evaluated correctly
- [ ] Results saved to student files

**Automation**
- [ ] File watcher monitors /Inbox
- [ ] Processed files moved to /Done

**Demo Scenario**
```
1. Create new student profile
2. Drop "test-request.md" in /Inbox
3. System generates 5 questions
4. Submit answers
5. View results in Dashboard.md
```

---

### Silver Tier Checklist (20-30 hrs)

**Intelligence**
- [ ] ERI calculated correctly (0-100)
- [ ] Weak areas identified with severity
- [ ] Diagnostic generates baseline test
- [ ] Adaptive tests target weak areas
- [ ] Study plan created from weak areas

**Engagement**
- [ ] WhatsApp bot sends daily question
- [ ] Tests completable via WhatsApp
- [ ] ERI badge generated as image
- [ ] Progress streaks tracked

**Social & Growth**
- [ ] Daily question posts to LinkedIn
- [ ] Human approval for social posts
- [ ] Shareable content created

**Automation**
- [ ] 2+ watchers (filesystem + WhatsApp)
- [ ] Cron scheduling for daily/weekly tasks
- [ ] Plan.md documents reasoning

**Monetization Hooks**
- [ ] Daily limit enforced for free users
- [ ] Upgrade CTAs displayed appropriately

**Demo Scenario**
```
1. New student completes diagnostic via WhatsApp
2. Baseline ERI: 45 (Developing)
3. Weak areas: Constitutional Amendments, Current Affairs
4. Study plan generated → awaits approval
5. Human approves plan
6. Daily reminder sent next morning
7. After 7 days: Progress report generated
8. ERI badge shared to LinkedIn
```

---

### Gold Tier Checklist (40+ hrs)

**Premium Features**
- [ ] Full 100-question timed mock exam
- [ ] Weak area deep dive analysis
- [ ] Predicted score calculation
- [ ] Challenge a friend works

**B2B Features**
- [ ] Academy dashboard shows 10+ students
- [ ] Batch test assigned to group
- [ ] Performance leaderboard
- [ ] Parent reports auto-sent

**Business Operations**
- [ ] Odoo tracks subscriptions
- [ ] Payments recorded and synced
- [ ] Auto-renewal reminders sent
- [ ] Weekly business audit generated
- [ ] CEO briefing produced

**Autonomous Operations**
- [ ] Ralph Wiggum loop runs (6hr cycle)
- [ ] Error recovery handles 90%+ failures
- [ ] Session logging complete
- [ ] Social posts to Twitter/Instagram

**Full Integration**
- [ ] WhatsApp + LinkedIn + Facebook + Email
- [ ] Odoo accounting synced
- [ ] GitHub for question bank

**Demo Scenario**
```
1. System runs autonomously for 1 week
2. Academy with 20 students tracked
3. Daily questions posted to all social
4. 5 premium conversions from free
5. Parent reports sent weekly
6. Business audit shows Rs 25,000 MRR
7. CEO briefing summarizes growth
8. One error occurred → auto-recovered
```

---

## 11. Implementation Timeline

### Week 1 (Dec 7-14): Phase 1 - Foundation

| Day | Task | Skills/Components |
|-----|------|-------------------|
| 1-2 | Set up Obsidian vault, folder structure | - |
| 2-3 | Implement student-profile-loader, question-bank-querier | CORE skills |
| 3-4 | Implement answer-evaluator, performance-tracker | CORE skills |
| 4-5 | Create Dashboard.md, Company_Handbook.md | Templates |
| 5-7 | Set up file watcher, test end-to-end | Automation |

### Week 2 (Dec 15-21): Phase 2 - Core Product

| Day | Task | Skills/Components |
|-----|------|-------------------|
| 8-9 | Implement exam-readiness-calculator | CORE skill |
| 9-10 | Implement weak-area-identifier | CORE skill |
| 10-11 | Implement diagnostic-assessment-generator | SUPPORTING skill |
| 11-12 | Implement adaptive-test-generator | SUPPORTING skill |
| 12-14 | Create assessment-examiner subagent, Plan.md loop | Subagent |

### Week 3 (Dec 22-28): Phase 3 - Growth Engine

| Day | Task | Skills/Components |
|-----|------|-------------------|
| 15-16 | Implement study-plan-generator | SUPPORTING skill |
| 16-17 | Set up WhatsApp MCP integration | MCP server |
| 17-18 | Implement daily-question-selector, social-post-generator | ENGAGEMENT skills |
| 18-19 | Create eri-badge-generator | ENGAGEMENT skill |
| 19-21 | Human approval workflow, cron scheduling | Automation |

### Week 4-6 (Dec 29 - Jan 18): Phase 4 - Full Platform & Autonomous

| Day | Task | Skills/Components |
|-----|------|-------------------|
| 22-23 | Implement batch-test-assigner, performance-comparator | B2B skills |
| 23-24 | Implement parent-report-generator | B2B skill |
| 24-25 | Create mock-exam-generator, deep-dive-analyzer | PREMIUM skills |
| 25-26 | Implement challenge-coordinator | ENGAGEMENT skill |
| 26-28 | Session logging, error recovery | OPTIONAL skills |
| 29-30 | Set up Odoo MCP, payment-tracker | BUSINESS skill |
| 30-31 | Implement subscription-manager, renewal-reminder | BUSINESS skills |
| 31-32 | Implement business-audit-generator | BUSINESS skill |
| 32-33 | Implement ceo-briefing-generator | BUSINESS skill |
| 33-35 | Ralph Wiggum autonomous loop | Automation |
| 35-42 | Testing, polish, demo preparation | - |

---

## 12. Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| WhatsApp API limitations | Can't send messages | Medium | Fallback to SMS/Email |
| Question bank too small | Poor UX | High | Start with PPSC Pakistan Studies only |
| Odoo integration complex | Miss Gold | Medium | Mock Odoo with JSON files first |
| ERI formula issues | Incorrect scores | Low | Unit test each component |
| Social API rate limits | Can't post | Medium | Queue posts, spread timing |
| Student data loss | Trust erosion | Low | Backup before every write |
| Scope creep | Miss deadlines | High | Strict phase gates |

---

## 13. Future Roadmap (Post-Hackathon)

### Q1 2026
- Mobile app (React Native)
- Voice interface for WhatsApp
- AI-generated questions from past papers

### Q2 2026
- Urdu language support
- Video explanations for wrong answers
- Study groups feature

### Q3 2026
- CSS/PMS exam support
- Banking exam support (SBP, NBP)
- International expansion (India PSC)

### Q4 2026
- Predictive analytics (pass probability)
- Resume builder integration
- Job board partnership

---

*Document Version: 2.0*
*Last Updated: Jan 2026*
*Status: Active Development*
