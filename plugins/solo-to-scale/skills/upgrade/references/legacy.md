# Legacy repos: set up by the earlier prompts, no version file

`upgrade_repo.py` maps what exists and proposes these moves. Each needs the founder's go; none is applied automatically.

| Found | Proposed move |
| --- | --- |
| `CLAUDE.md` and no `AGENTS.md` | Move shared content into `AGENTS.md`; `CLAUDE.md` starts with `@AGENTS.md` and keeps Claude-only lines. Together under `claude_md_max_lines`; area rules move to subdirectory `CLAUDE.md` files |
| `.claude/skills/{handoff,record-decision,weekly-review,release-check,publish-views,...}` | Replaced by the plugin's skills: delete the repo copies. Spec Kit (`speckit-*`, `.specify/`) stays in the repo |
| Handoff or weekly-review steps that publish `build/roadmap.html` | Remove them: publishing moves to `publish-views`, on the Monday scheduled task |
| `founder/roadmap.md` or a roadmap page | **ASK**: retire in favour of the Data dashboard, or register as a view in `founder/artifacts.md` |
| A model table with the weekly review on the smallest model | Correct it to mid-tier |
| An epic-to-role (function) mapping inside a script | Move it into `founder/team.md` "## Epic ownership", the only copy |
| A machine-readable slice file in another format | Point `slices_file` in `.claude/governance.json` at a JSON copy, or convert it (`founder/slices.json` schema in `tools/_s2s.py`) |

Existing plugin-owned paths (for example an older `tools/check_governance.py`) are shown as diffs to merge, not replaced, because in a legacy repo they were the repo's own.
