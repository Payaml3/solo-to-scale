@AGENTS.md

<!-- solo-to-scale:begin (plugin-owned; upgrade re-renders this block. AGENTS.md and this file stay under 200 lines together.) -->
## Claude Code only

- Skills come from the solo-to-scale plugin: `/solo-to-scale:<skill>`. Roles are plugin agents: `solo-to-scale:<role>`.
- The status line shows context use; the context guard warns, then asks for a handoff (limits in `.claude/governance.json`).
- Put conventions for one area in a `CLAUDE.md` in that directory, so they load only when Claude works there.
<!-- solo-to-scale:end -->
