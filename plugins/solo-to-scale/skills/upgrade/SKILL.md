---
name: upgrade
description: Update a repo's solo-to-scale operating system to the plugin's current version, or bring a repo set up by the earlier prompts onto the plugin - one PR with only the differences, never touching founder-owned content. Also applies a project rename.
---

# upgrade

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

`<plugin>` is this plugin's root: `${CLAUDE_PLUGIN_ROOT}` in Claude Code; in Codex, two folders above this file.

## 1. Plan, read-only

1. Read `founder/.solo-to-scale-version` (line 1: the version; `rendered-for:` the project name last rendered).
2. Run `python3 <plugin>/scripts/upgrade_repo.py plan --repo .` and show its summary:
   - **Update (plugin-owned)**: tools, protocol, standards, workflows, Claude Project pack, Codex roles
   - **Update the plugin block**: the solo-to-scale block in `AGENTS.md` and `CLAUDE.md`
   - **Create**: missing parts
   - **Founder-owned: left alone**: status, registers, business context, brand, playbook, team, views, `HANDOFF.md`
   - a rename report, when `founder/project.json` names the project differently
3. **No version file** (a repo set up by the earlier prompts): the plan is a map, not a rewrite. See `references/legacy.md`.
   - If `founder/project.json` is missing, ask for the name, working-name flag, repo, one line and stage, and pass them with `--answers`.
   - Only missing parts are created; everything else is proposed as a move.
4. Ask the **ASK** items the plan lists (for example, retiring a roadmap page) in one round. Then wait for the founder's go.

## 2. Apply and open one PR

1. `python3 <plugin>/scripts/upgrade_repo.py apply --repo . [--answers <answers.json>]`: branch `ops/solo-to-scale-<version>`; proposals in `.git/solo-to-scale-proposals.md`.
2. Carry out only the moves the founder approved, each as its own commit, for example `CLAUDE.md` content into `AGENTS.md` with `CLAUDE.md` importing it, the two together under the line limit.
3. Run `python3 tools/check_governance.py --base <default branch>` and `python3 -m pytest -q tools/tests`.
4. Commit, push, and open one PR (`gh pr create`, or the GitHub tools this session has; else print the body). In the body: the version change, each updated file, the proposals, the rename report, and what stays founder-owned.

## Renaming

The founder edits `founder/project.json`, then runs `upgrade`. Plugin-owned files are re-rendered with the new name; founder-owned files are listed where the old name still appears, for the founder to edit.

Never mark anything Approved without the founder's words. Close with a short close and a "Next session" line.
