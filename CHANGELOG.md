# Changelog

## v2.8.0 (2026-11-24)

A design pass on the dashboard and the portfolio with the design skills from v2.4.0: a scored review, layout and accessibility fixes, and motion with a job.

- **The review** is in `DESIGN-BRIEF.md`: each dimension scored 0 to 10 before and after, with the advice taken from UI/UX Pro Max and Emil Kowalski's skills. Everything that scored under 8 was fixed.
- **Layout and UX.** On desktop the tabs are a sidebar on the left, so every tab is visible at once; on phones and tablets they stay a strip along the top. The theme switch moved from a floating pill over the content into the header, with a sun or moon icon. On a phone, goal rows stack instead of squeezing to one word a line, and the tab strip fades at an edge that has more tabs. Goal bars follow their pace: green achieved, ink on track, amber behind (they were amber whenever a goal was short of 100%).
- **Accessibility.** The light `todo` grey is now `#6e6e6e` (5:1 on white; it was 3.3:1, under AA). Focus rings on document groups, cards and the document list. No more weight-700 text or uppercase labels, as `DESIGN.md` says.
- **Motion,** only `transform` and `opacity`, with a strong ease-out: the tab underline slides, a tab's content fades up as it opens, progress bars fill once, pressables scale on press, the toast rises in, and a working agent's status dot breathes. Hover effects only with a mouse. Reduced motion keeps short fades and drops the rest.
- **`DESIGN.md`** gains motion tokens and a Motion section. Existing repos get the new pages with `upgrade`.

## v2.7.0 (2026-11-24)

The goal tree: a North Star, short OKR cycles and initiatives, so every ticket traces back to one number.

- **Four layers in `founder/goals.json`.** The **North Star** (`goal` plus a measurable `north_star`: metric, unit, baseline, target, current, by), **cycles** (`C1`, `C2` with start and end dates: 6 weeks before product-market fit, then quarters), **objectives** with 2 to 4 **key results** each (now with `"cycle": "C1"`, and an optional `"stage": N` for the playbook gate a key result proves before launch), and **initiatives** (`I1`: the key actions and epics, each linked to one key result, with an owner, a status and an optional epic). Existing files keep working: every new field is optional.
- **Tickets link to initiatives.** `tickets.py new --initiative I1` adds the labels `initiative:I1` and its objective's `goal:O1`; sub-tickets inherit both. Once the active objectives have initiatives, a ticket that names none is refused.
- **`okr-plan`, a new skill.** Once the business model (stage 3) is approved, the chief of staff drafts the whole tree from the business model, the investment case or plan and the playbook, scores it, and opens one PR. `goals.json` is behind the `decision` gate, so the founder approves it by merging. It's refined at stage 5, and at each cycle's end it scores the cycle and drafts the next. A worked example is in `references/goals-example.md`.
- **`tools/goals.py`:** `show` prints the tree with `due:` (draft after stage 3, review at a cycle's end) and `advice:` lines (more than 3 objectives, a key result count outside 2 to 4, an objective with no initiatives). `cycle` adds the next 6-week cycle. `update north-star --value N` records the North Star. `check` covers the new layers.
- **The Goals tab shows the whole tree:** North Star with progress, the current cycle, then each objective's key results with the stage gate they prove, the initiatives under each, and each initiative's open tickets. The Overview's Goals panel adds the North Star and what's due. Pace uses the cycle's dates. The portfolio summary carries the North Star.
- **The playbook** (new repos) says when the goal tree is drafted, at stages 3 and 5. Existing repos keep their playbook (it is founder-owned); `okr-plan` works either way.
- **Docs:** the handbook's goals section is rewritten as "Goals: North Star, OKRs and initiatives", with a diagram; the cadence adds the cycle review; the chief of staff owns `okr-plan`.
- **Tests:** 6 new, covering the tree, the new checks, when drafting and reviews are due, the cycle and North Star commands, tickets naming initiatives, and the tree on the page.

## v2.6.0 (2026-11-24)

A Gantt chart on the dashboard's Roadmap tab.

- **Timeline panel** on Roadmap, under the counts: phases A to G with their stages, then the slices, as bars over time. A dashed box is the plan, a solid bar is what happened (green done, amber in progress, red past its target), with a line for today. Each phase bar spans its stages. Hover a bar for its dates. It works in both themes; on a phone the labels stay put and the chart scrolls sideways, opening on today.
- **Planned dates** come from optional `Start` and `Target` columns in `founder/playbook.md` and `start` and `target` on each slice in `founder/slices.json` (YYYY-MM-DD). Nothing is required: undated items are left out and the panel says how to add dates.
- **Actual dates** come from git: the commit that first moved a stage or slice to in progress, and the one that moved it to done. The dashboard workflow now checks out full history so it can read them. Existing repos get both with `upgrade`.
- **Tests:** 2 new: planned and actual dates from a repo's history, and a build without git.

## v2.5.0 (2026-11-24)

The Overview shows the journey from zero to scale simply, and keeps only what a founder checks every day.

- **Your journey, on the Overview.** The 7 phases as 7 cards, each with its question in plain words ("Is the problem real?", "What do we sell, and to whom?"), its stages as cells, how many are passed, and whether it is done, current (**You are here**) or ahead. Under them, the current phase's stages as steps, then the current stage: what "done" means, who leads it, what comes next, what blocks it and which agents are on it now. On a phone the phases stack as a list. Every card opens the full ladder.
- **Who leads a stage** comes from the playbook's Where column: `P 02` or `Code 04` is that role, `P 00` is you with the chief of staff. The roadmap data now carries `where` for each stage.
- **A shorter Overview.** Four tiles (needs you, agents working, runway, AI spend), each opening its tab; the top five of Needs you; your journey; your AI team with the latest four activities; the goals.
- **Moved, not removed.** The full stage ladder with gates and evidence is now in Scope and journey (it replaces the plain phase list there). Money is at the top of Costs. The last 14 days and recent merges are in Agent activity. Slices done, open tickets, decisions waiting and stuck work are tiles on Roadmap. The "This stage" panel is folded into the journey.
- **Tests:** 1 new: the Overview's order and contents, where each moved panel went, and the Where column reaching the page.

## v2.4.0 (2026-11-24)

The design gate: product design is finished and approved before any code.

- **Stage 9 is now Product design.** Once the product model (stage 5) and MVP scope (stage 7) are approved, `product-design` acts as the product designer and writes `docs/design/brief.md` (new template). The brief covers 3 to 5 reference products (Mobbin, Refero, Land-book, Httpster, Component Gallery), the look to follow (a company's DESIGN.md from awesome-design-md, adapted to the brand, or our own), the key flows, and where components come from for the stack. The founder approves it as a `D-` decision. The screen specs are written at the same stage, as before.
- **Stage 11 writes `DESIGN.md`** next to `tokens.json`, following the brief.
- **Enforced in CI.** `check_governance` fails a branch that moves stage 13 or later to Current or Passed unless stages 9 and 11 are Passed and `DESIGN.md` and `docs/design/brief.md` exist. Repos that were already building, or that adopt the playbook while building, get a warning instead.
- **Design tools across the journey:** reference products for the prototype at stage 6; Magic UI or Aceternity UI sections for the website at stage 18 when it uses React. The handbook's stage table and "The design gate" section cover all of this.
- **Existing repos:** the playbook is founder-owned, so `upgrade` doesn't rename stage 9. Rename it and update its gate by hand to pick up the new wording. The gate itself checks stage numbers, so it works either way.
- **`docs/design.md`: how we do design, in one place.** It covers the journey stage by stage, the design brief, the gate, component sources by stack, who leads when, the rules that always hold, and the design skills. The handbook's design sections moved there and the handbook points to it.
- **Design skills chosen.** `ui-ux-pro-max` gives industry rules and palette and type options for the brief, as advice only. Emil Kowalski's skills cover motion and polish at build and QA. `app-store-screenshots` is for mobile apps at launch, run outside the product repo. The built-in `frontend-design`, `impeccable`, `design-taste-frontend` and `emil-design-eng` keep their roles. All are recommended installs, none bundled. gstack was considered and not used: it overlaps with our roles, hooks and gates. Its 0-to-10 design review idea now scores the brief: everything under 8 is fixed before approval.
- **Tests:** 2 new: the gate blocking and then allowing the build, and the warning for a repo that was already building.

## v2.3.0 (2026-11-24)

A new look for the dashboard and the portfolio, written down in `DESIGN.md`.

- **`DESIGN.md`** at the repo root: the design system for the generated pages, in the DESIGN.md format agents read. It starts from the Vercel analysis in VoltAgent/awesome-design-md (MIT) and adapts it to a dense dashboard: our own name, system fonts (the page's security policy blocks web fonts), a real dark theme and status colours.
- **The pages follow it.** Near-white (or black) canvas, hairline cards with a soft stacked shadow, ink as the only accent, tighter headings and large tabular numbers, mono for build lines and tags, tinted status pills, a translucent sticky tab bar, and tables with a header band and row hover. Same layout, data and behaviour. Existing repos get it with `upgrade`.
- **Contrast fixes in dark mode:** text on filled status colours (the Needs you count, passed stage marks) and the founder's avatar now stay readable.
- **Design references in `design-system`:** at stage 11, each proposed direction may start from a company's DESIGN.md in awesome-design-md, and the chosen one becomes the venture's own `DESIGN.md`. The handbook says which component libraries fit which stack (shadcn/ui, 21st.dev, Magic UI and Aceternity UI need React; Uiverse is plain CSS).
- **CI:** the drift check fails if a colour in `DESIGN.md` and the pages' CSS disagree, in either theme.

## v2.2.0 (2026-11-24)

The venture stage, as a ladder on the Overview.

- **Venture stage panel.** Every stage of `founder/playbook.md`, phase by phase (A to G), marked passed, current, deferred or not started, like a readiness ladder. A strip shows all stages at a glance; each phase opens to its stages with the gate and the evidence that it was met. Phases up to the current one start open. It sits right under Needs you, above This stage.
- **Honest by construction.** A passed stage with no evidence says so. A stage before the current one that isn't Passed or Deferred shows as **Not passed** in red, so the page never shows more progress than the playbook records.
- **An Evidence column in the playbook** (new repos): decision IDs, files or links. Decision IDs open Decisions and repo files open Documents. Existing repos keep their playbook (it is founder-owned); add the column by hand, between Gate and Status, and the ladder picks it up. Until then it says the evidence isn't recorded. `weekly-review` names the evidence when it proposes a stage as Passed or Deferred.
- **Fixed:** This stage and Scope and journey only counted stages marked "done" as finished; they now count Passed and Deferred, the playbook's own words.
- **Tests:** 1 new: the ladder's data with evidence, hostile evidence text staying text, and an older playbook without the column.

## v2.1.0 (2026-11-23)

Vercel as a second home for the dashboard and the portfolio. Cloudflare stays the default.

- **`provider` in `founder/dashboard.json`** (and `founder/portfolio.json`): `"cloudflare"` (the default) or `"vercel"`, with `vercel_project` and `vercel_team` (a team slug or `team_` id; empty for a personal account). The only new secret is `VERCEL_TOKEN`.
- **Still behind a login, or not at all.** On Vercel, `guard` deploys only when the project has the host as a domain, has no Git repository connected (so a deploy can never replace the app itself), and has Vercel Authentication on All Deployments. Standard Protection leaves the production domain public, so it doesn't count, and a shared password doesn't either. `verify` then checks every domain of the project, plus `<project>.vercel.app`, as an anonymous visitor, and fails the run if any serves the page.
- **The workflows** deploy with the Vercel CLI (pinned) when the guard says so, using the project and account ids the guard read, and keep the Cloudflare step for everyone else.
- **The doctor** checks the Vercel setup: a known provider, a well-formed project and team, and `VERCEL_TOKEN` set.
- **Cost:** Vercel Authentication on All Deployments is free on every plan since Vercel's 2026 change; a company dashboard belongs on Pro ($20 a month per member) because Hobby is for non-commercial use. The handbook has the details.
- **Docs:** the handbook ("The startup dashboard": the Vercel setup steps and cost; "The portfolio") and the README.
- **Tests:** 6 new: Vercel without a token or with a bad provider, the guard failing closed (no login, previews only, Standard Protection, wrong domain, the app's own project, injected ids, the API refusing), a deploy allowed with team scope, verify across every domain, both workflows gated on the guard, and the doctor's Vercel check.

## v2.0.0 (2026-11-23)

Slice 12 of `ROADMAP-V2.md`: money. This completes v2.0 (slices 6 to 12).

- **Runway on the first screen.** A new founder-owned `founder/finance.json` (the `spend` gate) holds cash and its date, monthly revenue, fixed costs (tools, hosting, ads) and one-off items by month. The Overview's new Money panel shows monthly revenue, net burn, runway in months (red under six) and AI spend as a share of costs. AI spend is the cost log's month-end forecast, or the month so far. `tools/finance.py show` prints the same and `finance.py check` validates the file; `check_governance` fails on a malformed one. The portfolio summary carries MRR, net burn and runway.
- **A company-wide AI budget.** `company.monthly_budget_usd` in `founder/heartbeats.json` caps all roles together. Every `heartbeat.py start` checks it as well as the role's cap, and prints both. The 80% warning and the 100% stop apply to the total: at 100% every role stops and one company budget request (scope `heartbeat:company:<month>`) waits for the founder's `/approve`, which adds one more month's company budget. `heartbeat.py costs` shows the total against it. The Costs tab gets a company budget bar, and a spent company budget joins Needs you.
- **The doctor** checks that `founder/finance.json` is behind the `spend` gate, and `--repair` adds it. `upgrade` writes an empty `finance.json` into existing repos.
- **Docs:** the handbook (repository map, budgets, runway) and the `heartbeat` skill.
- **Tests:** 4 new: runway, burn, one-offs and AI share; an empty, profitable or malformed finance file; the company cap's warning, stop, single request and approval; and money and the company budget on the page.

## v1.14.0 (2026-11-23)

Slice 11 of `ROADMAP-V2.md`: review before approval and a chain of command.

- **Review before done.** A ticket can need a review by another role, shown by the label `needs-review:<role>`. `tickets.py new --review <role>` sets it, or the new `review` map in `founder/gates.json` does it per role (new repos: QA reviews the engineer, product reviews growth; `--review none` skips it). `tickets.py review <n> --verdict approved|changes --by <role> --note "..."` records a verdict on the ticket and in the activity log. `done` is refused until the reviewer's latest verdict is approved, and a role can never review its own ticket. `queue` lists the reviews waiting for a role.
- **Chain of command.** Every team role has `reports_to` in `roles/*.yaml` (the six roles report to the chief of staff, and the chief of staff to the founder), and each agent file gains a "Reports to" section. `tickets.py escalate <n> --by <role> --why "..."` labels the ticket `escalated-to:<manager>`, comments and logs it; the manager's `queue` shows it. Only the chief of staff escalates to the founder.
- **The dashboard:** escalations to you join the Needs you list, right after approvals, with their own tile. Agent cards show who each role reports to, and an agent's tickets show review and escalation state.
- **Not yet:** the CI gate check doesn't read review verdicts on gated pull requests; the founder's `founder-approved` label stays the only gate there.
- **Docs:** the handbook and the `coordinate` skill.
- **Tests:** 6 new: the review flow with changes then approval, no self-review and `--review none`, escalation up the chain, reviews in the queue, escalations and review state on the page, and `reports_to` agreeing with the tickets tool.

## v1.13.0 (2026-11-23)

Slice 10 of `ROADMAP-V2.md`: governance 2, control from the phone.

- **`/revise <what to change>`** on any approval request. The role changes the work and runs `approval.py resubmit <n> --note "..."`, and the request waits for the founder again on the same issue. A resubmission only moves a request from "revision" back to "waiting", never to approved. `check` exits 7 on a revision and prints the founder's note.
- **Pause and resume any agent.** One issue labelled `agent-controls` (`control.py issue` creates it) takes the founder's `/pause <role> [reason]`, `/pause all`, `/resume <role>` and `/resume all`. `heartbeat.py start` stops a paused role before it takes a lock or a ticket, and stops it too when the controls can't be read. Pausing is never gated. Resuming a budget-stopped role still needs the budget approval. `control.py status` lists the pauses.
- **Plan approval before execution.** A new `plan` gate (on in new repos; add it to `founder/gates.json` to turn it on elsewhere). `tickets.py plan <parent> --by <role>` asks the founder to approve the parent's sub-tickets as one plan. Until then none can be claimed, and a sub-ticket added later needs the new plan approved.
- **Approval reminders and expiry.** An approval waiting 3 days is overdue on the dashboard, and its last week shows "expires in N days". `approval.py expire`, run by the weekly review, closes requests unanswered for 14 days as not approved, and their roles re-plan.
- **More actions from the page.** Approvals get a **Revise** button next to Approve and Reject. Each agent card and record gets **Pause** or **Resume**, which opens the agent-controls issue and copies the command. Paused agents show as "paused by you", with the reason. Reassigning a ticket from the page waits for a later slice: hand-offs stay with the roles (`tickets.py handoff`).
- **The doctor** also checks for the `agent-controls` label.
- **Docs:** the handbook, and the `gate`, `coordinate` and `weekly-review` skills.
- **Tests:** 6 new: revise and resubmit, resubmit and expire through the commands, pause and resume from the founder only, a paused role never starting, the plan gate including a changed plan, and pauses and reminders on the page.

## v1.12.0 (2026-11-23)

Slice 9 of `ROADMAP-V2.md`: one "Needs you" inbox, stuck work, charts and a fresher page.

- **Needs you, in one list.** Approvals waiting, budget stops (unless a budget request is already waiting), stuck work, decisions still Proposed or Open, and the founder items from `status.md`. Overdue at 7 days, escalated at 30. The order is escalated, then overdue, then what only the founder can unblock, oldest first. The Overview shows the top eight. A new **Needs you** tab has them all, with counts by kind, a filter, Approve and Reject, and a count on the tab. The Approvals inbox stays.
- **Stuck work.** A claimed ticket with no update for 48 hours (`stale_hours` in `founder/dashboard.json`) or a role whose last run failed. Each links to the agent's record.
- **Metric cards and 14-day charts** on the Overview: needs you and overdue, stuck, then agent runs per day (worked and the rest), success rate per day, agent actions and merged pull requests. They are inline SVG with each day's numbers in a tooltip and the label. The run history reads last month's cost log too, so the chart spans a month change.
- **Freshness.** The header says how long ago the page was built (red after two hours) and links **Rebuild now** to the workflow page.
- **Faster refresh.** The `dashboard` workflow also runs on issue events and new comments, after a one-minute wait, and a newer event cancels a build still waiting. An approval you just sent shows within a few minutes, not an hour.
- **The portfolio summary** gains the counts by kind, the overdue count and the stuck count.
- **Tests:** 2 new: the inbox's order, escalation, budget stops, stuck tickets and failed runs, the threshold setting and the 14-day trend. The second checks the page and the workflow triggers.

## v1.11.0 (2026-11-23)

Slice 8 of `ROADMAP-V2.md`: the run log and a page per agent.

- **Every run leaves a record.** `heartbeat.py end` takes `--outcome` (worked, no-work, blocked, approval, failed; it defaults to worked with a ticket and no-work without), `--session` (an https link to the session or its transcript; `S2S_SESSION_URL` works too) and `--model`. It also records how long the run took, from the run lock, and the ticket's objective. All of it goes into the cost entry the run already writes, so old entries still count.
- **`heartbeat.py runs [--role R]`** lists the month's run log with the success rate: worked, out of the runs that had work. `costs` adds the month-end spend at this month's daily burn.
- **A record per agent on the dashboard.** Open it from the Overview's team strip, from a card in Team and board, or at `#agent/<role>`. It shows runs and outcomes, success rate, median run time, spend against budget, spend per day against the budget's even pace (drawn in the page, with no library), cost per worked run, and every run with a link to its session. Its tickets, activity and stories are there too.
- **Costs, four ways.** The Costs tab has spend by objective, by model and by outcome. It also shows the month-end forecast against the budgets, runs and success rate per role, and the run log with outcome, time, objective, model and session. Spend by epic waits until tickets carry their epic.
- **Untrusted by default.** Malformed entries, unknown outcomes and negative times are dropped. A session link is kept only if it is https.
- **Docs:** handbook, and the `heartbeat` and `handoff` skills.
- **Tests:** 3 new: the run record and `runs`, the stats and forecast, and the dashboard's groups, forecast and agent page.

## v1.10.0 (2026-11-23)

Slice 7 of `ROADMAP-V2.md`: quick start and the doctor.

- **The doctor (`tools/doctor.py` and the `doctor` skill):** one list of what's broken, what's still to do, what it couldn't check and what's fine, each with its fix and handbook section. It checks `project.json`, the workflows, that each founder file sits behind its gate, the company goal and objectives, a budget for every role whose heartbeat is on, the hosting secrets, the labels, a run in the last 72 hours from each enabled role, and the last dashboard build. `--offline` checks the repo only; `--json` for tools; exit 1 while anything is broken.
- **`--repair`** fixes what's safe: an empty `goals.json`, gate paths for the founder files, missing labels. The skill does it on a branch and opens a PR for the founder to merge. Goals, budgets and secrets stay the founder's.
- **Secrets are checked, never read.** The `dashboard` workflow passes only whether each secret is set; locally the doctor reads the secret names from the GitHub API. The workflow gains `actions: read`.
- **The Setup card** at the top of the dashboard's Overview lists what's broken and left to do. A failing check shows as unknown and never breaks the build.
- **Session start** adds one line while setup is unfinished, pointing to the doctor skill.
- **Quick start in `init`:** the name and the company goal, then defaults for the rest, listed in the plan. The goal is written into `founder/goals.json`. Init then offers three starter tickets and opens them only on the founder's yes.
- **Docs:** the handbook's Day 0 setup covers the quick start and the doctor; README counts fifteen skills.
- **Tests:** 10 new: a fresh repo's findings, repair, roles without budgets, hosting secrets from the workflow and from the API, labels, runs and the dashboard build, GitHub down, the Setup card, a broken check, the session-start line and the goal written by init.

## v1.9.0 (2026-11-23)

Slice 6 of `ROADMAP-V2.md`: goals and key results, as data.

- **`founder/goals.json` (founder-owned, the `decision` gate):** one company goal, the quarter's objectives (`O1`, ...) with an owner, a quarter and a status, and 2 to 4 key results each (`O1.1`, ...): metric, unit, baseline, target, current value and a dated history.
- **`tools/goals.py`:** `check` (malformed file, duplicate or badly formed ids, missing targets, slices or epics naming an objective that doesn't exist; also run by `check_governance.py`), `show`, and `update O1.1 --value N`, which records the value and its date for a PR.
- **Work names its objective.** Epics and slices take `"objective": "O1"` in `slices.json`; tickets carry the label `goal:O1` from `tickets.py new --objective O1`, and sub-tickets inherit it. While an objective is active, a ticket that names none is refused.
- **The dashboard:** a **Goals** tab (each objective's progress, pace against its quarter, key results with start, now, target, progress and a trend line, owner, linked slices, epics and open tickets, and open tickets with no objective), and a goals panel on the Overview. Every text stays text; the trend line is drawn in the page, with no library.
- **The portfolio** shows each venture's goal and its active objectives' progress. The summary carries titles and numbers only, never the reasons or the history.
- **In existing repos:** `upgrade` adds an empty `founder/goals.json`; add it to the `decision` gate's `paths` in `founder/gates.json` yourself (that file is founder-owned).
- **Docs:** the handbook explains goals and key results, and the quarterly review sets them in `goals.json`.
- **Tests:** 15 new: progress up and down, roll-up to objectives, each malformed case, unknown objectives, updates with history, ticket labels and inheritance, and goal text staying text on the dashboard and in the summary.

## v1.8.0 (2026-11-23)

The dashboard follows the journey: this stage, and every document the team writes, grouped.

- **This stage** at the top of the Overview: phase and stage ("stage 2 of 30"), progress through the phase, what "done" means (the gate) and what's next; the blockers (blocked agents, founder items, approvals and decisions waiting); the agents working now with their tickets; and the latest documents.
- **Documents, grouped into Business, Product and Technical.** The tab (was "Business documents") opens with a tile per group: how many documents and the latest one. Each document is a card with its group, its feature (`specs/<feature>/`), its size and when it last changed, newest first; it opens in place.
- **Product and technical documents are picked up automatically:** `specs/*/spec.md` and `specs/*/ux/` (product), `docs/product/` (product), plans, research, data models, contracts, quickstarts and tasks under `specs/`, the rest of `docs/` and `.specify/memory/constitution.md` (technical). `founder/dashboard.json`'s `documents` still lists the business ones. At most 150 documents.
- **Docs:** the handbook describes both.
- **Tests:** 1 new: documents land in the right group with their feature, and the page has the stage panel and the grouped tab.

## v1.7.1 (2026-11-23)

- **Name the portfolio:** `name` in `founder/portfolio.json` (for example your holding company) is the portfolio page's title and heading; empty means "Portfolio". Change it any time; the next hourly build shows it. A venture's dashboard can show the same name on its link back, with `portfolio_name` in its `founder/dashboard.json`. Venture names still come from each venture's `founder/project.json`.
- In existing repos, add the two fields yourself (both files are founder-owned and behind the `deploy` gate).
- **Tests:** 1 new: the name is one line of at most 80 characters, defaults to "Portfolio", and stays text.

## v1.7.0 (2026-11-23)

The dashboard shows the AI team as agents.

- **Org chart** at the top of Team and board: you as CEO and chair, Claude as chief of staff, the six roles, and the advisory board (advice only, no vote) on the side, each with its status.
- **A card per AI agent:** avatar with a status dot, an "AI agent" badge, its plugin name (`solo-to-scale:<role>`), what it owns, the ticket it's working on (or blocked on), its heartbeat in words with the next run ("weekdays at 09:00 UTC, next in 18h"), what it last did, its stories done and its spend against budget.
- **Your AI team on the Overview:** every agent's avatar and status at a glance. Avatars also appear in Agent activity and the team table; advisors get an "AI advisor" badge.
- Built from data the page already had (heartbeats, tickets, the activity log, costs, team.json); still no server. The `board` budget in `founder/heartbeats.json` is not shown as an agent.
- **Tests:** 1 new: the page carries the org chart, the agent cards and the status words, and the board budget isn't an agent.

## v1.6.0 (2026-11-23)

The dashboard and the portfolio: sort, filter and act from the page, still with no server.

- **Sort any table:** click a column heading; click again to reverse. Money and ages sort as numbers, and empty values go last.
- **Filter the long tables:** a search box and filters where they help: stories (epic, slice, status), slices (status), epics, open tickets (role, state), decisions (status, register), approvals (gate), the cost log (role, measured or estimated); in the portfolio, approvals (venture, gate), decisions and founder items, merges and per-role costs. A filter only appears when it has two or more values.
- **Approve or Reject in one click:** next to each approval waiting, on the dashboard's Overview and Approvals inbox and the portfolio's Needs you. The button opens the request's comment box on GitHub and copies `/approve` or `/reject ` for you to paste; you still send it from your own account, so the gate is unchanged. Buttons appear only for `github.com` links.
- **Fix:** an approval with no date no longer reads "requested by …,  ago".
- **Docs:** the handbook describes sorting, filters and the approve buttons.
- **Tests:** 2 new: both pages carry the sortable, filterable table and the approve actions, limited to GitHub links, and never use HTML strings.

## v1.5.1 (2026-11-23)

- **Back to the portfolio from each dashboard:** set `portfolio_url` in a venture's `founder/dashboard.json` and its dashboard shows a "← Portfolio" link at the top. Only an `https://` address is used. New repos get the empty field; in existing repos, add it yourself (the file is founder-owned and behind the `deploy` gate). The portfolio already links each venture to its dashboard.
- **Tests:** 1 new: the link appears only for an `https://` address.

## v1.5.0 (2026-11-23)

Slice 5 of `ROADMAP.md`: the portfolio. The roadmap is complete.

- **One overview of several ventures,** each in its own repo, with four tabs: Overview (a card per venture: stage, slices, approvals waiting, decisions and founder items, tickets, spend against budget, and whether its data is current), Needs you (every approval waiting across the ventures, oldest first, linked to its repo), Activity (what each team did, and recent merges) and Costs (per venture and per role).
- **`founder/portfolio.json` (founder-owned, the `deploy` gate):** the other ventures and where the overview is served. No ventures means no portfolio. `upgrade` adds it to existing repos; add it to the `deploy` gate's paths yourself.
- **Summaries, never documents:** the `dashboard` workflow now also keeps a short summary (`build_dashboard.py build --summary`) as the `dashboard-data` artifact. `tools/build_portfolio.py build` reads the newest one from each venture with `PORTFOLIO_TOKEN` (read-only Actions access), never runs a venture's code, checks repo names before calling GitHub, caps the download size, lists a venture it can't read with the reason, and marks an old summary stale.
- **`portfolio` workflow:** every hour and on changes to `founder/portfolio.json`; deploys to Cloudflare Pages only behind a Cloudflare Access login, with the dashboard's `guard` and `verify`, now shared. On the page, every text is shown as text and links from a venture's summary may only point to GitHub.
- **The Claude page stays as the backup:** `publish-views` publishes the overview when a portfolio is set up.
- **Docs:** the handbook explains the portfolio and its 10-minute setup.
- **Tests:** 6 new: the summary carries no business documents; the overview reads the newest unexpired summary, drops duplicates and lists unreadable, not-upgraded and malformed ventures; bad, oversized and old summaries are flagged; `PORTFOLIO_TOKEN` is used when set; no ventures means no portfolio; hosting is behind a login.
- **Roadmap:** slices 4 and 5 are done.

## v1.4.0 (2026-11-23)

Slice 4 of `ROADMAP.md`: the startup dashboard.

- **One page, ten tabs:** Overview (what needs you, latest activity, recent merges), Business documents, Progress trace, Roadmap, Scope and journey, Team and board, Agent activity (what the roles did and said to each other), Decisions, Approvals inbox (only the founder's own `/approve` counts) and Costs (spend against budget per role, the 80% warning and the 100% stop).
- **`tools/build_dashboard.py build`:** builds the page from the repo, through the existing generators, and from GitHub: the activity log, open tickets, approval requests, the month's cost log and merged pull requests. If GitHub can't be reached, the repo tabs are still built and the page says what's missing. Every text is shown with `textContent` and the embedded data is escaped, so nothing an agent or an issue says can run in the browser. The page has a strict content security policy, `noindex` and a `robots.txt` that disallows everything.
- **`dashboard` workflow:** rebuilds the page on every merge to main and every hour, and deploys it to Cloudflare Pages at the host in `founder/dashboard.json`. Until hosting is set up it only builds.
- **Behind a login, fail closed:** `guard` allows a deploy only when a Cloudflare Access application with a login policy covers both the host and `<project>.pages.dev`. A path-only rule, a preview-only wildcard, an `everyone` policy, a `bypass` policy or an unreadable API all stop the deploy. After each deploy, `verify` fails the run if an anonymous visitor gets the dashboard.
- **`founder/dashboard.json` (founder-owned, the `deploy` gate):** the host, the Pages project and the documents to show. `upgrade` adds it to existing repos; add it to the `deploy` gate's paths yourself.
- **The Claude page stays as the backup:** `publish-views` publishes the same page, and `founder/artifacts.md` gets a row for it.
- **Docs:** the handbook explains the tabs and the 15-minute setup (Cloudflare domain, Pages project, Access application, two secrets).
- **Tests:** 14 new, against a fake GitHub and a fake Cloudflare API: hostile text stays text; only the founder's `/approve` counts in the inbox; costs and budgets match the cost log; a GitHub outage still builds; documents never leave the repo; eight ways of being unprotected each stop the deploy; an exposed page fails `verify`.
- **Roadmap:** slice 3 is done.

## v1.3.0 (2026-11-23)

Slice 3 of `ROADMAP.md`: heartbeats and budgets.

- **`founder/heartbeats.json` (founder-owned, the `budget` gate):** per role, whether its heartbeat is on, its schedule (cron, UTC) and its monthly AI budget in USD, plus the API prices used to cost a run. Heartbeats start off; a role without a budget never runs one. `init` writes the budgets from its answers; `upgrade` seeds them from `founder/team.md`'s budget table, which now points here as the only copy.
- **`tools/heartbeat.py`:**
  - `start <role>` refuses (exit 6) when the heartbeat is off, no budget is set, the budget is spent, or another run of the role is active (a `refs/heartbeats/<role>` lock, stale after 6 hours). Otherwise it resumes the role's own claimed ticket or claims one ready ticket with slice 2's atomic claim; with nothing ready it exits 2 and frees the lock.
  - `end <role>` records the run's AI usage cost in the month's `cost-log` issue: measured from the Claude Code session transcript, given with `--usd`, or the policy's flat estimate, marked as such. It frees the run lock and reminds the role about a ticket it still holds.
  - Budgets: a warning at 80% (cost log and ticket), a hard stop at 100%. At 100% `start` opens one `budget` approval request; the founder's own `/approve` adds one more month's budget for that month. Nothing else raises it.
  - `plan` prints each role's schedule, budget and spend, and the prompt for its cloud scheduled task; `costs` shows the month per role.
- **`heartbeat` skill** (the 14th): one unattended run, one ticket, within budget; finish with a pull request, a hand-off, a blocker or an approval request, then `end`. No questions to the founder inside a run.
- **Gates:** `founder/heartbeats.json` is a gated path of `budget` in new repos' `founder/gates.json` (existing repos: add it yourself).
- **Review and handoff:** the weekly review reports cost per role from the cost log; the handoff records an interactive session's cost too.
- **Tests:** 9 new, against a fake GitHub: off, unbudgeted and spent roles never claim; a second concurrent run stops; resume beats a new claim; costs are summed across pages and months; 80% and 100% fire once; only the founder's `/approve` adds budget; transcripts are costed once per message; `upgrade` reads budgets from the team table.
- **Roadmap:** slices 1 and 2 are done.

## v1.2.0 (2026-11-23)

Slice 2 of `ROADMAP.md`: agent coordination.

- **`tools/tickets.py`:** roles delegate through GitHub issues labelled `ticket` and `role:<role>`.
  - `new` opens a sub-ticket with its parent (also linked as a GitHub sub-issue) and its blockers; `queue` lists a role's ready tickets; `tree` shows a parent and its sub-tickets.
  - `claim` is atomic: it creates a `refs/claims/<n>` ref, and creating a ref that exists fails, so only one claimant wins. It refuses another role's ticket, a closed one or a blocked one, and anything unclear claims nothing.
  - `handoff` moves a ticket to another role and frees the claim; `block` and `unblock` edit the ticket's "Blocked by" line; `release` lets go.
  - `done` closes a ticket, frees the claim, unblocks every ticket that waited only on it, and tells the parent when its last sub-ticket closes.
  - Only the claim holder, or the ticket's role when nobody holds it, can release, hand off or finish it.
- **Activity log:** every action is a comment on the ticket and an entry in one issue labelled `activity-log`; `log` reads it, by role or ticket. Agents' text is quoted, so it never reads as a founder's `/approve`.
- **`coordinate` skill** (the 13th): how roles claim, delegate, hand off, block and finish. Hand-offs name `role:<name>`, never `@<name>`, which would notify a real GitHub user.
- **`tickets` workflow:** when an issue closes any other way (a merged pull request, the founder), it frees the claim and unblocks what waited on it.
- **`claim`:** story-group claims take the same atomic lock.
- **Review and handoff:** the weekly review summarises team activity; the handoff closes out the claimed ticket.
- **Tests:** 10 new, against a fake GitHub: a second claimant always loses, even before the label is added; GitHub errors claim nothing; hand-offs, blockers, `done` and the workflow path wake the right tickets.

## v1.1.0 (2026-11-23)

Slice 1 of `ROADMAP.md`: founder approval gates.

- **`founder/gates.json` (founder-owned):** the critical actions only the founder approves: hire, budget, deploy, external, spend, decision, pricing, legal (`ask`), and secrets (`off`, founder only). Each gate can list file `paths`.
- **`tools/approval.py`:** `request` opens an approval issue (`needs-founder`, `gate:<name>`); `check` answers approved, waiting or no; plus `status`, `inbox` and `pr`. Only the founder's own `/approve`, `/approve always`, `/reject` or `/revoke` comment counts, and the latest wins. Everything unclear fails closed.
- **`gate` skill:** agents check before any gated action, request approval, stop that action and carry on with other work.
- **`founder-gates` workflow:** a pull request that changes a gated file passes only after a founder adds the `founder-approved` label.
- **Review and handoff:** the weekly review lists approvals waiting; handoffs list the requests a session opened.
- **Docs:** `ROADMAP.md` with the five slices toward an always-on AI team; the handbook explains the gates.
- **Tests:** 9 new, against a fake GitHub: non-founder comments, bots and labels never approve; one gate never covers another; standing rules respect scope and `/revoke`; GitHub errors and a missing policy fail closed.

## v1.0.2 (2026-11-23)

- Fix: the governance check no longer fails on register tables that have no status column, such as an approvals log of D- rows. Their IDs are still read, so citing them stays valid. A row in a table that has a status column still fails when its status is empty. Before, `upgrade` to 1.0.1 replaced a repo's own check and then reported every log row as "has no status".
- Tests: an empty status still fails, and a log table without a status column passes.

## v1.0.1 (2026-11-20)

- Fix: `init` and `upgrade` now enable the plugin in an existing `.claude/settings.json`. Before, `upgrade` left that file alone as founder-owned, and `init` only proposed the change. A repo whose own copies of `handoff`, `record-decision` and `weekly-review` were replaced then had none of those skills in cloud sessions or scheduled tasks. Only the plugin's marketplace and enabled flag are added; every other key is kept, and the rest stays a proposal.
- Tests: the legacy fixture now has a settings file with hooks and no plugin, the case that exposed the bug.

## v1.0.0 (2026-11-20)

- **Skills (11):** `init`, `upgrade`, `handoff`, `board-review`, `record-decision`, `weekly-review`, `release-check`, `publish-views`, `claim`, `product-design`, `design-system`. Each is under 80 lines and starts with the read-narrowly rule; details sit in `references/`.
- **Roles:** 7 team roles, 4 board advisors (growth, owner, customer and risk lenses) and an optional sales advisor, each with one source in `roles/*.yaml`. `scripts/sync_agents.py` generates the Claude Code and Codex agents from them; model tiers come from `models.yaml`.
- **Hooks**, shared by both tools:
  - context guard: Claude Code limits on percentage and tokens; Codex hands off at compaction
  - session start
  - stop check with loop guards
  - Claude status line
  - Codex `PreCompact` and `PostCompact`
- **Templates:**
  - Founder HQ
  - `AGENTS.md` and `CLAUDE.md`
  - the engineering standards
  - the Claude Project pack
  - generalised repo tools (governance check, roadmap, team and traceability data, claim, test-area), with tests
  - the governance workflow and an optional cross-review job
  - the story-group issue template
- **`init` and `upgrade` engines:**
  - never overwrite a file; existing files get merge proposals instead
  - plugin-owned, sectioned and founder-owned files are kept apart
  - legacy-repo mapping, and rename reports
- **Team view:** the four board seats beside the founder; one leftover domain term removed.
- **Handbook:** both diagrams redrawn as Mermaid; the "anything else hard to reverse" routing row added. CI fails if the handbook disagrees with `models.yaml` or `governance.json`.
- **One copy of the protocol:** it moved to `templates/founder/operating-protocol.md`, and the bootstrap prompt now points to it.
- **CI:**
  - tests on Linux, macOS and Windows
  - manifest check against both tools' documented fields
  - generated-file drift
  - skill and role sizes
  - project-name denylist

## v0.1.0 (2026-11-20)

- Repository skeleton: Claude Code and Codex marketplaces, both plugin manifests, install guide, `BUILD.md` and `sources/`.
- No project names: `init` asks for the name and stores it in `founder/project.json`; CI checks the repo against the `PROJECT_NAME_DENYLIST` secret.
- `templates/views/team-view.html`: the team-view page, with the project name as a placeholder.
- `docs/handbook.md`: the operating-system handbook, the single source for its Claude Docs view.
