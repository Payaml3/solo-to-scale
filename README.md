# Solo to Scale

**The startup operating system for solo founders and their AI team.** It runs a startup from first idea to scale, through one version-controlled system:

- **The repo is the memory.** Decisions, status and specs live in the startup's own repository.
- **You are the CEO and board.** Claude is the AI core, working with six AI roles and four board advisors.
- **Nothing becomes Approved without your words.** Merging a pull request is approval.
- **It works in Claude Code and Codex,** from one source.

> **Status: v0.1.0 skeleton.** The install files are in place, but the skills, roles and hooks are still being built from `BUILD.md`. Until v1.0.0, installing gives you an empty plugin.

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
1. assesses the repo
2. asks its questions, starting with your project's name. It saves the name once, in `founder/project.json`, and every file that needs it reads it from there. To rename the project, edit that file and run `upgrade`
3. opens one pull request that sets up Founder HQ, the registers, the playbook, the team, CI checks and the instruction files

It never overwrites an existing file.

**Every session in a repo, cloud sessions included:** `init` adds this marketplace and plugin to the repo's `.claude/settings.json`, under `extraKnownMarketplaces` and `enabledPlugins`. Anyone who opens the repo, and every cloud session, then gets the plugin automatically.

## Install in Codex

```
codex plugin marketplace add Payaml3/solo-to-scale
codex
/plugins
```

In the plugin browser, open the **solo-to-scale** marketplace and install **solo-to-scale**. Restart Codex afterwards. Then, in the startup's repository, ask Codex to run the `init` skill.

Codex reads `AGENTS.md` and the shared skills. Its hooks need plugin hooks enabled; see "Claude and Codex" in `docs/handbook.md` for what differs between the tools.

## Install on claude.ai, for Project chats

Add this repository as a plugin marketplace in your Claude account's plugin settings, by entering `Payaml3/solo-to-scale`. This gives Project chats the decision and review skills: `board-review`, `record-decision`, `weekly-review`.

## Private repository

While this repo is private, each machine needs GitHub access to it:
- **Claude Code and Codex** use your git credentials. Run `gh auth login` once.
- **claude.ai** needs GitHub connected to your account.

## Updating

- **Releases:** each release bumps `version` in both plugin manifests and in `.claude-plugin/marketplace.json`. It gets a `CHANGELOG.md` entry and a git tag `vX.Y.Z`.
- **Claude Code:** update the marketplace and the plugin from the `/plugin` menu, then run `/reload-plugins`.
- **Codex:** refresh the marketplace and update from `/plugins`, then restart Codex.
- **Each startup's repo:** run `upgrade`. It compares the repo's `founder/.solo-to-scale-version` with the plugin and opens one pull request with only the differences. Founder-owned content (status, registers, business context, brand) is never touched.

## Uninstall

1. Uninstall the plugin from `/plugin` in Claude Code, or `/plugins` in Codex.
2. In a startup's repo, revert the `init` pull request.

Your founder files stay yours.

## No project names in this repo

The plugin is generic. It contains no startup's name, repo, epics or links; examples use the fictional "Example Startup". CI enforces this with a `PROJECT_NAME_DENYLIST` repository secret: a comma-separated list of the project names it must never contain.

## What's in this repo

| Path | What it is |
|---|---|
| `.claude-plugin/marketplace.json` | Claude Code marketplace (one plugin) |
| `.agents/plugins/marketplace.json` | Codex marketplace (the same plugin) |
| `plugins/solo-to-scale/` | The plugin: `.claude-plugin/` and `.codex-plugin/` manifests, `skills/`, `roles/`, `agents/`, `hooks/`, `scripts/`, `templates/`, `docs/handbook.md` |
| `BUILD.md` | The build prompt that turns this skeleton into v1.0.0 |
| `sources/` | The prompts, scripts, protocol and handbook the build draws on |
| `CHANGELOG.md` | Release notes |

## Recommended companions (not bundled)

`init` checks for these and asks before enabling any of them in a repo:
- founder
- Superpowers
- marketing
- brand-skills
- GitHub Spec Kit

Enable only what a repo needs. Every enabled plugin's skill descriptions load into every session.

## Licence

All rights reserved for now. Choose a licence before making this repo public.
