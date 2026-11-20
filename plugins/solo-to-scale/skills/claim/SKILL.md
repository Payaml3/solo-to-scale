---
name: claim
description: Claim a story-group issue before starting work (label claimed, assign yourself), refusing one that is already claimed, and print its goal chain to start the session from.
---

# claim

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

One session, one claimed issue. Either tool can build, but only one tool per claimed issue.

## Steps

1. Pick the issue: the one named in the founder's first message or in the "Next session" line of `HANDOFF.md`.
2. Dry run first: `python3 tools/claim.py <issue> --dry-run`. It shows the labels to add (`claimed`, and the `role:` label from the issue's Owner section) and the goal chain.
3. Claim: `python3 tools/claim.py <issue>`. It uses `gh api`.
   - If `gh` isn't available, claim with the GitHub tools this session has: add the `claimed` label and assign yourself, then read the issue's "Goal chain" section.
   - If the issue is already labelled `claimed`, **stop**: tell the founder, and suggest the next unclaimed story group.
4. Start the session from the goal chain:

```
Goal chain: <company goal> → <initiative> → <stories> → <acceptance criteria>
Owner: role:<role> · Suggested model: <…> · Waits on: <…>
```

5. If the issue waits on something still open, say so before starting, and ask whether to proceed.

The claim is recorded in `.claude/state/claimed.json` (local, not committed), so the session-start hook shows it after a resume or a compaction. The handoff comments on, closes or hands on the issue at the end.
