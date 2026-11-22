# Changelog

## v1.0.1 (2026-11-20)

- Fix: `init` and `upgrade` now enable the plugin in an existing `.claude/settings.json`. Before, `upgrade` left that file alone as founder-owned, and `init` only proposed the change. A repo whose own copies of `handoff`, `record-decision` and `weekly-review` were replaced then had none of those skills in cloud sessions or scheduled tasks. Only the plugin's marketplace and enabled flag are added; every other key is kept, and the rest stays a proposal.
- Tests: the legacy fixture now has a settings file with hooks and no plugin, the case that exposed the bug.

## v1.0.0 (2026-11-20)

- **Skills (11):** `init`, `upgrade`, `handoff`, `board-review`, `record-decision`, `weekly-review`, `release-check`, `publish-views`, `claim`, `product-design`, `design-system`. Each is under 80 lines and starts with the read-narrowly rule; details sit in `references/`.
- **Roles:** 7 team roles, 4 board advisors (growth, owner, customer and risk lenses) and an optional sales advisor, each with one source in `roles/*.yaml`. `scripts/sync_agents.py` generates the Claude Code and Codex agents from them; model tiers come from `models.yaml`.
- **Hooks**, shared by both tools:
  - context guard: Claude Code limits on percentage and tokens; Codex hands off at compaction
  - session start
  - stop check with loop guards
  - Claude status line
  - Codex `PreCompact` and `PostCompact`
- **Templates:**
  - Founder HQ
  - `AGENTS.md` and `CLAUDE.md`
  - the engineering standards
  - the Claude Project pack
  - generalised repo tools (governance check, roadmap, team and traceability data, claim, test-area), with tests
  - the governance workflow and an optional cross-review job
  - the story-group issue template
- **`init` and `upgrade` engines:**
  - never overwrite a file; existing files get merge proposals instead
  - plugin-owned, sectioned and founder-owned files are kept apart
  - legacy-repo mapping, and rename reports
- **Team view:** the four board seats beside the founder; one leftover domain term removed.
- **Handbook:** both diagrams redrawn as Mermaid; the "anything else hard to reverse" routing row added. CI fails if the handbook disagrees with `models.yaml` or `governance.json`.
- **One copy of the protocol:** it moved to `templates/founder/operating-protocol.md`, and the bootstrap prompt now points to it.
- **CI:**
  - tests on Linux, macOS and Windows
  - manifest check against both tools' documented fields
  - generated-file drift
  - skill and role sizes
  - project-name denylist

## v0.1.0 (2026-11-20)

- Repository skeleton: Claude Code and Codex marketplaces, both plugin manifests, install guide, `BUILD.md` and `sources/`.
- No project names: `init` asks for the name and stores it in `founder/project.json`; CI checks the repo against the `PROJECT_NAME_DENYLIST` secret.
- `templates/views/team-view.html`: the team-view page, with the project name as a placeholder.
- `docs/handbook.md`: the operating-system handbook, the single source for its Claude Docs view.
