"""
security.py — Security utilities for the AI Exam Tutor Digital FTE
===================================================================

Provides:
  - DEV_MODE / DRY_RUN flag enforcement
  - Permission boundary checks (auto-approve vs always-require-approval)
  - Audit log writer (structured JSON, Section 6.3 of hackathon spec)
  - Credential safety checks
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment flags
# ---------------------------------------------------------------------------
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

if DRY_RUN:
    logger.info("[SECURITY] DRY_RUN=true — no real external actions will be taken")
if DEV_MODE:
    logger.info("[SECURITY] DEV_MODE=true — using sandbox/test accounts")

# ---------------------------------------------------------------------------
# Permission Boundaries
# ---------------------------------------------------------------------------
# Actions that can be auto-approved without human review
AUTO_APPROVE = {
    "whatsapp_send_known_student",   # message to a registered student
    "whatsapp_send_question",        # daily question to active student
    "log_write",                     # writing to local log files
    "memory_read",                   # reading student memory files
    "memory_write_session",          # writing session results
    "report_generate",               # generating (not sending) a report
    "eri_calculate",                 # pure computation
}

# Actions that ALWAYS require human approval via /pending_approval/ workflow
ALWAYS_REQUIRE_APPROVAL = {
    "whatsapp_send_new_contact",     # message to a number not in student list
    "whatsapp_bulk_send",            # sending to multiple students at once
    "linkedin_publish",              # publishing a LinkedIn post
    "study_plan_activate",           # activating a new study plan
    "weekly_report_send",            # sending weekly reports to students
    "student_profile_delete",        # deleting any student data
    "question_bank_modify",          # editing questions
}


def check_permission(action: str, context: dict = None) -> tuple[bool, str]:
    """
    Check if an action can proceed automatically or needs human approval.

    Returns:
        (can_proceed: bool, reason: str)
    """
    if DRY_RUN:
        return False, f"DRY_RUN mode — action '{action}' logged but not executed"

    if action in ALWAYS_REQUIRE_APPROVAL:
        return False, f"Action '{action}' always requires human approval. Write to pending_approval/."

    if action in AUTO_APPROVE:
        return True, f"Action '{action}' is pre-approved"

    # Unknown action — default to requiring approval (fail-safe)
    return False, f"Unknown action '{action}' — defaulting to require approval (fail-safe)"


# ---------------------------------------------------------------------------
# Audit Log Writer
# ---------------------------------------------------------------------------
def write_audit_log(
    project_root: Path,
    action_type: str,
    actor: str,
    target: str,
    parameters: dict = None,
    approval_status: str = "auto",
    approved_by: str = "system",
    result: str = "success",
):
    """
    Write a structured JSON audit log entry.

    Format follows hackathon spec Section 6.3:
    {
      "timestamp": "ISO8601",
      "action_type": "...",
      "actor": "claude_code|orchestrator|watchdog",
      "target": "...",
      "parameters": {},
      "approval_status": "approved|rejected|auto|pending",
      "approved_by": "human|system|watchdog",
      "result": "success|error|dry_run"
    }
    """
    log_dir = project_root / "logs" / "audit"
    log_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}.json"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action_type": action_type,
        "actor": actor,
        "target": target,
        "parameters": parameters or {},
        "approval_status": approval_status,
        "approved_by": approved_by,
        "result": "dry_run" if DRY_RUN else result,
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    return entry


# ---------------------------------------------------------------------------
# Credential Safety
# ---------------------------------------------------------------------------
REQUIRED_ENV_VARS = [
    "WHATSAPP_PHONE_ID",
    "WHATSAPP_ACCESS_TOKEN",
    "LINKEDIN_ACCESS_TOKEN",
    "GITHUB_TOKEN",
]


def check_credentials() -> dict[str, bool]:
    """Check which required credentials are set (without logging their values)."""
    status = {}
    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var, "")
        status[var] = bool(value and not value.startswith("your_"))
    return status


def assert_no_plain_text_secrets(project_root: Path):
    """
    Scan for common credential anti-patterns in project files.
    Logs warnings but does not raise — just informs.
    """
    dangerous_patterns = [
        "ghp_",           # GitHub token prefix
        "Bearer eyJ",     # JWT token
        "access_token=",  # URL-embedded token
    ]
    suspicious = []
    for ext in ("*.json", "*.md", "*.py", "*.txt"):
        for f in project_root.rglob(ext):
            if ".git" in str(f) or ".env" in str(f):
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                for pattern in dangerous_patterns:
                    if pattern in content:
                        suspicious.append((str(f.relative_to(project_root)), pattern))
            except Exception:
                pass

    if suspicious:
        for filepath, pattern in suspicious:
            logger.warning(f"[SECURITY] Possible credential in {filepath} (matched: {pattern!r})")
    return suspicious
