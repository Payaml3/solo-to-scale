# Roadmap: from an operating system to a working AI company

**The goal:** one solo founder runs a startup from idea to scale. The AI team does the work, works together and makes progress between the founder's sessions. Critical actions wait for the founder's approval. One dashboard, behind a login, shows the whole company: business documents, progress, decisions, approvals, and what the agents are doing and saying to each other.

**What v1 already has:**
- the journey (phases A–G, stages 1–30, gates)
- the business-document-to-tested-code trace
- the board of advisors
- the decision registers
- the engineering standards
- the handoffs and context guard
- Git as the memory

**What v1 lacks:** an always-on team. Roles work only when the founder opens a session. They coordinate one session at a time. The only approval gate is merging a pull request. Budgets are advisory, and the views are weekly snapshots.

## Design rules for every slice

- **GitHub stays the control plane.** No new server. Tickets are issues, conversations are issue comments, approvals are founder comments and labels, and work products are pull requests. GitHub already gives the founder notifications, mobile apps, an audit trail and access control.
- **The founder's words are the only approval.** A gate counts as approved only when the founder's own GitHub account approves it. An agent, a bot or a label added by anyone else never counts.
- **Fail closed.** An agent that can't confirm an approval treats the action as not approved.
- **Plain repo tools, standard library only,** tested on Linux, macOS and Windows.

## Slices

| # | Slice | What the founder gets | Status |
|---|---|---|---|
| 1 | **Founder approval gates** | `founder/gates.json` lists the critical actions: hire, budget, merge to main, deploy, external messages, spending, decisions, secrets, pricing, legal. Each is `ask`, `allow` or `off`. Agents request approval as an issue and stop that action; the founder replies `/approve`, `/approve always` or `/reject <reason>` from anywhere, including the GitHub phone app. A CI check blocks gated pull requests until the founder approves. | Done |
| 2 | **Agent coordination** | Roles delegate to each other through issues: a parent ticket, sub-tickets per role, `@role` hand-offs, blockers, and an atomic claim so two agents never take the same ticket. One activity log of who did what, and why. | Done |
| 3 | **Heartbeats and budgets** | Each role wakes on its own schedule as a cloud scheduled task. It checks its tickets, works one claimed item within its budget, comments, opens a pull request or an approval request, and hands off. A cost log per role, with a warning at 80% and a hard stop at 100%. | Done |
| 4 | **The startup dashboard** | One page with tabs: Overview, Business documents, Progress trace, Roadmap, Scope and journey, Team and board, Agent activity (the conversations between roles), Decisions, Approvals inbox, and Costs. It's rebuilt from the repo and GitHub on every merge and every hour, and hosted at `pm.<domain>` behind a login. The Claude page stays as a backup. | Done |
| 5 | **Portfolio** | Several ventures side by side, each in its own repo, with one overview. | Done |

Each slice is one pull request with a version bump. Startups pick it up through `upgrade`.
