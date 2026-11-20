"""The engine behind the `init` skill: assess a repo, plan the scaffold, apply it on a branch.

  python scripts/init_repo.py assess --repo <path>                      # read-only report
  python scripts/init_repo.py plan   --repo <path> --answers answers.json
  python scripts/init_repo.py apply  --repo <path> --answers answers.json [--branch ops/solo-to-scale]

`apply` creates the branch, writes only files that don't exist, and writes the merge proposals for
the PR description to <repo>/.git/solo-to-scale-proposals.md (inside .git, so never committed).
It never overwrites a file, never commits, pushes or calls the network: the skill does those steps.
answers.json holds init's ASK answers; see skills/init/references/answers.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s2s_render as r  # noqa: E402

PROTOCOL_MARKER = " → ".join(["Define", "Analyse", "Decide"])
OS_SKILLS = ("handoff", "record-decision", "weekly-review", "release-check", "publish-views", "claim",
             "board-review", "product-design", "design-system", "init", "upgrade")


def git(repo: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8",
                             timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def tracked(repo: Path) -> list[str]:
    out = git(repo, "ls-files")
    if out is None:
        return sorted(p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts)
    return out.splitlines()


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def assess(repo: Path) -> dict[str, Any]:
    files = tracked(repo)
    fset = set(files)
    default = (git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD") or "origin/main").split("/", 1)[-1]
    behind_ahead = git(repo, "rev-list", "--left-right", "--count", f"{default}...origin/{default}")
    current = ("unknown (no remote, or fetch first)" if not behind_ahead else
               "current" if behind_ahead.split() == ["0", "0"] else f"differs from origin (ahead/behind: {behind_ahead})")
    unmerged = [b.strip() for b in (git(repo, "branch", "-r", "--no-merged", f"origin/{default}") or "").splitlines() if b.strip()]
    decision_logs = [f for f in files if re.search(r"decision", Path(f).name, re.I) and f.endswith(".md")]
    protocol_copies = [f for f in files if PROTOCOL_MARKER in read(repo / f)]
    roadmaps = [f for f in files if re.search(r"roadmap", Path(f).name, re.I)]
    claude_lines = {f: len(read(repo / f).splitlines()) for f in files if Path(f).name in ("CLAUDE.md", "AGENTS.md")}
    repo_skills = sorted({f.split("/")[2] for f in files if f.startswith(".claude/skills/") and f.count("/") >= 3})
    react = sorted(f for f in files if Path(f).name == "package.json" and '"react"' in read(repo / f))
    settings = {}
    try:
        settings = json.loads(read(repo / ".claude/settings.json") or "{}")
    except ValueError:
        pass
    duplicates = []
    if len(decision_logs) > 1:
        duplicates.append(f"{len(decision_logs)} decision logs: {', '.join(decision_logs)}")
    if len(protocol_copies) > 1:
        duplicates.append(f"the protocol appears in {len(protocol_copies)} files: {', '.join(protocol_copies)}")
    if len(roadmaps) > 1:
        duplicates.append(f"{len(roadmaps)} roadmap files: {', '.join(roadmaps)}")
    return {
        "files": len(files),
        "exists": {k: k in fset or any(f.startswith(k.rstrip("/") + "/") for f in files) for k in
                   ("AGENTS.md", "CLAUDE.md", "HANDOFF.md", "founder/", "docs/", "specs/", ".claude/settings.json",
                    ".claude/hooks/", ".github/workflows/", "Makefile", ".specify/")},
        "version_file": (read(repo / "founder/.solo-to-scale-version").splitlines() or [None])[0],
        "project_json": "founder/project.json" in fset,
        "default_branch": default, "default_branch_state": current, "unmerged_branches": unmerged[:20],
        "instruction_lines": claude_lines, "duplicates": duplicates,
        "repo_skills": repo_skills, "os_skills_in_repo": [s for s in repo_skills if s in OS_SKILLS],
        "react_package_files": react, "enabled_plugins": sorted((settings.get("enabledPlugins") or {}).keys()),
        "workflows": sorted(f for f in files if f.startswith(".github/workflows/")),
        "suggest": "upgrade" if (repo / "founder/.solo-to-scale-version").exists() or "founder/status.md" in fset else "init",
    }


def sectioned_proposal(rel: str, old: str, new: str) -> tuple[str, str]:
    block = r.section(new) or new
    if rel == "CLAUDE.md":
        note = ("CLAUDE.md exists. Move its shared content into AGENTS.md, then make CLAUDE.md start with "
                "`@AGENTS.md` and keep only Claude-specific lines; the two stay under the line limit together.")
    else:
        note = "AGENTS.md exists. Add the solo-to-scale block below (between its markers), keeping your own content."
    return note, block


def plan_init(repo: Path, answers: dict[str, Any], today: str) -> r.Plan:
    plan = r.Plan()
    rendered = r.render_all(answers, today)
    for rel, text in rendered.items():
        dest = repo / rel
        own = r.owner(rel)
        if not dest.exists():
            plan.actions.append(r.Action(rel, "create", own, text))
            continue
        old = read(dest)
        if old == text:
            plan.actions.append(r.Action(rel, "same", own))
            continue
        if own == "section":
            note, block = sectioned_proposal(rel, old, text)
            plan.actions.append(r.Action(rel, "propose", own, block, note))
        elif rel.endswith(".json") and (merged := r.merged_json(old, text)):
            plan.actions.append(r.Action(rel, "propose", own, r.diff(rel, old, merged),
                                         "Your file plus the keys solo-to-scale needs (your values win)."))
        else:
            plan.actions.append(r.Action(rel, "propose", own, r.diff(rel, old, text),
                                         "Exists; merge the parts you want."))
    gi = read(repo / ".gitignore")
    if ".claude/state/" not in gi:
        if (repo / ".gitignore").exists():
            plan.actions.append(r.Action(".gitignore", "propose", "founder", "+.claude/state/",
                                         "Add `.claude/state/` (the hooks' local state) to .gitignore."))
        else:
            plan.actions.append(r.Action(".gitignore", "create", "founder", ".claude/state/\n__pycache__/\n"))
    a = assess(repo)
    if a["os_skills_in_repo"]:
        plan.notes.append("Repo copies of operating-system skills found (" + ", ".join(a["os_skills_in_repo"]) +
                          "); the plugin's replace them. Run `upgrade` to propose removing them. Spec Kit stays.")
    for d in a["duplicates"]:
        plan.notes.append(f"Duplicate: {d}. One becomes the source; the rest point to it.")
    return plan


def apply(repo: Path, plan: r.Plan, branch: str | None, title: str) -> list[str]:
    if branch:
        current = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        if current != branch:
            exists = git(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}") is not None
            if git(repo, "checkout", "-q", *([] if exists else ["-b"]), branch) is None:
                raise SystemExit(f"could not switch to branch {branch}; commit or stash first")
    written = []
    for a in plan.actions:
        if a.kind == "create":
            dest = repo / a.rel
            if dest.exists():
                continue  # never overwrite, even if the repo changed since the plan
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(a.content, encoding="utf-8", newline="\n")
            written.append(a.rel)
        elif a.kind in ("update", "section"):
            dest = repo / a.rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(a.content, encoding="utf-8", newline="\n")
            written.append(a.rel)
    for tool in ("build_roadmap", "build_team", "build_traceability"):  # view data, generated from the sources
        script = repo / "tools" / f"{tool}.py"
        if script.exists():
            subprocess.run([sys.executable, str(script)], cwd=repo, capture_output=True, check=False)
            out = f"founder/{tool.split('_', 1)[1]}.json"
            if (repo / out).exists() and out not in written:
                written.append(out)
    gitdir = Path(git(repo, "rev-parse", "--absolute-git-dir") or repo / ".git")
    text = r.proposal_text(plan, title)
    if text and gitdir.is_dir():
        (gitdir / "solo-to-scale-proposals.md").write_text(text, encoding="utf-8")
    return written


def load_answers(path: Path | None) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path else {}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="solo-to-scale init engine")
    ap.add_argument("command", choices=["assess", "plan", "apply"])
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--answers", type=Path)
    ap.add_argument("--branch", default="ops/solo-to-scale")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    args = ap.parse_args(argv)
    repo = args.repo.resolve()
    if args.command == "assess":
        print(json.dumps(assess(repo), indent=1))
        return 0
    plan = plan_init(repo, load_answers(args.answers), args.today)
    print(plan.summary())
    if args.command == "apply":
        written = apply(repo, plan, args.branch, "Merge proposals from solo-to-scale init")
        print(f"\nwrote {len(written)} files on {args.branch}; proposals: .git/solo-to-scale-proposals.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
