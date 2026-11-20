# init PR body: what each part does and how to turn it off

| Part | What it does | Turn it off |
| --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md` | Shared instructions; CLAUDE.md imports AGENTS.md | Edit outside the solo-to-scale block |
| `founder/` | Founder HQ: status, registers, context, brand, playbook, team, views, Claude Project pack | Founder-owned; edit freely through the skills |
| `HANDOFF.md` | Build state and next story groups | The `handoff` skill keeps it |
| `docs/engineering-standards.md` | Standards and the stage each starts | Plugin-owned; `upgrade` refreshes it |
| `.claude/settings.json` | Plugin enabled, status line, least-privilege permissions | Remove the `statusLine` or `enabledPlugins` entry |
| `.claude/governance.json` | Context-guard and check limits | Edit the values |
| `.codex/config.toml`, `.codex/agents/` | The same policies and roles for Codex | Delete the file or a role |
| Plugin hooks | Context guard, session start, stop check | Disable the plugin, or its hooks in the tool's hook settings |
| `tools/` | Governance check, view-data generators, claim, test-area | Plugin-owned |
| `.github/workflows/governance.yml` | Governance and view-data drift checks | Delete the file |
| `.github/workflows/cross-review.yml` | Optional cross-review (only if chosen) | Delete the file, or unset `CROSS_REVIEW` |
| `.github/ISSUE_TEMPLATE/story-group.md` | Story-group issues with the goal chain | Delete the file |
