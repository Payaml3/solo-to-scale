# Design checks to add at stage 11

1. **Raw values:** scan the interfaces' style and component files for hex, rgb() or hsl() colours and px/rem spacing literals outside `design/tokens.json` and generated files. Allow a short, explicit list of exceptions (for example `0`, `1px` borders).
2. **Token drift:** `python3 tools/build_tokens.py --check` fails when a generated file differs from `tokens.json`.
3. **Accessibility:** axe or pa11y in CI on the living component page and each key screen, at three breakpoints.
Each rule gets tests that show it passing and failing.
