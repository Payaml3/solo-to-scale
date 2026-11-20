# Engineering standards

Adapted from Anthropic, Google, Microsoft, DORA, SLSA and OWASP, sized for a startup. Each one starts at the stage where it pays off; `founder/playbook.md` gates point here. Plugin-owned: change it in solo-to-scale and run `upgrade`.

## Using Claude efficiently (day 0)

- `AGENTS.md` plus `CLAUDE.md` stay under {{gov.claude_md_max_lines}} lines together (CI fails above that). Area conventions go in a subdirectory `CLAUDE.md` or path-scoped rules.
- Rules that keep being broken become hooks or CI checks.
- Subagents only for searches across 10 or more files, 3 or more independent pieces of work, or an independent review.
- Test the changed area first: `python tools/test_area.py <path>`. CI runs the full suite.
- Choose the model at the start of a session; don't edit the instruction files or switch models partway through.
- The product's own AI calls cache long system prompts and use the Batch API for non-urgent work.
- Least-privilege tool permissions; no production secrets in development sessions (`.claude/settings.json`, `.codex/config.toml`).

## Delivery (stage 13)

- Five DORA metrics in the weekly review: deployment frequency, change lead time, change failure rate, failed-deployment recovery time, deployment rework rate. "n/a until deploys exist", never guesses.
- Small pull requests: the governance check warns above {{gov.pr_warn_lines}} changed lines, not counting generated and lock files.
- Merges within one business day. No merge may lower code health.

## Security

| Practice | Stage | Output |
| --- | --- | --- |
| Threat model (STRIDE) with a data-flow diagram | 10, a gate | `docs/security/threat-model.md` |
| Least privilege for agents and tools; the AI proposes, the rules decide | 10 | Constitution rules |
| Pinned dependencies, automated updates, a bill of materials per release | 16 | CI jobs |
| Signed build provenance (SLSA level 2) | 16 | Release artifacts |
| OWASP AI risks: prompt injection, excessive agency, unbounded consumption; spending caps per customer | 10 and 21 | Evaluation suites, rate limits |

## Reliability and scale

| Practice | Stage | Output |
| --- | --- | --- |
| Scale-ready defaults: stateless servers, idempotent APIs, queues, pooling, every query scoped to its customer | 10 | Constitution rules |
| Well-Architected review (six pillars) | 10, then quarterly from 27 | Review notes, `D-` decisions |
| Service targets, error budget and error-budget policy | 21 | `docs/operations/slo.md` |
| Alerts on user impact; restore and load tests | 21 | Monitoring, test reports |
| Monthly error-budget review; blameless postmortems recorded as decisions | 27 (postmortems from 22) | Review and postmortem notes |

## Performance and cost

- p95 latency budget per key endpoint, checked in CI. Integration tests flag repeated queries (N+1).
- Unit cost per customer, including AI tokens and hosting, reviewed monthly with budget alerts.
