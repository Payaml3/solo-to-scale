---
name: publish-views
description: Republish the live views (progress dashboard, team view, docs mirrors) whose sources changed since their last published commit. The only thing that publishes; runs after the Monday weekly review. Stops cleanly when this session has no artifact tools.
---

# publish-views

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

## 0. Can this session publish?

Check for artifact tools (for example an `Artifact` tool with publish). If there are none, reply exactly:
`Views need refreshing from a session with artifact tools.` and stop. No other reads.

## 1. Find what changed

For each row in `founder/artifacts.md`: if the last published commit is empty, or `git log --oneline <commit>..HEAD -- <source paths>` shows commits, the view needs a publish. Skip the rest. If none changed, say so in one line and stop.

## 2. Republish each changed view from its sources

- **Progress (Data dashboard):** regenerate `founder/roadmap.json` and `founder/traceability.json` (`python3 tools/build_roadmap.py`, `tools/build_traceability.py`), then publish them as a Data dashboard: stages and the current stage, slices with criteria done, blockers, decisions waiting (with age computed from their dates), the chain, completion by function, initiatives. One progress view only; it replaces any older roadmap page.
- **Startup dashboard (the Claude backup):** `python3 tools/build_dashboard.py build --out .dashboard` (it reads GitHub through `gh`; add `--offline` if this session can't), then publish `.dashboard/index.html` as a page as it is. Never commit `.dashboard/`. The hosted copy at `pm.<domain>` is the `dashboard` workflow's job, not this skill's.
- **Team view:** regenerate `founder/team.json` (`python3 tools/build_team.py`). Take `<plugin>/templates/views/team-view.html` (`<plugin>` is `${CLAUDE_PLUGIN_ROOT}`, or two folders above this file), replace `__PROJECT_NAME__` with `name` from `founder/project.json`, and replace `__DATA__` with the JSON plus `"commit"` (short HEAD) and `"date"` (its commit date). Publish it as a page.
- **Docs views:** read-only mirrors, headed `Generated from <path> at <commit>. Edit in GitHub.`
- **Design system:** from `design/tokens.json` and the components, once stage 11 has run.
- **The handbook** (only in the solo-to-scale plugin repo): its Claude Docs view is republished from `plugins/solo-to-scale/docs/handbook.md`, the only copy.

Publish to the row's existing slug or URL; create a new view only when the slug is empty, then record the slug.

## 3. Record and stop

Update each published row's slug and last published commit in `founder/artifacts.md`, on a branch, through a PR. Never treat a view as a source: turn comments on a view into proposed edits in the repo.
