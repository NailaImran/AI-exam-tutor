"""
retry_handler.py — Error recovery utilities for the AI Exam Tutor
==================================================================

Provides:
  - @with_retry decorator — exponential backoff for transient failures
  - GracefulDegradation — queue-based fallback for offline services
  - Error category classification

Error Categories (from hackathon spec Section 7.1):
  TRANSIENT     → Network timeout, API rate limit → retry with backoff
  AUTH          → Expired token, 401/403          → alert human, pause
  LOGIC         → Wrong answer format, bad data   → human review queue
  DATA          → Corrupted JSON, missing field   → quarantine + alert
  SYSTEM        → Process crash, disk full        → watchdog + restart
"""

import functools
import json
import logging
import time
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Type

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Error Categories
# ---------------------------------------------------------------------------
class ErrorCategory(Enum):
    TRANSIENT = "transient"
    AUTH = "auth"
    LOGIC = "logic"
    DATA = "data"
    SYSTEM = "system"


class TransientError(Exception):
    """Network timeouts, rate limits — safe to retry."""


class AuthError(Exception):
    """Token expired or revoked — pause and alert human."""


class LogicError(Exception):
    """Claude misinterpreted data — route to human review."""


class DataError(Exception):
    """Corrupted or missing data — quarantine the file."""


# ---------------------------------------------------------------------------
# Retry Decorator
# ---------------------------------------------------------------------------
def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple[Type[Exception], ...] = (TransientError, ConnectionError, TimeoutError),
):
    """
    Decorator that retries a function with exponential backoff on transient errors.

    Usage:
        @with_retry(max_attempts=3, base_delay=2)
        def call_whatsapp_api(payload):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if attempt == max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    logger.warning(
                        f"{func.__name__} attempt {attempt}/{max_attempts} failed: {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)
            raise last_error  # unreachable but satisfies linters
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Graceful Degradation Queue
# ---------------------------------------------------------------------------
class GracefulDegradation:
    """
    Queue-based fallback when an external service is unavailable.

    When a service is down:
    - Actions are queued to a local JSON file
    - On recovery, the queue is replayed
    - Payments are NEVER auto-retried (always require fresh approval)

    Usage:
        degradation = GracefulDegradation(project_root)

        # When WhatsApp API is down:
        degradation.queue("whatsapp_send", {"to": "...", "message": "..."})

        # On recovery:
        degradation.replay("whatsapp_send", send_function)
    """

    PAYMENT_ACTIONS = {"payment_send", "invoice_send", "bank_transfer"}

    def __init__(self, project_root: Path):
        self.queue_dir = project_root / "logs" / "degradation_queue"
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def queue_file(self, action_type: str) -> Path:
        return self.queue_dir / f"{action_type}.queue.json"

    def queue(self, action_type: str, payload: dict):
        """Add an action to the degradation queue."""
        if action_type in self.PAYMENT_ACTIONS:
            logger.warning(
                f"[SAFETY] Payment action '{action_type}' will NOT be auto-retried. "
                f"Requires fresh human approval."
            )
            return  # Never auto-retry payments

        qfile = self.queue_file(action_type)
        existing = []
        if qfile.exists():
            try:
                existing = json.loads(qfile.read_text())
            except Exception:
                existing = []

        entry = {
            "queued_at": datetime.now(timezone.utc).isoformat(),
            "action_type": action_type,
            "payload": payload,
            "attempts": 0,
        }
        existing.append(entry)
        qfile.write_text(json.dumps(existing, indent=2))
        logger.info(f"Queued action '{action_type}' for later replay ({len(existing)} in queue)")

    def replay(self, action_type: str, execute_fn: Callable[[dict], bool]) -> int:
        """
        Replay queued actions for an action_type.
        execute_fn should return True on success, False/raise on failure.
        Returns number of successfully replayed actions.
        """
        if action_type in self.PAYMENT_ACTIONS:
            logger.warning(f"Cannot replay payment action '{action_type}' automatically.")
            return 0

        qfile = self.queue_file(action_type)
        if not qfile.exists():
            return 0

        try:
            queue = json.loads(qfile.read_text())
        except Exception:
            logger.error(f"Could not read queue file for {action_type}")
            return 0

        succeeded = []
        failed = []

        for item in queue:
            try:
                ok = execute_fn(item["payload"])
                if ok:
                    succeeded.append(item)
                    logger.info(f"Replayed queued action: {action_type}")
                else:
                    item["attempts"] += 1
                    failed.append(item)
            except Exception as e:
                item["attempts"] += 1
                item["last_error"] = str(e)
                failed.append(item)
                logger.error(f"Failed to replay {action_type}: {e}")

        # Keep only failed items in queue
        if failed:
            qfile.write_text(json.dumps(failed, indent=2))
        else:
            qfile.unlink(missing_ok=True)

        return len(succeeded)


# ---------------------------------------------------------------------------
# Data Quarantine
# ---------------------------------------------------------------------------
def quarantine_file(filepath: Path, project_root: Path, reason: str):
    """
    Move a corrupted/problematic file to /logs/quarantine/ with a metadata note.
    """
    quarantine_dir = project_root / "logs" / "quarantine"
    quarantine_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dest = quarantine_dir / f"{ts}_{filepath.name}"

    try:
        filepath.rename(dest)
        meta = dest.with_suffix(".meta.json")
        meta.write_text(json.dumps({
            "original_path": str(filepath),
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
        }, indent=2))
        logger.warning(f"Quarantined {filepath.name}: {reason}")
    except Exception as e:
        logger.error(f"Failed to quarantine {filepath}: {e}")
