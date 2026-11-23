---
name: weekly-review
description: The Monday review (scheduled task, or on request) - quiet-week stop first, then progress, CI, DORA metrics, budgets per role, stale items and one focus, as a status PR that is never merged by the review itself. Runs on the mid-tier model.
---

# weekly-review

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

Model: mid-tier. Run on the default branch.

## Step 0: the quiet-week stop

`SINCE` = the "Last updated" date in `founder/status.md` (`grep -n "Last updated" founder/status.md`). Check three things:
1. commits on the default branch since `SINCE`: `git log --since=<SINCE> --oneline origin/<default>`
2. PR activity since `SINCE`: `gh pr list --state all --search "updated:>=<SINCE>"`, or the GitHub tools this session has
3. the last CI result on the default branch: `gh run list --branch <default> --limit 1`, or the GitHub tools

If nothing is new and CI passes, reply in 2 lines and stop: no branch, no further reads.
`No change since <SINCE>; CI passing. Still blocking: <top founder item>.`
If GitHub can't be reached, say so and use the local git log only.

## Otherwise: the review, at most 25 lines

- **Progress:** stages and slices moved (`founder/roadmap.json`), stories and criteria done
- **CI health:** last runs on the default branch, flaky or failing checks
- **Delivery (last 4 weeks):** the five DORA metrics; method in `references/dora.md`. Report "n/a until deploys exist" rather than guessing
- **AI cost by role this month:** `python3 tools/heartbeat.py costs`, against the budgets in `founder/heartbeats.json`. Name roles over 80% and roles stopped at 100%, and how many entries are estimated rather than measured
- **Stale items:** Proposed or Open rows older than 7 days (grep the status and date columns of both registers)
- **Contradictions,** with both sources named
- **Merged branches not yet deleted**
- **Founder items** blocking the next stage
- **Approvals waiting** for the founder: `python3 tools/approval.py inbox`, oldest first; then `python3 tools/approval.py expire` closes those unanswered for 14 days (their roles re-plan)
- **Team activity:** from `python3 tools/tickets.py log --limit 100`, tickets finished and handed off per role, and tickets blocked or claimed for over a week
- **One recommended focus** for the week

## Then

1. Edit only `founder/status.md` (with "Last updated" set to today) and the stage statuses in `founder/playbook.md`.
2. Regenerate the view data (`python3 tools/build_roadmap.py`, `build_team.py`, `build_traceability.py`).
3. Branch `review/<date>`, commit, push, open a PR. **Never merge it**; the founder does.
4. Run `publish-views`, which stops by itself if nothing changed.

Monthly (first Monday) and quarterly reviews add the rows in `references/cadence.md`; the quarterly review asks all four advisors (`board-review`) to check the strategy against the evidence.
