"""Hook behaviour for Claude Code and Codex inputs. Every hook must fail safe (exit 0, no output)."""
from __future__ import annotations

import json
import time
from pathlib import Path

import pytest
from conftest import context_of, git, run_hook, write


def set_state(project: Path, pct, tokens, age: float = 0, **extra) -> None:
    write(project / ".claude/state/context-s1.json", json.dumps(
        {"session_id": "s1", "used_pct": pct, "used_tokens": tokens, "window_tokens": 200000,
         "ts": time.time() - age, **extra}))


# ---- context guard (Claude)
def test_guard_silent_below_limits(project):
    set_state(project, 30, 60000)
    assert context_of(run_hook("context_guard", {"session_id": "s1"}, project)) is None


@pytest.mark.parametrize("pct,tokens,word", [(61, 10, "Finish the current step"), (10, 100001, "Finish the current step"),
                                             (76, 10, "Run the handoff skill"), (10, 140000, "Run the handoff skill")])
def test_guard_fires_at_whichever_comes_first(project, pct, tokens, word):
    set_state(project, pct, tokens)
    assert word in context_of(run_hook("context_guard", {"session_id": "s1"}, project))


def test_guard_fires_once_per_level(project):
    set_state(project, 65, 10)
    assert context_of(run_hook("context_guard", {"session_id": "s1"}, project))
    set_state(project, 66, 10, fired=["warn"])
    assert context_of(run_hook("context_guard", {"session_id": "s1"}, project)) is None
    set_state(project, 80, 10, fired=["warn"])
    assert "handoff" in context_of(run_hook("context_guard", {"session_id": "s1"}, project))
    set_state(project, 90, 10, fired=["handoff", "warn"])
    assert context_of(run_hook("context_guard", {"session_id": "s1"}, project)) is None


def test_guard_falls_back_to_transcript_when_state_is_stale(project, tmp_path):
    set_state(project, 1, 1, age=3600)
    tr = tmp_path / "t.jsonl"
    tr.write_text("not json\n" + json.dumps({"type": "assistant", "message": {"usage": {
        "input_tokens": 1000, "cache_creation_input_tokens": 500, "cache_read_input_tokens": 150000}}}) + "\n")
    text = context_of(run_hook("context_guard", {"session_id": "s1", "transcript_path": str(tr)}, project))
    assert "151,500 tokens" in text and "handoff" in text


@pytest.mark.parametrize("raw", ["", "not json", "[1,2]", '{"transcript_path": "/no/such/file"}'])
def test_guard_fails_safe(project, raw):
    out = run_hook("context_guard", None, project, raw=raw)
    assert out.returncode == 0 and out.stdout == ""


# ---- context guard and compaction (Codex)
def test_codex_guard_has_no_token_limits(project):
    set_state(project, 99, 999999)
    assert context_of(run_hook("context_guard", {"session_id": "s1"}, project, agent="codex")) is None


def test_codex_precompact_then_next_prompt_asks_for_handoff_once(project):
    pre = run_hook("pre_compact", {"session_id": "s1", "trigger": "auto"}, project, agent="codex")
    assert pre.returncode == 0 and "compacted" in json.loads(pre.stdout)["systemMessage"]
    post = run_hook("post_compact", {"session_id": "s1", "trigger": "auto"}, project, agent="codex")
    assert "HANDOFF.md" in json.loads(post.stdout)["systemMessage"]
    text = context_of(run_hook("context_guard", {"session_id": "s1", "prompt": "go"}, project, agent="codex"))
    assert "Run the handoff skill" in text and "re-read HANDOFF.md" in text
    assert context_of(run_hook("context_guard", {"session_id": "s1"}, project, agent="codex")) is None


@pytest.mark.parametrize("name", ["pre_compact", "post_compact", "session_start", "stop_check", "statusline"])
def test_every_hook_fails_safe_on_garbage(project, name):
    out = run_hook(name, None, project, agent="codex", raw="{{{")
    assert out.returncode == 0 and out.stderr == ""


# ---- session start
HANDOFF = """# HANDOFF

## Where we are
| Item | State |
|---|---|
| Stage | 13 Build |
| Now | Slice S1, story group 2 |

## Next story groups
- Group 3: CORE-04, CORE-05 · Model: mid-tier

## Known gaps
- none
"""
STATUS = """# Status
Last updated: 2026-11-20

## Open founder items
| Item | Owner | Needed by |
|---|---|---|
| Add the API key secret | Founder | S1 |
| Sign the data terms | Founder | S2 |
| Pick a domain | Founder | S3 |
| Fourth item | Founder | S4 |
"""


def test_session_start_summary(project):
    write(project / "HANDOFF.md", HANDOFF)
    write(project / "founder/status.md", STATUS)
    write(project / ".claude/state/claimed.json", json.dumps(
        {"issue": 12, "title": "CORE story group 2", "goal_chain": ["Goal: first paying customer", "Initiative: CORE"]}))
    text = context_of(run_hook("session_start", {"source": "startup", "session_id": "s1"}, project))
    lines = text.splitlines()
    assert lines[0].startswith("Example Startup session context")
    assert "| Now | Slice S1, story group 2 |" in lines
    assert any(ln.startswith("Next: Group 3") for ln in lines)
    assert "Claimed issue #12: CORE story group 2" in lines and "  Goal: first paying customer" in lines
    assert "- Add the API key secret" in lines and "- Fourth item" not in lines
    assert "warn at 60% or 100,000 tokens" in text and len(lines) <= 25
    assert json.loads((project / ".claude/state/plugin.json").read_text())["root"]


def test_session_start_compact_note_and_limit(project):
    write(project / "HANDOFF.md", HANDOFF.replace("| Now |", "\n".join(f"| R{i} | x |" for i in range(40)) + "\n| Now |"))
    lines = context_of(run_hook("session_start", {"source": "compact"}, project)).splitlines()
    assert len(lines) <= 25 and lines[-1].startswith("You were just compacted")


def test_session_start_codex_compact_asks_for_handoff_and_consumes_marker(project):
    run_hook("pre_compact", {"session_id": "s1"}, project, agent="codex")
    text = context_of(run_hook("session_start", {"source": "compact", "session_id": "s1"}, project, agent="codex"))
    assert "Run the handoff skill" in text and "handoff requested after each compaction" in text
    assert context_of(run_hook("context_guard", {"session_id": "s1"}, project, agent="codex")) is None


def test_session_start_without_files_still_answers(tmp_path):
    root = tmp_path / "bare"
    root.mkdir()
    text = context_of(run_hook("session_start", {"source": "startup", "cwd": str(root)}, root, env_project=False))
    assert text.startswith("Project session context")


def test_session_start_lists_unfinished_setup(project):
    import shutil
    from conftest import PLUGIN
    shutil.copytree(PLUGIN / "templates" / "tools", project / "tools", ignore=shutil.ignore_patterns("tests"))
    text = context_of(run_hook("session_start", {"source": "startup", "session_id": "s1"}, project))
    setup = [ln for ln in text.splitlines() if ln.startswith("Setup:")]
    assert setup and "doctor skill" in setup[0], text


# ---- status line
def test_statusline_writes_state_and_tags(project):
    out = run_hook("statusline", {"session_id": "s1", "model": {"display_name": "Opus"},
                                  "context_window": {"used_percentage": 77, "context_window_size": 200000,
                                                     "current_usage": None}}, project)
    assert out.stdout.startswith("Example Startup · Opus · ") and out.stdout.strip().endswith("ctx 77% · HANDOFF")
    state = json.loads((project / ".claude/state/context-s1.json").read_text())
    assert state["used_pct"] == 77 and state["used_tokens"] == 154000


def test_statusline_handles_nulls(project):
    out = run_hook("statusline", {"session_id": "s1", "context_window": {"used_percentage": None, "current_usage": None}}, project)
    assert "ctx --" in out.stdout


# ---- stop check
def slices(*done: str) -> str:
    return json.dumps({"slices": [{"id": s, "status": "done" if s in done else "todo"} for s in ("S1", "S2")]})


@pytest.fixture
def repo(project):
    git(project, "init", "-q")
    write(project / "founder/slices.json", slices())
    write(project / "HANDOFF.md", HANDOFF)
    git(project, "add", "-A")
    git(project, "commit", "-qm", "base")
    git(project, "checkout", "-qb", "work")
    return project


@pytest.mark.parametrize("agent", ["claude", "codex"])
def test_stop_asks_for_handoff_when_slice_done_without_it(repo, agent):
    write(repo / "founder/slices.json", slices("S1"))
    git(repo, "commit", "-qam", "S1 done")
    out = run_hook("stop_check", {"session_id": "s1", "stop_hook_active": False}, repo, agent=agent)
    assert out.returncode == 2 and "run the handoff skill" in out.stderr
    again = run_hook("stop_check", {"session_id": "s1", "stop_hook_active": False}, repo, agent=agent)
    assert again.returncode == 0, "own loop guard: asks once per commit"


def test_stop_respects_stop_hook_active(repo):
    write(repo / "founder/slices.json", slices("S1"))
    git(repo, "commit", "-qam", "S1 done")
    assert run_hook("stop_check", {"stop_hook_active": True}, repo).returncode == 0


def test_stop_passes_with_handoff_change(repo):
    write(repo / "founder/slices.json", slices("S1"))
    write(repo / "HANDOFF.md", HANDOFF + "\nS1 done.\n")
    git(repo, "commit", "-qam", "S1 done with handoff")
    assert run_hook("stop_check", {}, repo).returncode == 0


def test_stop_is_noop_without_slice_file(project):
    git(project, "init", "-q")
    out = run_hook("stop_check", {}, project)
    assert out.returncode == 0 and out.stderr == ""
