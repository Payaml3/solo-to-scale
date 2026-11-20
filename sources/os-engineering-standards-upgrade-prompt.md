# Prompt: upgrade an existing repo to the engineering standards (paste into a Claude Code session)

> For repos that already run Solo to Scale. New repos get all of this from bootstrap v2.
> Session name: `<Project> · OPS Engineering standards`. Model: mid-tier.
> Paste everything below the line.

---

Read `CLAUDE.md` and `HANDOFF.md`, then only the files named below. Work on branch `ops/engineering-standards` from `main` and open one PR.
- Never read a whole file over 150 lines: use `grep -n`, then read only the ranges you need.
- Use no subagents; this is a small change.
- Don't touch product code (`apps/`, `eval/`, `sdks/`, `chain/`).
- Show me the plan first and wait for my approval.

## 1. `docs/engineering-standards.md` (new, one page)

List each standard and the stage where it starts:

- **Claude efficiency (now):**
  - `CLAUDE.md` under 200 lines, with area rules in subdirectory `CLAUDE.md` files
  - repeated reminders turned into checks
  - subagents only to protect context
  - tests for the changed area first
  - model chosen at the start of a session
  - prompt caching and Batch API for the product's AI calls
- **Delivery (now):** the five DORA metrics, PRs warned above 400 changed lines, merges within one business day.
- **Security:**
  - threat model with STRIDE (stage 10, a gate)
  - least privilege for agents and tools
  - pinned dependencies, automated updates, bill of materials and signed provenance (stage 16)
  - OWASP AI risks: prompt injection, excessive agency, and spending caps per customer (stage 21)
- **Reliability and scale:**
  - scale-ready defaults in the constitution (stage 10)
  - Well-Architected review (stage 10, then quarterly)
  - service targets, error-budget policy, alerts on user impact, restore and load tests (stage 21)
  - blameless postmortems
- **Performance and cost:** p95 speed budgets per key endpoint in CI, repeated-query (N+1) checks, unit cost per customer.

Point `CLAUDE.md`'s "Operating protocol" section to this file in one line.

## 2. Claude efficiency, now

- **`CLAUDE.md` size:** if it's over 200 lines, bring it under and keep it there.
  - Move conventions that apply to one area into a `CLAUDE.md` in that area's directory. For example, console rules go to `apps/api/src/<pkg>/console/CLAUDE.md`.
  - Keep the invariants and commands in the root file.
  - Report the line count before and after.
- **Two lines in `CLAUDE.md`:**
  - "Choose the model at the start of a session; don't edit `CLAUDE.md` or switch models partway through."
  - "During a session, run `make test-area AREA=<path>` for the changed area; CI runs the full suite."
- **Makefile:** add `test-area`, which runs pytest on one path (add the database flag only if the area needs it).
- **Efficiency rule:** update the one in the skills and `HANDOFF.md` "How we work" to: "Use subagents only for searches across 10 or more files, 3 or more independent pieces of work, or an independent review."
- **`.claude/governance.json`:** add `"claude_md_max_lines": 200` and `"pr_warn_lines": 400`.
- **`tools/check_governance.py`:**
  - fail if any `CLAUDE.md` exceeds the limit
  - warn above the PR size limit, not counting generated files, lock files or `backlog/`/`specs/` output from `make backlog spec`
  - add tests for both

## 3. Delivery metrics, now

In the `weekly-review` skill, add a "Delivery" block for the last 4 weeks, built from `gh api` and CI runs on `main`:
- deployment frequency
- change lead time (PR opened to merged, or to deployed once deploys exist)
- change failure rate (merges followed by a revert or hotfix)
- failed-deployment recovery time
- rework rate

Only the website deploys today, so report the others as "n/a until deploys exist". Never fill them with guesses.

## 4. Later stages: record them, don't build them

- In `founder/status.md`, add the stage 10, 16, 21 and 27 standards that this project hasn't met yet as **Proposed** founder items, each with the slice it should land in. Typical placement:
  - threat model and Well-Architected review before the first production slice
  - supply-chain items in that slice
  - service targets, spending caps, restore and load tests in production readiness, which is after the MVP
- If the project has a playbook or roadmap generator, add the same gates to it.
- Write no service targets, threat model or supply-chain jobs in this change. They need their own sessions and my decisions.

## Validate and close

1. Run `make lint typecheck test-fast governance` and the tool tests.
2. Show the `CLAUDE.md` limit failing on a deliberately padded copy, then revert it.
3. Show the new Delivery block from a dry run of `weekly-review`.
4. Open the PR, then give a short close: Done / Pending / Next. Include the proposed founder items and the suggested next session for the threat model, with the strongest model.
