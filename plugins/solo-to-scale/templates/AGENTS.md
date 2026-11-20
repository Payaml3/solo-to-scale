# {{project.name}}

{{project.one_line}}

<!-- solo-to-scale:begin (plugin-owned; upgrade re-renders this block. Edit outside it.) -->
{{include:agents-fragment.md}}

## How we work

- **Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the ranges you need. Use `git diff` and `git log` to see changes.
- **One story group per session.** Finish well before the context guard's warn limit.
- **Test the changed area first:** `python tools/test_area.py <path>` (or `make test-area AREA=<path>`). CI runs the full suite.
- **Subagents** only for searches across 10 or more files, 3 or more independent pieces of work, or an independent review.
- **Plugins that write to `founder/`** (founder, brand-skills) never overwrite `status.md`, `decisions.md`, `business-context.md`, `playbook.md` or `artifacts.md`; those change through the skills. Brand outputs go to `founder/brand.md`.
- **No secrets** in the repo or in development sessions. Only the founder adds production secrets.
- **Session hygiene:** choose the model at the start of a session. Don't edit `AGENTS.md`/`CLAUDE.md` or switch models partway through; that rebuilds the prompt cache. A session can't switch its own model, so every "Next session" line recommends one.

## Model choice

| Work | Model |
| --- | --- |
| Architecture, security, money, data integrity, system foundations | Strongest available |
| Routine features, docs, copy, screens, reviews, handoffs, the weekly review | Mid-tier |
| Formatting, renames, simple lookups | Smallest that works |

The weekly review runs on the mid-tier model; its quiet-week stop keeps it cheap.

## Checks

- `python tools/check_governance.py`: registers, protocol in one place, handoffs, view data, instruction size, PR size.
- `python tools/build_roadmap.py --check`, `python tools/build_team.py --check` and `python tools/build_traceability.py --check`: view data matches its sources.
<!-- solo-to-scale:end -->

## Invariants

<!-- The rules that must always hold for this product. Open until the founder approves them at stage 10. -->
- Open

## Stack and commands

<!-- Filled in at stage 10, with the lint, type-check and test commands. -->
- Open
