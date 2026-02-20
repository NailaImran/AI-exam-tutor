#!/usr/bin/env python3
"""
Ralph Wiggum Stop Hook
======================
Intercepts Claude's exit and re-injects a prompt if there is unfinished work
in the /needs_action/ or /inbox/ folders.

Exit codes:
  0  → allow Claude to stop (nothing pending)
  2  → block exit, inject the message in the JSON output so Claude keeps working

Usage (registered in .claude/settings.json):
  {
    "hooks": {
      "Stop": [{ "matcher": "", "hooks": [{ "type": "command",
        "command": "python .claude/hooks/stop_hook.py" }] }]
    }
  }
"""

import json
import os
import sys
from pathlib import Path

# Project root is two levels above this file (.claude/hooks/stop_hook.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

WATCH_DIRS = [
    PROJECT_ROOT / "needs_action",
    PROJECT_ROOT / "inbox",
    PROJECT_ROOT / "pending_approval",
]

IGNORED_FILES = {".gitkeep", ".gitignore", "README.md"}

MAX_ITERATIONS = int(os.environ.get("RALPH_MAX_ITERATIONS", "10"))
ITERATION_FILE = PROJECT_ROOT / ".claude" / "hooks" / ".ralph_iteration"


def count_pending() -> list[str]:
    """Return list of pending file paths across all watch directories."""
    pending = []
    for watch_dir in WATCH_DIRS:
        if not watch_dir.exists():
            continue
        for f in watch_dir.iterdir():
            if f.is_file() and f.name not in IGNORED_FILES:
                pending.append(str(f.relative_to(PROJECT_ROOT)))
    return pending


def get_iteration() -> int:
    try:
        return int(ITERATION_FILE.read_text().strip())
    except Exception:
        return 0


def set_iteration(n: int):
    ITERATION_FILE.write_text(str(n))


def reset_iteration():
    if ITERATION_FILE.exists():
        ITERATION_FILE.unlink()


def main():
    pending = count_pending()

    if not pending:
        # Nothing to do — allow Claude to exit cleanly
        reset_iteration()
        sys.exit(0)

    iteration = get_iteration() + 1

    if iteration > MAX_ITERATIONS:
        # Safety valve: avoid infinite loops
        reset_iteration()
        print(
            json.dumps({
                "decision": "block",
                "reason": f"Ralph Wiggum safety stop: reached {MAX_ITERATIONS} iterations with {len(pending)} items still pending. Manual review required.",
            })
        )
        sys.exit(2)

    set_iteration(iteration)

    files_list = "\n".join(f"  - {p}" for p in pending[:10])
    more = f"\n  ... and {len(pending) - 10} more" if len(pending) > 10 else ""

    message = (
        f"[Ralph Wiggum Loop — iteration {iteration}/{MAX_ITERATIONS}]\n"
        f"There are {len(pending)} pending item(s) that still need processing:\n"
        f"{files_list}{more}\n\n"
        f"Please process each file:\n"
        f"1. Read the file to understand the request type.\n"
        f"2. Execute the appropriate skill/workflow.\n"
        f"3. Move the file to done/ when complete, or pending_approval/ if human review is needed.\n"
        f"4. Update logs/pipeline/ with the result.\n"
        f"Continue until all items are processed or moved to pending_approval/."
    )

    print(json.dumps({"decision": "block", "reason": message}))
    sys.exit(2)


if __name__ == "__main__":
    main()
