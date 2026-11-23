# answers.json

Written by the `init` skill from the founder's answers, kept outside the repo, never committed.

```json
{
  "project": {"name": "Example Startup", "working_name": true, "repo": "example/example-startup",
              "one_line": "What it is and for whom", "stage": 2},
  "goal": "100 paying studios by June 2027",
  "guard": {"warn_pct": 60, "handoff_pct": 75, "warn_tokens": 100000, "handoff_tokens": 140000},
  "budgets": {"chief-of-staff": "$40", "research": "$30", "product": "$30", "architect": "$40",
              "engineer": "$120", "qa": "$30", "growth": "$30", "board": "$20"},
  "enable_plugins": ["superpowers@<marketplace>", "founder@<marketplace>"],
  "react": ["apps/web"],
  "epics": {"architect": "CORE, RUNB", "qa": "TEST", "growth": "SITE, HELP", "engineer": "all other epics"},
  "cross_review": false,
  "labels": false,
  "sales_advisor": false
}
```

Only `project.name`, `project.repo` and `project.one_line` are required; everything else has a default. `goal` (one measurable sentence, at most 300 characters) becomes the company goal in `founder/goals.json`. A quick start writes only `project` and `goal`. `react` and `labels` steer the skill, not the templates.
