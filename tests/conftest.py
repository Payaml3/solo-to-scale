"""Shared test helpers: run a plugin script with JSON on stdin inside a throwaway repo."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "solo-to-scale"
HOOKS = PLUGIN / "scripts" / "hooks"
sys.path.insert(0, str(PLUGIN / "scripts"))


def run_hook(name: str, payload: Any, project: Path, agent: str = "claude", raw: str | None = None,
             env_project: bool = True) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
    if env_project:
        env["CLAUDE_PROJECT_DIR"] = str(project)
    return subprocess.run([sys.executable, str(HOOKS / f"{name}.py"), "--agent", agent],
                          input=raw if raw is not None else json.dumps(payload), capture_output=True,
                          text=True, env=env, timeout=30, check=False, cwd=project)


def git(cwd: Path, *args: str) -> str:
    out = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                          "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=main", *args],
                         cwd=cwd, capture_output=True, text=True, check=True)
    return out.stdout


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


GOV = {"warn_pct": 60, "handoff_pct": 75, "warn_tokens": 100000, "handoff_tokens": 140000,
       "context_window_tokens": None, "claude_md_max_lines": 200, "pr_warn_lines": 400,
       "slices_file": "founder/slices.json"}


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    write(root / ".claude" / "governance.json", json.dumps(GOV))
    write(root / "founder" / "project.json", json.dumps({"name": "Example Startup", "working_name": True,
                                                         "repo": "example/example-startup", "one_line": "x", "stage": 13}))
    return root


def context_of(out: subprocess.CompletedProcess[str]) -> str | None:
    if not out.stdout.strip():
        return None
    return json.loads(out.stdout)["hookSpecificOutput"]["additionalContext"]
