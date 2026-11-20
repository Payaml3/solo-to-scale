---
name: board-review
description: When a significant decision is proposed, before the founder decides - write a one-page brief, ask only the advisors the routing table names, and summarise where they agree and disagree. Advisors read only the brief.
---

# board-review

**Read narrowly.** Never read a whole file over 150 lines. Use `grep -n`, then read only the line ranges you need. Use `git diff` and `git log` to see changes.

Use it for significant, hard-to-reverse decisions only. Small calls go straight to the founder.

## 1. Write the brief (one page, at most 40 lines)

`founder/board/<decision ID>-brief.md`, with the next free ID from the register (`grep -n "^| B-" founder/decisions.md`):
- the decision in one line, and its type (the routing row)
- context: what we know, with evidence and its source; what is Assumption or Open
- 2 or 3 options with trade-offs and a recommended option
- what is irreversible, the cost, the time frame

## 2. Route it

Read the routing table in `founder/team.md` ("## Advisor routing"). Ask only the advisors on the matching row; "Anything else hard to reverse" means owner and risk.

## 3. Ask each advisor

Run each named advisor on the brief alone, never the repo:
- Claude Code: the plugin agent `solo-to-scale:<lens>-advisor` (for example `solo-to-scale:risk-advisor`), giving it the brief's text.
- Codex: the `<lens>-advisor` agent in `.codex/agents/`, given the brief's text.
- Neither available (a Project chat): adopt each advisor's charter from `roles/<lens>-advisor.yaml`, one at a time, in a separate message.

Each memo is at most 8 lines: verdict (support, concerns or oppose), biggest risk, what would change its mind, one metric to watch. The risk advisor's memo ends with whether a real lawyer is needed.

## 4. Summarise

Append to `founder/board/<decision ID>.md`: each memo under its lens name, then 3 to 6 lines on where they agree and where they disagree, and the open questions for the founder. Then hand the decision to the founder. The founder decides; record it with `record-decision`.

## Rules for every advisor output

Check each memo before saving (details: `references/rules.md`):
- Name advisors by their lens, never as the real person.
- No quotation marks around a real person's words; no first-person claims to be that person; no claim of endorsement.
- Frameworks are paraphrased, never copied from the books, essays or letters.
- No advisor names in anything public. The risk advisor is never legal advice.

Rewrite any memo that breaks a rule before saving it.
