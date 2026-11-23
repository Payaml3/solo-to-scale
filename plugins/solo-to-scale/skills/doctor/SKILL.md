---
name: doctor
description: Check that a startup repo's solo-to-scale setup is complete and healthy - plugin version, workflows, gates, goal, budgets, hosting secrets, labels, heartbeat runs and the dashboard build - then fix what is safe to fix in one PR and list the rest with the exact steps.
---

# doctor

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

`<plugin>` is this plugin's root: `${CLAUDE_PLUGIN_ROOT}` in Claude Code; in Codex, two folders above this file.

## 1. Check, read-only

1. **Version.** Compare line 1 of `founder/.solo-to-scale-version` with `version` in `<plugin>/.claude-plugin/plugin.json`. Older, or `tools/doctor.py` missing: say so and propose the `upgrade` skill first; the rest of the checks come with it.
2. Run `python3 tools/doctor.py` (add `--offline` if `gh` isn't signed in). It checks the project file, the CI workflows, that every founder-owned file sits behind its gate, the company goal and this quarter's objectives, heartbeats and budgets, dashboard and portfolio hosting and their secrets (whether they are set, never their values), the GitHub labels, whether each role that is on has run in the last 72 hours, and the last dashboard build.
3. Report in at most 20 lines: **Broken** first (something will silently not happen), then **To do**, then one line for what's fine. Each with its fix and handbook section, as the tool prints them. Say which ones `--repair` can fix.

## 2. Repair, with the founder's go

Ask once: "Fix the N items doctor can fix?" Then:
1. `git switch -c ops/doctor-<YYYY-MM-DD>` from the default branch.
2. `python3 tools/doctor.py --repair`: adds founder-owned files to their gates' paths, writes an empty `founder/goals.json`, and creates missing labels on GitHub (say so before running it: labels are visible on the repo).
3. If files changed: commit them ("doctor: repair setup"), push, and open one PR. `founder/gates.json` is founder-owned, so the founder merges it; never add the `founder-approved` label yourself.

## 3. The rest is the founder's

List what's left as numbered steps, in the founder's words: which secret to add where, which scheduled task to create (`python3 tools/heartbeat.py plan` prints its prompt), what to write in `founder/goals.json`. Never add a secret, change a budget or set the goal yourself.

Close with `Done / Pending / Next` and a "Next session" line.
