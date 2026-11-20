"""PostCompact hook (Codex): make sure HANDOFF.md is re-read after a compaction.

Codex's PostCompact output cannot add model context either, so this keeps the marker pending
(the next prompt then asks for the handoff and a re-read of HANDOFF.md) and tells the founder.
Any error exits 0 with no output.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c  # noqa: E402

NOTICE = "Compaction done. The next turn re-reads HANDOFF.md before continuing."


def main(argv: list[str] | None = None) -> int:
    try:
        c.parse_agent(argv)
        data = c.read_stdin_json(sys.stdin)
        root = c.project_dir(data)
        path = c.state_path(root, str(data.get("session_id") or "unknown"), "compact")
        c.write_state(path, {"pending": True, "compacted": c.now()})
        print(json.dumps({"systemMessage": NOTICE}))
    except Exception:  # noqa: BLE001 - fail safe
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
