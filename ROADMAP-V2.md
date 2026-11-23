# Roadmap v2: gaps against Paperclip, and what to build next

**What this is.** A gap analysis of Solo to Scale (v1.7.x, plus the "This stage" panel and document grouping in v1.8.0) against [Paperclip](https://github.com/paperclipai/paperclip), the MIT-licensed control plane for AI-agent companies that inspired our team model. It was written from Paperclip's code, docs and UI source on 2026-11-23: `README.md`, `ROADMAP.md`, `doc/` (product, goals, watchdog, artifacts, search, trust presets), `docs/guides/board-operator/` (dashboard, approvals, budgets, delegation, org structure, activity log, status cards), `docs/guides/execution-policy.md`, `docs/api/` (goals and projects, attention inbox, routines), the install and onboarding docs (`doc/INSTALLING.md`, `docs/start/`, `docs/cli/setup-commands.md`, `docs/deploy/deployment-modes.md`, `doc/onboarding-chat.md`, company import and export) and `ui/src/pages/` (Dashboard, AgentDetail, Goals, Costs, Timeline, Inbox, Search, Artifacts, Routines).

**What it is not.** A plan to copy Paperclip. We take ideas, never its branding, names, artwork or look. Every item below is re-expressed in our own model: the repo is the memory, GitHub is the control plane, and only the founder's own words approve.

**How to read the tables**
- **Priority:** P1 = build in v2.0, high value for a solo founder at low cost. P2 = v2.x, once P1 is in use. P3 = only when a real need shows up.
- **Size:** S = a small change inside one existing tool or page (about one session). M = one slice, one pull request with tests. L = several pull requests.
- **Fit:** *Fits* = works inside our no-server design. *Partial* = we can get most of the value without a server. *Trade-off* = we deliberately don't build it; the reason is given.

---

## The short version: the eleven things to build first

1. **Goals and key results as data** (D1–D3). Paperclip's core promise is that every task traces to a company goal and the founder sees progress against it. We have the goal chain as text; we need goals with targets, owners and progress the dashboard can count.
2. **A run log and a page per agent** (C1–C2). Paperclip shows every agent's runs, outcomes, cost and history. We record cost, not outcomes, so we can't say which agent is working well.
3. **One "Needs you" inbox with ageing** (A3). Approvals, blockers, revision requests, budget stops and stale decisions in one list, oldest and most blocking first.
4. **Stuck-work alerts** (A2, B7). Tickets in progress with no update, agents whose last run failed, and trees of work that stopped with nobody moving them.
5. **Money beyond AI spend** (E1–E2). Revenue, other costs, burn and runway, and a company-wide AI budget cap. Paperclip tracks finance events; a solo founder needs runway on the first screen.
6. **Request changes, not just approve or reject** (B1), and **pause or resume an agent from your phone** (B4).
7. **Review before approval** (B2). Work goes to a reviewer role that isn't its author before it reaches you, and every review leaves a recorded verdict.
8. **Plan approval before execution** (B3). An initiative's plan of sub-tickets waits for your approval before any agent claims it.
9. **Routines for recurring business work** (E4). Named jobs such as the investor update, support digest or content calendar, each run creating a ticket with an owner and a history.
10. **Charts and freshness** (A1, T1). Trends on the Overview, and a rebuild within a minute of an approval or a ticket change instead of up to an hour.
11. **A quicker start and a doctor** (H1–H3). Paperclip starts with one command and sensible defaults, checks its own health with `doctor --repair`, and ends onboarding with a goal and first tasks. Our `init` asks every question up front, hosting and the portfolio are set up by hand, and nothing checks in one place what's missing.

Suggested order and grouping are under **v2 slices** at the end.

---

## What we already match (not gaps)

So the lists below stay honest, these Paperclip capabilities already exist in v1, in our own form:

| Paperclip | Solo to Scale v1 |
|---|---|
| Ticket-based work, single assignee, atomic checkout | GitHub issues, `refs/claims/<n>` atomic claim (`claim`) |
| Delegation through parent and sub-tasks, blockers | `coordinate`: parent tickets, sub-tickets per role, "Blocked by", auto-unblock |
| Heartbeats with schedules and run locks | `heartbeat`, `founder/heartbeats.json`, one run lock per role |
| Per-agent monthly budgets, 80% warning, 100% stop | `cost-log` issue, enforced in every run and handoff |
| Approval gates, Allowed / Ask first / Off | `founder/gates.json` with `allow` / `ask` / `off`, `/approve` from the founder only, CI blocks gated PRs |
| Hire approval | The `hire` gate |
| Activity log and attribution | The `activity-log` issue, `tools/tickets.py log` |
| Org chart and agent cards with status | Team and board tab (v1.7.0) |
| Config revisions and rollback | Git history and revert through a PR |
| Multi-company in one place | The portfolio (v1.5.0) |
| Goal context for agents | The goal chain at the top of every issue and session |
| Mobile management | The GitHub app for approvals, and the dashboard behind Cloudflare Access |

---

## A. The interactive dashboard

| # | Gap | What Paperclip has | Why it matters for a solo founder | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| A1 | **Charts and metric cards** | Dashboard metric cards (agents enabled, tasks in progress, month spend, pending approvals) and 14-day charts: run activity, tasks by status, tasks by priority, run success rate | Tables say *what*; trends say *whether it's getting better*. Two seconds to know if the company moved this week | S | P1 | Fits | Add a metric-card row and four small inline SVG charts to Overview, built by `build_dashboard.py` from data it already reads. No chart library, no CSP change |
| A2 | **Stale and stuck work** | "Stale tasks": in progress too long without an update; agents in an error state; budget-paused agents and projects | A stuck agent wastes budget silently. You should see it before Monday's review | S | P1 | Fits | Flag tickets claimed or in progress with no comment for longer than a threshold (`founder/dashboard.json`, default 48h), and agents whose last run failed. Show them first on Overview and in the inbox |
| A3 | **One "Needs you" inbox, with ageing and escalation** | Attention inbox: one feed of everything waiting on a person, sorted by "decide", counts by kind; unowned items move up after 7 days, required items escalate after 30 | Today approvals, founder items, blockers and budget requests sit in different tabs. One list, oldest and most blocking first, is the founder's whole job on a busy day | S | P1 | Fits | Merge the Approvals inbox, founder items from `status.md`, blocked tickets waiting on the founder, revision requests (B1), budget stops and decisions Proposed for over 14 days into one sorted list with age badges. Keep the Approvals tab as a filter of it |
| A4 | **More actions from the page** | Pause, resume, reassign, request revision, override budget, all in the UI | You manage from a phone between meetings | S | P1 | Fits | Same pattern as v1.6.0's approve buttons: each button opens the right GitHub comment box with the command copied (`/revise`, `/pause <role>`, `/resume <role>`, `/reassign role:<name>`). The founder still sends it, so the gate is unchanged |
| A5 | **Company-wide search** | Search across tasks, comments, documents, agents, projects and artifacts, with matching excerpts and exact-ID hits first | "Where did we decide the pricing?" is a daily question once there are 200 tickets | M | P2 | Fits | A client-side index built into the page (titles, decision IDs, ticket numbers, document headings, activity notes), with excerpts and links. No server; size-capped |
| A6 | **Timeline view** | A zoomable timeline of work over dates | See whether slices land when planned, and what overlaps | M | P2 | Fits | A Gantt-style row per slice and epic from first claim to merge, with planned dates if set in `founder/slices.json` |
| A7 | **Work products gallery** | Artifacts page: every file and document agents produced, previewed, with comments on passages | Find "the landing page draft" without hunting through PRs | M | P2 | Partial | A Work products tab listing PRs, documents and published Claude pages per ticket and per role, linked to GitHub. Comments stay on GitHub PR reviews |
| A8 | **Freshness on screen** | Live updates in the browser | You need to trust that what you see is current | S | P1 | Fits | Show "built N minutes ago" and a "Rebuild now" link that opens the workflow's run page. Pairs with T1 |
| A9 | **AI summary cards** | Status cards: a sentence like "blocked launch work this week, tell me the next decision" becomes a watched query and a short AI summary, refreshed only when the data changes, with a daily token cap | A paragraph that tells you what matters beats ten tables | M | P3 | Partial | Let the chief of staff write a 5-line "Brief" into the dashboard data on each weekly review and on change, within its budget. Skip the query compiler |
| A10 | **Rate agent output** | Helpful / Needs work votes on any agent comment or document, with a reason, kept as feedback | The cheapest training signal there is, and input to scorecards (C3) | S | P2 | Fits | Count 👍 and 👎 reactions from the founder's account on agent comments and PRs; show them per role. No new UI |

## B. Governance and rules

| # | Gap | What Paperclip has | Why it matters | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| B1 | **Request revision** | Approval states pending → approved / rejected / revision requested → resubmitted | "Not like this, try again" is the most common answer. Reject makes the agent start over or give up | S | P1 | Fits | Add `/revise <what to change>` to `approval.py`: the request reopens for the same role with your note, and its resubmission links back. Only the founder's account counts, as today |
| B2 | **Review stage before approval** | Execution policy per task: an ordered review stage then approval stage; the reviewer is never the executor; every run must leave a comment; every decision is recorded with a comment | You shouldn't be the first reviewer of everything. A QA or architect pass catches most issues before you spend attention | M | P1 | Fits | A `review` field on tickets (label `needs-review:role:<name>`). `coordinate done` refuses to finish until a different role posts `review: approved` or `review: changes`. CI's gate check reads it for gated PRs. Record each verdict in the activity log |
| B3 | **Plan approval before execution** | The CEO's strategy needs board approval before tasks start; deep planning with revisioned plans and plan approvals | The most expensive mistake is a team executing the wrong plan well | S | P1 | Fits | A new gate, `plan`: a parent ticket's sub-ticket plan is posted as one comment, and its sub-tickets can't be claimed (`claim.py` checks) until you `/approve` it. A changed plan is a new revision that needs approval again |
| B4 | **Pause, resume and stop an agent** | Agent states active, idle, running, error, paused, terminated; pause any agent at any time | When an agent goes off track at 2am you want one tap, not a gated PR to `heartbeats.json` | S | P1 | Fits | `/pause <role>` and `/resume <role>` on a pinned control issue, from the founder only. `heartbeat.py` checks it first and stops. Pausing is never gated; resuming a budget-stopped role still needs the budget approval |
| B5 | **Approval reminders and expiry** | Requests that wait escalate after set times; idle approvals expire | Stale approvals block work invisibly | S | P2 | Fits | The hourly build marks approvals older than 3 days as overdue (on the page and in one digest comment); after 14 days the agent withdraws the request and re-plans |
| B6 | **Chain of command** | Every agent reports to one manager; blockers escalate up the chain; managers see their reports' work | With seven roles flat under you, every blocker lands on you | S | P2 | Fits | `reports_to` in `roles/*.yaml` (default: chief of staff). A blocked role escalates to its manager first; only the chief of staff escalates to the founder. The org chart already draws the lines |
| B7 | **Watchdog for stopped work** | Task watchdog: when a whole tree of tasks comes to rest with no live path, a verifier agent checks the evidence and restarts it if stopping was a mistake; liveness recovery for stalled in-progress work | Agents declare "done" without proof or misread a blocker, and nothing wakes anyone | M | P2 | Fits | The chief of staff's heartbeat scans parent tickets whose sub-tickets are all closed, blocked or waiting, with no claim alive; it checks the evidence (merged PR, passing CI, linked decision) and reopens or comments. Opt in per parent ticket with a `watch` label |
| B8 | **Bounded retries** | Recovery policies retry transient failures within limits, still subject to budgets and gates | A flaky network shouldn't cost a day | S | P2 | Fits | A failed run records `failed` (C2); the next heartbeat retries the same ticket once, then blocks it with the error |
| B9 | **Untrusted-input containment** | A low-trust preset for work that reads hostile input (outside PRs, external tickets), intersected with project and task policy, failing closed; a prompt-injection classifier on tool results | Once customers can open issues, an issue body is an attack surface for agents with write access | M | P1 | Fits | Mark any issue, comment or PR not authored by the founder or an agent as untrusted. A role working from untrusted text may read and comment only: no gated actions, no secrets, no merges, until the founder approves the ticket. Add tests with hostile fixtures |
| B10 | **Per-role permissions** | Separate controls for which agents can use which connection and action | Growth shouldn't be able to deploy; Engineers shouldn't send emails | S | P2 | Fits | Allow an optional `roles` list per gate in `gates.json` (for example `deploy: ask, roles: [qa]`); other roles can't even request it |
| B11 | **Scoped secrets** | Secrets manager with per-agent access and audited resolution | Least privilege limits the damage of one bad run | M | P3 | Partial | Use GitHub environment secrets per role workflow and fine-grained tokens per role. Document it; no secrets manager |

## C. Views and reports for each agent role

| # | Gap | What Paperclip has | Why it matters | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| C1 | **A page per agent** | Agent detail: overview counts, runs, run time, tokens, budget panel, costs panel, skills, instructions, direct reports, history and audit tab | The cards show *now*. To manage an agent you need its record: what it did this month, at what cost, how often it failed | M | P1 | Fits | Clicking an agent card opens its view (same page, no server): charter and skills from `roles/`, heartbeat, current and recent tickets, runs (C2) with outcome and cost, spend by day against budget, reviews given and received, founder reactions (A10) |
| C2 | **Run log with outcomes** | Every heartbeat run has a record: status, duration, cost, linked task, transcript | Without outcomes we can't compute success rate, find a failing agent or retry (B8) | S | P1 | Fits | Extend the `cost-log` entry each run already writes with `outcome` (worked, no work, blocked, asked approval, failed), ticket, duration and a link to the session. Prerequisite for C1, C3, A1, B8 |
| C3 | **Agent scorecards and monthly performance review** | Performance reviews and quality metrics for agents; evals and saved test runs | A solo founder can't watch every agent. A monthly scorecard says which to trust more, which to re-brief, which to pause | M | P1 | Fits | A monthly scorecard per role in the weekly-review's monthly run: tickets finished, median cycle time, reviews passed first time, reopen rate, cost per finished ticket, budget used, founder 👍/👎. Plus role-specific measures: **Engineers** PRs merged, CI pass rate, change failure rate; **QA** escaped defects, eval pass rate; **Product** stories made ready, specs approved first time; **Architect** decisions recorded, threat model age; **Research** interviews and evidence items logged; **Growth** pieces shipped, sign-ups or traffic once connected; **Chief of staff** handoffs on time, stale items closed |
| C4 | **Role reports in the weekly review** | Agents report status up the chain each heartbeat | You read one report, not seven threads | S | P2 | Fits | Each active role adds three lines to the weekly review (done, next, blocked) from its own activity; the chief of staff merges them |
| C5 | **Costs by goal, project and model, with a forecast** | Costs by agent, by project, by date range; burn rate; finance events | "What did the launch cost?" and "will we run out this month?" | S | P1 | Fits | Group the cost log by goal (D2), epic, role and model tier; add a date range and a month-end projection from the daily burn |
| C6 | **Tests for role prompts** | Skill Studio: saved test inputs, test runs, results, version history and restore | Editing a role's charter can quietly make it worse | M | P3 | Partial | A few saved test briefs per role in `tests/roles/`, run by hand before a role change; compare outputs in the PR. No studio UI |

## D. Startup objectives and goals

| # | Gap | What Paperclip has | Why it matters | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| D1 | **Goals as data** | A goal hierarchy (company → team → agent), with status planned, active, achieved or cancelled; the company is defined by its goal | Objectives in `status.md` are prose the dashboard can't count. Measurable goals produce better delegation, as Paperclip's own guide says | M | P1 | Fits | `founder/goals.json` (founder-owned, behind the `decision` gate): one company goal, quarterly objectives, and 2–4 key results each with metric, baseline, target, current value, owner role and status. `status.md` keeps the narrative and links to it |
| D2 | **Link work and spend to goals** | Tasks and projects carry goal ancestry; routines link to goals; costs by project | See *why* work happens, and stop work that serves no goal | S | P1 | Fits | Each parent ticket and slice names a goal ID; sub-tickets inherit it. `coordinate` refuses a parent ticket with no goal. Costs roll up by goal (C5) |
| D3 | **Goals view** | Goals page and goal detail: linked projects, tasks, progress | One screen answers "are we on track this quarter?" | S | P1 | Fits | A Goals tab and a goal strip on Overview: progress per key result, linked tickets open and done, spend, owner agents. On the portfolio, one line per venture |
| D4 | **Key result updates** | Agents receive goal context and report against it | Numbers go stale unless someone owns them | S | P2 | Fits | The owner role proposes a new current value with its evidence in the weekly review PR; merging the PR is the approval |
| D5 | **Goal context fed from data** | Goal-aware execution: agents see the "why", not just a title | Already partly done as text; data makes it exact | S | P2 | Fits | `heartbeat.py plan` and `coordinate` render the goal chain from `goals.json` instead of free text |

## E. Business capabilities

| # | Gap | What Paperclip has | Why it matters | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| E1 | **Revenue, costs, burn and runway** | Revenue and expenses at company level; finance events with credits, debits and net | Runway is the number that decides everything for a solo founder; we only track AI spend | M | P1 | Fits | `founder/finance.json` (founder-owned, the `spending` gate): cash, monthly revenue, fixed costs (tools, hosting, ads) and one-off items. Overview shows MRR, net burn, runway in months, and AI spend as a share of costs. Optional later: a read-only billing export through an Action |
| E2 | **Company-wide AI budget** | A monthly company budget on top of per-agent budgets | Seven role budgets can add up to more than you meant to spend | S | P1 | Fits | A `company` cap in `heartbeats.json`; every run checks both caps; the 80% warning and 100% stop apply to the total too |
| E3 | **Business metrics with history** | Company metrics on the dashboard | Stage 23's "5 stage metrics tracked weekly" has nowhere to live | S | P1 | Fits | Key results (D1) keep a dated history; the dashboard draws a sparkline per metric |
| E4 | **Routines for recurring work** | Scheduled routines with an owner, project and goal; each run creates a task with history; concurrency (coalesce, skip, always) and catch-up policies; webhook or API triggers | Investor updates, support digests, competitor scans and content calendars get forgotten without a schedule | M | P1 | Fits | `founder/routines.json`: name, owner role, schedule, goal, brief, and `if_running: skip / coalesce`. The role's heartbeat opens a ticket for each due routine and works it like any other. Starter routines: monthly investor update, weekly competitor scan, weekly support digest |
| E5 | **Intake queues** | Planned work queues for support, triage and backlog intake | Customer feedback and bug reports need a front door that routes to the right role | S | P3 | Fits | GitHub issue forms (feedback, bug, idea) labelled `intake`, triaged by the product role's heartbeat into tickets. Untrusted by default (B9) |
| E6 | **Templates for the next venture** | Export and import whole companies, agents and skills, with secrets scrubbed; a catalog of ready-made teams | Your second venture should start from what worked in the first | M | P2 | Fits | `upgrade export-template` writes the team setup (roles enabled, budgets, gates, routines, goals shape) without business content; `init --from <template>` reuses it. Fits the portfolio |
| E7 | **Notifications outside GitHub** | Chat and email connectors (Slack, Discord, Telegram, email) | Some founders live in email, not GitHub notifications | S | P3 | Partial | A daily digest email or Slack message from the dashboard workflow with the "Needs you" count and links. Approvals still happen on GitHub |

## F. Product capabilities

| # | Gap | What Paperclip has | Why it matters | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| F1 | **Setup checklist** | Guided onboarding and first-task flows | Hosting, heartbeats, budgets, portfolio token and Access are easy to half-finish | S | P1 | Fits | A "Setup" card on Overview listing each piece, its state (done, missing, failing) and the handbook link, until all are done |
| F2 | **Talk to one role** | Agent chat with any agent, including the CEO, whose plans hand off to linked tasks | Sometimes you want to ask Growth a question, not open a ticket | S | P2 | Partial | An "Ask the team" issue form with a `role:` field; the role's next heartbeat answers in the thread and, if work is needed, opens linked tickets. Real-time chat stays in Claude Code and claude.ai Projects |
| F3 | **Document history on the page** | Document revision history and restore; comments on passages | "What changed in the business plan?" | S | P2 | Fits | On Business documents, show last changed, by whom and the PR, with a link to the file's history on GitHub. Comments stay in PR reviews |
| F4 | **Lessons learned** | Planned automatic organisational learning: playbooks, recurring fixes and decision patterns from finished work | The same mistake twice is the most expensive kind | S | P2 | Fits | On `done`, a role adds one line to `founder/lessons.md` when something surprised it; the weekly review proposes promoting repeats into the playbook or a role charter |
| F5 | **A second human** | Multiple human users with shared board access | A co-founder, a contractor or a real lawyer may join | S | P3 | Partial | Cloudflare Access already allows more viewers. Allow an optional `delegates` list per gate (for example a lawyer for `legal`); the founder stays the only approver of everything else |

## G. Technical capabilities

| # | Gap | What Paperclip has | Why it matters | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| T1 | **Faster refresh** | Live updates over a persistent connection | An approval you just sent should show as done, not for up to an hour | S | P1 | Fits | Also rebuild the dashboard on `issues` and `issue_comment` events, with a concurrency group that cancels older builds, and a 60-second debounce. Still static, still behind the login |
| T2 | **Run transcripts and traces** | Run history with logs; optional OpenTelemetry export of agent runs | Debugging a bad run needs what it saw and did | S | P2 | Partial | Link each run (C2) to its cloud session or saved transcript. OpenTelemetry export is a trade-off (see below) |
| T3 | **Machine-readable status for agents** | A dashboard API agents and tools can call | Agents should read the same picture you see | S | P3 | Fits | Each heartbeat reads the newest `dashboard-data` summary for its own role instead of re-querying GitHub |
| T4 | **More agent runtimes** | Adapters for many harnesses (Cursor, Gemini CLI, OpenCode and others), plus HTTP and process agents | Choice of model and tool per role | L | P3 | Trade-off | Stay with Claude Code and Codex from one source. Add a third only when one is needed; `roles/` already makes it a generator change |

## H. Install, setup and upgrade

**Paperclip's path:** a checksummed installer script (or `npx paperclipai onboard --yes`) → **Quickstart** with local defaults, or **Advanced setup** → `run`, which onboards if needed, runs `doctor` with repair, then starts → the first screen asks for a company, a goal and a first agent, then opens a chat that gathers the goal and exit criteria and proposes first tasks. Updates follow a recorded channel (`update`, `--latest`, `--canary`, `--version`), take a database backup first, and can be rolled back. Imports start agents and routines paused and list what an export didn't carry.

**Ours:** install the plugin from the GitHub marketplace, run `init` (questions, then one PR), set up hosting and the portfolio by following the handbook, update with `upgrade` (one PR of differences), roll back by reverting PRs. That's already safer than most, because nothing changes until you merge, but it's slower to start and harder to check.

| # | Gap | What Paperclip has | Why it matters | Size | Pri | Fit | Recommendation |
|---|---|---|---|---|---|---|---|
| H1 | **Quick start with defaults** | `onboard --yes`: Quickstart defaults, nothing else asked, change later with `configure` | The first 10 minutes decide whether a founder keeps going | S | P1 | Fits | `init --quick`: ask only the project name and a one-line goal; take defaults for the rest (gates on `ask`, heartbeats off, starting budgets from the handbook) and list them in the PR so they can be changed before merging. Add `upgrade --configure` to change answers later |
| H2 | **Doctor, with repair** | `doctor` checks configuration, database, secrets, storage and missing files; `--repair` fixes them; `run` calls it on every start | Today nothing tells you that a secret is missing, a scheduled task was never created or the Access policy drifted, until something silently doesn't happen | M | P1 | Fits | A `doctor` skill and `tools/doctor.py`. It checks: the repo's version against the plugin, plugin-owned files, labels, CI workflows, the Cloudflare secrets and Access guard, `PORTFOLIO_TOKEN`, a scheduled task for each enabled heartbeat, budgets set, and gates covering the founder-owned files. `--repair` opens one PR for what it can fix and lists the rest with handbook links. The session-start hook runs the fast checks; the dashboard's Setup card (F1) shows the result |
| H3 | **Goal-first onboarding** | Onboarding ends in a conversation with the first agent that gathers the goal and clear exit criteria and proposes first tasks for you to accept | An empty repo with a team and nothing to do is where most setups stall | S | P1 | Fits | `init` ends by writing the company goal and first quarterly objective into `goals.json` (D1), and proposes three starter tickets (for example: write the business context, validate the idea, plan the first interviews) as a plan for your approval (B3) |
| H4 | **Pin, preview and roll back versions** | Update channels (stable, canary, a pinned version), a backup before each update, one-command rollback | A bad plugin release shouldn't reach every venture at once | S | P2 | Fits | `upgrade --to vX.Y.Z` to pin a version; a `next` marketplace ref for trying a release on one venture first; `upgrade --rollback` opens the revert PR for the last upgrade. Git is the backup |
| H5 | **Pinned install source** | A checksummed installer, pinned bootstrap scripts, and advice to pin to a tag or commit | The plugin's hooks run on your machine; a moving branch is a supply-chain risk | S | P2 | Fits | `init` writes the marketplace entry pinned to the release tag, and `upgrade` moves the pin. Document how to check a release tag |
| H6 | **Guided hosting setup** | Onboarding sets the deployment mode, URL and login; `doctor` is stricter for public deployments | The 15-minute Cloudflare setup is the step most likely to be skipped | M | P2 | Fits | `tools/build_dashboard.py setup` walks the Cloudflare steps through the API with your token: checks the zone, the Pages project and the Access application, and prints the exact next step. It never publishes an open page; `guard` still fails closed |
| H7 | **Safe import of a template** | Imported agents and routines start paused; an export lists what it didn't include | Starting the next venture from a template shouldn't start spending on day one | S | P2 | Fits | With E6: `init --from <template>` lands every heartbeat and routine off, and the template's README lists what it leaves out (documents, decisions, costs, history) |
| H8 | **Local and private modes** | `local_trusted` on localhost, or login-required on a private network or the internet | A choice of where the board lives | — | — | Trade-off | Not needed: the repo is the system and the dashboard is a static page. Our two modes are the Claude page (private, no hosting) and Cloudflare Access (login); `build_dashboard.py build` also works locally |

---

## Deliberate trade-offs: what we won't build, and why

Our design choice is **no server**: GitHub is the database, the queue, the login and the audit trail, and the dashboard is a static page. That gives us zero hosting to run, GitHub's mobile app and notifications for free, a full audit trail, and an approval that can't be faked by an agent. These Paperclip features need a server or a database, so we skip them on purpose:

| Paperclip feature | Why we skip it | What we do instead |
|---|---|---|
| A Node server, a database and a real-time web app | One more system to host, secure, back up and pay for, for one person | Static page rebuilt on change (T1), GitHub as the store |
| Multi-tenant hosting, SSO, role-based access for many humans | A solo founder is one approver; more humans means a different product | Cloudflare Access for viewing; founder-only approvals; optional delegates per gate (F5) |
| Plugin system and UI slots | Our plugin *is* the extension point; Claude Code and Codex plugins already compose | Companion plugins, enabled per repo |
| Sandbox provider integrations | Cloud scheduled tasks already run each role in an isolated container | Document the setup |
| A full skill studio with test runs in the UI | High build cost for a handful of role prompts | Saved test briefs in the repo (C6) |
| In-app agent chat | Claude Code, Codex and claude.ai Projects already are the chat | "Ask the team" issue form (F2) |
| Secrets manager and governed tool gateway | GitHub secrets and gates cover a solo company's needs | Per-role gates (B10), scoped tokens (B11) |
| OpenTelemetry tracing | Useful at scale, noise for a solo founder | Transcript links per run (T2) |

**When to switch.** The handbook's rule still stands: once more than about five agents run on schedules at once (phase F or G), run Paperclip itself for orchestration, and keep this repo as the memory and governance. Everything v2 adds (goals, routines, run log, scorecards) is plain data in the repo, so it carries over.

---

## v2 slices

Each slice is one pull request with a version bump, tests and handbook text, picked up by startups through `upgrade`, as in v1. The design rules in `ROADMAP.md` still apply to every slice.

| # | Slice | Items | Size | Why this order |
|---|---|---|---|---|
| 6 | **Goals and key results** (done in v1.9.0) | D1, D2, D3, E3 | M | Everything else reports against goals |
| 7 | **Quick start and doctor** (done in v1.10.0) | H1, H2, H3, F1 | M | A new venture is running in minutes, and every later slice's setup is checked in one place |
| 8 | **Run log and agent pages** (done in v1.11.0) | C2, C1, C5, T2 | M | Outcomes are the data scorecards, charts and retries need |
| 9 | **Needs you, stuck work and charts** (done in v1.12.0) | A3, A2, A1, A8, T1 | M | The founder's daily screen, now trustworthy and current |
| 10 | **Governance 2** (done in v1.13.0) | B1, B4, A4, B3, B5 | M | Revise, pause and plan approval: control from the phone |
| 11 | **Review before approval** (done in v1.14.0) | B2, B6 | M | Fewer things reach the founder, and they arrive checked |
| 12 | **Money** | E1, E2 | M | Runway and a total budget on the first screen |
| 13 | **Routines** | E4, D4 | M | Recurring business work runs itself, linked to goals |
| 14 | **Untrusted input and per-role permissions** | B9, B10 | M | Required before opening intake to customers (E5) |
| 15 | **Scorecards and the monthly agent review** | C3, C4, A10 | M | Needs three months of run log from slice 8 |
| 16 | **Watchdog and retries** | B7, B8 | M | Safety net once more roles run on schedules |
| 17 | **Safer upgrades and templates** | H4, H5, H6, E6, H7 | M | Before running several ventures from one plugin version |
| Later | Search, timeline, work products, lessons, ask the team, intake, document history, digests, delegates, role prompt tests | A5, A6, A7, F4, F2, E5, F3, E7, F5, C6, A9, B11, T3, T4 | S–M each | Add when the need shows up |

**v2.0 is slices 6 to 12.** They give a solo founder a measurable goal, a quick start that checks itself, an honest record of each agent, one inbox, control from the phone, a review step before them, and runway on the first screen, all with no server.

---

*Source: [paperclipai/paperclip](https://github.com/paperclipai/paperclip), MIT licence, read on 2026-11-23. Paperclip moves fast; check its `ROADMAP.md` before starting a slice.*
