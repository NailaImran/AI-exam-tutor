# MCP Integration Reference

This document describes the Model Context Protocol (MCP) servers required by the Exam Tutor skills.

## Required MCP Servers

### 1. Filesystem MCP Server

The primary MCP server used by all skills for file-based operations.

#### Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-server-filesystem",
        "--root", "./",
        "--allowed-paths", [
          "memory/",
          "question-bank/",
          "syllabus/",
          "logs/"
        ]
      ]
    }
  }
}
```

#### Available Tools

| Tool | Description | Used By |
|------|-------------|---------|
| `mcp__filesystem__read_file` | Read file contents | All skills except answer-evaluator |
| `mcp__filesystem__write_file` | Write/create files | performance-tracker, study-plan-generator, progress-report-generator, session-logger |
| `mcp__filesystem__list_directory` | List directory contents | student-profile-loader, question-bank-querier, diagnostic-assessment-generator |
| `mcp__filesystem__create_directory` | Create directories | session-logger |
| `mcp__filesystem__search_files` | Search for files | question-bank-querier (optional) |

#### Permission Model

```
Read Paths:
  - memory/students/**        (student data)
  - students/**               (student data - alternate location)
  - question-bank/**          (questions)
  - syllabus/**               (syllabus structure)
  - logs/**                   (session logs)
  - inbox/**                  (test requests)

Write Paths:
  - memory/students/**        (student data updates)
  - students/**               (student data - alternate location)
  - logs/**                   (session and watcher logs)
  - done/**                   (processed requests)
  - needs_action/**           (invalid requests)
```

## Skill-to-MCP Tool Mapping

### CORE Skills

| Skill | MCP Tools Used |
|-------|----------------|
| student-profile-loader | read_file, list_directory |
| question-bank-querier | read_file, list_directory, search_files |
| answer-evaluator | *None (pure computation)* |
| performance-tracker | read_file, write_file |
| exam-readiness-calculator | read_file |
| weak-area-identifier | read_file |

### SUPPORTING Skills

| Skill | MCP Tools Used |
|-------|----------------|
| diagnostic-assessment-generator | read_file, list_directory |
| adaptive-test-generator | read_file, list_directory |
| study-plan-generator | read_file, write_file |
| progress-report-generator | read_file, write_file, list_directory |

### OPTIONAL Skills

| Skill | MCP Tools Used |
|-------|----------------|
| session-logger | write_file, create_directory |
| syllabus-mapper | read_file |

## Tool Usage Patterns

### Reading Student Data

```
Tool: mcp__filesystem__read_file
Input: {
  "path": "memory/students/{student_id}/profile.json"
}
Output: JSON string (parse before use)
```

### Writing Session Results

```
Tool: mcp__filesystem__write_file
Input: {
  "path": "memory/students/{student_id}/sessions/{session_id}.json",
  "content": "{...serialized JSON...}"
}
Output: Success/failure status
```

### Listing Question Files

```
Tool: mcp__filesystem__list_directory
Input: {
  "path": "question-bank/PPSC/Pakistan_Studies"
}
Output: Array of filenames
```

## Error Handling

### Common MCP Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `FileNotFoundError` | File does not exist | Check path, create if appropriate |
| `PermissionDeniedError` | Path not in allowed list | Verify MCP configuration |
| `InvalidJSONError` | Malformed JSON in file | Validate JSON before write |
| `DirectoryNotFoundError` | Parent directory missing | Create directory first |

### Retry Strategy

```
Max retries: 3
Backoff: Exponential (100ms, 200ms, 400ms)
Idempotent operations: Retry safe
Non-idempotent operations: Single attempt
```

### 2. GitHub MCP Server

GitHub integration for repository management, issues, and pull requests.

#### Configuration

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

#### Setup Requirements

1. Create a GitHub Personal Access Token:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token (classic) with scopes:
     - `repo` (full repository access)
     - `read:org` (read organization data)
     - `read:user` (read user profile)

2. Set environment variable:
   ```bash
   # Windows
   set GITHUB_TOKEN=ghp_your_token_here

   # Linux/Mac
   export GITHUB_TOKEN=ghp_your_token_here
   ```

#### Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `mcp__github__create_repository` | Create new repository | Initialize exam-tutor repo |
| `mcp__github__get_file_contents` | Read file from repo | Fetch remote question banks |
| `mcp__github__push_files` | Push files to repo | Sync question bank updates |
| `mcp__github__create_issue` | Create GitHub issue | Track student support requests |
| `mcp__github__create_pull_request` | Create PR | Propose question bank additions |
| `mcp__github__search_repositories` | Search repos | Find community question banks |
| `mcp__github__search_issues` | Search issues | Find related discussions |
| `mcp__github__list_commits` | List commits | Track question bank changes |
| `mcp__github__get_issue` | Get issue details | Review feature requests |
| `mcp__github__create_or_update_file` | Create/update file | Update remote syllabus |
| `mcp__github__fork_repository` | Fork a repo | Fork community resources |
| `mcp__github__create_branch` | Create branch | Branch for new exam content |

#### Use Cases for Exam Tutor

| Scenario | GitHub Tool |
|----------|-------------|
| Backup student progress | `push_files` to private repo |
| Share question bank | `create_repository`, `push_files` |
| Import community questions | `get_file_contents`, `fork_repository` |
| Track content requests | `create_issue` |
| Collaborate on syllabus | `create_pull_request` |
| Version control questions | `create_or_update_file`, `list_commits` |

#### Example: Push Question Bank Update

```
Tool: mcp__github__push_files
Input: {
  "owner": "your-username",
  "repo": "exam-tutor-questions",
  "branch": "main",
  "files": [
    {
      "path": "PPSC/Pakistan_Studies/new-questions.json",
      "content": "{...JSON content...}"
    }
  ],
  "message": "Add 20 new Pakistan Studies questions"
}
```

#### Example: Create Issue for Missing Topic

```
Tool: mcp__github__create_issue
Input: {
  "owner": "your-username",
  "repo": "exam-tutor",
  "title": "Missing topic: Environmental Studies",
  "body": "Need questions for Environmental Studies topic in PPSC syllabus."
}
```

### 3. Context7 MCP Server

Context7 provides up-to-date documentation lookup for libraries, frameworks, and APIs directly from their official sources.

#### Configuration

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

#### Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `mcp__context7__resolve-library-id` | Find library ID from name | Lookup library before fetching docs |
| `mcp__context7__get-library-docs` | Get documentation for library | Fetch current API docs, examples |

#### How Context7 Works

1. **Resolve Library ID**: First, find the Context7 library identifier
   ```
   Tool: mcp__context7__resolve-library-id
   Input: { "libraryName": "react" }
   Output: { "libraryId": "/facebook/react" }
   ```

2. **Get Documentation**: Then fetch relevant documentation
   ```
   Tool: mcp__context7__get-library-docs
   Input: {
     "libraryId": "/facebook/react",
     "topic": "hooks"
   }
   Output: Up-to-date documentation on React hooks
   ```

#### Use Cases for Exam Tutor

| Scenario | Context7 Tool |
|----------|---------------|
| Check PDF library APIs | `get-library-docs` for pdfplumber, PyPDF2 |
| Lookup JSON schema validation | `get-library-docs` for jsonschema |
| Find chart library syntax | `get-library-docs` for matplotlib, chart.js |
| Verify date handling | `get-library-docs` for dayjs, date-fns |
| Check testing frameworks | `get-library-docs` for pytest, jest |

#### Example: Lookup PDF Processing Library

```
# Step 1: Resolve library ID
Tool: mcp__context7__resolve-library-id
Input: { "libraryName": "pdfplumber" }

# Step 2: Get specific documentation
Tool: mcp__context7__get-library-docs
Input: {
  "libraryId": "/jsvine/pdfplumber",
  "topic": "extract tables"
}
```

#### Benefits

- **Always Current**: Documentation pulled from live sources
- **Version Aware**: Get docs for specific library versions
- **Reduces Hallucination**: Use real API signatures, not guessed ones
- **Comprehensive**: Covers major libraries and frameworks

## Alternative MCP Servers (Optional)

### Memory MCP Server

For caching frequently accessed data:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-memory"]
    }
  }
}
```

Useful for:
- Caching syllabus structure (rarely changes)
- Caching topic weights
- Session-level caching of student profile

### SQLite MCP Server

For future scalability with structured queries:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-server-sqlite",
        "--database", "./data/exam-tutor.db"
      ]
    }
  }
}
```

Migration path for:
- Question bank storage
- Performance history queries
- Analytics and reporting

## MCP Health Check

Before session start, verify MCP connectivity:

1. Test read operation: `read_file("syllabus/PPSC/syllabus-structure.json")`
2. Test write operation: `write_file("logs/health-check.txt", timestamp)`
3. Test list operation: `list_directory("question-bank/")`

All three must succeed for skills to function properly.
