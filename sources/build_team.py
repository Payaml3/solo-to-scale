"""Build team-map data (JSON) for the AI-team view: roles, tasks (stories, founder items, decisions,
business items) and their dependencies, from a Solo to Scale repo.

Usage: python -I build_team.py <repo_dir> <out_json>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

def epic_roles(repo):
    """Epic-to-role mapping from founder/team.md, the only copy: lines like `- architect: FND, OPS`."""
    roles = {}
    text = (repo / "founder/team.md").read_text() if (repo / "founder/team.md").exists() else ""
    block = text.split("## Epic ownership", 1)[-1] if "## Epic ownership" in text else ""
    for line in block.splitlines():
        m = re.match(r"\s*-\s*(architect|qa|growth|engineer|product|research)\s*:\s*(.+)", line)
        if m:
            for code in re.findall(r"\b[A-Z]{2,5}\b", m.group(2)):
                roles[code] = m.group(1)
    return roles


def repo_name(repo):
    url = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    m = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", url)
    return m.group(1) if m else repo.resolve().name


repo, out = Path(sys.argv[1]), Path(sys.argv[2])
spec = next((repo / "specs").glob("001-*"))
commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
date = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%cs"], capture_output=True, text=True).stdout.strip()

sdoc = yaml.safe_load((repo / "backlog/stories.yaml").read_text())
epics, stories = sdoc["epics"], sdoc["stories"]
slices = yaml.safe_load((spec / "slices.yaml").read_text())["slices"]
items = yaml.safe_load((repo / "backlog/model-items.yaml").read_text())
items = items if isinstance(items, list) else items.get("items", items)
decisions_md = (spec / "decisions.md").read_text()
status_md = (repo / "founder/status.md").read_text()

ROLE_OF_EPIC = epic_roles(repo)  # founder/team.md is the single source
slice_order = [s["id"] for s in slices]
slice_name = {s["id"]: s["name"].replace(" (done)", "") for s in slices}
slice_status = {s["id"]: s.get("status", "todo") for s in slices}

tasks = []
for s in stories:
    total, done = len(s.get("ac", [])), len(s.get("done", []) or [])
    tasks.append({
        "id": s["id"], "title": s["title"], "kind": "story",
        "role": ROLE_OF_EPIC.get(s["epic"], "engineer"), "epic": s["epic"], "initiative": epics[s["epic"]]["name"],
        "slice": s.get("ms", ""), "priority": s.get("pri", ""),
        "status": "done" if total and done == total else ("in_progress" if done else "todo"),
        "progress": f"{done}/{total}", "deps": list(s.get("deps", []) or []),
    })

# Founder (CEO) items, parsed from founder/status.md "Open founder items"
block = status_md.split("## Open founder items", 1)[1].split("\n## ", 1)[0]
story_ids = {t["id"] for t in tasks}
for i, line in enumerate([l for l in block.splitlines() if l.startswith("| ") and not l.startswith("| Item") and not l.startswith("|---")]):
    cells = [c.strip() for c in line.strip("|").split("|")]
    text = re.sub(r"`", "", cells[0])
    blocks = sorted({m for m in re.findall(r"\b[A-Z]{3}-\d{2}\b", text) if m in story_ids})
    tasks.append({
        "id": f"CEO-{i + 1:02d}", "title": text if len(text) < 120 else text[:117] + "...", "kind": "founder",
        "role": "founder", "slice": (cells[2] if len(cells) > 2 else "").split(" ")[0].strip("(),"),
        "status": "todo", "progress": "", "deps": [], "blocks": blocks,
    })

# Decisions waiting: the product manager prepares them, the founder approves
for did, text, st in re.findall(r"^\| ((?:C|G|A)-\d+) \| ([^|]+)\|.*\*\*(Proposed|Open)\*\*", decisions_md, re.M):
    text = text.strip()
    tasks.append({
        "id": did, "title": text if len(text) < 120 else text[:117] + "...", "kind": "decision",
        "role": "product", "slice": "", "status": "todo", "progress": st, "deps": [],
    })

# Business items outside software (research and strategy)
for it in items:
    if it.get("status") == "non-software":
        tasks.append({
            "id": it["code"], "title": it["item"], "kind": "business", "role": "research",
            "slice": "", "status": "todo", "progress": "", "deps": [],
        })

# Reverse links
by_id = {t["id"]: t for t in tasks}
for t in tasks:
    for b in t.get("blocks", []):
        by_id[b]["deps"].append(t["id"])
for t in tasks:
    t["dependents"] = [u["id"] for u in tasks if t["id"] in u["deps"]]

data = {
    "repo": repo_name(repo), "commit": commit, "date": date,
    "slices": [{"id": s, "name": slice_name[s], "status": slice_status[s]} for s in slice_order],
    "tasks": tasks,
}
out.write_text(json.dumps(data, ensure_ascii=False))
from collections import Counter
print(commit, date, len(tasks), Counter(t["role"] for t in tasks), Counter(t["status"] for t in tasks))
print("founder items:", [(t["id"], t["blocks"]) for t in tasks if t["kind"] == "founder"])
