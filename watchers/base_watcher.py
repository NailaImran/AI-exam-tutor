"""
base_watcher.py — Abstract base class for all AI Exam Tutor watchers.

All watchers follow the same Perception loop:
  1. check_for_updates() → detect new events from external source
  2. create_action_file()  → write a .md file into /needs_action/ or /inbox/
  3. Sleep for check_interval, repeat

The orchestrator then triggers Claude Code to process the /inbox/ folder.
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class BaseWatcher(ABC):
    """Abstract base for all event watchers."""

    def __init__(self, project_root: str, check_interval: int = 60):
        self.project_root = Path(project_root).resolve()
        self.inbox = self.project_root / "inbox"
        self.needs_action = self.project_root / "needs_action"
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        # Ensure target dirs exist
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.needs_action.mkdir(parents=True, exist_ok=True)

        # Audit log path
        self.log_dir = self.project_root / "logs" / "watcher"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return a list of new items detected from the external source."""

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Write a .md action file into /inbox/ or /needs_action/ and return its path."""

    def log_event(self, level: str, message: str):
        """Append a timestamped line to today's watcher log."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{today}.log"
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {level.upper()}: {message}\n")

    def run(self):
        """Main loop — runs indefinitely. Use PM2 or Watchdog to keep alive."""
        self.logger.info(f"Starting {self.__class__.__name__} (interval={self.check_interval}s)")
        self.log_event("INFO", f"{self.__class__.__name__} started")

        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    path = self.create_action_file(item)
                    self.logger.info(f"Action file created: {path.name}")
                    self.log_event("INFO", f"Action file created: {path}")
            except KeyboardInterrupt:
                self.logger.info("Watcher stopped by user.")
                self.log_event("INFO", f"{self.__class__.__name__} stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in watcher loop: {e}", exc_info=True)
                self.log_event("ERROR", str(e))
            time.sleep(self.check_interval)
