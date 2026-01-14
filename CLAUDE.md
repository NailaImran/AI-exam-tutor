# Claude Code Rules - AI Exam Tutor

This project is a **Digital FTE Competitive Exam Tutor** for Pakistani provincial public service commission exams (SPSC, PPSC, KPPSC).

## Project Overview

**Purpose:** Diagnose student readiness, administer practice tests, track progress, calculate Exam Readiness Index (ERI), and generate adaptive study plans.

**Target Exams:**
- SPSC (Sindh Public Service Commission)
- PPSC (Punjab Public Service Commission)
- KPPSC (Khyber Pakhtunkhwa Public Service Commission)

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
│       └── reports/                # Generated progress reports
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

### Skill Inventory (12 Total)

| Category | Skill | Purpose |
|----------|-------|---------|
| CORE | student-profile-loader | Load student context from memory |
| CORE | question-bank-querier | Retrieve questions by criteria |
| CORE | answer-evaluator | Evaluate responses (pure computation) |
| CORE | performance-tracker | Persist results to memory |
| CORE | exam-readiness-calculator | Calculate ERI (0-100) |
| CORE | weak-area-identifier | Find topics needing practice |
| SUPPORTING | diagnostic-assessment-generator | Create baseline tests |
| SUPPORTING | adaptive-test-generator | Generate personalized tests |
| SUPPORTING | study-plan-generator | Create study schedules |
| SUPPORTING | progress-report-generator | Generate progress reports |
| OPTIONAL | session-logger | Audit logging |
| OPTIONAL | syllabus-mapper | Cross-exam topic mapping |

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

This project uses three MCP servers: **filesystem** (core operations), **github** (version control), and **context7** (documentation lookup).

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
