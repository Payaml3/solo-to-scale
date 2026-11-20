"""Checks both marketplaces and both plugin manifests parse, agree on name and version, and point at a real plugin folder."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []


def load(rel):
    try:
        return json.loads((root / rel).read_text())
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{rel}: {exc}")
        return {}


claude_mkt = load(".claude-plugin/marketplace.json")
codex_mkt = load(".agents/plugins/marketplace.json")
claude_pl = load("plugins/solo-to-scale/.claude-plugin/plugin.json")
codex_pl = load("plugins/solo-to-scale/.codex-plugin/plugin.json")

for rel, m in ((".claude-plugin/marketplace.json", claude_mkt), (".agents/plugins/marketplace.json", codex_mkt)):
    for key in ("name", "owner", "plugins"):
        if key not in m:
            errors.append(f"{rel}: missing {key}")
    for p in m.get("plugins", []):
        src = p.get("source")
        path = src if isinstance(src, str) else (src or {}).get("path", "")
        if not (root / path).is_dir():
            errors.append(f"{rel}: plugin source {path!r} is not a folder")

names = {claude_pl.get("name"), codex_pl.get("name")} | {p.get("name") for p in claude_mkt.get("plugins", [])}
if len(names) != 1:
    errors.append(f"plugin names disagree: {sorted(map(str, names))}")
versions = {claude_pl.get("version"), codex_pl.get("version")} | {p.get("version") for p in claude_mkt.get("plugins", []) if "version" in p}
if len(versions) != 1:
    errors.append(f"versions disagree: {sorted(map(str, versions))}")
if f"## v{claude_pl.get('version')}" not in (root / "CHANGELOG.md").read_text():
    errors.append("CHANGELOG.md has no entry for the current version")

print("\n".join(errors) or "manifests ok")
sys.exit(1 if errors else 0)
