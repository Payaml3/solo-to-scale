---
name: handoff
description: Close a session - a short close for small work or a story group, or a full handoff when a slice is done or the context guard fires - with the goal chain, the issue comment and the next-session line. Use when the founder says close, handoff or wrap up.
---

# handoff

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

Stop starting new work. Finish or revert the step in progress first.

## Pick the mode

| Situation | Mode |
| --- | --- |
| Small task, or a story group done with the slice still unfinished | **Short close** |
| A slice is done, or the context guard fired mid-slice | **Full handoff** |

When unsure, use the full handoff. A handoff happens at a slice end or when the guard fires; never write "stage done" for build work.

## Short close

1. In the chat, 3 lines: `Done: … / Pending: … / Next: …`.
2. Change `HANDOFF.md` only if the next step changed: one line in "Where we are" (`grep -n "| Now" HANDOFF.md`).
3. If slices, stories, registers or `founder/status.md` changed, run `python3 tools/build_roadmap.py`, `tools/build_team.py` and `tools/build_traceability.py`, and commit the data files.
4. Comment the 3 lines on the claimed issue (`gh issue comment <n>`, or the GitHub tools this session has).
5. Commit and push the branch.

## Full handoff

1. Summary of at most 15 lines (the protocol's closing summary):
   `Outcome / Approved (the founder's words only) / Pending (IDs) / Files changed / Risks / Next`.
   Pending includes any approval requests this session opened (`python3 tools/approval.py inbox`).
   Close out the claimed ticket with `python3 tools/tickets.py done`, `handoff` or `release` (`coordinate` skill), and list the tickets this session opened.
2. Write it into the files with line-level edits, never whole-file rewrites:
   - `HANDOFF.md`: build state, what was built, known gaps, next story groups
   - `founder/status.md`: risks, founder items, "Last updated"
   - decisions approved this session: through `record-decision`
   - slice done: `"status": "done"` in `founder/slices.json`, then regenerate the view data
3. Slice done: propose the next slice's story groups in `HANDOFF.md`, one line each:
   `Group N: <story IDs> (why grouped) · Model: <strongest | mid-tier>`.
4. Note which live views are now out of date (rows in `founder/artifacts.md` whose sources changed). **Never publish views here**; `publish-views` does that on Mondays.
5. Run `python3 tools/check_governance.py`; fix the cause of any failure, never weaken the check.
6. Commit, push, and open or update the PR. Close the claimed issue, or hand it to the next role with a comment and its `role:` label.

## Next session (both modes)

Start with the goal chain and the issue number, then end with exactly:

```
Goal chain: <company goal> → <initiative> → <stories> → <criteria>   (#<issue>)
Next session: <Project> · <slice> <group or task> | Model: <strongest | mid-tier> | First message: Claim issue #<n>, start from its goal chain, read AGENTS.md and HANDOFF.md, then <action>.
```

`<Project>` is `name` in `founder/project.json`. Never mark anything Approved without the founder's words in this session.
