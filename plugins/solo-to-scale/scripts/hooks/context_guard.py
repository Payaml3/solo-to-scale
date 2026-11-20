"""UserPromptSubmit hook: warn, then ask for a handoff, as the context fills up.

Claude Code: reads usage from the status line's state file; if that is missing or older than 10
minutes, reads the last assistant message's usage from the transcript. Each level fires once per session.
Codex: its hook input exposes no token usage, so this hook only acts after a compaction. The PreCompact
hook leaves a marker, and the next prompt is asked for a handoff, once.
It never blocks a prompt: any error exits 0 with no output.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def from_transcript(path: str | None) -> int | None:
    if not path:
        return None
    last: int | None = None
    with Path(path).open(encoding="utf-8") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            msg = entry.get("message") if isinstance(entry, dict) else None
            if entry.get("type") != "assistant" or not isinstance(msg, dict):
                continue
            u = msg.get("usage")
            if isinstance(u, dict):
                keys = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
                last = sum(int(u.get(k) or 0) for k in keys)
    return last


def current_usage(data: dict[str, Any], state: dict[str, Any], cfg: dict[str, Any]) -> tuple[float | None, int | None]:
    ts = state.get("ts")
    fresh = isinstance(ts, (int, float)) and c.now() - ts <= c.STALE_SECONDS
    if fresh and (state.get("used_pct") is not None or state.get("used_tokens") is not None):
        return state.get("used_pct"), state.get("used_tokens")
    tokens = from_transcript(data.get("transcript_path"))
    if tokens is None:
        return None, None
    window = int(cfg.get("context_window_tokens") or state.get("window_tokens") or c.FALLBACK_WINDOW)
    return tokens / window * 100, tokens


def claude(data: dict[str, Any], root: Path) -> str | None:
    cfg = c.load_config(root)
    path = c.state_path(root, str(data.get("session_id") or "unknown"))
    state = c.read_state(path)
    pct, tokens = current_usage(data, state, cfg)
    lvl = c.level(pct, tokens, cfg)
    fired = list(state.get("fired") or [])
    if lvl is None or lvl in fired:
        return None
    c.write_state(path, {"fired": sorted({*fired, lvl, "warn"})})  # a handoff also retires the warning
    if pct is None and tokens is not None:
        pct = tokens / c.FALLBACK_WINDOW * 100
    return (c.HANDOFF_TEXT if lvl == "handoff" else c.WARN_TEXT).format(
        pct=f"{pct:.0f}" if pct is not None else "?", tokens=f"{tokens:,}" if tokens is not None else "?")


def codex(data: dict[str, Any], root: Path) -> str | None:
    path = c.state_path(root, str(data.get("session_id") or "unknown"), "compact")
    state = c.read_state(path)
    if not state.get("pending"):
        return None
    c.write_state(path, {"pending": False, "asked": c.now()})
    return c.COMPACT_HANDOFF_TEXT


def main(argv: list[str] | None = None) -> int:
    try:
        agent = c.parse_agent(argv)
        data = c.read_stdin_json(sys.stdin)
        root = c.project_dir(data)
        text = claude(data, root) if agent == "claude" else codex(data, root)
        if text:
            print(c.context_output("UserPromptSubmit", text))
    except Exception:  # noqa: BLE001 - fail safe
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
