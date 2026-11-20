# Prompt: set up the AI team (paste into a Claude Code session)

> For any repo on Solo to Scale. Session name: `<Project> · OPS AI team`. Model: mid-tier.
> Paste everything below the line.

---

Read `CLAUDE.md` and `HANDOFF.md`, then only the files named below.
- Work on branch `ops/ai-team` from `main` and open one PR.
- Don't touch product code.
- Never read a whole file over 150 lines; use `grep -n` and ranges.
- Show me the plan first and wait for my approval.

## 1. Role definitions (`.claude/agents/<role>.md`, each under 60 lines)

Create seven role files: `chief-of-staff`, `research`, `product`, `architect`, `engineer`, `qa`, `growth`. Each one has:
- **frontmatter:** `name`, and a one-line `description` saying when to use the role. Keep descriptions short, because they load into every session.
- **mission:** one or two sentences
- **what it owns:** functions, epics and files
- **skills:** the ones it uses, as listed in the operating system doc's "The AI team" table
- **tools:** least privilege. Engineers get edit, test and git; research gets web search and read-only repo access; nobody gets production secrets.
- **model:** recommended per task type
- **inputs and outputs:** which issues, files and registers it reads and writes
- **approval:** what needs the founder's approval
- **never:** at least the rule in the doc

Epic ownership: the default split by kind of epic (`init` lists the repo's epics and the founder confirms the mapping):
- architect: foundation, operations and audit epics
- qa: evaluation and test epics
- growth: website, docs and SDK epics
- engineer: all other epics
- product: prepares the C-, G- and A- decisions
- research: the non-software model items

Write the mapping once, in `founder/team.md`. The roles, `tools/build_team.py` and `tools/build_traceability.py` all read it. In the dashboard, Architecture counts criteria in the architect's epics, Engineering counts the engineers' epics, and Founder HQ counts decisions resolved.

## 2. `founder/team.md` (one page)

- The org: the founder as CEO and board, Claude as the AI core, and the six roles.
- The epic-to-role mapping.
- Each role's schedule.
- Each role's monthly Claude budget, in a table with role and budget. Mark the budgets **ASK**, because I set them.
- The rules:
  - one role per session
  - roles talk only through issues, PRs, registers and `HANDOFF.md`
  - a role proposes, the founder approves

## 3. Tickets with a claim step

- Add `.github/ISSUE_TEMPLATE/story-group.md`. It has:
  - the goal chain at the top: company goal → initiative → stories → acceptance criteria
  - the owner role, and the suggested model
  - "waits on", meaning the issue or founder-item IDs it depends on
  - a definition-of-done checklist
- Create the labels `role:<role>`, `claimed`, `blocked` and `founder-item`.
- Add `tools/claim.py <issue>`. Using `gh api`, it refuses to claim an issue already labelled `claimed`. Otherwise it labels and assigns the issue, then prints the goal chain to start the session with.
- Update the `handoff` skill: a short close comments on the issue, and a full handoff closes it or hands it to the next role.
- **ASK** before creating issues for the next slice's story groups. Creating them is visible, so show me the list first.

## 4. Goal chain everywhere

- Update the "Next session" line in the `handoff` skill. It now starts with the goal chain and the issue number.
- Update `session_start.py` to print the claimed issue's goal chain, if there is one, within its 25-line limit.

## 5. Budgets in the weekly review

Add a block to the `weekly-review` skill: **Claude usage by role this month**, against the budgets in `founder/team.md`.
- Warn at 80% of a role's budget.
- At 100%, propose pausing that role.
- If usage can't be measured per role yet, say so plainly, and show the session count per role from the issue labels instead.

## 6. Keep the team view live

- Add `tools/build_team.py`; I'll provide the script. It writes `founder/team.json` with roles, tasks and dependencies.
- Add `make team` with a `--check` mode for CI.
- Register the team view in `founder/artifacts.md` with the slug its first publish returns, so `publish-views` rebuilds it.
- Register the traceability dashboard the same way, with its slug and `tools/build_traceability.py`.

## Validate and close

1. Run `make lint typecheck test-fast governance` and the tool tests.
2. Run `tools/claim.py` in dry-run mode on a sample issue.
3. Check that each role file is under 60 lines.
4. Open the PR, then give a short close, listing the **ASK** items I still need to answer: the budgets and the issue list.
