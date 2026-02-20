# AI Exam Tutor — Digital FTE for Pakistani Competitive Exams

> **Personal AI Employee Hackathon 0** submission
> *Your exam preparation on autopilot. Local-first, agent-driven, human-in-the-loop.*

A fully autonomous AI tutor that prepares students for **PPSC, SPSC, and KPPSC** provincial public service commission exams. Built on Claude Code with a complete Digital FTE architecture: proactive coaching, adaptive testing, WhatsApp delivery, LinkedIn social presence, and a self-healing autonomous loop.

---

## Demo

> **[Demo Video — 5 min walkthrough](#)** *(link here)*
> **GitHub:** https://github.com/NailaImran/AI-exam-tutor

---

## What It Does

| Capability | Description |
|---|---|
| **Adaptive Testing** | Generates personalized MCQ tests weighted toward each student's weak areas |
| **Exam Readiness Index (ERI)** | 0–100 score tracking 4 dimensions: Accuracy, Coverage, Recency, Consistency |
| **WhatsApp Coaching** | Daily questions, test sessions, and progress reports delivered via WhatsApp |
| **Autonomous Coaching** | Proactively detects disengagement, predicts knowledge gaps, schedules revision |
| **Mock Exams** | Full 100-question timed exams with pressure simulation |
| **LinkedIn Posts** | Daily exam questions auto-posted for student engagement and enrollment |
| **Weekly Briefings** | Monday morning KPI report: ERI distribution, engagement, risk flags |
| **Ralph Wiggum Loop** | Claude keeps working autonomously until every pending task is complete |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERCEPTION LAYER                             │
│  inbox_watcher.py        whatsapp_watcher.py                    │
│  (file drops → action)   (student replies → action)            │
└──────────────────────┬──────────────────────────────────────────┘
                       │ writes .md files
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VAULT (Local Markdown + JSON)                │
│  /inbox/         /needs_action/    /plans/                      │
│  /pending_approval/  /approved/   /rejected/   /done/          │
│  Dashboard.md    Company_Handbook.md   Business_Goals.md        │
└──────────────────────┬──────────────────────────────────────────┘
                       │ triggers
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REASONING LAYER                              │
│  Claude Code + 35 Agent Skills + 7 Subagents                    │
│  Ralph Wiggum Stop Hook (autonomous iteration until done)       │
└──────────┬──────────────────────────────┬───────────────────────┘
           │ sensitive actions            │ auto-approved actions
           ▼                              ▼
┌──────────────────┐           ┌──────────────────────────────────┐
│  HUMAN-IN-LOOP   │  approve  │  ACTION LAYER (MCP Servers)      │
│  /pending_       │ ────────► │  WhatsApp · LinkedIn             │
│  approval/       │           │  GitHub · Filesystem             │
└──────────────────┘           └──────────────────────────────────┘
                       ▲
┌──────────────────────┴──────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                          │
│  orchestrator.py — scheduling, folder watching, Claude triggers │
│  watchdog.py     — health monitor, auto-restart on crash        │
└─────────────────────────────────────────────────────────────────┘
```

### The Ralph Wiggum Loop

When Claude finishes a task, the Stop Hook (`.claude/hooks/stop_hook.py`) checks `inbox/`, `needs_action/`, and `pending_approval/` for unprocessed files. If any exist, it blocks Claude's exit and re-injects a processing prompt — keeping the AI working autonomously until all items are done or routed to human review (max 10 iterations).

---

## Tech Stack

| Component | Technology |
|---|---|
| **Brain** | Claude Code (claude-sonnet-4-6) |
| **Memory / Vault** | Local Markdown + JSON files |
| **Autonomy** | Claude Code Stop Hook (Ralph Wiggum pattern) |
| **Scheduling** | `orchestrator.py` + Windows Task Scheduler |
| **Watchers** | Python (`watchdog` library + polling) |
| **Process Management** | `watchdog.py` + PM2 / Task Scheduler |
| **External Actions** | MCP Servers (filesystem, WhatsApp, LinkedIn, GitHub) |
| **Error Recovery** | Exponential backoff, graceful degradation queue |
| **Security** | Permission boundaries, audit logging, DRY_RUN mode |

---

## Project Structure

```
AI-exam-tutor/
│
├── orchestrator.py          # Master process: scheduling + folder watching
├── watchdog.py              # Health monitor: restarts dead processes
│
├── watchers/
│   ├── base_watcher.py      # Abstract base for all watchers
│   ├── inbox_watcher.py     # Monitors /inbox/ for dropped files
│   └── whatsapp_watcher.py  # Polls WhatsApp API for student replies
│
├── utils/
│   ├── security.py          # Permission boundaries + audit log writer
│   └── retry_handler.py     # @with_retry, GracefulDegradation, quarantine
│
├── .claude/
│   ├── hooks/stop_hook.py   # Ralph Wiggum autonomous loop
│   ├── agents/              # 7 subagents
│   ├── skills/exam-tutor/   # 35 agent skills
│   └── mcp.json             # MCP server configuration
│
├── question-bank/           # 1,793 MCQ questions
│   ├── PPSC/{Subject}/
│   ├── SPSC/{Subject}/
│   └── KPPSC/{Subject}/
│
├── memory/students/{id}/    # Per-student state (JSON)
│   ├── profile.json
│   ├── topic-stats.json
│   ├── history.json
│   ├── active-plan.json
│   ├── revision-queue.json
│   └── sessions/
│
├── syllabus/                # Exam structures + topic weights
├── inbox/                   # Drop zone for incoming requests
├── needs_action/            # Claude's processing queue
├── plans/                   # Claude's reasoning artifacts
├── pending_approval/        # Awaiting human review
├── approved/                # Approved → orchestrator executes
├── rejected/                # Declined actions
├── done/                    # Completed items
├── logs/audit/              # Structured JSON audit trail
│
├── Dashboard.md             # Real-time student state view
├── Business_Goals.md        # KPI tracker + weekly audit logic
└── Company_Handbook.md      # AI rules of engagement
```

---

## Skill Inventory (35 Skills + 7 Subagents)

### Core Skills
| Skill | Purpose |
|---|---|
| `student-profile-loader` | Load student context from memory |
| `question-bank-querier` | Retrieve questions by criteria |
| `answer-evaluator` | Evaluate MCQ responses |
| `performance-tracker` | Persist results to memory |
| `exam-readiness-calculator` | Calculate ERI (0–100) |
| `weak-area-identifier` | Find topics needing practice |

### Tutoring Skills
| Skill | Purpose |
|---|---|
| `diagnostic-assessment-generator` | Baseline tests for new students |
| `adaptive-test-generator` | Personalized tests weighted to weak areas |
| `study-plan-generator` | Personalized study schedules |
| `progress-report-generator` | Session-by-session summaries |
| `mock-exam-generator` | Full 100-question timed exams |
| `mock-exam-evaluator` | Comprehensive mock scoring |
| `exam-pressure-simulator` | Time pressure simulation |

### Autonomous Coaching Skills (Phase 4)
| Skill | Purpose |
|---|---|
| `learning-pattern-detector` | Find optimal study windows |
| `knowledge-gap-predictor` | Predict future weak areas |
| `forgetting-curve-tracker` | Track knowledge decay |
| `revision-cycle-manager` | Spaced repetition scheduling |
| `motivation-monitor` | Detect disengagement |
| `autonomous-session-initiator` | Proactive session triggers |
| `study-pattern-optimizer` | Schedule optimization |
| `exam-countdown-calibrator` | Smart urgency adjustment |
| `deep-dive-analyzer` | Root-cause weakness analysis |

### Engagement Skills
| Skill | Purpose |
|---|---|
| `whatsapp-message-sender` | Send messages via WhatsApp MCP |
| `daily-question-selector` | Daily question with rotation tracking |
| `social-post-generator` | LinkedIn post generation |
| `eri-badge-generator` | Shareable ERI achievement badges |
| `approval-workflow` | Human-in-the-loop file routing |
| `scheduled-task-runner` | Cron-like task execution |

### Subagents
| Subagent | Purpose |
|---|---|
| `assessment-examiner` | Evaluate MCQs, calculate ERI, identify weak areas |
| `study-strategy-planner` | Orchestrate personalized study plans |
| `progress-reporting-coordinator` | Weekly reports with trend analysis |
| `social-media-coordinator` | LinkedIn post workflow with approval |
| `autonomous-coach-coordinator` | Master orchestrator for proactive coaching |
| `mock-exam-conductor` | End-to-end mock exam management |
| `deep-diagnostic-analyst` | Comprehensive weakness analysis |

---

## Exam Readiness Index (ERI)

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

| Band | Score | Meaning |
|---|---|---|
| Not Ready | 0–20 | Significant preparation needed |
| Developing | 21–40 | Building foundational knowledge |
| Approaching | 41–60 | Moderate readiness, gaps remain |
| Ready | 61–80 | Good preparation level |
| Exam Ready | 81–100 | Strong readiness for examination |

---

## Setup

### Prerequisites

- Claude Code (active subscription)
- Python 3.10+
- Node.js v18+ (for MCP servers)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/NailaImran/AI-exam-tutor.git
cd AI-exam-tutor
```

### 2. Install Python dependencies

```bash
pip install -r watchers/requirements.txt
```

### 3. Configure credentials

```bash
copy .env.example .env
```

Edit `.env` and fill in:

```env
DRY_RUN=false
DEV_MODE=false

GITHUB_TOKEN=ghp_your_token
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_ACCESS_TOKEN=your_access_token
LINKEDIN_ACCESS_TOKEN=your_access_token
```

### 4. Configure MCP servers

The `.claude/mcp.json` is pre-configured. MCP servers are launched automatically by Claude Code when you open the project.

### 5. Test in dry-run mode

```bash
DRY_RUN=true python orchestrator.py
```

You should see scheduled tasks registered and folder polling start. No real API calls are made.

### 6. Register as a Windows service (always-on)

Follow the PowerShell commands in `setup/windows_task_scheduler.md` to register the watchdog as a startup service. Or use PM2:

```bash
npm install -g pm2
pm2 start watchdog.py --interpreter python3 --name exam-tutor
pm2 save && pm2 startup
```

---

## How to Use

### Onboard a New Student

1. Create `memory/students/{student_id}/profile.json` (see `memory/students/_templates/`)
2. Drop a diagnostic request into `inbox/`:
   ```
   inbox/diagnostic_request_{student_id}.md
   ```
3. The Ralph Wiggum loop fires automatically — diagnostic test is generated and delivered

### Trigger a Practice Session

Drop a file into `inbox/`:

```markdown
---
type: test_request
student_id: student-001
exam_type: PPSC
subject: Pakistan Studies
question_count: 10
difficulty: adaptive
---
```

Claude processes it, generates the adaptive test, and saves the session to `memory/students/student-001/sessions/`.

### Approve a Pending Action

When Claude writes a file to `pending_approval/`, review it and:
- Move to `approved/` → orchestrator executes within 15 seconds
- Move to `rejected/` → action is skipped and logged

### Run a Mock Exam

Drop into `inbox/`:

```markdown
---
type: mock_exam_request
student_id: student-001
exam_type: PPSC
duration_minutes: 120
---
```

---

## Security

- **DRY_RUN=true** during development — all actions logged, none executed
- **DEV_MODE=true** — uses sandbox/test accounts
- **Permission boundaries** — see `setup/permission_boundaries.md`
  - Auto-approved: sending to known students, reading/writing memory, ERI calculation
  - Always requires approval: LinkedIn publish, bulk WhatsApp, study plan activation, any data deletion
- **Payments** are never auto-retried — always require fresh human approval
- **Audit trail** — every action logged to `logs/audit/YYYY-MM-DD.json` with actor, target, approval status, and result
- **Credentials** — stored in `.env` only (never committed), loaded via `python-dotenv`
- **Oversight schedule**: daily dashboard check, weekly log review, monthly audit, quarterly credential rotation

---

## Hackathon Tier

| Tier | Status |
|---|---|
| Bronze — Foundation | ✅ Complete |
| Silver — Functional Assistant | ✅ Complete |
| Gold — Autonomous Employee | ✅ Complete |
| Platinum — Always-On Cloud | 🔄 In Progress |

---

## Supported Exams & Question Bank

| Exam | Subjects | Questions |
|---|---|---|
| PPSC | Pakistan Studies, General Knowledge, English, Islamic Studies, Current Affairs, Everyday Science, Computer Science | 1,000+ |
| SPSC | Pakistan Studies, General Knowledge, English, Islamic Studies | 400+ |
| KPPSC | Pakistan Studies, General Knowledge, English, Islamic Studies | 300+ |
| **Total** | | **1,793 questions** |

---

## License

MIT — See LICENSE for details.

---

*Built for the Personal AI Employee Hackathon 0 — Panaversity 2026*
