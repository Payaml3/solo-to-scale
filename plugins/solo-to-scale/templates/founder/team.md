# Team: {{project.name}}

The founder is CEO and chairs the board. Claude is the AI core and chief of staff. Six AI roles each own one function, and four AI advisors sit on the board. Role definitions come from the solo-to-scale plugin (`roles/`).

## Org

| Seat | Who | Owns |
| --- | --- | --- |
| CEO and chair | Founder | Goal, approvals, secrets, money, go-live |
| AI core | Claude (`chief-of-staff`) | The operating system: briefs, memory, weekly review, views |
| 01 | `research` | Evidence and business work outside software |
| 02 | `product` | Requirements, stories, screen specs; prepares decisions |
| 03 | `architect` | Stack, architecture, threat model |
| 04 | `engineer` | Product build, one story group per session |
| 05 | `qa` | Evaluation, release check, accessibility review |
| 06 | `growth` | Brand, website, docs, content, launch |
| Board | `growth-advisor` (acquisition lens), `owner-advisor` (long-term value lens), `customer-advisor` (demand lens), `risk-advisor` (regulator's lens) | Advice only; no vote |

## Epic ownership

The only copy of the epic-to-role mapping. `tools/build_team.py` and `tools/build_traceability.py` read it. List epic codes (2 to 5 capitals) after each role; `init` proposes the split and the founder confirms it.

- architect: {{epics.architect}}
- qa: {{epics.qa}}
- growth: {{epics.growth}}
- engineer: {{epics.engineer}}
- product: prepares the C-, G- and A- decisions
- research: the non-software model items

## Schedule

| Role | Runs |
| --- | --- |
| chief-of-staff | Every session start and end; Mondays (scheduled task) |
| research | Each discovery sprint; monthly evidence review |
| product | Each stage; whenever a decision waits |
| architect | Stage 10; quarterly review |
| engineer | Each story group |
| qa | Nightly through CI; before each release |
| growth | Weekly; each launch |
| board | Significant decisions (`board-review`); the quarterly strategy review |

## Monthly budget per role

Advisory only: nothing enforces a Claude budget. The weekly review warns at 80% and proposes a pause at 100%; the founder decides.

| Role | Monthly budget |
| --- | --- |
| chief-of-staff | {{budget.chief-of-staff}} |
| research | {{budget.research}} |
| product | {{budget.product}} |
| architect | {{budget.architect}} |
| engineer | {{budget.engineer}} |
| qa | {{budget.qa}} |
| growth | {{budget.growth}} |
| board | {{budget.board}} |

## Advisor routing

`board-review` asks only the advisors this table names. Each writes at most 8 lines; memos go in `board/<decision ID>.md`.

| Decision | Advisors |
| --- | --- |
| Pricing, positioning | growth, owner, customer |
| Scope, a new feature | customer, risk |
| Fundraising, large spend | owner, growth |
| Go-live, data, partners | risk, customer |
| Hiring | owner |
| Anything else hard to reverse | owner, risk |

The sales advisor (enterprise lens) is {{sales_advisor}}.

## Rules

- One role per session.
- Roles talk only through issues, PRs, the registers and `HANDOFF.md`.
- A role proposes; the founder approves. Critical actions go through the `gate` skill and `founder/gates.json`; only the founder's own `/approve` counts, and `founder/gates.json` changes only by the founder.
- Advisors are named by their lens, never as real people. No invented quotes, no claimed endorsement, no advisor names in anything public. The risk advisor is never legal advice.
