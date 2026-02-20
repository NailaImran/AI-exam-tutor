"""
whatsapp_watcher.py — WhatsApp reply watcher for the Exam Tutor.

Polls the WhatsApp Business API for incoming student replies and writes
action files into /needs_action/ for Claude to process.

Supported message types:
  - Test answers (A/B/C/D replies during an active session)
  - "start test" trigger
  - "report" or "progress" request
  - "help" request
  - General messages

Usage:
    python watchers/whatsapp_watcher.py

Environment variables required (.env):
    WHATSAPP_PHONE_ID
    WHATSAPP_ACCESS_TOKEN
    WHATSAPP_VERIFY_TOKEN   (for webhook, optional)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "watchers"))

from base_watcher import BaseWatcher  # noqa: E402

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# Trigger keywords and their mapped request types
KEYWORD_MAP = {
    "start test": "whatsapp_test_start",
    "start": "whatsapp_test_start",
    "report": "whatsapp_report_request",
    "progress": "whatsapp_report_request",
    "help": "whatsapp_help_request",
    "study plan": "whatsapp_study_plan_request",
    "plan": "whatsapp_study_plan_request",
}

ANSWER_CHOICES = {"a", "b", "c", "d", "1", "2", "3", "4"}


class WhatsAppWatcher(BaseWatcher):
    """
    Polls WhatsApp Business API for incoming messages.

    Each message is classified by type and written as a structured .md
    action file into /needs_action/ for Claude to process.
    """

    def __init__(self, project_root: str = str(PROJECT_ROOT)):
        super().__init__(project_root, check_interval=30)
        self.phone_id = os.getenv("WHATSAPP_PHONE_ID", "")
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
        self.processed_ids: set[str] = set()
        self.dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        self.dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"

        if not self.phone_id or not self.access_token:
            self.logger.warning(
                "WHATSAPP_PHONE_ID or WHATSAPP_ACCESS_TOKEN not set. "
                "Running in simulation mode."
            )

    def classify_message(self, text: str) -> str:
        """Classify an incoming WhatsApp message by content."""
        lower = text.strip().lower()
        # Single-character answer during a test session
        if lower in ANSWER_CHOICES:
            return "whatsapp_test_answer"
        for keyword, req_type in KEYWORD_MAP.items():
            if keyword in lower:
                return req_type
        return "whatsapp_general"

    def fetch_messages_from_api(self) -> list[dict]:
        """Fetch unread messages from the WhatsApp Cloud API."""
        if not REQUESTS_AVAILABLE:
            self.logger.warning("requests library not installed. pip install requests")
            return []
        if not self.phone_id or not self.access_token:
            return []

        url = f"https://graph.facebook.com/v19.0/{self.phone_id}/messages"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", [])
        except Exception as e:
            self.log_event("ERROR", f"WhatsApp API error: {e}")
            return []

    def check_for_updates(self) -> list[dict]:
        """Return new messages not yet processed."""
        if self.dry_run or self.dev_mode:
            return []  # No real API calls in dry-run/dev mode
        messages = self.fetch_messages_from_api()
        new = [m for m in messages if m.get("id") not in self.processed_ids]
        return new

    def create_action_file(self, message: dict) -> Path:
        """Write a structured .md action file for an incoming WhatsApp message."""
        msg_id = message.get("id", "unknown")
        sender = message.get("from", "unknown")
        text = message.get("text", {}).get("body", "") if isinstance(message.get("text"), dict) else str(message.get("text", ""))
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        req_type = self.classify_message(text)

        filename = f"WA_{req_type}_{sender}_{ts}.md"
        filepath = self.needs_action / filename

        content = (
            f"---\n"
            f"type: {req_type}\n"
            f"source: whatsapp\n"
            f"message_id: {msg_id}\n"
            f"sender: {sender}\n"
            f"text: \"{text}\"\n"
            f"received: {datetime.utcnow().isoformat()}Z\n"
            f"status: pending\n"
            f"---\n\n"
            f"## Incoming WhatsApp Message\n\n"
            f"**From**: {sender}  \n"
            f"**Message**: {text}  \n"
            f"**Classified as**: {req_type}\n\n"
            f"## Required Action\n\n"
        )

        if req_type == "whatsapp_test_answer":
            content += (
                f"1. Load student profile for sender `{sender}`\n"
                f"2. Find their active test session\n"
                f"3. Evaluate answer `{text.upper()}`\n"
                f"4. Send next question or test summary via WhatsApp MCP\n"
            )
        elif req_type == "whatsapp_test_start":
            content += (
                f"1. Load student profile for sender `{sender}`\n"
                f"2. Run adaptive-test-generator skill\n"
                f"3. Send first question via WhatsApp MCP\n"
            )
        elif req_type == "whatsapp_report_request":
            content += (
                f"1. Load student profile for sender `{sender}`\n"
                f"2. Run progress-report-generator skill\n"
                f"3. Send summary via WhatsApp MCP\n"
            )
        else:
            content += (
                f"1. Load student profile for sender `{sender}`\n"
                f"2. Determine appropriate response\n"
                f"3. Reply via WhatsApp MCP\n"
            )

        filepath.write_text(content, encoding="utf-8")
        self.processed_ids.add(msg_id)
        return filepath


if __name__ == "__main__":
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    if dry_run:
        print("[DRY RUN] WhatsAppWatcher would start polling WhatsApp API")
        print(f"  Phone ID: {os.getenv('WHATSAPP_PHONE_ID', 'NOT SET')}")
        print(f"  Interval: 30s")
    else:
        watcher = WhatsAppWatcher()
        watcher.run()
