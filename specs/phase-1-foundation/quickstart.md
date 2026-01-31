# Quickstart: Exam Tutor Phase 1

**Feature**: 001-phase1-foundation
**Date**: 2026-01-17

## Prerequisites

- Claude Code CLI installed
- Obsidian desktop application
- MCP filesystem server configured

## Quick Setup (5 minutes)

### 1. Verify MCP Configuration

Check `.claude/mcp.json` exists with filesystem server:

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

### 2. Open Vault in Obsidian

1. Open Obsidian
2. Open folder as vault: `E:/AI-exam-tutor`
3. Trust the vault when prompted

### 3. Create Your Student Profile

Create folder and file: `Students/STU001/profile.json`

```json
{
  "$schema": "exam-tutor/student-profile/v1",
  "student_id": "STU001",
  "name": "Your Name",
  "email": "your@email.com",
  "exam_target": "PPSC",
  "created_at": "2026-01-17T10:00:00Z",
  "updated_at": "2026-01-17T10:00:00Z",
  "preferences": {
    "daily_time_minutes": 60,
    "difficulty_preference": "adaptive"
  },
  "status": "active"
}
```

### 4. Start Your First Practice Test

Create file: `Inbox/test-request.md`

```markdown
# Test Request

**Student ID**: STU001
**Exam Type**: PPSC
**Subject**: Pakistan Studies
**Difficulty**: mixed
**Question Count**: 5
```

### 5. Complete the Test

Claude will generate questions. Answer in the test file:

```markdown
## My Answers

1. B
2. A
3. C
4. D
5. A
```

### 6. View Your Results

After evaluation:
- Results saved to `Students/STU001/sessions/`
- ERI score displayed in `Dashboard.md`
- Check your readiness band!

---

## Folder Structure Reference

```
ExamTutor-Vault/
├── Dashboard.md          ← Your home page
├── Company_Handbook.md   ← System documentation
├── Inbox/               ← Drop test requests here
├── Done/                ← Completed requests
├── Students/STU001/     ← Your data
│   ├── profile.json
│   ├── history.json
│   └── sessions/
├── Question-Bank/PPSC/  ← Practice questions
└── Syllabus/PPSC/       ← Exam structure
```

---

## Common Commands

| Action | How To |
|--------|--------|
| Start practice | Create `Inbox/test-request.md` |
| View ERI | Open `Dashboard.md` |
| Check history | Open `Students/STU001/history.json` |
| See handbook | Open `Company_Handbook.md` |

---

## Troubleshooting

### "Student not found"
- Verify `Students/{id}/profile.json` exists
- Check student_id matches in request

### "No questions available"
- Check `Question-Bank/PPSC/PakistanStudies/` has JSON files
- Verify subject name matches exactly

### MCP not working
- Restart Claude Code
- Check mcp.json syntax
- Verify file paths are correct

---

## Next Steps

1. Complete 3+ practice sessions for accurate ERI
2. Try different topics to improve coverage
3. Practice daily for best recency score
4. Review weak areas shown in Dashboard
