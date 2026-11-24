---
name: okr-plan
description: Draft the goal tree in founder/goals.json - the North Star, the cycle's objectives and key results, and the initiatives under them - once the business model (stage 3) is approved; and score each cycle and draft the next. The founder approves it by merging.
---

# okr-plan

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need.

Read `AGENTS.md`, `HANDOFF.md` and `founder/operating-protocol.md` first. Run as `chief-of-staff`, with `product` and `growth` consulted for their key results. Model: strongest for the first North Star, mid-tier for later cycles. No subagents.

## When

- **First draft:** stage 3 (Business model and positioning) is Passed, or `python tools/goals.py show` prints `due: draft`. Refine it when stage 5 (Product and operating model) is approved.
- **Each cycle's end:** `goals.py show` prints `due: review`, or the weekly review finds the cycle has ended.
- Never before stage 3 is approved: a North Star needs an approved business model. Until then, work names no objective.

## Inputs: approved material only

`founder/business-context.md`, the approved business-model and positioning decisions (`B-` in `founder/decisions.md`), the investment case or plan in `founder/sources/` if there is one, `founder/playbook.md` (the current stage and its gates) and `founder/finance.json`. If the target the business model needs is Proposed or Open, **stop and ask**.

## The method: four layers, each linked to the one above

1. **North Star:** `goal` (one sentence, at most 300 characters) and `north_star` (`metric`, `unit`, `baseline`, `target`, `current`, `by`). One number that says the business works, taken from the business model: "£10k MRR by November 2027", not "grow".
2. **Cycle OKRs:** `cycles` (`C1`, `start`, `end`). Before product-market fit (stage 24 not Passed) a cycle is 6 weeks (`goals.py cycle`); after it, a quarter. Each cycle has **2 or 3 objectives** (`O1`: a qualitative outcome, an owner role, `"cycle": "C1"`, `why`) with **2 to 4 key results** each (`O1.1`: a metric with baseline, target and current). Outcomes, not tasks: "5 of 8 interviews confirm the pain", never "do interviews".
3. **Tie key results to stage gates before launch.** Until stage 22 (General availability) is Passed, at least one key result per cycle proves the next playbook gate and carries `"stage": N` (stage 2: "5 to 8 interviews show pain and willingness to pay"). Passing the gate still goes through `weekly-review` and the founder.
4. **Initiatives:** `initiatives` (`I1`, `title`, `key_result`, `owner`, `status` planned, active, done or dropped, optional `epic`). The key actions and epics that move one key result. Each key result has 1 to 3. Then every ticket names its initiative: `python tools/tickets.py new <role> ... --initiative I1` (the label `initiative:I1`, plus the objective's `goal:O1`); sub-tickets inherit both. Epics and slices in `slices.json` keep `"objective": "O1"`.

Template and a worked example: `references/goals-example.md`.

## Draft

1. Write the tree in `founder/goals.json` on a branch. Score it before asking: is every key result measurable now, owned, and reachable in the cycle; does every objective serve the North Star; is there an initiative for every key result? Fix what fails.
2. `python tools/goals.py check` must pass; `python tools/goals.py show` prints the tree for the PR body. Fix every `advice:` line or say why it stays.
3. Open one PR titled `Goals: North Star and cycle C1`. `goals.json` is behind the `decision` gate, so it needs the founder's approval label: say so, list the open choices (the North Star number, the cycle length) with a recommendation, and never merge it. The founder's approval is recorded with `record-decision` as a `B-` decision.
4. After the merge, open the tickets for the active initiatives with `coordinate`.

## Review a cycle

At the cycle's end: record each key result's final value (`goals.py update`), score each objective (its progress; 70% is a good cycle), and write three lines in the PR: what moved the North Star, what didn't, what changes. Mark objectives `achieved` or `cancelled`, initiatives `done` or `dropped`. Then `goals.py cycle` and draft the next cycle as above, in the same PR. Values in between change through `goals.py update` PRs by each key result's owner.

Close with `handoff`.
