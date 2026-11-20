# Decisions: company register (`B-`)

Business decisions: GTM, pricing, brand, legal, hiring. Product and engineering decisions (`D-`, plus `C-` contradictions, `G-` gaps, `A-` assumptions) live in `specs/<feature>/decisions.md` once Spec Kit creates it; until then this register holds everything, with a Type column.

- Status is one of Approved, Proposed, Assumption, Open. Only the founder's words make a row Approved.
- A changed decision gets a new row that supersedes the old one. Board memos: `board/<ID>.md`.
- Layers: Business → Product → MVP → Architecture → Tasks → Tests → Release.

| ID | Decision | Type | Status | Date | Source (founder's words) | Layers | Board |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B-01 | Run the startup on the solo-to-scale operating system | Business | Proposed | {{today}} | (approved by merging the init PR) | Business | |
