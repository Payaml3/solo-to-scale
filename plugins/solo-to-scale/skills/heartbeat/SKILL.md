---
name: heartbeat
description: Use when a scheduled task wakes a role, or to set up or review role heartbeats and AI budgets - check the role's budget, take its run lock, resume or claim one ticket, work it, hand off or open a pull request or approval request, record the run's cost, and stop; also lists schedules, task prompts and spend per role.
---

# heartbeat

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need.

A heartbeat is one short, unattended run of one role: one ticket, within its budget, then stop. The policy is `founder/heartbeats.json` (founder-owned; changing it is the `budget` gate). Everything goes through `python tools/heartbeat.py`.

## Set up (chief-of-staff, with the founder)

1. The founder sets `enabled` and `monthly_budget_usd` per role in `founder/heartbeats.json`, through a pull request with the `founder-approved` label. A role without a budget never runs.
2. `python tools/heartbeat.py plan` prints each role's schedule (cron, UTC), budget, spend, and the prompt for its task.
3. The founder creates one cloud scheduled task per enabled role on this repo, with that schedule, that prompt, and the role's model from the `AGENTS.md` table (Claude Code: `/schedule`, or the scheduled tasks page). Creating them is the founder's step: tasks spend money.

## Each run

1. `python tools/heartbeat.py start <role>`.
   - Exit 6 (stop): heartbeat off, no budget, budget spent, or another run of this role is active. Do nothing else; end the turn. At 100% it opens one budget request for the founder.
   - Exit 2 (nothing to do): no ready ticket. Run step 5 and stop. No other work.
   - Exit 5: GitHub was unclear; nothing is claimed. Stop.
   - Exit 0: it prints `resume #n` (your earlier claim) or `work on #n` (claimed now, atomically). It also prints the budget left; over 80%, keep the run small.
2. Read the ticket's Goal and Done when, and its goal chain. Work only on it, as that role, inside this run.
3. Gated actions (deploy, external, spend, pricing...) go through the `gate` skill: request approval and do not wait in the run. Release or block the ticket and end.
4. Finish with one of (the `coordinate` skill):
   - open a pull request that closes the ticket (`Closes #n`); then `tickets.py handoff` to `qa` or the reviewer role, or `done` if nothing is left;
   - `tickets.py handoff <n> --to <role> --note "<state, what's left, where>"`;
   - `tickets.py block` or `release` with the state, when it can't go on.
   A ticket you keep claimed is resumed next run; say so in its comment.
5. `python tools/heartbeat.py end <role> --ticket <n> --note "<one line>"`: it records the run's cost (measured from this session's transcript, or `--usd`; else a flat estimate) and frees the run lock. Always run it, even after exit 2 or an error.

## Budgets

- Costs are AI usage only (API-equivalent prices in the policy), one issue per month labelled `cost-log`. `python tools/heartbeat.py costs` shows spend per role against budget.
- 80%: a warning in the cost log (and on the ticket). 100%: `start` refuses until next month, or until the founder `/approve`s the budget request, which adds one more month's budget for this month.
- Interactive sessions count too: the `handoff` skill runs `heartbeat.py end <role>` with the session's cost.
- Never edit `founder/heartbeats.json`, a cost entry or a budget request yourself. A budget raise is the founder's.

## Rules

- One ticket per run, one run per role at a time. Never claim a second ticket in the same run.
- No questions to the founder inside a run: nobody is watching. Put them on the ticket or an approval request.
- Write `role:<name>`, never `@<name>`.
