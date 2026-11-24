# Design: how we do what

This is the single source for how a venture gets its product design, from the first prototype to launch. The handbook points here. Decisions in this file are the plugin's defaults. A venture records its own choices (the look, the references) as `D-` decisions.

## The principle

The product should look and feel like a top company's product, and that is decided **before any code**. Design starts lightly at discovery, gets serious once the product model and MVP scope are approved, and is a hard gate before the build. Agents design from written references (real products, a DESIGN.md, a brief), never from adjectives alone.

## The journey, stage by stage

| Stage | What happens | Lead skill | Helpers | Output |
| --- | --- | --- | --- | --- |
| 4. Brand strategy | Name, voice, first brand ideas | brand-skills | | `founder/brand.md` |
| 6. UX prototype and test | A clickable prototype of the key journeys, shaped by 2 or 3 reference products | `product-design` | Mobbin or Refero for references | Prototype, test notes |
| 9. Product design (**gate**) | The product designer's work: references, the look, flows, screen specs | `product-design` | `ui-ux-pro-max` (industry rules, palette and type options), awesome-design-md, galleries | `docs/design/brief.md`, `specs/*/ux/*.md` |
| 9. Design review (**gate**) | Score the brief 0 to 10 on each dimension; fix everything under 8 | `product-design` | `impeccable` | Scores in the brief |
| 11. Design system (**gate**) | Turn the approved look into the system | `design-system`, taste leads art direction | brand-skills: brand-identity | `DESIGN.md`, `tokens.json`, components |
| 13. Build | Screens built from the specs and the system | Engineers | `frontend-design` for craft within the tokens; Emil's skills for motion | Code, screenshots |
| QA (level 5) | One reviewer per pass | `impeccable` for UX and accessibility, or taste for visual quality | `review-animations` for motion | Review notes |
| 18. Demo and website | The public site | Taste | Magic UI or Aceternity UI sections where the site uses React; founder: landing-page for copy | Site |
| 18 to 22. App launch (mobile only) | Store screenshots that sell | `app-store-screenshots` | | Store assets |

**The gate.** `check_governance` fails a branch that moves stage 13 or later to Current or Passed until stages 9 and 11 are Passed and `DESIGN.md` and `docs/design/brief.md` exist. Repos that were already building, or that adopt the playbook while building, get a warning instead.

## The design brief (stage 9)

`product-design` writes `docs/design/brief.md` from its template once stages 5 and 7 are approved. It holds:

1. **Users and the feeling:** who uses it, where, and three words for how it should feel.
2. **References:** 3 to 5 shipped products in the same category or for the same users, from Mobbin, Refero, Land-book, Httpster or Component Gallery, each with what to take and what to avoid.
3. **The look:** 2 or 3 options, each starting from a company's DESIGN.md in [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) or from `ui-ux-pro-max`'s recommendation for the industry, adapted to `founder/brand.md`. The founder picks one.
4. **Key flows** for the MVP journeys, each linked to its screen specs.
5. **Component sources** for the stack (below).
6. **Review scores:** hierarchy, consistency, accessibility, responsiveness, empty and error states, motion and brand fit, each 0 to 10, with a fix for anything under 8.

The founder approves the brief and the look as a `D-` decision. Stage 11 then writes `DESIGN.md` (look, rules, do's and don'ts, pointing to `tokens.json` for values) and `tokens.json`.

## Component sources, by stack

| The interface uses | Use | Don't |
| --- | --- | --- |
| React | shadcn/ui as the base; 21st.dev, Magic UI and Aceternity UI for richer pieces; mapcn for maps | Mix several animated libraries on one screen |
| No React (server templates, static pages) | Native components built from the same tokens; Uiverse for small CSS pieces | Add React or Tailwind without a decision |
| Any | Spline (3D) or maps only where they serve a task, with a reason in the brief | Decoration that slows the page |

Adding React or Tailwind is a framework change: it is proposed as a decision, never made in passing.

## The skills we use

Install these once per machine or account. None is bundled into the plugin.

| Skill | Source | Install | Used for |
| --- | --- | --- | --- |
| `product-design`, `design-system` | solo-to-scale | With the plugin | The brief, screen specs, the system, the gate |
| `design-taste-frontend`, `impeccable`, `frontend-design`, `emil-design-eng` | Built in to Claude | Nothing to install | Art direction, UX and accessibility review, build craft, polish |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT) | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill`, then `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill`. Needs Python 3 | Industry rules, style, palette and type options for the brief. Advice only: it suggests and never rewrites the app. The brief, not its database, decides |
| Emil Kowalski's skills | [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT) | `npx skills@latest add emilkowalski/skills` | Motion and polish at build and QA: `animate`, `review-animations`, `improve-animations`, `animation-performance` |
| `app-store-screenshots` | [ParthJadhav/app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots) (MIT) | `npx skills add ParthJadhav/app-store-screenshots` | Mobile apps only, at launch. It scaffolds its own Next.js editor, so run it in a separate folder, never inside the product repo |

**Considered and not used: gstack.** Its design review idea (score each dimension 0 to 10, fix everything below the bar) is good, and the brief's review scores use it. The toolkit itself is a large bundle with its own roles, hooks and shipping process that would overlap with this operating system's roles, context guard and gates, so we don't install it.

## Who leads when

The taste skill chooses its own art direction, so it leads only where no design system exists yet.

| Stage | Leads | Supports |
| --- | --- | --- |
| 9. Product design | `product-design` | `ui-ux-pro-max`, awesome-design-md, galleries |
| 11. Design system | Taste: art direction for type, palette and composition, which becomes `DESIGN.md` and `tokens.json` | brand-skills: brand-identity |
| 13. Product screens | `design-system` and `product-design` | Taste for review only, within the existing tokens and components; `frontend-design` and Emil's skills while building |
| 18. Website and landing pages | Taste: public pages, with its screenshot check | founder: landing-page for copy |
| Design QA (level 5) | One reviewer per pass: taste for visual quality, or `impeccable` for UX and accessibility | Never both on the same pass |

On screens covered by the design system, no skill may add colours, fonts or components without a `D-` decision.

## Rules that always hold

- **Inspired by, never copied.** Take structure, density and rules from references; never another company's name, logo, wordmark or artwork.
- **One look.** One DESIGN.md and one `tokens.json` per product. Raw colour and spacing values appear only in the token files.
- **Accessible by default.** WCAG 2.2 AA, keyboard paths, focus order, reduced motion, checked at three breakpoints.
- **Every state designed.** Loading, empty, success, error and permission-denied, in the screen spec before the code.
- **Motion has a job.** It explains a change or confirms an action; it never just decorates.

## The plugin's own pages

The dashboard and the portfolio follow the plugin repo's own `DESIGN.md` (a Vercel-inspired look from awesome-design-md, with system fonts because the pages' security policy blocks web fonts). CI fails if the colours in `DESIGN.md` and the pages' CSS disagree.
