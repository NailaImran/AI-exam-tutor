# Build Instructions: Phase 1 - Foundation

**Feature**: Exam Tutor Phase 1 - Foundation (Bronze Tier)
**Branch**: `001-phase1-foundation`
**Status**: ✅ COMPLETE (All tasks done)
**Created**: 2026-01-20

This document provides step-by-step implementation instructions for Phase 1 of the AI Exam Tutor system. Phase 1 establishes the foundational vault structure, MCP configuration, and core infrastructure needed for student practice sessions.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Build Order](#build-order)
3. [Task Execution](#task-execution)
4. [Validation Commands](#validation-commands)
5. [Integration Points](#integration-points)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **MCP Server**: `@anthropic-ai/mcp-server-filesystem` configured
- **Claude Code**: Latest version with MCP support
- **Git**: Version control (repository already initialized)

### Configuration Files
- `.claude/mcp.json` - MCP filesystem server configuration
- `.gitignore` - Git ignore rules (created)

### MCP Filesystem Configuration

Verify `.claude/mcp.json` contains:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "E:/AI-exam-tutor"]
    }
  }
}
```

**Note**: Update the path to match your project root directory.

---

## Build Order

Phase 1 consists of **6 sequential tasks** organized in a single setup phase. All tasks have been completed.

### Execution Sequence

```
Phase 1: Setup (Shared Infrastructure)
├── T001: Create vault root folder structure
├── T002-T005: Create subdirectories [PARALLEL]
└── T006: Verify MCP filesystem configuration

Status: 6/6 tasks complete ✅
```

### Dependency Graph

```
T001 (Root folders)
  ├── T002 (Question-Bank subdirs) [P]
  ├── T003 (Syllabus subdirs) [P]
  ├── T004 (Logs subdirs) [P]
  └── T005 (Students subdirs) [P]

T001-T005 → T006 (MCP verification)
```

**Legend**:
- `[P]` = Parallelizable task
- `→` = Dependency relationship

---

## Task Execution

### Phase 1: Setup (Shared Infrastructure)

**Goal**: Create vault folder structure and verify MCP configuration.

**Independent Test**: Verify all directories exist and MCP can read/write vault paths.

---

#### ✅ T001: Create Vault Root Folder Structure

**Status**: COMPLETE

**Objective**: Create top-level directories for the Obsidian vault structure.

**Implementation**:

```bash
cd E:/AI-exam-tutor

# Create root directories
mkdir -p inbox
mkdir -p needs_action
mkdir -p done
mkdir -p students
mkdir -p question-bank
mkdir -p syllabus
mkdir -p logs
```

**Windows Alternative**:
```cmd
mkdir inbox needs_action done students question-bank syllabus logs
```

**Validation**:
```bash
ls -la | grep -E "inbox|needs_action|done|students|question-bank|syllabus|logs"
```

**Expected Output**:
```
drwxr-xr-x  inbox/
drwxr-xr-x  needs_action/
drwxr-xr-x  done/
drwxr-xr-x  students/
drwxr-xr-x  question-bank/
drwxr-xr-x  syllabus/
drwxr-xr-x  logs/
```

**Acceptance Criteria**:
- [x] All 7 directories created
- [x] Directories accessible by MCP filesystem server
- [x] No permission errors

---

#### ✅ T002: Create Question-Bank Subdirectories [PARALLEL]

**Status**: COMPLETE

**Objective**: Create exam-specific subdirectories for organizing questions.

**Implementation**:

```bash
cd E:/AI-exam-tutor

# Create Question-Bank structure
mkdir -p question-bank/SPSC/Pakistan-Studies
mkdir -p question-bank/PPSC/Pakistan-Studies
mkdir -p question-bank/KPPSC/Pakistan-Studies
```

**Validation**:
```bash
ls -R question-bank/
```

**Expected Output**:
```
question-bank/:
KPPSC/  PPSC/  SPSC/

question-bank/KPPSC:
Pakistan-Studies/

question-bank/PPSC:
Pakistan-Studies/

question-bank/SPSC:
Pakistan-Studies/
```

**Acceptance Criteria**:
- [x] Three exam directories created (SPSC, PPSC, KPPSC)
- [x] Pakistan-Studies subdirectory in each exam folder
- [x] Consistent naming convention followed

---

#### ✅ T003: Create Syllabus Subdirectories [PARALLEL]

**Status**: COMPLETE

**Objective**: Create exam-specific syllabus directories.

**Implementation**:

```bash
cd E:/AI-exam-tutor

# Create Syllabus structure
mkdir -p syllabus/SPSC
mkdir -p syllabus/PPSC
mkdir -p syllabus/KPPSC
```

**Validation**:
```bash
ls syllabus/
```

**Expected Output**:
```
KPPSC/  PPSC/  SPSC/
```

**Acceptance Criteria**:
- [x] Three exam directories created
- [x] Ready for syllabus-structure.json and topic-weights.json files

---

#### ✅ T004: Create Logs Subdirectory [PARALLEL]

**Status**: COMPLETE

**Objective**: Create logging directory structure.

**Implementation**:

```bash
cd E:/AI-exam-tutor

# Create Logs structure
mkdir -p logs/watcher
```

**Validation**:
```bash
ls logs/
```

**Expected Output**:
```
watcher/
```

**Acceptance Criteria**:
- [x] Watcher subdirectory created
- [x] Ready for log file writes

---

#### ✅ T005: Create Sample Student Sessions Directory [PARALLEL]

**Status**: COMPLETE

**Objective**: Create directory structure for student STU001 with sessions subdirectory.

**Implementation**:

```bash
cd E:/AI-exam-tutor

# Create student directory with sessions
mkdir -p students/STU001/sessions
```

**Validation**:
```bash
ls -R students/
```

**Expected Output**:
```
students/:
STU001/

students/STU001:
sessions/
```

**Acceptance Criteria**:
- [x] STU001 directory created
- [x] sessions subdirectory exists
- [x] Ready for profile.json, history.json, topic-stats.json, eri.json

---

#### ✅ T006: Verify MCP Filesystem Configuration

**Status**: COMPLETE

**Objective**: Confirm MCP filesystem server can read/write vault paths.

**Implementation**:

**Step 1**: Test MCP Read Operation

Use Claude Code to test:
```
Read the file: E:/AI-exam-tutor/.claude/mcp.json
```

**Step 2**: Test MCP Write Operation

Create a test file:
```bash
echo '{"test": "mcp-verification"}' > students/STU001/test.json
```

Use Claude Code to read it:
```
Read the file: E:/AI-exam-tutor/students/STU001/test.json
```

**Step 3**: Test MCP List Directory

Use Claude Code:
```
List directory: E:/AI-exam-tutor/students/STU001
```

**Step 4**: Clean up test file
```bash
rm students/STU001/test.json
```

**Validation**:
- MCP can read `.claude/mcp.json`
- MCP can read files in vault directories
- MCP can list directory contents
- No permission errors

**Acceptance Criteria**:
- [x] MCP filesystem server operational
- [x] Read operations successful
- [x] Write operations successful
- [x] List operations successful
- [x] All vault paths accessible

---

## Validation Commands

### Complete Directory Structure Check

```bash
cd E:/AI-exam-tutor

# Verify all directories exist
find . -type d -name "inbox" -o -name "needs_action" -o -name "done" \
  -o -name "students" -o -name "question-bank" -o -name "syllabus" -o -name "logs"
```

**Expected**: 7 directories found

### MCP Verification Script

Create `scripts/verify-mcp.sh`:

```bash
#!/bin/bash

echo "Testing MCP Filesystem Access..."

# Test 1: Read configuration
if [ -f ".claude/mcp.json" ]; then
  echo "✓ MCP configuration exists"
else
  echo "✗ MCP configuration missing"
  exit 1
fi

# Test 2: Check vault directories
DIRS=("inbox" "needs_action" "done" "students" "question-bank" "syllabus" "logs")
for dir in "${DIRS[@]}"; do
  if [ -d "$dir" ]; then
    echo "✓ Directory exists: $dir"
  else
    echo "✗ Directory missing: $dir"
    exit 1
  fi
done

# Test 3: Check subdirectories
if [ -d "question-bank/PPSC/Pakistan-Studies" ]; then
  echo "✓ Question bank structure verified"
else
  echo "✗ Question bank structure incomplete"
  exit 1
fi

echo ""
echo "All checks passed! ✅"
```

Run:
```bash
chmod +x scripts/verify-mcp.sh
./scripts/verify-mcp.sh
```

---

## Integration Points

### Data Flow Architecture

Phase 1 establishes the **file-based storage layer** that all skills depend on:

```
┌─────────────────────────────────────────────┐
│          Obsidian Vault (File System)      │
│                                             │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐ │
│  │ Students│  │ Question │  │ Syllabus  │ │
│  │ Profiles│  │   Bank   │  │ Structure │ │
│  └────┬────┘  └─────┬────┘  └─────┬─────┘ │
│       │            │              │        │
└───────┼────────────┼──────────────┼────────┘
        │            │              │
        ▼            ▼              ▼
   ┌────────────────────────────────────┐
   │   MCP Filesystem Server            │
   │   (@anthropic-ai/mcp-server-fs)    │
   └────────────────┬───────────────────┘
                    │
                    ▼
   ┌────────────────────────────────────┐
   │         Claude Code Skills         │
   │  • student-profile-loader          │
   │  • question-bank-querier           │
   │  • answer-evaluator                │
   │  • eri-calculator                  │
   │  • performance-tracker             │
   └────────────────────────────────────┘
```

### File Paths Reference

| Entity | Path Pattern | Created By |
|--------|--------------|------------|
| Student Profile | `students/{student_id}/profile.json` | Phase 2 |
| Session History | `students/{student_id}/history.json` | Phase 2 |
| Topic Stats | `students/{student_id}/topic-stats.json` | Phase 2 |
| ERI Score | `students/{student_id}/eri.json` | Phase 2 |
| Session Detail | `students/{student_id}/sessions/{session_id}.json` | Phase 2 |
| Questions | `question-bank/{exam}/{subject}/{topic}.json` | Phase 2 |
| Syllabus | `syllabus/{exam}/syllabus-structure.json` | Phase 2 |
| Topic Weights | `syllabus/{exam}/topic-weights.json` | Phase 2 |
| Watcher Logs | `logs/watcher/{date}.log` | Phase 2 |

### Skill Dependencies

Phase 1 provides the **storage infrastructure**. Skills will be implemented in later phases:

| Skill | Input | Output | MCP Tools Required | Phase |
|-------|-------|--------|-------------------|-------|
| student-profile-loader | student_id | profile object | read_file, list_directory | 2 |
| question-bank-querier | exam, subject, count | questions array | read_file, list_directory | 2 |
| answer-evaluator | questions, answers | score, feedback | none (pure compute) | 2 |
| eri-calculator | student_id | eri object | read_file | 2 |
| performance-tracker | student_id, session | confirmation | read_file, write_file | 2 |

---

## Troubleshooting

### Common Issues

#### Issue 1: MCP Filesystem Server Not Found

**Symptoms**:
- Claude Code cannot read files
- "MCP server not configured" error

**Solution**:
```bash
# Install MCP filesystem server
npx -y @anthropic-ai/mcp-server-filesystem --version

# Verify .claude/mcp.json exists and has correct path
cat .claude/mcp.json
```

#### Issue 2: Permission Denied on Directory Creation

**Symptoms**:
- `mkdir: cannot create directory: Permission denied`

**Solution**:
```bash
# Check current user permissions
ls -la .

# Create directories with explicit permissions
mkdir -m 755 -p students/STU001/sessions
```

#### Issue 3: Directory Already Exists

**Symptoms**:
- `mkdir: cannot create directory 'students': File exists`

**Solution**:
This is expected if tasks were already run. Verify structure:
```bash
# Check if directory exists and is accessible
ls -la students/
```

#### Issue 4: Windows Path Issues

**Symptoms**:
- MCP cannot find files on Windows
- Path separators incorrect

**Solution**:
Use forward slashes in `.claude/mcp.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "E:/AI-exam-tutor"]
    }
  }
}
```

#### Issue 5: Git Not Tracking Empty Directories

**Symptoms**:
- Empty directories not appearing in git status

**Solution**:
Git doesn't track empty directories. Add `.gitkeep` files:
```bash
find . -type d -empty -exec touch {}/.gitkeep \;
```

---

## Phase 1 Completion Checklist

### Infrastructure ✅

- [x] All vault root directories created (inbox, needs_action, done, students, question-bank, syllabus, logs)
- [x] Question-Bank subdirectories created (SPSC, PPSC, KPPSC with Pakistan-Studies)
- [x] Syllabus subdirectories created (SPSC, PPSC, KPPSC)
- [x] Logs subdirectory created (watcher)
- [x] Sample student directory created (STU001 with sessions)
- [x] MCP filesystem configuration verified

### Configuration ✅

- [x] `.claude/mcp.json` configured with filesystem server
- [x] `.gitignore` created with appropriate rules
- [x] Git repository initialized

### Documentation ✅

- [x] SPEC.md completed with requirements
- [x] PLAN.md completed with technical context
- [x] BUILD.md created (this file)
- [x] TASKS.md created with Phase 1 tasks

---

## Phase Gate

Before proceeding to Phase 2, verify:

- [x] All Phase 1 tasks complete (6/6)
- [x] All vault folders exist and accessible
- [x] MCP filesystem can read/write vault paths
- [x] Directory structure matches PLAN.md specification

**✅ Phase 1 Complete → Ready for Phase 2**

---

## Next Steps

Phase 1 has established the foundational infrastructure. The next phase will:

1. **Phase 2: Foundational** (Blocking Prerequisites)
   - Create question bank with 150+ questions
   - Define syllabus structure for all three exams
   - Create skill reference documents
   - Implement core agent skills

2. **Review Phase 2 Specification**
   - Location: `/specs/phase-2-question-bank/`
   - Read: `SPEC.md`, `PLAN.md`, `tasks.md`

3. **Do NOT Start Phase 2 Until**:
   - Phase 1 gate passed ✅
   - Phase 2 specification reviewed
   - Phase 2 tasks understood

---

## References

- **Feature Specification**: [SPEC.md](./SPEC.md)
- **Implementation Plan**: [PLAN.md](./PLAN.md)
- **Task Breakdown**: [TASKS.md](./TASKS.md)
- **Project Constitution**: [/specs/CONSTITUTION.md](/specs/CONSTITUTION.md)
- **Main Documentation**: [/CLAUDE.md](/CLAUDE.md)

---

**Build Status**: ✅ COMPLETE
**Date Completed**: 2026-01-20
**Ready for Phase 2**: YES
