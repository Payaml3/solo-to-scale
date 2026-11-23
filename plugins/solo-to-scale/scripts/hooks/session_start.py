"""SessionStart hook (startup, resume, compact): where the build is, in at most 25 lines.

Injects the "Where we are" rows and the next step from HANDOFF.md, the top 3 open founder items
from founder/status.md, the claimed issue's goal chain (if claim.py recorded one) and one line naming
the protocol and the context-guard limits, and how many setup items need the founder (the repo's
tools/doctor.py, offline). After a compaction it adds a re-read note.
Any error exits 0 with no output.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as c  # noqa: E402

MAX_LINES = 25
COMPACT_NOTE = "You were just compacted. Re-read HANDOFF.md and the current task before continuing."


def section(text: str, heading: str) -> list[str]:
    """Lines under the first `## <heading>...` up to the next `## `."""
    out: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip().lower().startswith(heading.lower())
            continue
        if inside:
            out.append(line)
    return out


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def table_rows(lines: list[str]) -> list[str]:
    rows = [ln.strip() for ln in lines if ln.strip().startswith("|")]
    return [r for r in rows[2:] if not set(r) <= set("|-: ")] if len(rows) > 2 else []


def founder_items(status: str) -> list[str]:
    lines = section(status, "Open founder items")
    items = [f"- {r.strip('|').split('|')[0].strip()}" for r in table_rows(lines)]
    items += [ln.strip() for ln in lines if re.match(r"^- ", ln)]
    return [i if len(i) <= 160 else i[:157] + "..." for i in items if i.strip("- ")]


def claimed(root: Path) -> list[str]:
    data = c.read_state(root / ".claude" / "state" / "claimed.json")
    if not data.get("issue"):
        return []
    lines = [f"Claimed issue #{data['issue']}: {data.get('title', '')}".rstrip()]
    lines += [f"  {x}" for x in (data.get("goal_chain") or [])[:5]]
    return lines


def setup(root: Path) -> list[str]:
    """One line when the repo's own doctor (offline: files only) finds setup items for the founder."""
    tools = root / "tools"
    if not (tools / "doctor.py").exists():
        return []
    try:
        sys.path.insert(0, str(tools))
        import doctor  # type: ignore[import-not-found]  # noqa: PLC0415
        todo = doctor.needs_you(doctor.run(root, offline=True))
    except Exception:  # noqa: BLE001 - an old or broken doctor never blocks a session
        return []
    finally:
        if sys.path and sys.path[0] == str(tools):
            sys.path.pop(0)
    if not todo:
        return []
    return [f"Setup: {len(todo)} item{'s' if len(todo) != 1 else ''} to finish ({', '.join(x['title'] for x in todo[:3])}"
            f"{', ...' if len(todo) > 3 else ''}). The doctor skill lists them and fixes what it can."]


def summary(root: Path, source: str, agent: str, session_id: str) -> list[str]:
    cfg = c.load_config(root)
    handoff = read(root / "HANDOFF.md")
    lines = [f"{c.project_name(root)} session context (from HANDOFF.md):"]
    lines += table_rows(section(handoff, "Where we are"))[:8]
    nxt = [ln.strip() for ln in section(handoff, "Next") if ln.strip()]
    if nxt:
        lines.append("Next: " + nxt[0].lstrip("-# ").strip())
    lines += claimed(root)
    items = founder_items(read(root / "founder" / "status.md"))
    if items:
        lines.append("Top open founder items:")
        lines += items[:3]
    guard = (f"warn at {cfg['warn_pct']}% or {cfg['warn_tokens']:,} tokens, handoff at "
             f"{cfg['handoff_pct']}% or {cfg['handoff_tokens']:,} tokens" if agent == "claude"
             else "handoff requested after each compaction")
    lines += setup(root)
    lines.append(f"Protocol: founder/operating-protocol.md. Context guard: {guard}.")
    if source == "compact":
        note = [COMPACT_NOTE]
        if agent == "codex":
            note.append(c.COMPACT_HANDOFF_TEXT)
            c.write_state(c.state_path(root, session_id, "compact"), {"pending": False, "asked": c.now()})
        return [*lines[: MAX_LINES - len(note)], *note]
    return lines[:MAX_LINES]


def main(argv: list[str] | None = None) -> int:
    try:
        agent = c.parse_agent(argv)
        data = c.read_stdin_json(sys.stdin)
        root = c.project_dir(data)
        if agent == "claude":  # lets the repo's .claude/statusline.py shim find this plugin's status line
            c.write_state(root / ".claude" / "state" / "plugin.json", {"root": str(Path(__file__).resolve().parents[2])})
        text = "\n".join(summary(root, str(data.get("source") or "startup"), agent,
                                 str(data.get("session_id") or "unknown")))
        print(c.context_output("SessionStart", text))
    except Exception:  # noqa: BLE001 - fail safe
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
