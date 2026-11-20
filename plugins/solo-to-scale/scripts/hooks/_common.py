"""Shared helpers for the solo-to-scale hooks (Claude Code and Codex). Standard library only.

Every hook fails safe: callers wrap main() so that any error exits 0 with no output.
Hooks never make network calls; they read the repository and write only .claude/state/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any

DEFAULTS: dict[str, Any] = {
    "warn_pct": 60,
    "handoff_pct": 75,
    "warn_tokens": 100_000,
    "handoff_tokens": 140_000,
    "context_window_tokens": None,
    "slices_file": "founder/slices.json",
}
FALLBACK_WINDOW = 200_000  # only when neither the config nor the tool gives a window size
STALE_SECONDS = 600
AGENTS = ("claude", "codex")


def parse_agent(argv: list[str] | None) -> str:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--agent", choices=AGENTS, default="claude")
    args, _ = ap.parse_known_args(argv)
    return args.agent


def read_stdin_json(stream: Any) -> dict[str, Any]:
    data = json.loads(stream.read() or "{}")
    return data if isinstance(data, dict) else {}


def project_dir(data: dict[str, Any] | None = None) -> Path:
    """The repository root: $CLAUDE_PROJECT_DIR, else the hook's cwd (walked up to the git root)."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    start = Path((data or {}).get("cwd") or os.getcwd()).resolve()
    for d in (start, *start.parents):
        if (d / ".git").exists() or (d / "AGENTS.md").is_file():
            return d
    return start


def load_config(root: Path) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    try:
        loaded = json.loads((root / ".claude" / "governance.json").read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            cfg.update(loaded)
    except (OSError, ValueError):
        pass
    return cfg


def project_name(root: Path) -> str:
    try:
        name = json.loads((root / "founder" / "project.json").read_text(encoding="utf-8")).get("name")
        return str(name) if name else "Project"
    except (OSError, ValueError, AttributeError):
        return "Project"


def state_path(root: Path, session_id: str, kind: str = "context") -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id or "unknown")
    return root / ".claude" / "state" / f"{kind}-{safe}.json"


def read_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def write_state(path: Path, updates: dict[str, Any]) -> None:
    """Merge `updates` into the state file, keeping keys other writers own."""
    state = read_state(path)
    state.update(updates)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state), encoding="utf-8")
    tmp.replace(path)


def now() -> float:
    return time.time()


def level(pct: float | None, tokens: int | None, cfg: dict[str, Any]) -> str | None:
    """'handoff', 'warn' or None. Each level fires at whichever comes first: percentage or tokens."""

    def hit(pct_key: str, tok_key: str) -> bool:
        p, t = cfg.get(pct_key), cfg.get(tok_key)
        return (pct is not None and p is not None and pct >= p) or (
            tokens is not None and t is not None and tokens >= t
        )

    if hit("handoff_pct", "handoff_tokens"):
        return "handoff"
    if hit("warn_pct", "warn_tokens"):
        return "warn"
    return None


def git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                             encoding="utf-8", timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def context_output(event: str, text: str) -> str:
    return json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}})


HANDOFF_TEXT = ("Context at {pct}% ({tokens} tokens). Stop new work. Run the handoff skill (full mode if "
                "mid-slice), then tell the founder to start a new session.")
WARN_TEXT = ("Context at {pct}% ({tokens} tokens). Finish the current step, start nothing large, "
             "and keep answers short.")
COMPACT_HANDOFF_TEXT = ("The context was just compacted. Stop new work. Run the handoff skill (full mode if "
                        "mid-slice), re-read HANDOFF.md, then tell the founder to start a new session.")
