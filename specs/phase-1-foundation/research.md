# Research: Exam Tutor Phase 1 - Foundation

**Feature**: 001-phase1-foundation
**Date**: 2026-01-17
**Status**: Complete

## Research Questions Addressed

### R1: Question Bank Content Sources

**Question**: How should we source 50+ questions for PPSC Pakistan Studies?

**Decision**: Create curated question set manually based on publicly available PPSC past paper patterns.

**Rationale**:
- Web scraping of past papers requires parsing PDFs and OCR, adding complexity beyond Phase 1 scope
- Official PPSC website has limited structured content
- Manual curation ensures quality and correct answer verification
- 50 questions is achievable within timeline

**Alternatives Considered**:

| Alternative | Pros | Cons | Verdict |
|-------------|------|------|---------|
| Automated web scraping | Fast, scalable | Complex PDF parsing, OCR errors, quality issues | Rejected |
| Official API integration | Accurate, authoritative | No APIs exist for PPSC | Rejected |
| Crowdsourcing | Large volume possible | Requires user management, Phase 3+ feature | Rejected |
| Manual curation | Quality control, verified answers | Time-intensive, limited scale | **Selected** |

**Implementation Notes**:
- Focus on 5 key Pakistan Studies topics
- Minimum 10 questions per topic
- Include easy/medium/hard difficulty distribution
- All questions must have verified correct answers

---

### R2: File Watcher Implementation

**Question**: How should we implement file watching for /Inbox folder without native OS watchers?

**Decision**: Polling-based approach using MCP filesystem operations within skill orchestration.

**Rationale**:
- MCP filesystem server doesn't provide native file watching events
- Skills can check /Inbox on each session start
- On-demand polling rather than continuous background watching
- Simpler implementation, no external processes required

**Alternatives Considered**:

| Alternative | Pros | Cons | Verdict |
|-------------|------|------|---------|
| Native OS file watchers | Real-time notifications | Requires external code, not MCP-based | Rejected |
| Continuous polling script | Background monitoring | Resource overhead, complexity, requires daemon | Rejected |
| On-demand polling | Simple, MCP-native, no background process | Not real-time | **Selected** |

**Implementation Notes**:
- Parent agent lists /Inbox directory at session start
- Process all .md files found matching test-request pattern
- Move processed files to /Done or /Needs_Action
- User initiates check by starting conversation

---

### R3: ERI First-Session Calculation

**Question**: How should ERI be calculated for students with only one session?

**Decision**: Use baseline defaults for new students with single session.

**Rationale**:
- Providing immediate ERI delivers value faster
- Formula components can be calculated or defaulted:
  - **Accuracy**: Direct calculation from session results
  - **Coverage**: Topics in session / Total syllabus topics
  - **Recency**: 100 (just practiced today)
  - **Consistency**: 100 (single session = no variance)

**Alternatives Considered**:

| Alternative | Pros | Cons | Verdict |
|-------------|------|------|---------|
| Require 3+ sessions | More accurate consistency | Delays value delivery | Rejected |
| Different first-session formula | Accounts for limited data | Adds complexity, confusing | Rejected |
| Use defaults for missing components | Simple, immediate value | May overestimate readiness initially | **Selected** |

**Implementation Notes**:
- Document that first ERI may be optimistic
- Consistency improves accuracy after 3+ sessions
- Show "Based on X sessions" in Dashboard

---

### R4: Syllabus Topic Count for Coverage

**Question**: How many topics should PPSC Pakistan Studies syllabus have for coverage calculation?

**Decision**: Use ~20 topics based on official PPSC syllabus structure.

**Rationale**:
- Provides reasonable coverage denominator
- Matches typical PPSC exam scope
- Topics map directly to question bank organization
- Granular enough to show progress, not too many to overwhelm

**Research Findings**:

PPSC Pakistan Studies typically covers:

| Category | Topics | Count |
|----------|--------|-------|
| Constitutional History | 1947 Constitution, 1956 Constitution, 1962 Constitution, 1973 Constitution, Amendments | 5 |
| Independence Movement | Pakistan Movement, Muslim League, Partition Events | 3 |
| Geography | Physical Geography, Climate, Natural Resources, Administrative Divisions | 4 |
| Economy | Agriculture, Industry, Trade, Economic Policies | 4 |
| Foreign Relations | Relations with India, China, USA, Muslim World | 4 |
| **Total** | | **20** |

**Implementation Notes**:
- Create syllabus-structure.json with 20 topics
- Each topic has weight based on typical exam frequency
- Question bank organized to match topic structure

---

### R5: Question ID Format

**Question**: What format should question IDs follow?

**Decision**: Use format `{EXAM}-{SUBJECT_CODE}-{NNNNN}` (e.g., PPSC-PK-00001)

**Rationale**:
- Unique across all exams and subjects
- Human-readable, indicates source
- Sortable, allows for large question banks
- Consistent with schemas.md reference

**Subject Codes**:
| Subject | Code |
|---------|------|
| Pakistan Studies | PK |
| General Knowledge | GK |
| Current Affairs | CA |
| English | ENG |
| Mathematics | MTH |
| Islamiat | ISL |
| Computer Science | CS |

---

### R6: Session ID Format

**Question**: What format should session IDs follow?

**Decision**: Use format `{STUDENT_ID}-{YYYYMMDD}-{HHmmss}` (e.g., STU001-20260117-143052)

**Rationale**:
- Unique per student
- Chronologically sortable
- Human-readable timestamp
- Ties session to student

---

## Technology Decisions

### MCP Filesystem Server Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-server-filesystem",
        "E:/AI-exam-tutor"
      ]
    }
  }
}
```

### File Format Decisions

| Content Type | Format | Rationale |
|--------------|--------|-----------|
| Structured data | JSON | Machine-readable, schema validation |
| User documents | Markdown | Human-readable, Obsidian-native |
| Test requests | Markdown | User-friendly input format |
| Results display | Markdown | Readable in Obsidian |

---

## Clarifications Resolved

All research questions have been resolved. No outstanding clarifications remain.

| Question | Status | Decision |
|----------|--------|----------|
| Question sources | RESOLVED | Manual curation |
| File watcher | RESOLVED | On-demand polling |
| First-session ERI | RESOLVED | Use defaults |
| Syllabus topics | RESOLVED | 20 topics |
| Question ID format | RESOLVED | EXAM-SUBJ-NNNNN |
| Session ID format | RESOLVED | STUID-DATE-TIME |
