# HANDOFF

The build state, where the next session starts, and the known gaps. The `handoff` skill keeps it current with line-level edits.

## Where we are

| Item | State |
| --- | --- |
| Stage | {{project.stage}} (see `founder/playbook.md`) |
| Now | Operating system set up by solo-to-scale `init` |
| Branches | `main` |

## Next story groups

- Merge the `ops/solo-to-scale` PR, then create the Claude Project and the Monday scheduled task. Model: mid-tier

## Known gaps

- Open: invariants, stack and commands in `AGENTS.md` (stage 10)

## How we work

- One session per story group: 3 to 6 related stories that share files, finished well before the warn limit. A slice can take several sessions.
- A short close for small work; a full handoff when a slice is done or the context guard fires.
- Start each session by claiming its issue and reading its goal chain.
