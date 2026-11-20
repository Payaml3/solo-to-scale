"""Fails if any file in this repo contains a startup's name from PROJECT_NAME_DENYLIST.

The plugin is generic: project names live only in each startup's founder/project.json.
PROJECT_NAME_DENYLIST is a comma-separated repository secret; the check is skipped when it's unset.
"""
import os
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
names = [n.strip() for n in os.environ.get("PROJECT_NAME_DENYLIST", "").split(",") if n.strip()]
if not names:
    print("PROJECT_NAME_DENYLIST not set: skipped")
    sys.exit(0)
pattern = re.compile("|".join(re.escape(n) for n in names), re.IGNORECASE)
hits = []
for path in sorted(root.rglob("*")):
    if not path.is_file() or ".git" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for number, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            hits.append(f"{path.relative_to(root)}:{number}")
# Print locations only, never the matched names, so CI logs don't leak the denylist.
print("\n".join(hits) or "no project names found")
sys.exit(1 if hits else 0)
