# Design brief: the dashboard and the portfolio

The plugin's own pages get the same stage 9 review a venture's product gets (`plugins/solo-to-scale/docs/design.md`): score each dimension 0 to 10 and fix everything under 8. The look itself is in `DESIGN.md`; this file records the review behind it. Review it again whenever a tab or panel is added.

## Users and the feeling

One founder, usually alone, checking the company several times a day: at a desk between sessions, and on a phone away from it. They come to answer three questions fast: what needs me, where are we on the journey, and is anything stuck or overspending. Three words: **calm, exact, alive**. Calm because the page is read every day; exact because every number is a decision input; alive because agents work while the founder is away, and the page should show that without shouting.

## References

| Reference | Take | Avoid |
| --- | --- | --- |
| Vercel dashboard (via awesome-design-md, already the base) | Black-and-white canvas, hairlines, one ink accent, mono for technical labels, the sliding tab underline | Marketing gradients, Geist web fonts (the page's security policy blocks them) |
| Linear | Status as the only colour, quiet density, fast state changes | Keyboard-first chrome we don't need |
| GitHub Actions run pages | Live status dots, timestamps in mono | Dense iconography |

## Advice from the skills

- **UI/UX Pro Max** (its rules for a data-dense dashboard and its UX guidelines, read from the skill's data files): keep a neutral canvas with status colours only; text at least 4.5:1; visible focus on every control; touch-sized targets; no horizontal page scroll; reduced motion honoured; animate one or two things per view at most; no hover-only meaning.
- **Emil Kowalski's design engineering and animate skills:** motion only where it explains a change or confirms an action; ease-out curves, under 300 ms for UI; only `transform` and `opacity`; press feedback on pressables; hover effects only on devices with a fine pointer; nothing animated on keyboard actions that repeat all day.
- **frontend-design / taste:** stay inside the existing tokens; no new hue, font or component library.

## Review scores

Scored on a demo venture (stage 13, 12 tabs, GitHub data present), at 1280 px and 390 px, light and dark.

| Dimension | Before | After | What changed |
| --- | --- | --- | --- |
| Hierarchy | 8 | 9 | On desktop the tabs moved into a left sidebar (the founder's call): all 12 are visible at once instead of 8 running off the edge, and the content gets the full height. The theme switch moved from a floating pill over the content into the header, next to the title. |
| Consistency | 6 | 9 | Removed the uppercase phase labels and the three weight-700 spots (DESIGN.md allows neither). Goal bars no longer turn amber whenever a goal is short of 100%: achieved is green, on track is ink, behind is amber, so the bar agrees with its pill. The portfolio follows the same rules. |
| Accessibility | 6 | 9 | The light `todo` grey was 3.3:1 on white, under AA for pill text; it is now `#6e6e6e` (5:1). Focus rings added to the document groups, document cards, document list and the theme switch. The theme switch has an accessible name and a sun or moon icon. |
| Responsiveness | 6 | 8 | On a phone the goal rows stack (label on its own line, bar and percent under it) instead of squeezing to one word a line. The tab strip fades at an edge that has more tabs, so the 8 tabs past the screen edge are discoverable; its scrollbar is hidden. |
| Empty and error states | 8 | 8 | Already covered on every tab (no data, GitHub down, stale build); unchanged. |
| Motion | 3 | 8 | There was none. Now, each with a job: the tab underline slides to the selected tab (where you went); the tab's content fades up 4 px in 200 ms (that it changed); progress bars fill from the left once when shown (what the number means); pressables scale to 0.97 (the press registered); the toast rises in; a working agent's status dot breathes (the one live thing on the page); the ladder's chevron turns. All use `transform` and `opacity` with a strong ease-out. With reduced motion, movement goes and only short fades stay. Arrow-key tab changes still move instantly apart from the underline. |
| Brand fit | 8 | 9 | Still the black-and-white operator look, no new colours or fonts; motion is crisp and short to match a professional tool. |

## Left as is, on purpose

- **Agent avatars keep their per-role hue.** They are identity, not decoration, and the team view needs them told apart at a glance.
- **No skeleton loaders.** The page is static and complete when it opens; there is nothing to load.
- **No web fonts or icon fonts.** The security policy blocks them; the two icons are inline SVG.
