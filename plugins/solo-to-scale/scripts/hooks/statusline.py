"""Claude Code status line: project, model, branch, context use, and a WARN or HANDOFF tag.

Also writes .claude/state/context-<session_id>.json for the context guard. Codex has no
command status line, so this script is Claude-only (see the README's parity table).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def usage(data: dict[str, Any], cfg: dict[str, Any]) -> tuple[float | None, int | None, int]:
    cw = data.get("context_window") or {}
    window = int(cfg.get("context_window_tokens") or cw.get("context_window_size") or c.FALLBACK_WINDOW)
    pct = cw.get("used_percentage")
    pct = float(pct) if isinstance(pct, (int, float)) else None
    cur = cw.get("current_usage") or {}
    tokens: int | None = None
    if isinstance(cur, dict) and cur:
        keys = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
        tokens = sum(int(cur.get(k) or 0) for k in keys)
    if tokens is None and pct is not None:
        tokens = round(pct / 100 * window)
    if pct is None and tokens is not None:
        pct = tokens / window * 100
    return pct, tokens, window


def main(argv: list[str] | None = None) -> int:
    try:
        data = c.read_stdin_json(sys.stdin)
        root = c.project_dir({"cwd": (data.get("workspace") or {}).get("project_dir") or data.get("cwd")})
        cfg = c.load_config(root)
        pct, tokens, window = usage(data, cfg)
        sid = str(data.get("session_id") or "unknown")
        c.write_state(c.state_path(root, sid), {"session_id": sid, "used_pct": pct, "used_tokens": tokens,
                                                 "window_tokens": window, "ts": c.now()})
        model = (data.get("model") or {}).get("display_name") or "Claude"
        cwd = Path((data.get("workspace") or {}).get("current_dir") or data.get("cwd") or root)
        branch = c.git(cwd, "rev-parse", "--abbrev-ref", "HEAD") or "-"
        ctx = "ctx --" if pct is None else f"ctx {pct:.0f}%"
        tag = {"warn": " · WARN", "handoff": " · HANDOFF"}.get(c.level(pct, tokens, cfg) or "", "")
        print(f"{c.project_name(root)} · {model} · {branch} · {ctx}{tag}")
    except Exception:  # noqa: BLE001 - fail safe
        print("Claude")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
