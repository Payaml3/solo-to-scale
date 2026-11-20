"""PreCompact hook (Codex): leave a marker so the next prompt asks for a handoff.

Codex's PreCompact output cannot add model context, so the marker is read by context_guard.py
(UserPromptSubmit) and session_start.py (source "compact"). A short systemMessage tells the founder.
Any error exits 0 with no output.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c  # noqa: E402

NOTICE = "Context is being compacted. The next turn will ask for a handoff (solo-to-scale context guard)."


def main(argv: list[str] | None = None) -> int:
    try:
        c.parse_agent(argv)
        data = c.read_stdin_json(sys.stdin)
        root = c.project_dir(data)
        sid = str(data.get("session_id") or "unknown")
        c.write_state(c.state_path(root, sid, "compact"),
                      {"pending": True, "trigger": data.get("trigger"), "ts": c.now()})
        print(json.dumps({"systemMessage": NOTICE}))
    except Exception:  # noqa: BLE001 - fail safe
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
