# Claude Code Rules - AI Exam Tutor

This project is a **Digital FTE Competitive Exam Tutor** for Pakistani provincial public service commission exams (SPSC, PPSC, KPPSC).

## Project Overview

**Purpose:** Diagnose student readiness, administer practice tests, track progress, calculate Exam Readiness Index (ERI), and generate adaptive study plans.

**Target Exams:**
- SPSC (Sindh Public Service Commission)
- PPSC (Punjab Public Service Commission)
- KPPSC (Khyber Pakhtunkhwa Public Service Commission)

## Phase Structure

| Phase | Name | Status | Spec Folder |
|-------|------|--------|-------------|
| **Phase 1** | Foundation | Complete | `specs/phase-1-foundation/` |
| **Phase 2** | Question Bank | Complete | `specs/phase-2-question-bank/` |
| **Phase 3** | Growth Engine | Complete | `specs/phase-3-core-tutoring/` |
| **Phase 4** | Autonomous Coach | In Progress | `specs/phase-4-gold-tier/` |

**Phase Scope:**
- **Phase 1**: Vault structure, 4 core skills, basic Q&A loop
- **Phase 2**: Question bank automation, 1500+ questions
- **Phase 3**: ERI, adaptive tests, WhatsApp, study plans, social media
- **Phase 4**: Full autonomy, mock exams, deep diagnosis, predictive coaching

## Project Structure

```
AI-exam-tutor/
├── .claude/
│   ├── mcp.json                    # MCP server configuration
│   ├── commands/                   # Slash commands (sp.*)
│   └── skills/
│       └── exam-tutor/             # Main skill bundle
│           ├── SKILL.md            # Bundle overview
│           ├── references/         # Schemas, MCP docs, orchestration
│           │
│           ├── student-profile-loader/      (CORE)
│           ├── question-bank-querier/       (CORE)
│           ├── answer-evaluator/            (CORE)
│           ├── performance-tracker/         (CORE)
│           ├── exam-readiness-calculator/   (CORE)
│           ├── weak-area-identifier/        (CORE)
│           │
│           ├── diagnostic-assessment-generator/  (SUPPORTING)
│           ├── adaptive-test-generator/          (SUPPORTING)
│           ├── study-plan-generator/             (SUPPORTING)
│           ├── progress-report-generator/        (SUPPORTING)
│           │
│           ├── session-logger/              (OPTIONAL)
│           └── syllabus-mapper/             (OPTIONAL)
│
├── memory/
│   └── students/{student_id}/
│       ├── profile.json            # Student profile
│       ├── history.json            # Session history
│       ├── topic-stats.json        # Topic-level performance
│       ├── active-plan.json        # Current study plan
│       ├── sessions/               # Individual session details
│       ├── reports/                # Generated progress reports
│       ├── learning-profile.json   # Phase 4: Learning patterns
│       ├── revision-queue.json     # Phase 4: Spaced repetition queue
│       ├── gap-predictions.json    # Phase 4: Predicted weak areas
│       ├── urgency-config.json     # Phase 4: Exam countdown config
│       ├── engagement-tracking.json # Phase 4: Disengagement state
│       ├── daily-interactions.json # Phase 4: Daily message limits
│       └── mock-exams/             # Phase 4: Mock exam sessions
│
├── question-bank/
│   ├── SPSC/{Subject}/*.json
│   ├── PPSC/{Subject}/*.json
│   └── KPPSC/{Subject}/*.json
│
├── syllabus/
│   ├── cross-exam-mapping.json     # Topic equivalents across exams
│   ├── SPSC/
│   ├── PPSC/
│   └── KPPSC/
│       ├── syllabus-structure.json
│       └── topic-weights.json
│
├── logs/
│   └── sessions/{student_id}/      # Audit logs
│
├── .specify/                       # SpecKit Plus templates
├── history/                        # PHRs and ADRs
└── specs/                          # Feature specifications
```

## Skill Architecture

### Skill Inventory

| Phase | Category | Skill | Purpose |
|-------|----------|-------|---------|
| 1 | CORE | student-profile-loader | Load student context from memory |
| 1 | CORE | question-bank-querier | Retrieve questions by criteria |
| 1 | CORE | answer-evaluator | Evaluate responses (pure computation) |
| 1 | CORE | performance-tracker | Persist results to memory |
| 2 | CORE | exam-readiness-calculator | Calculate ERI (0-100) |
| 2 | CORE | weak-area-identifier | Find topics needing practice |
| 2 | SUPPORTING | diagnostic-assessment-generator | Create baseline tests |
| 2 | SUPPORTING | adaptive-test-generator | Generate personalized tests |
| 3 | SUPPORTING | study-plan-generator | Create study schedules |
| 3 | SUPPORTING | progress-report-generator | Generate progress reports |
| 3 | ENGAGEMENT | whatsapp-message-sender | WhatsApp messaging & test sessions |
| 3 | ENGAGEMENT | daily-question-selector | Select daily questions with rotation |
| 3 | ENGAGEMENT | scheduled-task-runner | Cron-like task execution |
| 3 | ENGAGEMENT | approval-workflow | Human-in-the-loop approvals |
| 3 | ENGAGEMENT | eri-badge-generator | Generate shareable ERI badges |
| 3 | ENGAGEMENT | social-post-generator | LinkedIn post generation |
| 4 | CORE | session-logger | Audit trail for all interactions |
| 4 | CORE | syllabus-mapper | Cross-exam topic mapping |
| 4 | MASTERY | mock-exam-generator | Full timed mock exams |
| 4 | MASTERY | mock-exam-evaluator | Comprehensive mock scoring |
| 4 | MASTERY | exam-pressure-simulator | Time pressure simulation |
| 4 | INTELLIGENCE | deep-dive-analyzer | Root-cause weak area analysis |
| 4 | INTELLIGENCE | learning-pattern-detector | Identify optimal study patterns |
| 4 | INTELLIGENCE | knowledge-gap-predictor | Predict future weak areas |
| 4 | INTELLIGENCE | forgetting-curve-tracker | Track knowledge decay |
| 4 | AUTONOMY | autonomous-session-initiator | Proactive session triggers |
| 4 | AUTONOMY | study-pattern-optimizer | Study schedule optimization |
| 4 | AUTONOMY | revision-cycle-manager | Spaced repetition management |
| 4 | AUTONOMY | exam-countdown-calibrator | Smart urgency adjustment |
| 4 | AUTONOMY | motivation-monitor | Engagement tracking |

### Subagent Inventory (7 Total)

| Subagent | Phase | Purpose |
|----------|-------|---------|
| assessment-examiner | 2 | Evaluate MCQs, calculate ERI, identify weak areas |
| study-strategy-planner | 3 | Orchestrate study plan creation with approval |
| progress-reporting-coordinator | 3 | Weekly report generation and delivery |
| social-media-coordinator | 3 | LinkedIn post workflow with approval |
| autonomous-coach-coordinator | 4 | Master orchestrator for proactive coaching |
| mock-exam-conductor | 4 | End-to-end mock exam management |
| deep-diagnostic-analyst | 4 | Comprehensive weakness analysis |

### Exam Readiness Index (ERI)

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

| Band | Score | Meaning |
|------|-------|---------|
| not_ready | 0-20 | Significant preparation needed |
| developing | 21-40 | Building foundational knowledge |
| approaching | 41-60 | Moderate readiness, gaps remain |
| ready | 61-80 | Good preparation level |
| exam_ready | 81-100 | Strong readiness for examination |

## MCP Integration

This project uses five MCP servers: **filesystem** (core operations), **github** (version control), **context7** (documentation lookup), **whatsapp** (Phase 3 messaging), and **linkedin** (Phase 3 social posts).

### Configuration (`.claude/mcp.json`)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "E:/AI-exam-tutor"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### GitHub Setup

Set the `GITHUB_TOKEN` environment variable with a Personal Access Token:
```bash
# Windows
set GITHUB_TOKEN=ghp_your_token_here

# Linux/Mac
export GITHUB_TOKEN=ghp_your_token_here
```

Required token scopes: `repo`, `read:org`, `read:user`

### Filesystem MCP Tools

| Tool | Purpose | Used By |
|------|---------|---------|
| `mcp__filesystem__read_file` | Read JSON/MD files | All skills except answer-evaluator |
| `mcp__filesystem__write_file` | Write/update files | performance-tracker, study-plan-generator, progress-report-generator |
| `mcp__filesystem__list_directory` | List files | question-bank-querier, diagnostic-assessment-generator |
| `mcp__filesystem__create_directory` | Create directories | session-logger |

### GitHub MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__github__create_repository` | Create new repository |
| `mcp__github__get_file_contents` | Read file from remote repo |
| `mcp__github__push_files` | Push files to repo |
| `mcp__github__create_issue` | Create GitHub issue |
| `mcp__github__create_pull_request` | Create PR |
| `mcp__github__search_repositories` | Search repos |
| `mcp__github__list_commits` | Track changes |
| `mcp__github__create_or_update_file` | Update remote files |
| `mcp__github__fork_repository` | Fork a repo |
| `mcp__github__create_branch` | Create branch |

### Context7 MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__context7__resolve-library-id` | Find library ID from name |
| `mcp__context7__get-library-docs` | Get up-to-date documentation for a library |

Context7 provides real-time documentation lookup to ensure accurate API usage and reduce hallucination.

## Standard Workflows

### Daily Practice Session
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

### New Student Onboarding
```
1. Create profile files
2. diagnostic-assessment-generator → Baseline test
3. [Student completes diagnostic]
4. answer-evaluator               → Evaluate
5. performance-tracker            → Initialize stats
6. exam-readiness-calculator      → Baseline ERI
7. weak-area-identifier           → Initial weak areas
8. study-plan-generator           → Create plan
```

### Phase 3: WhatsApp Daily Question
```
1. scheduled-task-runner      → Trigger at 8 AM PKT
2. daily-question-selector    → Select question with rotation
3. student-profile-loader     → Load student context
4. whatsapp-message-sender    → Send daily_question message
5. [Student replies A/B/C/D]
6. answer-evaluator           → Evaluate response
7. performance-tracker        → Update stats
8. exam-readiness-calculator  → Recalculate ERI
9. whatsapp-message-sender    → Send feedback message
```

### Phase 3: WhatsApp Test Session
```
1. [Student sends "start test"]
2. whatsapp-message-sender    → Start session, create test
3. adaptive-test-generator    → Create 5-question test
4. whatsapp-message-sender    → Send test_start with Q1
5. [Student answers each question]
6. whatsapp-message-sender    → Send test_next_question
7. [After all questions]
8. answer-evaluator           → Batch evaluate
9. performance-tracker        → Save session
10. exam-readiness-calculator → Update ERI
11. whatsapp-message-sender   → Send test_complete
```

### Phase 3: Study Plan Approval
```
1. study-strategy-planner     → Orchestrate workflow
2. weak-area-identifier       → Get priority topics
3. study-plan-generator       → Create plan draft
4. approval-workflow          → Save to needs_action/
5. [Human reviews and approves]
6. approval-workflow          → Move to done/, activate
7. whatsapp-message-sender    → Notify student
```

### Phase 3: LinkedIn Post Generation
```
1. scheduled-task-runner      → Trigger at 9 AM PKT
2. social-media-coordinator   → Orchestrate workflow
3. daily-question-selector    → Select with rotation
4. social-post-generator      → Create formatted post
5. approval-workflow          → Save to needs_action/
6. [Human reviews and approves]
7. approval-workflow          → Publish via LinkedIn MCP
```

### Phase 4: Autonomous Daily Coaching
```
1. autonomous-session-initiator  → Check if session needed
2. learning-pattern-detector     → Get optimal study window
3. motivation-monitor            → Check engagement level
4. revision-cycle-manager        → Get due revision items
5. knowledge-gap-predictor       → Identify at-risk topics
6. [Generate personalized session]
7. whatsapp-message-sender       → Proactively engage student
8. session-logger                → Record session
```

### Phase 4: Full Mock Exam
```
1. mock-exam-generator           → Create full exam (100 questions)
2. exam-pressure-simulator       → Configure time pressure
3. whatsapp-message-sender       → Deliver exam
4. [Student completes mock]
5. mock-exam-evaluator           → Score with breakdown
6. deep-dive-analyzer            → Analyze weak sections
7. exam-countdown-calibrator     → Recalibrate urgency
8. session-logger                → Record completion
```

### Phase 4: Predictive Gap Intervention
```
1. forgetting-curve-tracker      → Identify decaying knowledge
2. knowledge-gap-predictor       → Project future weak areas
3. revision-cycle-manager        → Schedule preventive revision
4. autonomous-session-initiator  → Trigger intervention
5. whatsapp-message-sender       → Notify student
```

## Development Guidelines

### Skill Design Principles

1. **Atomic** - Each skill has single responsibility
2. **Deterministic** - Same inputs produce same outputs
3. **File-based** - All state persisted as JSON/Markdown
4. **Composable** - Skills orchestrated by parent agent
5. **No user interaction** - Skills execute, parent agent communicates

### When Working on Skills

- Read skill SKILL.md before modification
- Maintain input/output schema compatibility
- Update references/schemas.md for data changes
- Test with MCP filesystem operations
- Follow the constraint specifications

### Data Schemas

All data structures are documented in:
- `.claude/skills/exam-tutor/references/schemas.md`

Key schemas:
- Student profile: `memory/students/{id}/profile.json`
- Question format: `question-bank/{exam}/{subject}/*.json`
- Syllabus structure: `syllabus/{exam}/syllabus-structure.json`

## SpecKit Plus Integration

### PHR Routing
- Constitution → `history/prompts/constitution/`
- Feature-specific → `history/prompts/<feature-name>/`
- General → `history/prompts/general/`

### ADR Suggestions
When significant architectural decisions are made, suggest:
```
📋 Architectural decision detected: <brief>
   Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `.claude/skills/exam-tutor/SKILL.md` | Main skill bundle documentation |
| `.claude/skills/exam-tutor/references/schemas.md` | All data schemas |
| `.claude/skills/exam-tutor/references/mcp-integration.md` | MCP configuration |
| `.claude/skills/exam-tutor/references/skill-orchestration.md` | Workflow patterns |
| `.claude/mcp.json` | MCP server configuration |
| `.specify/memory/constitution.md` | Project principles |

## Code Standards

### File Operations
- Always use MCP filesystem tools for reads/writes
- Validate JSON before writing
- Handle missing files gracefully
- Atomic writes for session data

### Question Bank
- Question IDs follow format: `{EXAM}-{SUBJECT_CODE}-{NUMBER}`
- Example: `PPSC-PK-001` (PPSC, Pakistan Studies, Question 1)
- Include correct_answer, topic, difficulty for all questions

### Student Data
- Never delete student history, only append
- Update topic-stats atomically
- Maintain backward compatibility with schemas

## Testing Considerations

When testing skills:
1. Create test student profile in `memory/students/test-student/`
2. Use sample questions from `question-bank/PPSC/`
3. Verify ERI calculation matches formula
4. Check file writes succeed and maintain schema

## Constraints

- Skills must NOT communicate directly with users
- Skills must NOT contain business logic spanning multiple responsibilities
- Skills must NOT decide strategy—only execute
- All file paths relative to project root
- Exam types limited to: SPSC, PPSC, KPPSC

## Active Technologies
- Claude Code Skills (Markdown-based prompts), JSON (data), Markdown (documents)
- MCP Filesystem Server (@anthropic-ai/mcp-server-filesystem)
- MCP GitHub Server (@modelcontextprotocol/server-github)
- MCP Context7 Server (@upstash/context7-mcp)
- Local file system (JSON files in memory/, question-bank/, syllabus/)

## Recent Changes
- **Phase 4 Implementation In Progress** - Autonomous Coach skills and subagents being built
- Completed Phase 4 skills: session-logger, syllabus-mapper, mock-exam-generator, mock-exam-evaluator, exam-pressure-simulator, deep-dive-analyzer, learning-pattern-detector, knowledge-gap-predictor, forgetting-curve-tracker, autonomous-session-initiator, study-pattern-optimizer, revision-cycle-manager, exam-countdown-calibrator, motivation-monitor
- Completed Phase 4 subagents: autonomous-coach-coordinator, mock-exam-conductor, deep-diagnostic-analyst
- Updated cross-exam-mapping.json with complete bidirectional mappings for SPSC/PPSC/KPPSC
- Phase 1-3: Complete | Phase 4: In Progress (Autonomous Coach)
