---
name: exam-tutor
description: Digital FTE Competitive Exam Tutor for SPSC, PPSC, and KPPSC provincial public service commission exams. Use this skill bundle when students need exam preparation help including diagnostic assessments, adaptive practice tests, progress tracking, weak area identification, Exam Readiness Index (ERI) calculation, and personalized study plans. Supports the complete exam preparation lifecycle from initial diagnosis to exam readiness.
---

# Exam Tutor Skill Bundle

A comprehensive skill bundle for competitive exam preparation targeting Pakistani provincial public service commissions.

## Supported Exams

| Exam | Full Name | Province |
|------|-----------|----------|
| SPSC | Sindh Public Service Commission | Sindh |
| PPSC | Punjab Public Service Commission | Punjab |
| KPPSC | Khyber Pakhtunkhwa Public Service Commission | KPK |

## Skill Inventory

### CORE Skills (6)

Essential skills for basic tutoring functionality:

| Skill | Purpose | MCP Tools |
|-------|---------|-----------|
| [student-profile-loader](./student-profile-loader/SKILL.md) | Load student context | read_file, list_directory |
| [question-bank-querier](./question-bank-querier/SKILL.md) | Retrieve questions | read_file, list_directory |
| [answer-evaluator](./answer-evaluator/SKILL.md) | Evaluate responses | *None (pure computation)* |
| [performance-tracker](./performance-tracker/SKILL.md) | Persist results | read_file, write_file |
| [exam-readiness-calculator](./exam-readiness-calculator/SKILL.md) | Calculate ERI | read_file |
| [weak-area-identifier](./weak-area-identifier/SKILL.md) | Find weak topics | read_file |

### SUPPORTING Skills (4)

Skills that enhance the tutoring experience:

| Skill | Purpose | MCP Tools |
|-------|---------|-----------|
| [diagnostic-assessment-generator](./diagnostic-assessment-generator/SKILL.md) | Create baseline tests | read_file, list_directory |
| [adaptive-test-generator](./adaptive-test-generator/SKILL.md) | Generate personalized tests | read_file, list_directory |
| [study-plan-generator](./study-plan-generator/SKILL.md) | Create study schedules | read_file, write_file |
| [progress-report-generator](./progress-report-generator/SKILL.md) | Generate reports | read_file, write_file |

### OPTIONAL Skills (2)

Additional capabilities for specific use cases:

| Skill | Purpose | MCP Tools |
|-------|---------|-----------|
| [session-logger](./session-logger/SKILL.md) | Audit logging | write_file, create_directory |
| [syllabus-mapper](./syllabus-mapper/SKILL.md) | Cross-exam mapping | read_file |

## MCP Server Requirements

This skill bundle requires the **filesystem MCP server**:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-server-filesystem",
        "--root", "./",
        "--allowed-paths", ["memory/", "question-bank/", "syllabus/", "logs/"]
      ]
    }
  }
}
```

See [references/mcp-integration.md](./references/mcp-integration.md) for detailed MCP configuration.

## Data Directory Structure

```
project-root/
├── memory/
│   └── students/
│       └── {student_id}/
│           ├── profile.json
│           ├── history.json
│           ├── topic-stats.json
│           ├── active-plan.json
│           ├── sessions/
│           │   └── {session_id}.json
│           └── reports/
│               └── {date}.md
├── question-bank/
│   ├── SPSC/
│   ├── PPSC/
│   └── KPPSC/
│       └── {Subject}/
│           └── {questions}.json
├── syllabus/
│   ├── SPSC/
│   ├── PPSC/
│   └── KPPSC/
│       ├── syllabus-structure.json
│       └── topic-weights.json
└── logs/
    └── sessions/
        └── {student_id}/
            └── {session_id}.json
```

## Exam Readiness Index (ERI)

The ERI is a 0-100 score indicating exam preparedness:

```
ERI = (Accuracy × 0.40) + (Coverage × 0.25) + (Recency × 0.20) + (Consistency × 0.15)
```

### Readiness Bands

| Band | Score | Meaning |
|------|-------|---------|
| `not_ready` | 0-20 | Significant preparation needed |
| `developing` | 21-40 | Building foundational knowledge |
| `approaching` | 41-60 | Moderate readiness, gaps remain |
| `ready` | 61-80 | Good preparation level |
| `exam_ready` | 81-100 | Strong readiness for examination |

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
4. answer-evaluator          → Evaluate
5. performance-tracker       → Initialize stats
6. exam-readiness-calculator → Baseline ERI
7. weak-area-identifier      → Initial weak areas
8. study-plan-generator      → Create plan
```

See [references/skill-orchestration.md](./references/skill-orchestration.md) for complete workflow documentation.

## Reference Documentation

- [schemas.md](./references/schemas.md) - All data structure schemas
- [mcp-integration.md](./references/mcp-integration.md) - MCP server configuration
- [skill-orchestration.md](./references/skill-orchestration.md) - Workflow patterns

## Key Principles

1. **File-based memory** - All state persisted as JSON/Markdown files
2. **Atomic skills** - Each skill has single responsibility
3. **Deterministic** - Same inputs produce same outputs
4. **Composable** - Skills can be orchestrated by parent agent
5. **No user interaction** - Skills execute, parent agent communicates
