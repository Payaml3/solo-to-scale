"""Fail if docs/handbook.md and the templates disagree on any value in models.yaml or governance.json.

Checks the handbook and templates/AGENTS.md "Model choice" rows against models.yaml `use`, and every
limit the handbook states (context-guard levels, the instruction-file limit, the PR size warning)
against templates/.claude/governance.json. It also fails on diagram placeholders left by an export.

  python scripts/check_handbook.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s2s_yaml  # noqa: E402

PLUGIN = Path(__file__).resolve().parents[1]
TIER_LABEL = {"strongest": "Strongest available", "mid": "Mid-tier", "small": "Smallest that works"}


def model_rows(text: str) -> dict[str, str]:
    rows = {}
    for label in TIER_LABEL.values():
        m = re.search(rf"^\|\s*([^|\n]+?)\s*\|\s*{re.escape(label)}\s*\|\s*$", text, re.M | re.I)
        if m:
            rows[label] = m.group(1)
    return rows


def k(n: int) -> str:
    return f"{n // 1000}k" if n % 1000 == 0 else str(n)


def check(plugin: Path = PLUGIN) -> list[str]:
    errors = []
    hb = (plugin / "docs" / "handbook.md").read_text(encoding="utf-8")
    agents = (plugin / "templates" / "AGENTS.md").read_text(encoding="utf-8")
    use = s2s_yaml.load(plugin / "models.yaml")["use"]
    gov = json.loads((plugin / "templates" / ".claude" / "governance.json").read_text(encoding="utf-8"))

    for name, text in (("docs/handbook.md", hb), ("templates/AGENTS.md", agents)):
        rows = model_rows(text)
        for tier, label in TIER_LABEL.items():
            if rows.get(label) != use[tier]:
                errors.append(f"{name}: Model choice row '{label}' says {rows.get(label)!r}; models.yaml says {use[tier]!r}")

    for level, pct, tok in (("Warn", "warn_pct", "warn_tokens"), ("Handoff", "handoff_pct", "handoff_tokens")):
        m = re.search(rf"^\|\s*{level}\s*\|\s*(\d+)% or (\w+) tokens", hb, re.M)
        want = (str(gov[pct]), k(gov[tok]))
        if not m or (m.group(1), m.group(2)) != want:
            errors.append(f"handbook: {level} row should read '{want[0]}% or {want[1]} tokens'")
    for m in re.finditer(r"under (\d+) lines", hb):
        if int(m.group(1)) != gov["claude_md_max_lines"]:
            errors.append(f"handbook: 'under {m.group(1)} lines' but claude_md_max_lines is {gov['claude_md_max_lines']}")
    for m in re.finditer(r"(?:over|above) (\d+) changed lines", hb):
        if int(m.group(1)) != gov["pr_warn_lines"]:
            errors.append(f"handbook: '{m.group(0)}' but pr_warn_lines is {gov['pr_warn_lines']}")
    if not re.search(r"(?:over|above) \d+ changed lines", hb):
        errors.append("handbook: the PR size warning is not stated")
    for m in re.finditer(r"no more than (\d+) days old", hb):
        if int(m.group(1)) != gov["status_stale_days"]:
            errors.append(f"handbook: '{m.group(0)}' but status_stale_days is {gov['status_stale_days']}")
    if "embedded content" in hb:
        errors.append("handbook: an export placeholder is left; draw it as Mermaid")
    return errors


def main() -> int:
    errors = check()
    print("\n".join(errors) or "handbook: agrees with models.yaml and governance.json")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
