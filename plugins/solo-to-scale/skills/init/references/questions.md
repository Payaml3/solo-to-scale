# init questions: defaults and why

| # | Question | Default | Notes |
| --- | --- | --- | --- |
| 1 | Name, working name?, repo, one line, stage, company goal | none: always ask (the goal may be blank) | Saved once in `founder/project.json`; every file and hook reads it from there. Stage hints: idea 1, validating 2, building the MVP 13, launched 22 |
| 2 | Context-guard limits | warn 60% or 100,000 tokens; handoff 75% or 140,000 tokens | Each level fires at whichever comes first. `context_window_tokens` stays null unless the founder sets it |
| 3 | Monthly AI budget per role (USD) | Open | Written to `founder/heartbeats.json`. Enforced for heartbeats: a warning at 80%, a stop at 100%. A role without a budget never runs a heartbeat; heartbeats start off |
| 4 | Plugins to enable | the ones the project needs | Enabled plugins' skill descriptions load into every session: recommend disabling unrelated ones (social media, for example). Use the exact identifiers this session shows (`name@marketplace`) |
| 5 | React interfaces | none | Only React interfaces use shadcn/ui and Tailwind; others build the same components natively |
| 6 | Epic-to-role split | architect: foundation, operations, audit; qa: evaluation and test; growth: website, docs, SDK; engineer: all other epics | Written once, in `founder/team.md` "## Epic ownership" |
| 7 | Cross-review CI job | off | Codex reviews Claude's PRs and the reverse; needs API-key secrets |
| 8 | Create labels now | no | Creating labels is visible on GitHub; list them as a manual step otherwise |
| 9 | Sales advisor | off | Offered from stage 20 (design partners) |
