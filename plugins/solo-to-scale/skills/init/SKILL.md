---
name: init
description: Set up a startup's repo with the solo-to-scale operating system - assess read-only, ask the founder's questions together, then scaffold Founder HQ, instructions, tools and CI on branch ops/solo-to-scale and open one PR. Never overwrites a file.
---

# init

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

`<plugin>` is this plugin's root: `${CLAUDE_PLUGIN_ROOT}` in Claude Code; in Codex, two folders above this file. Run its scripts with `python3` (or `python` on Windows).

## 1. Assess, read-only, then stop

Run `python3 <plugin>/scripts/init_repo.py assess --repo .` and report in at most 25 lines:
- what exists (docs, specs, registers, CI, instruction files, `.claude/`, skills, hooks)
- whether the default branch is current, and work that sits only on unmerged branches
- duplicates and contradictions (two registers, two plans, the protocol in several places)
- which recommended plugins this session can see: founder, Superpowers, marketing, brand-skills, Spec Kit. List your available skills; being enabled on an account doesn't mean a repo session loads it
- which interfaces use React (only those can use shadcn/ui)

If the report suggests `upgrade` (a version file or existing Founder HQ), stop and propose the `upgrade` skill instead.

## 2. Ask: quick start, or everything in one round

Offer **quick start** first: ask only question 1 and the company goal, take every default in `references/questions.md`, and list those defaults in the plan and the PR so the founder can change any before merging (or later, by editing the founder-owned files). Otherwise ask all of them in one round.

Ask with your question tool (AskUserQuestion in Claude Code; a plain numbered list in Codex). Details and defaults: `references/questions.md`.
1. Project name, and whether it's a working name; repo (`owner/name`); one line; stage (1 to 30); and the company goal in one measurable sentence ("100 paying studios by June 2027"), or blank for later
2. The four context-guard limits (default 60%, 75%, 100k, 140k tokens)
3. The monthly budget for each role
4. Which recommended plugins to enable in `.claude/settings.json` (only those the project needs)
5. Which interfaces use React
6. The epic-to-role split (propose one from the repo's epics; the founder confirms)
7. Whether to add the optional cross-review CI job (off by default)
8. Whether to create the labels `role:*`, `claimed`, `blocked`, `founder-item` now
9. At stage 20 or later: whether to enable the sales advisor

Write the answers to a temporary `answers.json` outside the repo (format: `references/answers.md`). Never put secrets in it.

## 3. Show the plan, wait for approval

Run `python3 <plugin>/scripts/init_repo.py plan --repo . --answers <answers.json>` and show the summary: files to create, files that exist (merge proposed, never overwritten), notes. Wait for the founder's go.

## 4. Scaffold and open one PR

1. `python3 <plugin>/scripts/init_repo.py apply --repo . --answers <answers.json>`: switches to `ops/solo-to-scale`, writes only missing files, generates the view data, and writes the merge proposals to `.git/solo-to-scale-proposals.md`.
2. Run `python3 tools/check_governance.py --base <default branch>` and `python3 -m pytest -q tools/tests`; fix any failure the scaffold caused.
3. `git add` the written files only, commit ("solo-to-scale init"), `git push -u origin ops/solo-to-scale`.
4. Open one PR into the default branch: `gh pr create`, or the GitHub tools this session has; if neither works, print the title and body for the founder. Body: what each file does, how to turn each automation off (`references/pr-body.md`), the merge proposals, the ASK answers under **Approved**, everything else under **Proposed**. If the product's code has its own brand or name setting, point it at `founder/project.json` and say so.
5. Labels: only if the founder said yes in step 2 (`gh label create`, or list them as a manual step).

Never push to the default branch. Never mark anything Approved beyond the founder's answers.

## 5. First work, then the manual steps

Propose three starter tickets for after the merge, matched to the stage (for example: write the business context; validate the idea with `founder:validate-idea`; plan five customer interviews). Open them with `python3 tools/tickets.py new ...` only when the founder says yes. Then suggest setting this quarter's objectives in `founder/goals.json`, and running the `doctor` skill once the PR is merged: it lists what is still to set up.


1. Create the Claude Project from `founder/claude-project/` (paste `instructions.md`; add the 8 files in `knowledge.md`).
2. Create the Monday scheduled task from `founder/claude-project/weekly-review-task.md`, in a session with artifact tools.
3. Add the solo-to-scale marketplace on claude.ai (`Payaml3/solo-to-scale`), so Project chats get the decision skills.
4. Add the repo secrets the founder items list. Never commit them.
5. Before stage 6, where `product-design` is first used, confirm the design skills are available. At stage 11, run `design-system` to set the foundations.

Close with a short close: `Done / Pending / Next`, and a "Next session" line naming the project, model and first message.
