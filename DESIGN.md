---
version: alpha
name: solo-to-scale views
description: The look of the pages the plugin generates (the startup dashboard and the portfolio). A calm, data-dense, black-and-white developer-tool style with one ink accent, hairline borders, stacked soft shadows and tabular numbers. Inspired by Vercel's design language as analysed in VoltAgent/awesome-design-md (MIT); our own name, no brand marks.

colors:
  light:
    paper: "#fafafa"        # page
    surface: "#ffffff"      # panels, tiles, cards
    sunk: "#f2f2f2"         # table heads, hover rows, inset regions, empty bars
    ink: "#171717"          # text and the single accent
    muted: "#666666"        # secondary text (AA on white)
    line: "#ebebeb"         # hairlines
    line-strong: "#c9c9c9"  # secondary button borders, the open agent page
    accent: "#171717"
    on-accent: "#ffffff"
    on-status: "#ffffff"   # text on a filled status colour
    link: "#0068d6"
    done: "#1a7f37"
    progress: "#ab570a"
    todo: "#8f8f8f"
    waiting: "#cb2a2f"
    group-business: "#ab570a"
    group-product: "#7928ca"
    group-technical: "#0068d6"
  dark:
    paper: "#000000"
    surface: "#0a0a0a"
    sunk: "#1a1a1a"
    ink: "#ededed"
    muted: "#a1a1a1"
    line: "#2e2e2e"
    line-strong: "#454545"
    accent: "#ededed"
    on-accent: "#0a0a0a"
    on-status: "#0a0a0a"
    link: "#52a8ff"
    done: "#62c073"
    progress: "#f2a33a"
    todo: "#8f8f8f"
    waiting: "#ff6166"
    group-business: "#f2a33a"
    group-product: "#bf7af0"
    group-technical: "#52a8ff"

typography:
  family: '"Geist", "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
  mono: '"Geist Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace'
  page-title: { size: 2rem, weight: 600, letterSpacing: -0.04em }
  section-title: { size: 1.125rem, weight: 600, letterSpacing: -0.02em }
  metric: { size: 1.6rem, weight: 600, letterSpacing: -0.03em, numeric: tabular-nums }
  body: { size: 15px, lineHeight: 1.5, weight: 400 }
  label-mono: { size: .7rem to .75rem, weight: 500, family: mono }

rounded: { xs: 4px, sm: 6px, md: 8px, lg: 12px, full: 9999px }
spacing: [4px, 8px, 12px, 16px, 20px, 24px, 32px]
shadow:
  light: "0 1px 1px rgba(0,0,0,.02), 0 2px 2px rgba(0,0,0,.04)"
  dark: none
---

# DESIGN.md: solo-to-scale views

How the generated pages look. Agents: follow this file whenever you change `templates/tools/dashboard.html` or `templates/tools/portfolio.html`. The CSS custom properties at the top of each page are the implementation of the tokens above; change both together.

## Overview

The pages are operator tools a founder reads every day, so they should feel like a top developer platform's dashboard: quiet, exact and fast to scan. Near-white (or pure black) canvas, white (or near-black) cards held by a 1px hairline and a barely-there stacked shadow, black ink as the only accent, and colour only where it carries meaning (status). Numbers are large, tight and tabular. Technical labels (commit, build time, paths, tags) are set in mono.

## Hard constraints

- **One static HTML file.** No build step, no React, no Tailwind. A strict CSP (`default-src 'none'`) blocks every outside script, stylesheet, font and image. So: no web fonts (Geist and Inter are used only if installed; the system sans is the real default), no CDN component libraries, no icon fonts. Icons, if ever needed, are inline SVG.
- **Both themes, always.** Light and dark are defined three times in each page (light, the system dark setting, and the toggle). Never add a colour to one block only.
- **Text stays text.** Data from the repo or GitHub goes in with `textContent`, never as HTML.

## Colours and roles

- `accent` is ink. It marks the selected tab, the current stage, primary action buttons and the founder's own node. There is no brand hue.
- Status colours (`done`, `progress`, `todo`, `waiting`) are the only saturated colours on a page. Use them for status text, pills, bars and marks, never for decoration.
- Pills are tinted, not outlined: `currentColor` text on a 12% `currentColor` background, fully rounded.
- Document groups (business, product, technical) use the `group-*` tokens as a 3px edge and a mono tag.
- Text on a filled status colour uses `--on-status` (white in light mode, near-black in dark mode) so it keeps contrast in both.

## Typography

- One sans family, one mono family. Weight ceiling is 600; never bold 700 for headings.
- Headlines in sentence case with negative tracking (page title -0.04em, section titles -0.02em, metrics -0.03em). No all-caps labels; use the mono label style instead.
- Every number that can change sits in `tabular-nums`.

## Layout

- Max width 1180px, 16px gutters on phones, no horizontal page scroll (wide tables scroll inside `.table-wrap`).
- Cards: 8px radius, 1px `line` border, `--shadow`, 20px padding (tiles 14px 16px). Never a single heavy drop shadow.
- Sticky tab bar: translucent `paper` with a backdrop blur, 2px ink underline on the selected tab, hover lifts the label to `ink`.
- Tables: muted 0.75rem headers on a `sunk` band, 9px 10px cells, hairline rows, `sunk` row hover.
- Inputs and selects: 36px high, 6px radius, hairline border.

## Do

- Keep the page black, white and grey; let status colour be the signal.
- Use mono for build lines, commit hashes, paths, slugs and tags.
- Check every change in light and dark, on a phone width and on desktop.

## Don't

- Don't add a brand hue, a gradient or a second accent.
- Don't load anything from outside the page.
- Don't use uppercase micro-labels or weight 700.
- Don't copy another company's logo, wordmark or name into the page.

## Where this came from

Starting point: the Vercel analysis in [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT), adapted for a dense internal dashboard: system fonts instead of Geist web fonts, a real dark theme, status colours for an operating system rather than marketing gradients. For a venture's own product, `design-system` can start from any file in that collection as one of its proposed directions.
