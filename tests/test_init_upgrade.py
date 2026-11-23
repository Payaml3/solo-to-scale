"""init on an empty repo and a repo with CLAUDE.md and CI; upgrade on the legacy "Example Startup" repo; rename."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import PLUGIN, git

import init_repo
import upgrade_repo

FIX = Path(__file__).resolve().parent / "fixtures"
ANSWERS = {"project": {"name": "Example Startup", "working_name": True, "repo": "example/example-startup",
                       "one_line": "Invoicing for small studios", "stage": 13},
           "guard": {"warn_pct": 55}, "budgets": {"engineer": "$120"},
           "enable_plugins": ["superpowers@claude-plugins-official"]}
TODAY = "2026-11-20"


def make_repo(tmp_path: Path, fixture: str) -> Path:
    repo = tmp_path / fixture
    shutil.copytree(FIX / fixture, repo)
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "fixture")
    return repo


def snapshot(repo: Path) -> dict[str, bytes]:
    return {p.relative_to(repo).as_posix(): p.read_bytes() for p in repo.rglob("*")
            if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts}


def governance(repo: Path) -> subprocess.CompletedProcess[str]:
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "solo-to-scale init")
    return subprocess.run([sys.executable, "tools/check_governance.py", "--base", "main"], cwd=repo,
                          capture_output=True, text=True)


def assert_only_plugin_enabled(before: bytes, after: bytes) -> None:
    """The settings file gains exactly the plugin's marketplace and enabled flag; every existing key is kept."""
    old, new = json.loads(before), json.loads(after)
    assert new["enabledPlugins"] == {**old.get("enabledPlugins", {}), "solo-to-scale@solo-to-scale": True}
    assert new["extraKnownMarketplaces"]["solo-to-scale"]["source"]["source"] == "github"
    assert {k: v for k, v in new.items() if k not in ("enabledPlugins", "extraKnownMarketplaces")} == \
        {k: v for k, v in old.items() if k not in ("enabledPlugins", "extraKnownMarketplaces")}


def test_enable_plugin_keeps_other_plugins_and_is_idempotent():
    from s2s_render import enable_plugin
    old = json.dumps({"enabledPlugins": {"superpowers@claude-plugins-official": False}, "model": "x"})
    new = json.loads(enable_plugin(old))
    assert new["enabledPlugins"] == {"superpowers@claude-plugins-official": False, "solo-to-scale@solo-to-scale": True}
    assert new["model"] == "x"
    assert enable_plugin(json.dumps(new)) is None, "already enabled: nothing to do"
    assert enable_plugin("not json") is None and enable_plugin("[]") is None


def test_init_empty_repo(tmp_path):
    repo = make_repo(tmp_path, "empty")
    plan = init_repo.plan_init(repo, ANSWERS, TODAY)
    assert not plan.by("propose")
    written = init_repo.apply(repo, plan, "ops/solo-to-scale", "t")
    assert git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip() == "ops/solo-to-scale"
    for rel in ("AGENTS.md", "CLAUDE.md", "HANDOFF.md", "founder/project.json", "founder/operating-protocol.md",
                "founder/claude-project/knowledge.md", "docs/engineering-standards.md", ".claude/settings.json",
                ".codex/config.toml", ".codex/agents/engineer.toml", "tools/check_governance.py",
                ".github/ISSUE_TEMPLATE/story-group.md", "founder/roadmap.json", "founder/team.json"):
        assert rel in written, rel
    assert not (repo / ".github/workflows/cross-review.yml").exists(), "cross-review is off by default"
    assert json.loads((repo / ".claude/governance.json").read_text())["warn_pct"] == 55
    settings = json.loads((repo / ".claude/settings.json").read_text())
    assert settings["enabledPlugins"] == {"solo-to-scale@solo-to-scale": True, "superpowers@claude-plugins-official": True}
    beats = json.loads((repo / "founder/heartbeats.json").read_text())["roles"]
    assert beats["engineer"]["monthly_budget_usd"] == 120.0 and not beats["engineer"]["enabled"]
    assert json.loads((repo / "founder/dashboard.json").read_text())["host"] == "", "the dashboard deploys nowhere until set"
    assert "founder/dashboard.json" in json.loads((repo / "founder/gates.json").read_text())["gates"]["deploy"]["paths"]
    assert (repo / ".github/workflows/dashboard.yml").exists() and (repo / "tools/dashboard.html").exists()
    assert json.loads((repo / "founder/portfolio.json").read_text())["ventures"] == [], "no portfolio until set"
    assert "founder/portfolio.json" in json.loads((repo / "founder/gates.json").read_text())["gates"]["deploy"]["paths"]
    assert json.loads((repo / "founder/goals.json").read_text())["objectives"] == [], "no objectives until the founder sets them"
    assert "founder/goals.json" in json.loads((repo / "founder/gates.json").read_text())["gates"]["decision"]["paths"]
    assert (repo / ".github/workflows/portfolio.yml").exists() and (repo / "tools/portfolio.html").exists()
    knowledge = (repo / "founder/claude-project/knowledge.md").read_text()
    assert sum(1 for ln in knowledge.splitlines() if ln[:2].rstrip(".").isdigit()) == 8
    out = governance(repo)
    assert out.returncode == 0, out.stdout
    tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "tools/tests"], cwd=repo, capture_output=True, text=True)
    assert tests.returncode == 0, tests.stdout[-2000:]


def test_quick_start_writes_the_founders_goal(tmp_path):
    repo = make_repo(tmp_path, "empty")
    goal = 'First 10 paying studios, "no discounts"\n by June'
    init_repo.apply(repo, init_repo.plan_init(repo, {**ANSWERS, "goal": goal}, TODAY), "ops/solo-to-scale", "t")
    data = json.loads((repo / "founder/goals.json").read_text())
    assert data["goal"] == 'First 10 paying studios, "no discounts" by June' and data["objectives"] == []


def test_init_never_overwrites_existing_files(tmp_path):
    repo = make_repo(tmp_path, "existing")
    before = snapshot(repo)
    plan = init_repo.plan_init(repo, ANSWERS, TODAY)
    proposed = {a.rel for a in plan.by("propose")}
    assert {"CLAUDE.md", ".claude/settings.json", "Makefile", ".gitignore"} <= proposed
    init_repo.apply(repo, plan, "ops/solo-to-scale", "t")
    after = snapshot(repo)
    for rel, text in before.items():
        if rel != ".claude/settings.json":
            assert after[rel] == text, f"{rel} was changed"
    assert_only_plugin_enabled(before[".claude/settings.json"], after[".claude/settings.json"])
    proposals = (repo / ".git/solo-to-scale-proposals.md").read_text()
    assert "Move its shared content into AGENTS.md" in proposals
    assert '"Bash(make test)"' in proposals and "solo-to-scale@solo-to-scale" in proposals, "settings merged, the repo's values kept"
    assert (repo / ".github/workflows/ci.yml").read_bytes() == before[".github/workflows/ci.yml"]
    assert (repo / ".github/workflows/governance.yml").exists()


def test_init_suggests_upgrade_for_an_existing_os(tmp_path):
    repo = make_repo(tmp_path, "legacy-example")
    a = init_repo.assess(repo)
    assert a["suggest"] == "upgrade"
    assert a["os_skills_in_repo"] == ["handoff"] and a["instruction_lines"]["CLAUDE.md"] > 200


def test_upgrade_legacy_maps_and_proposes_moves(tmp_path):
    repo = make_repo(tmp_path, "legacy-example")
    with pytest.raises(SystemExit):
        upgrade_repo.plan_upgrade(repo, {}, TODAY)  # no project.json: the skill must ask for the name
    before = snapshot(repo)
    plan, legacy = upgrade_repo.plan_upgrade(repo, {"project": ANSWERS["project"]}, TODAY)
    assert legacy
    notes = "\n".join(plan.notes)
    assert "CLAUDE.md (232 lines) content into AGENTS.md" in notes
    assert ".claude/skills/handoff" in notes and "Spec Kit" in notes
    assert "publish build/roadmap.html" in notes
    assert "ASK: retire founder/roadmap.md" in notes
    assert "weekly review on the smallest model" in notes
    assert "tools/build_traceability.py" in notes and "founder/team.md" in notes
    kinds = {a.rel: a.kind for a in plan.actions}
    assert kinds["founder/status.md"] == "keep" and kinds["founder/decisions.md"] == "keep"
    assert kinds["tools/build_traceability.py"] == "propose", "the repo's own script is never replaced in legacy mode"
    assert kinds["founder/project.json"] == "create"
    assert kinds[".claude/settings.json"] == "enable", "the repo's own skills go, so the plugin must be enabled"
    init_repo.apply(repo, plan, "ops/solo-to-scale-1.0.0", "t")
    after = snapshot(repo)
    for rel, text in before.items():
        if rel != ".claude/settings.json":
            assert after[rel] == text, f"{rel} was changed"
    assert_only_plugin_enabled(before[".claude/settings.json"], after[".claude/settings.json"])
    again, _ = upgrade_repo.plan_upgrade(repo, {"project": ANSWERS["project"]}, TODAY)
    assert {a.rel: a.kind for a in again.actions}[".claude/settings.json"] == "keep", "enabling is done once"


def test_upgrade_rerenders_plugin_files_and_reports_rename(tmp_path):
    repo = make_repo(tmp_path, "empty")
    init_repo.apply(repo, init_repo.plan_init(repo, ANSWERS, TODAY), "ops/solo-to-scale", "t")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    # the founder edits founder-owned content, a plugin-owned tool drifts, and the project is renamed
    status = repo / "founder/status.md"
    status.write_text(status.read_text() + "\nFounder note.\n")
    (repo / "tools/claim.py").write_text("# stale\n")
    project = json.loads((repo / "founder/project.json").read_text())
    project["name"] = "Example Labs"
    (repo / "founder/project.json").write_text(json.dumps(project))
    plan, legacy = upgrade_repo.plan_upgrade(repo, {}, TODAY)
    assert not legacy
    kinds = {a.rel: a.kind for a in plan.actions}
    assert kinds["tools/claim.py"] == "update"
    assert kinds["AGENTS.md"] == "same", "the plugin block is unchanged; the founder's title stays"
    assert kinds["founder/status.md"] == "keep"
    assert kinds["founder/claude-project/instructions.md"] == "update"
    notes = "\n".join(plan.notes)
    assert "Renamed: 'Example Startup' -> 'Example Labs'" in notes and "founder/status.md:1" in notes
    init_repo.apply(repo, plan, "ops/solo-to-scale-1.0.0", "t")
    assert "Founder note." in status.read_text()
    assert "Example Labs" in (repo / "founder/claude-project/instructions.md").read_text()
    assert "rendered-for: Example Labs" in (repo / "founder/.solo-to-scale-version").read_text()


def test_upgrade_seeds_heartbeat_budgets_from_the_team_table(tmp_path):
    (tmp_path / "founder").mkdir()
    (tmp_path / "founder/team.md").write_text("## Monthly budget per role\n\n| Role | Monthly budget |\n| --- | --- |\n"
                                              "| engineer | $120 |\n| qa | Open (founder sets it) |\n| 04 | x |\n",
                                              encoding="utf-8")
    answers = upgrade_repo.answers_from_repo(tmp_path, {})
    assert answers["budgets"] == {"engineer": "$120"}
    assert upgrade_repo.r.usd("$120") == 120.0 and upgrade_repo.r.usd("Open (founder sets it)") is None
    assert upgrade_repo.r.usd("40 USD/month") == 40.0 and upgrade_repo.r.usd(0) is None
