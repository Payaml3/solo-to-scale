"""Stop hook: a slice newly marked done on this branch needs HANDOFF.md updated too.

Reads the machine-readable slice file named by `slices_file` in .claude/governance.json
(default founder/slices.json: {"slices": [{"id": ..., "status": "done" | ...}]}). If the repo has no
such file, this hook is a no-op. Exits 2 with a reason (both tools then keep going and read it) only
when a slice is newly done and HANDOFF.md is unchanged since the default branch.
Loop guards: Claude Code's and Codex's `stop_hook_active`, plus our own once-per-HEAD marker.
Any error exits 0.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c  # noqa: E402

MESSAGE = "A slice is marked done but HANDOFF.md is not updated: run the handoff skill (full mode)."


def done_slices(text: str | None) -> set[str]:
    try:
        data = json.loads(text or "{}")
    except ValueError:
        return set()
    slices = data.get("slices", []) if isinstance(data, dict) else []
    return {str(s.get("id")) for s in slices if isinstance(s, dict) and s.get("status") == "done"}


def base_commit(root: Path) -> str | None:
    for ref in ("origin/HEAD", "origin/main", "main", "origin/master", "master"):
        base = c.git(root, "merge-base", ref, "HEAD")
        if base:
            return base
    return None


def needs_handoff(root: Path) -> bool:
    rel = str(c.load_config(root).get("slices_file") or "")
    if not rel or not (root / rel).is_file():
        return False  # no machine-readable slice status yet: no-op
    base = base_commit(root)
    if not base:
        return False
    newly = done_slices(c.git(root, "show", f"HEAD:{rel}")) - done_slices(c.git(root, "show", f"{base}:{rel}"))
    if not newly:
        return False
    return c.git(root, "diff", "--name-only", base, "HEAD", "--", "HANDOFF.md") == ""


def main(argv: list[str] | None = None) -> int:
    try:
        c.parse_agent(argv)
        data = c.read_stdin_json(sys.stdin)
        if data.get("stop_hook_active"):
            return 0
        root = c.project_dir(data)
        if not needs_handoff(root):
            return 0
        marker = c.state_path(root, str(data.get("session_id") or "unknown"), "stop")
        head = c.git(root, "rev-parse", "HEAD")
        if c.read_state(marker).get("head") == head:
            return 0  # already asked for this commit: never loop
        c.write_state(marker, {"head": head, "ts": c.now()})
        print(MESSAGE, file=sys.stderr)
        return 2
    except Exception:  # noqa: BLE001 - fail safe
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
