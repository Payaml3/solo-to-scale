"""Checks both marketplaces and both plugin manifests: they parse, agree on name and version, point at
real files, and use only the fields each tool documents (Claude Code: code.claude.com plugins
reference; Codex: the plugin manifest and marketplace parsers in the openai/codex source)."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plugin = root / "plugins" / "solo-to-scale"
errors = []

CLAUDE_PLUGIN_FIELDS = {"$schema", "name", "displayName", "version", "description", "author", "homepage", "repository",
                        "license", "keywords", "metadata", "icon", "documentationUrl", "supportUrl", "privacyPolicyUrl",
                        "termsOfServiceUrl", "defaultEnabled", "engines", "dependencies", "network", "userConfig", "types",
                        "channels", "skills", "commands", "agents", "hooks", "mcpServers", "lspServers", "outputStyles",
                        "workflows", "experimental"}
CODEX_PLUGIN_FIELDS = {"name", "version", "description", "keywords", "skills", "mcpServers", "apps", "hooks", "interface",
                       "extensions", "author", "homepage", "repository", "license"}
CODEX_INTERFACE_FIELDS = {"displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities",
                          "websiteUrl", "privacyPolicyUrl", "termsOfServiceUrl", "defaultPrompt", "brandColor",
                          "composerIcon", "logo", "logoDark", "screenshots"}
HOOK_EVENTS = {"claude": {"SessionStart", "UserPromptSubmit", "Stop", "PreCompact", "PostCompact"},
               "codex": {"SessionStart", "UserPromptSubmit", "Stop", "PreCompact", "PostCompact"}}


def load(rel):
    try:
        return json.loads((root / rel).read_text(encoding="utf-8"))
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
for p in codex_mkt.get("plugins", []):
    src = p.get("source")
    if isinstance(src, dict) and src.get("source") != "local":
        errors.append("codex marketplace: only a local source is used here")
    pol = p.get("policy", {})
    if pol.get("installation", "AVAILABLE") not in ("AVAILABLE", "NOT_AVAILABLE", "INSTALLED_BY_DEFAULT"):
        errors.append("codex marketplace: bad policy.installation")
    if pol.get("authentication", "ON_INSTALL") not in ("ON_INSTALL", "ON_USE"):
        errors.append("codex marketplace: bad policy.authentication")


def check_paths(label, manifest, keys):
    for key in keys:
        val = manifest.get(key)
        for v in (val if isinstance(val, list) else [val] if val else []):
            if not isinstance(v, str) or not v.startswith("./"):
                errors.append(f"{label}: {key} path {v!r} must start with ./")
            elif not (plugin / v).exists():
                errors.append(f"{label}: {key} path {v!r} does not exist")


for k in set(claude_pl) - CLAUDE_PLUGIN_FIELDS:
    errors.append(f"claude plugin.json: unknown field {k!r}")
for k in set(codex_pl) - CODEX_PLUGIN_FIELDS:
    errors.append(f"codex plugin.json: unknown field {k!r}")
for k in set(codex_pl.get("interface", {})) - CODEX_INTERFACE_FIELDS:
    errors.append(f"codex plugin.json: unknown interface field {k!r}")
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", claude_pl.get("name", "")):
    errors.append("plugin name must be kebab-case")
check_paths("claude plugin.json", claude_pl, ("skills", "agents", "hooks"))
check_paths("codex plugin.json", codex_pl, ("skills", "hooks"))

for tool, rel in (("claude", claude_pl.get("hooks")), ("codex", codex_pl.get("hooks"))):
    if not rel:
        errors.append(f"{tool}: no hooks file registered")
        continue
    hooks = load(f"plugins/solo-to-scale/{rel[2:]}")
    if set(hooks) - {"description", "hooks"} or "hooks" not in hooks:
        errors.append(f"{rel}: must be {{\"description\"?, \"hooks\": {{...}}}}")
    for event, groups in (hooks.get("hooks") or {}).items():
        if event not in HOOK_EVENTS[tool]:
            errors.append(f"{rel}: unexpected event {event}")
        for g in groups:
            for h in g.get("hooks", []):
                cmd = h.get("command", "")
                var = "${CLAUDE_PLUGIN_ROOT}" if tool == "claude" else "$PLUGIN_ROOT"
                script = re.search(r"/(scripts/hooks/\w+\.py)", cmd)
                if var not in cmd or not script or not (plugin / script.group(1)).is_file():
                    errors.append(f"{rel}: {event} command must run a real script under {var}: {cmd}")
                if f"--agent {tool}" not in cmd:
                    errors.append(f"{rel}: {event} command must pass --agent {tool}")

for skill in sorted((plugin / "skills").glob("*/SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", text, re.S)
    if not m or m.group(1) != skill.parent.name:
        errors.append(f"{skill.relative_to(root)}: frontmatter must start with name (= folder) and description")

names = {claude_pl.get("name"), codex_pl.get("name")} | {p.get("name") for p in claude_mkt.get("plugins", []) + codex_mkt.get("plugins", [])}
if len(names) != 1:
    errors.append(f"plugin names disagree: {sorted(map(str, names))}")
versions = {claude_pl.get("version"), codex_pl.get("version")} | {p.get("version") for p in claude_mkt.get("plugins", []) if "version" in p}
if len(versions) != 1:
    errors.append(f"versions disagree: {sorted(map(str, versions))}")
if f"## v{claude_pl.get('version')}" not in (root / "CHANGELOG.md").read_text(encoding="utf-8"):
    errors.append("CHANGELOG.md has no entry for the current version")

print("\n".join(errors) or "manifests ok")
sys.exit(1 if errors else 0)
