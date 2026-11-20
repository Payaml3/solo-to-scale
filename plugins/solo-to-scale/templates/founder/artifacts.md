# Live views

Views are generated from the repo and never edited as the source. `publish-views` republishes only rows whose sources changed since the last published commit, on the Monday scheduled task. Comments on a view become proposed edits in the repo.

| View | Artifact type | Slug | Sources | Last published commit |
| --- | --- | --- | --- | --- |
| {{project.name}} progress | Data (dashboard) | | founder/roadmap.json, founder/traceability.json | |
| {{project.name}} AI team | Team view page | | founder/team.json | |
| Business docs | Docs | | founder/business-context.md, founder/brand.md, founder/status.md | |
| Design system | Design System | | design/tokens.json | |
