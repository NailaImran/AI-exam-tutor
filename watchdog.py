"""
watchdog.py — Process Health Monitor for the AI Exam Tutor Digital FTE
=======================================================================

Monitors critical processes (orchestrator, watchers) and restarts them
if they crash. Also sends alert entries to the audit log.

Usage:
    python watchdog.py              # Normal mode
    DRY_RUN=true python watchdog.py # Log only, no restarts

For always-on operation on Windows, register as a Task Scheduler job:
    See: setup/windows_task_scheduler.md
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

PROJECT_ROOT = Path(__file__).resolve().parent
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("Watchdog")

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
CHECK_INTERVAL = int(os.getenv("WATCHDOG_INTERVAL", "60"))  # seconds
MAX_RESTART_ATTEMPTS = int(os.getenv("MAX_RESTART_ATTEMPTS", "5"))

AUDIT_LOG_DIR = PROJECT_ROOT / "logs" / "pipeline"
PID_DIR = PROJECT_ROOT / ".claude" / "hooks"

# Processes that must stay alive
MANAGED_PROCESSES = {
    "orchestrator": {
        "cmd": [sys.executable, str(PROJECT_ROOT / "orchestrator.py")],
        "pid_file": PID_DIR / "orchestrator.pid",
        "restarts": 0,
    },
}


def write_audit(action_type: str, target: str, result: str):
    AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = AUDIT_LOG_DIR / f"{today}.json"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action_type": action_type,
        "actor": "watchdog",
        "target": target,
        "parameters": {},
        "approval_status": "system",
        "approved_by": "watchdog",
        "result": result,
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def read_pid(pid_file: Path) -> int | None:
    try:
        return int(pid_file.read_text().strip())
    except Exception:
        return None


def write_pid(pid_file: Path, pid: int):
    PID_DIR.mkdir(parents=True, exist_ok=True)
    pid_file.write_text(str(pid))


def is_running(pid: int) -> bool:
    """Check if a process with the given PID is still alive."""
    if pid is None:
        return False
    try:
        # On Windows and Unix, sending signal 0 checks existence without killing
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False
    except OSError:
        return False


_running_procs: dict[str, subprocess.Popen] = {}


def start_process(name: str, config: dict) -> bool:
    """Start a managed process and record its PID."""
    if DRY_RUN:
        logger.info(f"[DRY RUN] Would start: {name}")
        return True

    if config["restarts"] >= MAX_RESTART_ATTEMPTS:
        logger.error(
            f"{name} has been restarted {config['restarts']} times. "
            f"Giving up — manual intervention required."
        )
        write_audit("process_abandoned", name, f"exceeded max_restarts={MAX_RESTART_ATTEMPTS}")
        return False

    env = os.environ.copy()
    try:
        proc = subprocess.Popen(
            config["cmd"],
            cwd=str(PROJECT_ROOT),
            env=env,
            stdout=open(PROJECT_ROOT / "logs" / f"{name}.stdout.log", "a"),
            stderr=open(PROJECT_ROOT / "logs" / f"{name}.stderr.log", "a"),
        )
        _running_procs[name] = proc
        write_pid(config["pid_file"], proc.pid)
        config["restarts"] += 1
        logger.info(f"Started {name} (PID {proc.pid}, restart #{config['restarts']})")
        write_audit("process_start", name, f"pid={proc.pid}")
        return True
    except Exception as e:
        logger.error(f"Failed to start {name}: {e}")
        write_audit("process_start_failed", name, str(e))
        return False


def check_all():
    """Check all managed processes and restart dead ones."""
    for name, config in MANAGED_PROCESSES.items():
        proc = _running_procs.get(name)

        if proc is not None:
            # Check if popen process is still running
            if proc.poll() is not None:
                logger.warning(f"{name} exited with code {proc.returncode}. Restarting...")
                write_audit("process_died", name, f"exit_code={proc.returncode}")
                start_process(name, config)
        else:
            # Try to find via PID file (survives orchestrator restarts)
            pid = read_pid(config["pid_file"])
            if pid and is_running(pid):
                logger.info(f"{name} already running (PID {pid}) — not restarting")
            else:
                logger.info(f"{name} not running — starting...")
                start_process(name, config)


def main():
    logger.info("=" * 50)
    logger.info("AI Exam Tutor Watchdog starting")
    logger.info(f"  Dry-run    : {DRY_RUN}")
    logger.info(f"  Check every: {CHECK_INTERVAL}s")
    logger.info(f"  Max restarts: {MAX_RESTART_ATTEMPTS}")
    logger.info("=" * 50)

    write_audit("watchdog_start", "main", "started")

    # Initial start
    check_all()

    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            check_all()
        except KeyboardInterrupt:
            logger.info("Watchdog stopped by user")
            write_audit("watchdog_stop", "main", "stopped_by_user")
            for name, proc in _running_procs.items():
                proc.terminate()
                logger.info(f"Terminated {name}")
            break
        except Exception as e:
            logger.error(f"Watchdog error: {e}", exc_info=True)
            write_audit("watchdog_error", "main", str(e))


if __name__ == "__main__":
    main()
