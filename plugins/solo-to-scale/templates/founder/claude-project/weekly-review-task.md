# Monday scheduled task: weekly review, then refresh the views

Create this as a weekly scheduled task (Mondays), in a Claude Code session on `{{project.repo}}` that has artifact tools. Model: mid-tier.

## Prompt

Read AGENTS.md and HANDOFF.md. On the default branch, run the solo-to-scale `weekly-review` skill, starting with its quiet-week stop: if nothing changed since the "Last updated" date in founder/status.md and CI passes, reply in 2 lines and stop. Otherwise open the review PR and never merge it. Then run the `publish-views` skill. It republishes only the views whose sources changed, and stops if none did or if this session has no artifact tools.
