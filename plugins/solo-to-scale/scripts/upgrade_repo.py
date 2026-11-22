"""The engine behind the `upgrade` skill: bring a repo's operating system up to the plugin's version.

  python scripts/upgrade_repo.py plan  --repo <path> [--answers answers.json]
  python scripts/upgrade_repo.py apply --repo <path> [--answers answers.json] [--branch <name>]

With founder/.solo-to-scale-version: re-renders plugin-owned files and the plugin block in AGENTS.md
and CLAUDE.md, creates missing parts, and never touches founder-owned content (status, registers,
business context, brand...). If founder/project.json names the project differently from the last
render, it lists where the old name still appears in founder-owned files.
Without a version file (a repo set up by the earlier prompts): maps what exists and proposes only the
missing parts and the moves; it changes nothing that exists. It needs founder/project.json, or
answers.json with the project fields (the skill asks for the name).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import init_repo as ini  # noqa: E402
import s2s_render as r  # noqa: E402

VERSION_FILE = "founder/.solo-to-scale-version"


def version_info(repo: Path) -> tuple[str | None, str | None]:
    lines = ini.read(repo / VERSION_FILE).splitlines()
    if not lines:
        return None, None
    old_name = next((ln.split(":", 1)[1].strip() for ln in lines[1:] if ln.startswith("rendered-for:")), None)
    return lines[0].strip(), old_name


def answers_from_repo(repo: Path, extra: dict[str, Any]) -> dict[str, Any]:
    answers = dict(extra)
    try:
        project = json.loads(ini.read(repo / "founder/project.json") or "{}")
    except ValueError:
        project = {}
    answers["project"] = {**project, **(extra.get("project") or {})}
    try:
        gov = json.loads(ini.read(repo / ".claude/governance.json") or "{}")
        answers.setdefault("guard", {k: v for k, v in gov.items() if k in
                                     ("warn_pct", "handoff_pct", "warn_tokens", "handoff_tokens", "context_window_tokens")})
    except ValueError:
        pass
    answers.setdefault("cross_review", (repo / ".github/workflows/cross-review.yml").exists())
    answers.setdefault("sales_advisor", (repo / ".codex/agents/sales-advisor.toml").exists())
    return answers


def name_report(repo: Path, old: str, new: str) -> list[str]:
    if not old or old == new:
        return []
    hits = []
    for rel in r.FOUNDER_OWNED + r.SECTIONED:
        for i, line in enumerate(ini.read(repo / rel).splitlines(), 1):
            if old in line:
                hits.append(f"  - {rel}:{i}: {line.strip()[:100]}")
    head = f"Renamed: '{old}' -> '{new}'. Plugin-owned files are re-rendered; founder-owned files still say '{old}' here (edit them yourself):"
    return [head, *(hits or ["  - (no occurrences)"])]


def legacy_moves(repo: Path, a: dict[str, Any]) -> list[str]:
    moves = []
    claude, agents = ini.read(repo / "CLAUDE.md"), ini.read(repo / "AGENTS.md")
    if claude and not agents:
        moves.append(f"Move: CLAUDE.md ({len(claude.splitlines())} lines) content into AGENTS.md; CLAUDE.md then "
                     "imports it (`@AGENTS.md`) and keeps only Claude-specific lines. Together under the line limit; "
                     "area conventions go to subdirectory CLAUDE.md files.")
    if a["os_skills_in_repo"]:
        moves.append("Move: repo skills " + ", ".join(f".claude/skills/{s}" for s in a["os_skills_in_repo"]) +
                     " are replaced by the plugin's; delete them. Spec Kit (`speckit-*`, `.specify/`) stays in the repo.")
    publishing = [f for f in ini.tracked(repo) if f.startswith(".claude/skills/") and f.endswith("SKILL.md")
                  and "roadmap.html" in ini.read(repo / f)]
    if publishing:
        moves.append("Move: remove the steps that publish build/roadmap.html from " + ", ".join(publishing) +
                     ". Publishing moves to `publish-views`, on the Monday scheduled task.")
    roadmap_pages = [f for f in ini.tracked(repo) if re.search(r"roadmap\.(md|html)$", f)]
    if roadmap_pages:
        moves.append("ASK: retire " + ", ".join(roadmap_pages) + " in favour of the Data dashboard, or register "
                     "them as a view in founder/artifacts.md?")
    for rel in ("CLAUDE.md", "AGENTS.md"):
        text = ini.read(repo / rel)
        if re.search(r"weekly review[^\n|]*\|\s*small", text, re.I) or re.search(r"small[^\n]*weekly review", text, re.I):
            moves.append(f"Fix: {rel}'s model table puts the weekly review on the smallest model; it runs on mid-tier.")
    mapping = [f for f in ini.tracked(repo) if f.endswith(".py") and not f.startswith("tests/")
               and re.search(r"(FUNCTION_OF_EPIC|ROLE_OF_EPIC|EPIC_ROLES?|epic_to_role)\s*=\s*\{", ini.read(repo / f))]
    if mapping:
        moves.append("Move: the epic-to-role mapping hard-coded in " + ", ".join(mapping) + " goes into founder/team.md "
                     "\"## Epic ownership\", the only copy; the generators read it from there.")
    return moves


def plan_upgrade(repo: Path, extra: dict[str, Any], today: str) -> tuple[r.Plan, bool]:
    version, old_name = version_info(repo)
    legacy = version is None
    answers = answers_from_repo(repo, extra)
    if not (answers.get("project") or {}).get("name"):
        raise SystemExit("founder/project.json is missing: ask the founder for the project's name, one line, repo "
                         "and stage, and pass them with --answers")
    plan = r.Plan()
    for rel, text in r.render_all(answers, today).items():
        dest, own = repo / rel, r.owner(rel)
        if not dest.exists():
            if own == "section" and rel == "AGENTS.md" and legacy and (repo / "CLAUDE.md").exists():
                plan.actions.append(r.Action(rel, "create", own, text, "new; move shared CLAUDE.md content here"))
            else:
                plan.actions.append(r.Action(rel, "create", own, text))
            continue
        old = ini.read(dest)
        if rel == r.SETTINGS and (enabled := r.enable_plugin(old)):
            # Founder-owned, but the plugin must be enabled or the repo loses its skills (see enable_plugin).
            plan.actions.append(r.Action(rel, "enable", own, enabled))
        elif old == text:
            plan.actions.append(r.Action(rel, "same", own))
        elif own == "founder":
            plan.actions.append(r.Action(rel, "keep", own))
        elif legacy:
            note, body = (ini.sectioned_proposal(rel, old, text) if own == "section"
                          else ("Existing repo version; the plugin's replaces it.", r.diff(rel, old, text)))
            plan.actions.append(r.Action(rel, "propose", own, body, note))
        elif own == "section":
            new_block, old_block = r.section(text), r.section(old)
            if old_block is None:
                plan.actions.append(r.Action(rel, "propose", own, new_block or "", "No solo-to-scale markers; add this block."))
            elif old_block != new_block:
                plan.actions.append(r.Action(rel, "section", own, old.replace(old_block, new_block or "")))
            else:
                plan.actions.append(r.Action(rel, "same", own))
        else:
            plan.actions.append(r.Action(rel, "update", own, text))
    if legacy:
        plan.notes += ["Legacy repo (no version file): only missing parts are created; moves are proposed."]
        plan.notes += legacy_moves(repo, ini.assess(repo))
    else:
        plan.notes.append(f"Upgrade {version} -> {r.plugin_version()}.")
        plan.notes += name_report(repo, old_name or "", answers["project"]["name"])
    return plan, legacy


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="solo-to-scale upgrade engine")
    ap.add_argument("command", choices=["plan", "apply"])
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--answers", type=Path)
    ap.add_argument("--branch", default=None)
    ap.add_argument("--today", default=dt.date.today().isoformat())
    args = ap.parse_args(argv)
    repo = args.repo.resolve()
    plan, _ = plan_upgrade(repo, ini.load_answers(args.answers), args.today)
    print(plan.summary())
    if args.command == "apply":
        branch = args.branch or f"ops/solo-to-scale-{r.plugin_version()}"
        written = ini.apply(repo, plan, branch, "Merge proposals from solo-to-scale upgrade")
        print(f"\nwrote {len(written)} files on {branch}; proposals: .git/solo-to-scale-proposals.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
