"""
inbox_watcher.py — File System Watcher for the /inbox/ drop folder.

Monitors /inbox/ for new .md, .json, or .txt files dropped by external
systems (WhatsApp MCP callbacks, manual drops, cron scripts, etc.) and
copies them into /needs_action/ so the orchestrator can trigger Claude.

Usage:
    python watchers/inbox_watcher.py

Install watchdog first:
    pip install watchdog
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Allow running from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "watchers"))

from base_watcher import BaseWatcher  # noqa: E402

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


WATCHED_EXTENSIONS = {".md", ".json", ".txt"}
IGNORED_FILES = {".gitkeep", ".gitignore", "README.md"}


class InboxDropHandler(FileSystemEventHandler):
    """Handles filesystem events in the /inbox/ folder."""

    def __init__(self, watcher: "InboxWatcher"):
        self.watcher = watcher

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        if source.name in IGNORED_FILES:
            return
        if source.suffix.lower() not in WATCHED_EXTENSIONS:
            return
        self.watcher.process_dropped_file(source)


class InboxWatcher(BaseWatcher):
    """
    Watches the /inbox/ drop folder for new files.

    When a file is dropped:
    1. Detect its type (test_request, whatsapp_reply, study_plan_request, etc.)
    2. Enrich with metadata
    3. Copy to /needs_action/ for Claude to process
    4. Log the event
    """

    def __init__(self, project_root: str = str(PROJECT_ROOT)):
        super().__init__(project_root, check_interval=5)
        self.processed = set()

        # Load already-processed files from log to survive restarts
        self._load_processed_history()

    def _load_processed_history(self):
        history_file = self.project_root / ".claude" / "hooks" / ".inbox_processed"
        if history_file.exists():
            try:
                self.processed = set(history_file.read_text().splitlines())
            except Exception:
                self.processed = set()

    def _save_processed_history(self):
        history_file = self.project_root / ".claude" / "hooks" / ".inbox_processed"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        history_file.write_text("\n".join(list(self.processed)[-500:]))  # keep last 500

    def detect_request_type(self, filepath: Path) -> str:
        """Infer the type of request from filename and content."""
        name = filepath.stem.lower()
        if "test" in name or "practice" in name:
            return "test_request"
        if "whatsapp" in name or "wa_" in name:
            return "whatsapp_reply"
        if "study_plan" in name or "plan_request" in name:
            return "study_plan_request"
        if "report" in name:
            return "report_request"
        if "diagnostic" in name:
            return "diagnostic_request"
        return "unknown_request"

    def process_dropped_file(self, source: Path):
        """Process a newly detected file from /inbox/."""
        if str(source) in self.processed:
            return

        request_type = self.detect_request_type(source)
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        dest_name = f"{request_type.upper()}_{source.stem}_{ts}{source.suffix}"
        dest = self.needs_action / dest_name

        try:
            # If it's a plain file, enrich with a metadata header
            if source.suffix == ".md":
                original_content = source.read_text(encoding="utf-8")
                enriched = (
                    f"---\n"
                    f"type: {request_type}\n"
                    f"source: inbox/{source.name}\n"
                    f"detected: {datetime.utcnow().isoformat()}Z\n"
                    f"status: pending\n"
                    f"---\n\n"
                    f"{original_content}"
                )
                dest.write_text(enriched, encoding="utf-8")
            else:
                shutil.copy2(source, dest)

            self.processed.add(str(source))
            self._save_processed_history()
            self.log_event("INFO", f"Inbox drop processed: {source.name} → {dest.name} [{request_type}]")
            self.logger.info(f"Inbox drop: {source.name} → needs_action/{dest.name}")

        except Exception as e:
            self.log_event("ERROR", f"Failed to process {source.name}: {e}")
            self.logger.error(f"Failed to process {source.name}: {e}")

    def check_for_updates(self) -> list:
        """Poll-based fallback: scan /inbox/ for new files."""
        new_files = []
        for f in self.inbox.iterdir():
            if f.is_file() and f.name not in IGNORED_FILES and f.suffix.lower() in WATCHED_EXTENSIONS:
                if str(f) not in self.processed:
                    new_files.append(f)
        return new_files

    def create_action_file(self, item: Path) -> Path:
        self.process_dropped_file(item)
        # Return path of the created needs_action file (approximate)
        return self.needs_action

    def run(self):
        """Run with watchdog event-based detection (preferred) or polling fallback."""
        if WATCHDOG_AVAILABLE:
            self.logger.info("Using watchdog for real-time file detection")
            self.log_event("INFO", "InboxWatcher started (watchdog mode)")
            handler = InboxDropHandler(self)
            observer = Observer()
            observer.schedule(handler, str(self.inbox), recursive=False)
            observer.start()
            try:
                import time
                while True:
                    time.sleep(self.check_interval)
            except KeyboardInterrupt:
                observer.stop()
                self.log_event("INFO", "InboxWatcher stopped by user")
            observer.join()
        else:
            self.logger.warning("watchdog not installed — falling back to polling mode")
            self.logger.warning("Install with: pip install watchdog")
            super().run()


if __name__ == "__main__":
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    if dry_run:
        print("[DRY RUN] InboxWatcher would start monitoring inbox/")
        print(f"  Project root: {PROJECT_ROOT}")
        print(f"  Watching: {PROJECT_ROOT / 'inbox'}")
        print(f"  Writing to: {PROJECT_ROOT / 'needs_action'}")
    else:
        watcher = InboxWatcher()
        watcher.run()
