---
name: release-check
description: Go or no-go before every demo, launch or production step - runs the repo's checks, reads the latest evaluation summary, lists the blocking gaps and founder items, and answers in at most 15 lines.
---

# release-check

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

## 1. Run every level

1. The repo's lint, type check, test and evaluation commands, from "Stack and commands" in `AGENTS.md`. If none are recorded, say so: that alone is a no-go for production.
2. `python3 tools/check_governance.py`.
3. The latest evaluation report: read only its summary section (`grep -n "^## " <report>`, then that range).

## 2. List what blocks it

- open known gaps in `HANDOFF.md` ("## Known gaps") that touch this release
- open founder items in `founder/status.md` that block it
- Proposed or Open decisions the release depends on
- **Production step only:** every row of "## Production readiness" in `founder/playbook.md` (security test, legal and data terms, monitoring and alerts, runbooks and the incident process, backups and restore, load test, service targets, spending caps, regulatory advice). Any row still To do is a no-go unless a decision marks it Not needed.

## 3. Answer in at most 15 lines

```
Release check: <demo | launch | production> at <commit>
Verdict: Go | No-go
Failing: <items, each with its source>
To turn it into a go: <the smallest set of actions>
```

A failing level is never a go. Prototype is not production: say which one this is. The founder decides; for production, the founder's approval is the second gate.
