# Playbook: the journey from zero to scale

30 stages in 7 phases (A to G). A stage starts only when the previous gate is passed or explicitly deferred. Inside stages 13 to 17, work ships in slices, built one story group per session. Status is one of To do, Current, Passed or Deferred. Evidence says what shows the gate was met: decision IDs from the registers, files (`founder/sources/interviews.md`) or links, and the dashboard's Venture stage ladder shows it next to each gate. `weekly-review` proposes status and evidence changes; the founder approves them. Engineering-standards gates point to `docs/engineering-standards.md`. **The design gate:** no build (stage 13) starts until stage 9 (Product design) and stage 11 (Design system) are Passed and `DESIGN.md` and `docs/design/brief.md` exist; `check_governance` fails a branch that starts the build without them.

## Stages

| # | Phase | Stage | Where | Gate | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A Discover | Problem validation | P 01 | Pain confirmed by evidence, not assumption |  | To do |
| 2 | A Discover | Customer discovery | P 01 | 5 to 8 interviews show pain and willingness to pay |  | To do |
| 3 | B Define | Business model and positioning | P 01 | Founder approves |  | To do |
| 4 | B Define | Brand strategy | P 06 | Name, trademark and domain checked |  | To do |
| 5 | B Define | Product and operating model | P 02 | Founder approves |  | To do |
| 6 | B Define | UX prototype and test | P 02, Code | Tested with 3 to 5 target users |  | To do |
| 7 | B Define | MVP scope and launch criteria | P 02 | Founder approves scope |  | To do |
| 8 | C Specify and design | Specify | Code | Every open item answered or deferred |  | To do |
| 9 | C Specify and design | Product design | Code | Founder approves the design brief (`docs/design/brief.md`: references, chosen look, flows); screen specs with criteria linked to stories |  | To do |
| 10 | C Specify and design | Plan the system | Code, P 03 | Founder approves architecture, threat model and Well-Architected review; threat model (STRIDE), Well-Architected review, scale-ready defaults in the constitution |  | To do |
| 11 | C Specify and design | Design system | Code | Founder approves foundations; `DESIGN.md` and `tokens.json` follow the brief |  | To do |
| 12 | C Specify and design | Tasks and story groups | Code | `analyze` finds no contradictions |  | To do |
| 13 | D Build and prove | Build, one session per story group | Code 04 | Definition of done met |  | To do |
| 14 | D Build and prove | Test at 5 levels | CI, founder | All levels pass |  | To do |
| 15 | D Build and prove | Integrate continuously | GitHub | Founder merges |  | To do |
| 16 | D Build and prove | Deploy continuously, to non-production | CI | Test data only; dependencies pinned, builds signed; pinned dependencies, automated updates, bill of materials, signed build provenance |  | To do |
| 17 | D Build and prove | Release check | P 05, Code | Go |  | To do |
| 18 | E Launch | Demo and website | Code, P 06 | Honesty checklist signed |  | To do |
| 19 | E Launch | Sandbox or beta | Code | External user completes the core flow |  | To do |
| 20 | E Launch | Design partners | P 06 | Partner confirms value |  | To do |
| 21 | E Launch | Production readiness | P 05, Code | All readiness items closed; service targets and error-budget policy, alerts on user impact, restore and load tests, AI spending caps per customer |  | To do |
| 22 | E Launch | General availability | P 00 | Founder go-live decision |  | To do |
| 23 | F Grow to product-market fit | Measure | P 00, Task | 5 stage metrics tracked weekly |  | To do |
| 24 | F Grow to product-market fit | Iterate | P 01, P 06 | Retention and conversion hit targets |  | To do |
| 25 | F Grow to product-market fit | Fundraise | P 00 | Round closed or deferred |  | To do |
| 26 | G Scale | Team and ownership | P 00 | Every area has a human owner |  | To do |
| 27 | G Scale | Operations | Code, P 05 | Targets met for a quarter; monthly error-budget review, blameless postmortems |  | To do |
| 28 | G Scale | Compliance and certifications | P 03, P 05 | Audit passed |  | To do |
| 29 | G Scale | Platform and new products | Code, P 03 | Architecture approved |  | To do |
| 30 | G Scale | Governance cadence | P 00, Task | Cadence running |  | To do |

## Production readiness

Checked by `release-check` before any production step. Each item is To do, Done or Not needed (with a decision ID).

| Item | Status |
| --- | --- |
| Security review and penetration test | To do |
| Legal terms, privacy and data-processing terms, including the AI provider's data terms | To do |
| Monitoring, alerting on user impact, runbooks and an incident process | To do |
| Backups and a tested restore | To do |
| Load test at expected volume | To do |
| Service targets and error-budget policy (`docs/operations/slo.md`) | To do |
| AI spending caps and rate limits per customer | To do |
| Regulatory advice the domain needs | To do |
