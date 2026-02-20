# Permission Boundaries

Defines which actions the AI can take automatically vs. which require human approval.

## Auto-Approved Actions (No Human Review Required)

| Action | Description |
|--------|-------------|
| `whatsapp_send_known_student` | Send a message to a registered student number |
| `whatsapp_send_question` | Send daily question to an active student |
| `log_write` | Write to local log files |
| `memory_read` | Read student profile/history files |
| `memory_write_session` | Save session results |
| `report_generate` | Generate a report (not send) |
| `eri_calculate` | Compute Exam Readiness Index |

## Always Require Human Approval (via /pending_approval/)

| Action | Reason |
|--------|--------|
| `whatsapp_send_new_contact` | Unknown recipient — must verify |
| `whatsapp_bulk_send` | Mass messaging — high impact |
| `linkedin_publish` | Public content — reputational risk |
| `study_plan_activate` | Changes student's learning path |
| `weekly_report_send` | Sending data to external parties |
| `student_profile_delete` | Irreversible data deletion |
| `question_bank_modify` | Modifies shared content |

## How Approval Works

1. Claude detects an action requiring approval
2. Writes `APPROVAL_{action}_{date}.md` to `/pending_approval/`
3. Human reviews the file and moves it to:
   - `/approved/` → Orchestrator executes the action
   - `/rejected/` → Action is skipped, logged to audit

## Oversight Schedule

| Frequency | Action |
|-----------|--------|
| Daily     | 2-minute check of Dashboard.md |
| Weekly    | Review `/logs/audit/YYYY-MM-DD.json` |
| Monthly   | Full audit of all actions taken |
| Quarterly | Rotate API credentials |
