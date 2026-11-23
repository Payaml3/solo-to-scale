---
name: coordinate
description: Use to delegate work between roles through GitHub issues - split a goal into sub-tickets per role, claim a ticket atomically, hand off to another role, record blockers, finish a ticket so its dependents wake up, see a role's queue, and read the activity log of who did what and why.
---

# coordinate

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need.

Roles work together only through tickets: GitHub issues labelled `ticket` and `role:<role>`. Every action goes through `python tools/tickets.py`, which comments on the ticket and appends to the activity log (the issue labelled `activity-log`). Always pass your own role (`--by` or `--role`).

## Start: find and claim work

1. `python tools/tickets.py queue <your role>`: open tickets for you that nobody holds and nothing blocks, oldest first.
2. `python tools/tickets.py claim <n> --role <your role> --why "<one line>"`.
   - The claim is atomic (a `refs/claims/<n>` ref): if it says refused, someone else has it. Pick another; never work on it anyway.
   - Refused also when the ticket is another role's, closed or blocked. Exit 5: GitHub was unclear; nothing is claimed.
3. Read the ticket's Goal and Done when. If it has a parent, `python tools/tickets.py tree <parent>` shows the plan.

## Delegate: split a goal across roles

- One sub-ticket per role and outcome: `python tools/tickets.py new <role> --title "<outcome>" --goal "<what>" --done-when "<check>" --why "<reason>" --parent <n> [--blocked-by <m> ...] --by <your role>`. A ticket with no parent names the objective it serves with `--objective O1` (`founder/goals.json`); sub-tickets inherit their parent's.
- Order the work with `--blocked-by`, not with prose. `--dry-run` shows the ticket first.
- With the `plan` gate on (`founder/gates.json`), run `python tools/tickets.py plan <parent> --by <your role> --note "<why this plan>"` once the sub-tickets exist: none can be claimed until the founder approves it. Adding a sub-ticket later means asking again.
- Delegate only to the six team roles or `chief-of-staff`. Advisors are asked through `board-review`, never ticketed.
- Adding a role, or giving one new powers, is the `hire` gate: use the `gate` skill.

## While working

- Waiting on another ticket: `python tools/tickets.py block <n> --on <m> --why "<what you need>" --by <your role>`, then release or pick ungated work.
- Need another role to continue: `python tools/tickets.py handoff <n> --to <role> --note "<state, what's left, where>" --by <your role>`. It frees your claim and moves the ticket to them.
- Stopping without finishing: `python tools/tickets.py release <n> --role <your role> --why "<state>"`.

## Finish

`python tools/tickets.py done <n> --role <your role> --note "<what you did, evidence, pull request>"` closes the ticket, releases the claim and unblocks every ticket that waited only on it. When the last sub-ticket closes, the parent gets a comment so its role can check the goal. Issues closed any other way (a merged pull request's `Closes #n`, the founder) get the same through the `tickets` workflow.

## Rules

- Write `role:<name>` in comments, never `@<name>`: an `@` notifies a real GitHub user of that name.
- A ticket never approves anything. A gated action on a ticket still goes through the `gate` skill; the founder's `/approve` lives on the approval request. Your notes are quoted, so they can't read as a founder command.
- One claimed ticket per session, as with `claim`. The handoff lists what you claimed, handed off and opened.
- `python tools/tickets.py log [--role R] [--ticket N]` shows the activity log; the weekly review summarises it.
