"""
orchestrator.py — Master Orchestrator for the AI Exam Tutor Digital FTE
========================================================================

Responsibilities:
  1. SCHEDULING    — Trigger timed tasks (daily questions at 8 AM PKT,
                     weekly reports on Sunday, LinkedIn posts at 9 AM PKT)
  2. FOLDER WATCH  — Monitor /inbox/ and /approved/ for new files and
                     trigger Claude Code to process them
  3. PROCESS MGMT  — Spawn and monitor watcher sub-processes
  4. APPROVAL LOOP — Watch /approved/ and /rejected/ and execute or log actions

Usage:
    python orchestrator.py              # Normal mode
    DRY_RUN=true python orchestrator.py # Dry-run (no real actions)

Install dependencies first:
    pip install -r watchers/requirements.txt
"""

import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("Orchestrator")

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "15"))  # seconds

# Folders to watch
INBOX_DIR = PROJECT_ROOT / "inbox"
NEEDS_ACTION_DIR = PROJECT_ROOT / "needs_action"
APPROVED_DIR = PROJECT_ROOT / "approved"
REJECTED_DIR = PROJECT_ROOT / "rejected"
DONE_DIR = PROJECT_ROOT / "done"
PLANS_DIR = PROJECT_ROOT / "plans"
LOGS_DIR = PROJECT_ROOT / "logs" / "pipeline"

IGNORED_FILES = {".gitkeep", ".gitignore", "README.md"}

# Watcher sub-processes to manage
WATCHER_PROCESSES = {
    "inbox_watcher": [sys.executable, str(PROJECT_ROOT / "watchers" / "inbox_watcher.py")],
    "whatsapp_watcher": [sys.executable, str(PROJECT_ROOT / "watchers" / "whatsapp_watcher.py")],
}

# ---------------------------------------------------------------------------
# Audit Logging
# ---------------------------------------------------------------------------
def audit_log(action_type: str, target: str, result: str,
              parameters: dict = None, approval_status: str = "auto",
              approved_by: str = "system"):
    """Write a structured JSON audit log entry."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"{today}.json"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action_type": action_type,
        "actor": "orchestrator",
        "target": target,
        "parameters": parameters or {},
        "approval_status": approval_status,
        "approved_by": approved_by,
        "result": result,
        "dry_run": DRY_RUN,
    }

    # Append to daily JSON log (newline-delimited JSON)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    return entry


# ---------------------------------------------------------------------------
# Claude Code Trigger
# ---------------------------------------------------------------------------
def trigger_claude(prompt: str, context_file: Path = None) -> bool:
    """
    Trigger Claude Code to process a task.
    In dry-run mode, just logs what would happen.
    """
    if DRY_RUN:
        logger.info(f"[DRY RUN] Would trigger Claude with: {prompt[:80]}...")
        return True

    cmd = ["claude", "--print", "--no-stream", prompt]
    if context_file:
        cmd += ["--context", str(context_file)]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            audit_log("claude_trigger", prompt[:60], "success")
            return True
        else:
            logger.error(f"Claude returned non-zero: {result.stderr[:200]}")
            audit_log("claude_trigger", prompt[:60], f"error: {result.stderr[:100]}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Claude trigger timed out after 5 minutes")
        audit_log("claude_trigger", prompt[:60], "timeout")
        return False
    except FileNotFoundError:
        logger.warning("'claude' command not found — is Claude Code installed?")
        return False


# ---------------------------------------------------------------------------
# Folder Processors
# ---------------------------------------------------------------------------
def process_needs_action():
    """Check /needs_action/ for pending files and trigger Claude."""
    if not NEEDS_ACTION_DIR.exists():
        return

    pending = [
        f for f in NEEDS_ACTION_DIR.iterdir()
        if f.is_file() and f.name not in IGNORED_FILES
    ]

    if not pending:
        return

    logger.info(f"Found {len(pending)} item(s) in needs_action/")
    prompt = (
        f"Process all pending files in needs_action/. "
        f"For each file: read it, execute the appropriate exam tutor skill, "
        f"move sensitive actions to pending_approval/, and move completed items to done/. "
        f"Files: {[f.name for f in pending]}"
    )
    trigger_claude(prompt)


def process_approved():
    """Check /approved/ and execute approved actions."""
    if not APPROVED_DIR.exists():
        return

    approved = [
        f for f in APPROVED_DIR.iterdir()
        if f.is_file() and f.name not in IGNORED_FILES
    ]

    for approval_file in approved:
        logger.info(f"Processing approved action: {approval_file.name}")
        prompt = (
            f"An action has been approved by the human operator. "
            f"Read {approval_file} and execute the approved action using the appropriate MCP tool. "
            f"Then move the file to done/ and log the result."
        )
        success = trigger_claude(prompt)
        if success:
            audit_log("approved_action", approval_file.name, "executed", approval_status="approved", approved_by="human")


def process_rejected():
    """Check /rejected/ and log rejected actions."""
    if not REJECTED_DIR.exists():
        return

    rejected = [
        f for f in REJECTED_DIR.iterdir()
        if f.is_file() and f.name not in IGNORED_FILES
    ]

    for rejection_file in rejected:
        logger.info(f"Logging rejected action: {rejection_file.name}")
        audit_log("rejected_action", rejection_file.name, "skipped", approval_status="rejected", approved_by="human")
        done_path = DONE_DIR / f"REJECTED_{rejection_file.name}"
        if not DRY_RUN:
            rejection_file.rename(done_path)


# ---------------------------------------------------------------------------
# Scheduled Tasks
# ---------------------------------------------------------------------------
def daily_question_task():
    """8:00 AM PKT — Send daily question to all active students via WhatsApp."""
    logger.info("Scheduled: Daily question task triggered")
    prompt = (
        "Execute the daily question workflow: "
        "1. Run daily-question-selector skill to pick today's question with rotation. "
        "2. For each active student in memory/students/, send the question via WhatsApp MCP. "
        "3. Log all sends to logs/pipeline/. "
        "4. If approval is needed for any message, write to pending_approval/."
    )
    trigger_claude(prompt)
    audit_log("scheduled_task", "daily_question", "triggered")


def weekly_report_task():
    """Sunday 9:00 PM PKT — Generate weekly progress reports."""
    logger.info("Scheduled: Weekly report task triggered")
    prompt = (
        "Execute the weekly report workflow: "
        "1. For each student in memory/students/, run progress-report-generator skill. "
        "2. Save reports to memory/students/{id}/reports/. "
        "3. Create approval request in pending_approval/ for sending reports via WhatsApp. "
        "4. Update Dashboard.md with this week's aggregate stats."
    )
    trigger_claude(prompt)
    audit_log("scheduled_task", "weekly_report", "triggered")


def linkedin_post_task():
    """9:00 AM PKT daily — Generate and queue LinkedIn post."""
    logger.info("Scheduled: LinkedIn post task triggered")
    prompt = (
        "Execute the LinkedIn post workflow: "
        "1. Run social-media-coordinator subagent. "
        "2. Select a question with daily-question-selector (LinkedIn rotation). "
        "3. Generate post with social-post-generator skill. "
        "4. Write approval request to pending_approval/LINKEDIN_{date}.md. "
        "Do NOT publish without approval."
    )
    trigger_claude(prompt)
    audit_log("scheduled_task", "linkedin_post", "triggered")


def setup_schedule():
    """Register all scheduled tasks."""
    if not SCHEDULE_AVAILABLE:
        logger.warning("'schedule' package not installed — scheduled tasks disabled. pip install schedule")
        return

    # Times in PKT (UTC+5) — schedule library uses local time
    # Adjust if your server is in UTC by subtracting 5 hours
    schedule.every().day.at("08:00").do(daily_question_task)
    schedule.every().day.at("09:00").do(linkedin_post_task)
    schedule.every().sunday.at("21:00").do(weekly_report_task)

    logger.info("Scheduled tasks registered:")
    logger.info("  08:00 PKT -> Daily Question (WhatsApp)")
    logger.info("  09:00 PKT -> LinkedIn Post (pending approval)")
    logger.info("  21:00 PKT Sunday -> Weekly Reports (pending approval)")


# ---------------------------------------------------------------------------
# Sub-process Management
# ---------------------------------------------------------------------------
_watcher_procs: dict[str, subprocess.Popen] = {}


def start_watchers():
    """Launch watcher sub-processes."""
    env = os.environ.copy()

    for name, cmd in WATCHER_PROCESSES.items():
        if DRY_RUN:
            logger.info(f"[DRY RUN] Would start watcher: {name}")
            continue
        try:
            proc = subprocess.Popen(cmd, cwd=str(PROJECT_ROOT), env=env)
            _watcher_procs[name] = proc
            logger.info(f"Started watcher: {name} (PID {proc.pid})")
            audit_log("process_start", name, f"pid={proc.pid}")
        except FileNotFoundError as e:
            logger.error(f"Could not start {name}: {e}")


def check_watcher_health():
    """Restart any watcher that has died."""
    env = os.environ.copy()

    for name, cmd in WATCHER_PROCESSES.items():
        proc = _watcher_procs.get(name)
        if proc is None:
            continue
        if proc.poll() is not None:  # process has exited
            logger.warning(f"Watcher {name} died (exit={proc.returncode}), restarting...")
            audit_log("process_restart", name, f"died with exit={proc.returncode}")
            try:
                new_proc = subprocess.Popen(cmd, cwd=str(PROJECT_ROOT), env=env)
                _watcher_procs[name] = new_proc
                logger.info(f"Restarted {name} (PID {new_proc.pid})")
            except Exception as e:
                logger.error(f"Failed to restart {name}: {e}")


# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------
def main():
    logger.info("=" * 60)
    logger.info("AI Exam Tutor Orchestrator starting")
    logger.info(f"  Project root : {PROJECT_ROOT}")
    logger.info(f"  Dry-run mode : {DRY_RUN}")
    logger.info(f"  Dev mode     : {DEV_MODE}")
    logger.info(f"  Poll interval: {POLL_INTERVAL}s")
    logger.info("=" * 60)

    audit_log("orchestrator_start", "main", "started")

    if not DRY_RUN:
        start_watchers()

    setup_schedule()

    iteration = 0
    while True:
        try:
            iteration += 1

            # Process file-based workflows
            process_needs_action()
            process_approved()
            process_rejected()

            # Run scheduled tasks
            if SCHEDULE_AVAILABLE:
                schedule.run_pending()

            # Health check watchers every 5 minutes
            if iteration % (300 // POLL_INTERVAL) == 0:
                check_watcher_health()

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Orchestrator stopped by user")
            audit_log("orchestrator_stop", "main", "stopped_by_user")
            # Clean up watcher processes
            for name, proc in _watcher_procs.items():
                proc.terminate()
                logger.info(f"Terminated {name}")
            break
        except Exception as e:
            logger.error(f"Orchestrator error: {e}", exc_info=True)
            audit_log("orchestrator_error", "main", str(e))
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
