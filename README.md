# Solo to Scale

**The startup operating system for solo founders and their AI team.** It runs a startup from first idea to scale, through one version-controlled system:

- **The repo is the memory.** Decisions, status and specs live in the startup's own repository.
- **You are the CEO and chair the board.** Claude is the AI core, working with six AI roles and four board advisors.
- **Nothing becomes Approved without your words.** Merging a pull request is approval.
- **It works in Claude Code and Codex,** from one source.

**Status: v2.15.1.** Sixteen skills, seven team roles, four board advisors (plus an optional sales advisor), shared hooks, and `init` and `upgrade` for each startup's repo. The handbook is `plugins/solo-to-scale/docs/handbook.md`.

---

## Install in Claude Code

In Claude Code, run:

```
/plugin marketplace add Payaml3/solo-to-scale
/plugin install solo-to-scale@solo-to-scale
/reload-plugins
```

Then, inside a startup's repository:

```
/solo-to-scale:init
```

`init` makes no changes until you approve its plan. It then:
1. assesses the repo, read-only
2. asks its questions together, starting with your project's name. It saves the name once, in `founder/project.json`, and every file and hook reads it from there
3. opens one pull request from `ops/solo-to-scale`. It sets up Founder HQ, the registers, the playbook, the team, the CI checks and the instruction files

It never overwrites an existing file. Where a file exists, the PR description proposes a merge instead.

**Every session in a repo:** `init` adds this marketplace and plugin to the repo's `.claude/settings.json`, under `extraKnownMarketplaces` and `enabledPlugins`. Claude Code honours them once you accept the folder's trust dialog. Committing them doesn't download the plugin for others: each collaborator installs it once per clone, either when Claude Code offers to or with `claude plugin install solo-to-scale@solo-to-scale --scope project`.

## Install in Codex

```
codex plugin marketplace add Payaml3/solo-to-scale
codex
/plugins
```

In the plugin browser, open the **solo-to-scale** marketplace and install **solo-to-scale**, then restart Codex. In the startup's repository, ask Codex to run the `init` skill.

- **Hooks** are on by default in current Codex releases; the old `plugin_hooks` flag has been removed. Codex asks you to trust a plugin's hooks before they run.
- **Instructions:** Codex reads `AGENTS.md`, which `init` writes.
- **Roles:** `init` writes them into `.codex/agents/`, because a Codex plugin can't ship agents.

## Install on claude.ai, for Project chats

Add this repository as a plugin marketplace in your Claude account's plugin settings, by entering `Payaml3/solo-to-scale`. Project chats then get the decision and review skills: `board-review`, `record-decision` and `weekly-review`.

## Claude Code and Codex: what each tool gets

| Feature | Claude Code | Codex |
| --- | --- | --- |
| Instructions | `CLAUDE.md` imports `AGENTS.md` | `AGENTS.md` |
| Skills | From the plugin, as `/solo-to-scale:<skill>` | From the plugin |
| Roles | Plugin agents generated into `agents/claude/*.md` | `.codex/agents/*.toml`, written into the repo by `init` from `agents/codex/` |
| Context guard | Status-line percentage plus token limits: warns, then asks for a handoff (`UserPromptSubmit`) | `PreCompact` leaves a marker. The next prompt (or `SessionStart` with `compact`) asks for the handoff and a re-read of `HANDOFF.md`. `PostCompact` notifies you |
| Session start | `SessionStart` with `startup\|resume\|compact` | The same |
| Stop check | `Stop`, respecting `stop_hook_active` | `Stop`, with Codex's `stop_hook_active` plus our own once-per-commit marker |

**Gaps, stated plainly:**
- **No token limits on Codex.** Its hook input doesn't expose token usage; it was checked in the Codex source, not assumed. The guard therefore acts on compaction only.
- **Codex `PreCompact` and `PostCompact` can't add model context.** Their output only reaches you as a system message. So the handoff request arrives with your next prompt, or with the post-compaction session start, not during the compaction.
- **No Codex status line.** Codex has no command status line; the percentage display is Claude-only.
- **Claude Code plugins can't register a status line.** `init` writes it into `.claude/settings.json`. It calls a small shim, `.claude/statusline.py`, which finds the plugin through a note the session-start hook leaves.
- **No `AGENTS.md` injection from a Codex plugin.** The Codex manifest has no field for it. The text in `agents-fragment.md` reaches Codex through the repo's `AGENTS.md`, which `init` renders from it.
- **Windows:**
  - Codex hooks use `commandWindows` with `cmd` syntax.
  - Claude Code hooks use POSIX shell syntax, which Claude Code on Windows runs through Git Bash.
  - Every script is plain Python 3 with `pathlib`, and is tested on Linux, macOS and Windows.
- **Budgets cover AI usage only.** Heartbeat runs and handoffs record their cost, measured from the Claude Code transcript where they can be; Codex runs are recorded at the flat estimate.
- **Live views need artifact tools.** `publish-views` stops cleanly in sessions without them, which includes Codex. The startup dashboard doesn't: GitHub Actions builds it.
- **The dashboard's login is Cloudflare Access, or Vercel Authentication.** Serving it at `pm.<domain>` needs that domain on Cloudflare (the free plan is enough), or a Vercel project of its own with Vercel Authentication on All Deployments. Without either the dashboard is still built on every run, and the Claude page is the way to see it.
- **The portfolio reads other repos with a token you add.** `PORTFOLIO_TOKEN` needs read-only Actions access to each venture's repo, and each venture must run 1.5.0 or later.

## Private repository

While this repo is private, each machine needs GitHub access to it:
- **Claude Code and Codex** use your git credentials. Run `gh auth login` once.
- **claude.ai** needs GitHub connected to your account.

## Updating

- **Releases:** each release bumps `version` in both plugin manifests and in `.claude-plugin/marketplace.json`, adds a `CHANGELOG.md` entry, and gets a git tag `vX.Y.Z`.
- **Claude Code:** update the marketplace and the plugin from the `/plugin` menu, then run `/reload-plugins`.
- **Codex:** refresh the marketplace and update from `/plugins`, then restart Codex.
- **Each startup's repo:** run `upgrade`. It compares `founder/.solo-to-scale-version` with the plugin and opens one pull request with only the differences. Founder-owned content (status, registers, business context, brand) is never touched.
- **Renaming a project:** edit `founder/project.json` and run `upgrade`. It re-renders the plugin-owned files and lists where the old name still appears in your own files.

## Roll back

1. Uninstall the plugin: from `/plugin` in Claude Code, or `/plugins` in Codex.
2. In each startup's repo, revert the `init` pull request (and any `upgrade` pull requests): `git revert -m 1 <merge commit>`, through a PR.

Your founder files stay yours. Nothing outside the repo needs undoing, apart from the Claude Project and the Monday scheduled task, which you created by hand.

## No project names in this repo

The plugin is generic. It contains no startup's name, repo, epics, slices, invariants, view links or domain terms; examples and fixtures use the fictional "Example Startup". CI enforces this with a `PROJECT_NAME_DENYLIST` repository secret, a comma-separated list of names it must never contain.

## What's in this repo

| Path | What it is |
| --- | --- |
| `.claude-plugin/marketplace.json` | Claude Code marketplace (one plugin) |
| `.agents/plugins/marketplace.json` | Codex marketplace (the same plugin) |
| `plugins/solo-to-scale/.claude-plugin/`, `.codex-plugin/` | The two plugin manifests |
| `plugins/solo-to-scale/skills/` | The 16 skills, in the shared `SKILL.md` format, with details in `references/` |
| `plugins/solo-to-scale/roles/` | One source per role: 7 team roles, 4 advisors and the sales template |
| `plugins/solo-to-scale/agents/` | Generated from `roles/` by `scripts/sync_agents.py`; never edit by hand |
| `plugins/solo-to-scale/hooks/`, `scripts/hooks/` | Hook registrations for each tool, and the shared hook scripts (`--agent claude\|codex`) |
| `plugins/solo-to-scale/scripts/` | The agent generator, the `init` and `upgrade` engines, the handbook check |
| `plugins/solo-to-scale/templates/` | Everything `init` writes into a startup's repo, with each file's owner recorded in `scripts/s2s_render.py` |
| `plugins/solo-to-scale/models.yaml` | Tier to model, for each tool: the only place model names live |
| `plugins/solo-to-scale/docs/handbook.md` | The handbook, the only copy |
| `tests/` | Pytest for every script, fixture repos, manifest, drift, size and name checks |
| `BUILD.md`, `sources/` | The build prompt and its source material |

## Recommended companions (not bundled)

`init` checks for these and asks before enabling any of them in a repo:
- founder
- Superpowers
- marketing
- brand-skills
- GitHub Spec Kit

Enable only what a repo needs: every enabled plugin's skill descriptions load into every session.

## Developing the plugin

```
python -m pytest -q tests plugins/solo-to-scale/templates/tools/tests
python tests/check_manifests.py && python tests/check_drift.py && python tests/check_sizes.py
python plugins/solo-to-scale/scripts/sync_agents.py   # after editing roles/ or models.yaml
claude plugin validate ./plugins/solo-to-scale && claude plugin validate .   # where the Claude Code CLI is installed
```

## Licence

All rights reserved for now. Choose a licence before making this repo public.
