"""Plugin-level tests: YAML subset, agent generation and drift, advisors, handbook agreement, rendering."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import PLUGIN, REPO

import check_handbook
import s2s_render as r
import s2s_yaml
import sync_agents


# ---- YAML subset
def test_yaml_subset():
    data = s2s_yaml.loads("# c\na: 1\nb: hello: world\nc: |\n  line one\n\n  line two\nd:\n  - x\n  - 'y'\ne:\n  k: v\nf: true\n")
    assert data == {"a": 1, "b": "hello: world", "c": "line one\n\nline two", "d": ["x", "y"], "e": {"k": "v"}, "f": True}


@pytest.mark.parametrize("bad", ["  indented: 1\n", "a: 1\na: 2\n", "a:\n  - x\n  k: v\n", "no colon\n"])
def test_yaml_rejects_what_it_cannot_read(bad):
    with pytest.raises(ValueError):
        s2s_yaml.loads(bad)


# ---- roles and agents
def test_roles_complete():
    roles = {x["name"]: x for x in sync_agents.load_roles()}
    team = {"chief-of-staff", "research", "product", "architect", "engineer", "qa", "growth"}
    board = {"growth-advisor", "owner-advisor", "customer-advisor", "risk-advisor"}
    assert team | board | {"sales-advisor"} == set(roles)
    assert not roles["sales-advisor"]["enabled"]
    for name in board:
        assert roles[name]["tier"] == "strongest" and roles[name]["access"] == "read-only"


def test_models_have_every_tier():
    models = s2s_yaml.load(PLUGIN / "models.yaml")
    for tool in ("claude", "codex"):
        assert set(models[tool]) == {"strongest", "mid", "small"}
    assert "gpt" not in (PLUGIN / "roles" / "engineer.yaml").read_text(), "roles name a tier, never a model"


def test_agents_match_roles():
    assert sync_agents.main(["--check"]) == 0


def test_drift_check_fails_on_edited_agent_then_passes(tmp_path):
    plugin = tmp_path / "plugin"
    shutil.copytree(PLUGIN, plugin, ignore=shutil.ignore_patterns("__pycache__"))
    target = plugin / "agents" / "claude" / "engineer.md"
    original = target.read_text()
    target.write_text(original + "hand edit\n")
    assert sync_agents.main(["--check", "--plugin", str(plugin)]) == 1
    target.write_text(original)
    assert sync_agents.main(["--check", "--plugin", str(plugin)]) == 0


def test_codex_agents_are_valid_toml():
    import tomllib
    for p in (PLUGIN / "agents" / "codex").glob("*.toml"):
        data = tomllib.loads(p.read_text())
        assert set(data) == {"name", "description", "model", "model_reasoning_effort", "sandbox_mode", "developer_instructions"}
        assert data["developer_instructions"].strip()


def test_claude_agents_frontmatter():
    for p in (PLUGIN / "agents" / "claude").glob("*.md"):
        head = p.read_text().split("---")[1]
        keys = {ln.split(":", 1)[0] for ln in head.strip().splitlines()}
        assert keys == {"name", "description", "tools", "model"}, p.name
    assert not (PLUGIN / "agents" / "claude" / "sales-advisor.md").exists(), "sales advisor is off by default"


# ---- advisors: no impersonation
REAL = ["Hormozi", "Buffett", "Graham", "Fitzpatrick", "Cagan"]


def advisor_violations(text: str) -> list[str]:
    bad = []
    for name in REAL:
        for m in re.finditer(r"[\"“]([^\"”]{3,})[\"”]", text):
            window = text[max(0, m.start() - 80): m.end() + 80]
            if name in window:
                bad.append(f"quote near {name}: {m.group(0)}")
        if re.search(rf"\b(I am|I'm|As|Speaking as)\s+(\w+\s+)?{name}\b", text) or re.search(rf"\bI,\s+\w*\s*{name}", text):
            bad.append(f"first-person claim to be {name}")
        if re.search(rf"{name}\w*\s+(endorses|approves|supports|would approve)", text):
            bad.append(f"claimed endorsement by {name}")
    return bad


SAMPLE_MEMO = """Growth advisor (acquisition lens) on B-07: price per seat
Verdict: concerns
Biggest risk: per-seat pricing caps expansion in small studios, our first 100 customers.
What would change my mind: 5 studios paying per seat after a two-week trial.
Metric to watch: trial-to-paid conversion within 30 days.
Offer value: the dream outcome is faster invoicing; per-seat pricing adds effort for the buyer.
Warm outreach to the 40 studios we know brings the first customers faster than paid ads.
Lifetime value against acquisition cost works only above 3 seats per account.
"""


def test_sample_advisor_memo_passes_the_rules():
    assert advisor_violations(SAMPLE_MEMO) == []
    assert len(SAMPLE_MEMO.strip().splitlines()) <= 9  # title + at most 8 lines


@pytest.mark.parametrize("bad", ['As Buffett, I would never do this.', 'Hormozi says "make an offer so good people feel stupid saying no".',
                                 "Buffett endorses this plan."])
def test_advisor_checker_catches_violations(bad):
    assert advisor_violations(bad)


def test_every_advisor_file_follows_the_rules():
    for p in list((PLUGIN / "roles").glob("*-advisor.yaml")) + list((PLUGIN / "agents").rglob("*-advisor.*")):
        text = p.read_text()
        assert advisor_violations(text) == [], p.name
        assert "never as the real person" in text and "no invented quotes" in text, p.name
    assert "Real lawyer needed" in (PLUGIN / "roles" / "risk-advisor.yaml").read_text()


# ---- handbook agrees with the templates
def test_handbook_agrees():
    assert check_handbook.check() == []


def test_handbook_check_fails_on_disagreement(tmp_path):
    plugin = tmp_path / "plugin"
    shutil.copytree(PLUGIN, plugin, ignore=shutil.ignore_patterns("__pycache__"))
    gov = plugin / "templates" / ".claude" / "governance.json"
    data = json.loads(gov.read_text())
    data["warn_pct"] = 65
    gov.write_text(json.dumps(data))
    models = plugin / "models.yaml"
    models.write_text(models.read_text().replace("Formatting, renames, simple lookups", "Formatting only"))
    errors = check_handbook.check(plugin)
    assert any("Warn row" in e for e in errors) and any("Smallest that works" in e for e in errors)


# ---- rendering
ANSWERS = {"project": {"name": "Example Startup", "working_name": True, "repo": "example/example-startup",
                       "one_line": 'Invoices for "small" studios', "stage": 13}}


def test_every_template_has_an_owner_and_renders():
    out = r.render_all(ANSWERS, "2026-11-20")
    for rel, text in out.items():
        r.owner(rel)
        assert not r.PLACEHOLDER.search(text), rel
    assert json.loads(out["founder/project.json"])["one_line"] == 'Invoices for "small" studios'
    assert "| 13 | D Build and prove | Build, one session per story group |" in out["founder/playbook.md"]
    assert re.search(r"^\| 13 \|.*\| Current \|$", out["founder/playbook.md"], re.M)
    assert out["AGENTS.md"].count("## Operating protocol") == 1
    assert len(out["AGENTS.md"].splitlines()) + len(out["CLAUDE.md"].splitlines()) < 200


def test_cross_review_keeps_github_expressions():
    out = r.render_all({**ANSWERS, "cross_review": True}, "2026-11-20")
    assert "${{ secrets.OPENAI_API_KEY }}" in out[".github/workflows/cross-review.yml"]


def test_render_requires_the_project_name():
    with pytest.raises(ValueError):
        r.render_all({"project": {"repo": "x/y", "one_line": "z"}}, "2026-11-20")


def test_render_reports_unknown_placeholder():
    with pytest.raises(KeyError):
        r.render_text("{{nope}}", r.context(ANSWERS, "2026-11-20"), "x.md")


def test_protocol_lives_in_one_file():
    marker = " → ".join(["Define", "Analyse", "Decide"])
    hits = [p for p in REPO.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts
            and marker in p.read_text(encoding="utf-8", errors="ignore")]
    assert hits == [PLUGIN / "templates" / "founder" / "operating-protocol.md"]
