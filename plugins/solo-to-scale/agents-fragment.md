## Operating protocol

- Follow `founder/operating-protocol.md`, the only copy of the protocol. Founder HQ is `founder/`: status, decisions (`B-`), business context, brand, playbook, team, live views.
- The repo is the memory. Nothing becomes Approved without the founder's words; merging a PR is approval.
- Start every session from `HANDOFF.md`. End it with the `handoff` skill: a short close, or a full handoff when a slice is done or the context guard fires.
- Claim a story-group issue first (`claim` skill), and start from its goal chain.
- Work with other roles only through tickets (`coordinate` skill): claim, delegate, hand off, block and finish with `tools/tickets.py`. Write `role:<name>`, never `@<name>`.
- Heartbeats: a scheduled run of a role uses the `heartbeat` skill: one ticket within its budget (`founder/heartbeats.json`), then hand off and record the cost with `tools/heartbeat.py end`.
- Significant decision: run `board-review` before the founder decides, then `record-decision` after.
- Approval gates: before any critical action listed in `founder/gates.json` (hire, budget, deploy, external messages, spending, decisions, pricing, legal), run the `gate` skill and wait. Only the founder's own `/approve` counts; fail closed.
- Engineering standards: `docs/engineering-standards.md`. Journey and gates: `founder/playbook.md`.
- Terms: phase (A to G), stage (1 to 30), slice (a shippable increment with an exit check, stages 13 to 17), story group (3 to 6 related stories in one session).
