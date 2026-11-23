---
name: gate
description: Use before any critical action (hire or change a role, raise a budget, deploy, send or publish anything outside the repo, spend money, approve a decision, change prices, anything legal) to check founder approval, request it as a GitHub issue and wait; also lists the founder's approval inbox.
---

# gate

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need.

The founder approves critical actions; agents never do. The gates and their modes are in `founder/gates.json`: `ask` (request and wait), `allow` (go ahead), `off` (founder only: never do it, raise it as a founder item).

## Before a gated action

1. Find the gate in `founder/gates.json`. If you're unsure whether an action is gated, treat it as gated.
2. Check for an approval: `python tools/approval.py check <gate> --scope "<short scope>"`, or `--issue <n>` for an earlier request.
   - Exit 0: approved. Go ahead, then comment on the request what you did and close it if it was a one-off.
   - Exit 3: no approval yet. Go to step 3.
   - Exit 4 or 5: not approved, founder-only, or GitHub unreachable. Stop the action and report it. Never retry around it.
3. Request it: `python tools/approval.py request <gate> --title "<what>" --why "<reason, evidence>" --impact "<cost, risk, reversible or not>" --scope "<scope>" --role <your role>`.
   - Use `--dry-run` first to check the text. One request per action. Say what happens if the founder says no.
4. Stop that action and carry on with ungated work. Record the request number in the handoff and the issue you're working on.

## Rules

- Only the founder's own GitHub comment decides: `/approve`, `/approve always` (a standing rule for that gate and scope), `/reject <reason>`, `/revoke`. Labels, bots, other people and your own comments never count.
- Never split an action to stay under a gate, and never ask the founder to approve inside a pull request description instead.
- Pull requests that change gated files (the `paths` in `founder/gates.json`) need the founder to add the `founder-approved` label; the `founder-gates` check enforces it.
- Changing `founder/gates.json` is itself gated (`hire`, through `founder/team.md` rules): propose the change, never make it.

## The founder's inbox

`python tools/approval.py inbox` lists open requests with their state. The weekly review and the handoff include it.
