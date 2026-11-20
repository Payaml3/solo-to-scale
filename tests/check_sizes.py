"""Every skill is under 80 lines and starts with the read-narrowly rule; every role file is under 60 lines."""
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "solo-to-scale"
RULE = "**Read narrowly.** Never read a whole file over 150 lines."
errors, rows = [], []
for p in sorted((PLUGIN / "skills").glob("*/SKILL.md")):
    lines = p.read_text(encoding="utf-8").splitlines()
    rows.append((p.relative_to(PLUGIN).as_posix(), len(lines)))
    body = [ln for ln in lines[lines.index("---", 1) + 1:] if ln.strip() and not ln.startswith("# ")]
    if len(lines) >= 80:
        errors.append(f"{p.parent.name}: {len(lines)} lines (limit: under 80)")
    if not body or not body[0].startswith(RULE):
        errors.append(f"{p.parent.name}: must start with the read-narrowly rule")
for p in sorted((PLUGIN / "roles").glob("*.yaml")) + sorted((PLUGIN / "agents").rglob("*.*")):
    n = len(p.read_text(encoding="utf-8").splitlines())
    rows.append((p.relative_to(PLUGIN).as_posix(), n))
    if n >= 60:
        errors.append(f"{p.name}: {n} lines (limit: under 60)")
if "--report" in sys.argv:
    for name, n in rows:
        print(f"{n:4d}  {name}")
print("\n".join(errors) or f"sizes: OK ({len(rows)} files)")
sys.exit(1 if errors else 0)
