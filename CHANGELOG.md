# Changelog

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
