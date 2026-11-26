---
name: record-decision
description: After the founder decides - write the decision row with the founder's own words, link the board memos, then list the downstream impact layer by layer and prepare the edits. Use when the founder approves, rejects or changes a decision.
---

# record-decision

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

## 1. Pick the register and the ID

- Business, GTM, pricing, brand, legal, hiring: `founder/decisions.md` (`B-`).
- Product behaviour, architecture, design, engineering: `specs/<feature>/decisions.md` (`D-`, plus `C-`, `G-`, `A-`) once Spec Kit has created it; until then the company register, with a Type column.
- Next ID: `grep -n "^| B-" founder/decisions.md | tail -1`.

## 2. Write the row

| Field | Rule |
| --- | --- |
| Status | Approved only with the founder's words in this session; otherwise Proposed, Assumption or Open |
| Date | Today |
| Source | The founder's exact words, quoted |
| Layers | Business → Product → MVP → Architecture → Tasks → Tests → Release: the ones it touches |
| Board | Link `board/<ID>.md` if `board-review` ran |

A changed decision gets a **new row** that supersedes the old one ("Supersedes B-04"), and the old row's status stays as it was, with "superseded by B-09" added.

## 3. Find the downstream impact

Layer by layer, search with `grep -n` for the decision's subject and the old ID across `founder/`, `specs/`, `docs/`, `founder/slices.json` and tests. List each affected item with its path and line.

## 4. File what it defers

Anything the decision leaves for later gets a row in `founder/next.md` now, not a "maybe later" in prose: the version it belongs to (`v1`, `v2`, ... or `always`), what, **why later** (exactly one of: not possible, needs a credential, out of scope), how it would be done (the mechanism and a link), and the decision ID as the source. The dashboard's Roadmap shows these as the version rail.

## 5. Prepare the edits

Write the edits as a list (path, line, change). Apply them **only if the founder says so**. Then:
1. Regenerate the view data if registers or slices changed (`python3 tools/build_roadmap.py`, `build_team.py`, `build_traceability.py`).
2. Run `python3 tools/check_governance.py`.
3. Commit with the ID in the message, for example `B-07: price per seat`.

In a Project chat (no repo access), give update-ready blocks, each labelled with its target path, instead of claiming files changed.
