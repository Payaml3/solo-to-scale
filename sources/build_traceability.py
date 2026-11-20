"""Build traceability datasets (CSV) from a Solo to Scale repo: source documents -> model items ->
requirements -> stories -> acceptance criteria -> test evidence, plus completion per function.

Usage: python -I build_traceability.py <repo_dir> <out_dir>
Reads: backlog/model-items.yaml, backlog/stories.yaml, specs/001-*/requirements.yaml,
       specs/001-*/test-map.yaml, specs/001-*/slices.yaml, specs/001-*/decisions.md
"""
import csv
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


repo, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
spec = next((repo / "specs").glob("001-*"))
commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
                        capture_output=True, text=True).stdout.strip()

items = yaml.safe_load((repo / "backlog/model-items.yaml").read_text())
items = items if isinstance(items, list) else items.get("items", items)
sdoc = yaml.safe_load((repo / "backlog/stories.yaml").read_text())
epics, stories = sdoc["epics"], sdoc["stories"]
reqs = yaml.safe_load((spec / "requirements.yaml").read_text())["requirements"]
tmap = yaml.safe_load((spec / "test-map.yaml").read_text()) or {}
slices = yaml.safe_load((spec / "slices.yaml").read_text())["slices"]
decisions_md = (spec / "decisions.md").read_text()


def source_group(src: str) -> str:
    s = src.lower()
    if s.startswith("product model"):
        return "Product model"
    if s.startswith("operating model"):
        return "Operating model"
    if s.startswith("mvp") or "launch criteria" in s:
        return "MVP scope"
    if s.startswith("developer portal"):
        return "Developer portal spec"
    return "Other notes"


# Function (protocol section) per epic, derived from the role mapping in founder/team.md (the single source)
FUNCTION_OF_ROLE = {"architect": "03 Architecture", "qa": "05 QA", "growth": "06 GTM", "engineer": "04 Engineering"}
FUNCTION_OF_EPIC = {code: FUNCTION_OF_ROLE.get(role, "04 Engineering") for code, role in epic_roles(repo).items()}

slice_name = {s["id"]: s["name"].replace(" (done)", "") for s in slices}
slice_status = {s["id"]: s.get("status", "todo") for s in slices}

# ---- stories
story_rows, by_id = [], {}
for s in stories:
    total = len(s.get("ac", []))
    done_idx = s.get("done", []) or []
    evidence = tmap.get(s["id"], {}) or {}
    evidenced = sum(1 for i in done_idx if evidence.get(i) or evidence.get(str(i)))
    ep = epics[s["epic"]]
    row = {
        "story": s["id"], "title": s["title"], "epic": s["epic"], "initiative": ep["name"],
        "track": ep.get("track", ""), "layer": ep.get("layer", ""),
        "function": FUNCTION_OF_EPIC.get(s["epic"], "04 Engineering"),
        "slice": s.get("ms", ""), "slice_name": slice_name.get(s.get("ms", ""), ""),
        "priority": s.get("pri", ""), "criteria": total, "criteria_done": len(done_idx),
        "criteria_tested": evidenced,
        "status": "Done" if total and len(done_idx) == total else ("In progress" if done_idx else "To do"),
        "trace": " ".join(s.get("trace", []) or []),
    }
    story_rows.append(row)
    by_id[s["id"]] = row

# ---- model items (with the stories that deliver each)
delivered_by = {}
for s in stories:
    for code in s.get("trace", []) or []:
        delivered_by.setdefault(code, []).append(s["id"])
item_rows = []
for it in items:
    sids = delivered_by.get(it["code"], [])
    tot = sum(by_id[x]["criteria"] for x in sids)
    dn = sum(by_id[x]["criteria_done"] for x in sids)
    item_rows.append({
        "code": it["code"], "source": source_group(it.get("source", "")), "source_detail": it.get("source", ""),
        "item": it["item"], "scope": it.get("status", ""), "stories": " ".join(sids), "story_count": len(sids),
        "criteria": tot, "criteria_done": dn,
        "status": ("Not software" if it.get("status") == "non-software" else
                   "Later" if it.get("status") == "later" and not sids else
                   "Not traced" if not sids else
                   "Done" if tot and dn == tot else "In progress" if dn else "To do"),
    })

# ---- initiatives (epics)
init_rows = []
for code, ep in epics.items():
    rows = [r for r in story_rows if r["epic"] == code]
    tot = sum(r["criteria"] for r in rows)
    dn = sum(r["criteria_done"] for r in rows)
    init_rows.append({
        "initiative": ep["name"], "code": code, "function": FUNCTION_OF_EPIC.get(code, "04 Engineering"),
        "layer": ep.get("layer", ""), "track": ep.get("track", ""), "goal": ep.get("goal", ""),
        "stories": len(rows), "stories_done": sum(r["status"] == "Done" for r in rows),
        "criteria": tot, "criteria_done": dn, "pct_done": round(100 * dn / tot) if tot else 0,
        "slices": " ".join(sorted({r["slice"] for r in rows})),
    })

# ---- decisions register counts
dec = {k: len(re.findall(rf"\*\*{k}\*\*", decisions_md)) for k in ("Confirmed", "Proposed", "Open")}
open_items = re.findall(r"^\| ((?:C|G|A)-\d+) \| ([^|]+)\|.*\*\*(Proposed|Open)\*\*", decisions_md, re.M)

# ---- translation chain (each layer derived from the one before)
n_src = len({r["source"] for r in item_rows})
software = [r for r in item_rows if r["scope"] in ("mvp", "partly")]
chain = [
    {"order": 1, "level": "Source documents", "total": n_src, "done": n_src,
     "note": "Product model, operating model, MVP scope, developer portal spec, notes"},
    {"order": 2, "level": "Model items (in MVP software scope)", "total": len(software),
     "done": sum(1 for r in software if r["story_count"]), "note": "done = traced to at least one story"},
    {"order": 3, "level": "Requirements (Spec Kit)", "total": len(reqs),
     "done": sum(1 for r in reqs if r.get("status") == "confirmed"), "note": "done = confirmed"},
    {"order": 4, "level": "User stories", "total": len(story_rows),
     "done": sum(r["status"] == "Done" for r in story_rows), "note": "done = every criterion done"},
    {"order": 5, "level": "Acceptance criteria", "total": sum(r["criteria"] for r in story_rows),
     "done": sum(r["criteria_done"] for r in story_rows), "note": "done = ticked"},
    {"order": 6, "level": "Criteria with test evidence", "total": sum(r["criteria"] for r in story_rows),
     "done": sum(r["criteria_tested"] for r in story_rows), "note": "done = evidence in test-map"},
]

# ---- completion per function (protocol sections); each uses the measure that fits its work
def crit(fn):
    rows = [r for r in story_rows if r["function"] == fn]
    return sum(r["criteria_done"] for r in rows), sum(r["criteria"] for r in rows)

eng_d, eng_t = crit("04 Engineering")
arc_d, arc_t = crit("03 Architecture")
qa_d, qa_t = crit("05 QA")
gtm_d, gtm_t = crit("06 GTM")
nonsw = [r for r in item_rows if r["scope"] == "non-software"]
functions = [
    {"function": "00 Founder HQ", "measure": "Contradictions, gaps and assumptions resolved",
     "done": dec["Confirmed"], "total": sum(dec.values())},
    {"function": "01 Business", "measure": "Business items tracked as done (not yet tracked in the repo)",
     "done": 0, "total": len(nonsw)},
    {"function": "02 Product", "measure": "Requirements confirmed", "done": chain[2]["done"], "total": chain[2]["total"]},
    {"function": "03 Architecture", "measure": "Acceptance criteria done (foundation, operations and audit epics)", "done": arc_d, "total": arc_t},
    {"function": "04 Engineering", "measure": "Acceptance criteria done (product build epics)", "done": eng_d, "total": eng_t},
    {"function": "05 QA", "measure": "Evaluation criteria done", "done": qa_d, "total": qa_t},
    {"function": "06 GTM", "measure": "Website, docs and SDK criteria done", "done": gtm_d, "total": gtm_t},
]
for f in functions:
    f["pct_done"] = round(100 * f["done"] / f["total"]) if f["total"] else 0

waiting = [{"id": i, "item": t.strip(), "status": s} for i, t, s in open_items]


def write(name, rows):
    with (out / name).open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


generated = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%cs"],
                           capture_output=True, text=True).stdout.strip()
for r in chain:
    r["pct"] = round(100 * r["done"] / r["total"]) if r["total"] else 0
    r["commit"] = commit
    r["commit_date"] = generated
write("chain.csv", chain)
write("functions.csv", functions)
write("initiatives.csv", init_rows)
write("items.csv", item_rows)
write("stories.csv", story_rows)
write("decisions_waiting.csv", waiting)
print(f"commit {commit}")
for r in chain:
    print(f"{r['level']}: {r['done']}/{r['total']}")
for f in functions:
    print(f"{f['function']}: {f['done']}/{f['total']} ({f['pct_done']}%)")
print("decisions", dec, "waiting rows", len(waiting))
