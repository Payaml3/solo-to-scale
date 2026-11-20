Follow `founder/operating-protocol.md` in project knowledge. If it's missing, say so before substantial work.

## Project specifics

- Project: {{project.name}}. {{project.one_line}}
- Repository: `{{project.repo}}`, the source of truth. Project knowledge is a copy and can be out of date.
- Status: `founder/status.md`. Business decisions: `founder/decisions.md` (`B-`). Product and engineering decisions: `specs/<feature>/decisions.md` (`D-`).
- Business context: `founder/business-context.md`. Team, routing and budgets: `founder/team.md`. Journey: `founder/playbook.md` (read on demand).
- Claude Code sessions are named `{{project.name}} · <slice or group> <name>`.

## Chat rules

- Prefix every chat: `00 | Founder HQ`, `01 | Business`, `02 | Product`, `03 | Architecture`, `05 | QA` or `06 | GTM`. Engineering (04) runs in Claude Code.
- One task per chat. Rename it with "(done)" when it's closed.
- Never mark anything Approved without the founder's words. New content starts as Proposed, Assumption or Open.
- Significant decision: use `board-review` (only the advisors the routing table in `team.md` names), then `record-decision` once the founder decides.
- Read narrowly: ask for, or search, only the sections you need.
- Project chats can't see context usage. Offer a close when the deliverable is done, after a large document is loaded, or after about 20 exchanges.
- Close with a short close (3 lines: Done / Pending / Next) or a full handoff. A full handoff ends with update-ready blocks, one per file, each labelled with its target path, because Project chats can't write to the repo.
