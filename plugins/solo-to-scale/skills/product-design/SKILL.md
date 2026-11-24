---
name: product-design
description: Turn approved requirements into screen specifications - journeys, information architecture, interactions, validations, permissions, every state, responsive and accessibility rules, and acceptance criteria tied to story IDs; and, at stage 9, the design brief that must be approved before any code. First used at stage 6.
---

# product-design

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

Read `AGENTS.md`, `HANDOFF.md` and `founder/operating-protocol.md` first. No subagents, except an independent visual review of a large set of screens. Model: strongest for system-level journeys, mid-tier for single screens.

## Inputs: approved requirements only

Spec Kit `spec.md` and requirements, and the stories with their IDs. If a requirement it needs is Proposed or Open, **stop and ask**. Never design on top of an unapproved requirement.

## Design brief (stage 9): the gate before code

Once the product model (stage 5) and MVP scope (stage 7) are approved and the specs are being written, act as the product designer and write `docs/design/brief.md` (template: `references/design-brief.md`):
- **References:** 3 to 5 shipped products in the same category or for the same users, from Mobbin, Refero, Land-book, Httpster or Component Gallery, each with what to take (a flow, a layout, a density) and what to avoid.
- **The look:** one company's DESIGN.md from [awesome-design-md](https://github.com/VoltAgent/awesome-design-md), or our own direction, and how it is adapted to `founder/brand.md`. Never copy another brand's name, logo or marks.
- **Key flows** for the MVP journeys, and the **component sources** for this stack: shadcn/ui, 21st.dev, Magic UI or Aceternity UI only where the interface uses React; otherwise native components, with Uiverse for small CSS pieces.

Offer 2 or 3 options where the choice is real; the founder picks and the choice is recorded with `record-decision` as a `D-` decision. Stage 11 (`design-system`) then turns it into `DESIGN.md` and `tokens.json`. The build (stage 13) cannot start until stages 9 and 11 are Passed; `check_governance` enforces it. At stage 6, use the same references lightly for the prototype.

## What it produces

One screen spec per screen: `specs/<feature>/ux/<screen>.md`, next to the requirements it serves (template: `references/screen-spec.md`). Each spec:
- links requirements and stories by ID; it never copies them
- defines the journey step, information architecture and layout regions
- defines interactions, validations, permissions and edge cases
- specifies every state: loading, empty, success, error, permission-denied
- defines responsive behaviour and accessibility: WCAG 2.2 AA, keyboard paths, focus order, labels
- lists implementation acceptance criteria, each referencing a story ID

If a screen spec adds or changes acceptance criteria, **propose the change to the story** through Spec Kit or the backlog source. Never keep a second list.

## Workflow for every new screen

Approved requirement → UX specification → design-system components → frontend implementation → visual and accessibility review → acceptance tests.
1. Review the approved requirements, by ID.
2. Write or update the screen spec with this skill.
3. Reuse design-system components; create a new one only if none fits, and say why (`design-system` skill).
4. Implement every state and interaction in the spec.
5. Validate: automated accessibility checks (axe or pa11y) at three breakpoints; screenshots in the handoff; one review pass, `impeccable` by default, taste only when visual quality is the question.
6. New design decisions go to `record-decision`: product and UX in the product register, brand in `founder/decisions.md`.

New content starts as Proposed. Close with `handoff`.
