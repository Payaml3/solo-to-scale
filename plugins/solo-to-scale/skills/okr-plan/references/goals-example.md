# goals.json: a worked example

Example Startup, after its business model (stage 3) was approved, in its first 6-week cycle. Stage 2 (Customer discovery) is the next gate, so `O1.1` proves it.

```json
{
  "about": "The goal tree. Only the founder edits this file (the decision gate).",
  "goal": "£10k MRR from independent studios by November 2027",
  "horizon": "2027-11",
  "north_star": {"metric": "MRR", "unit": "£", "baseline": 0, "target": 10000, "current": 0, "by": "2027-11"},
  "cycles": [{"id": "C1", "start": "2026-12-01", "end": "2027-01-11"}],
  "objectives": [
    {"id": "O1", "title": "Studios confirm the booking pain is worth paying for", "cycle": "C1",
     "owner": "research", "status": "active", "why": "The business model assumes a £49 plan; prove it first",
     "key_results": [
       {"id": "O1.1", "metric": "Interviews showing pain and willingness to pay", "baseline": 0, "target": 5, "current": 0, "stage": 2},
       {"id": "O1.2", "metric": "Studios saying they'd pay £49 a month", "baseline": 0, "target": 3, "current": 0}]},
    {"id": "O2", "title": "Build an audience before the product", "cycle": "C1", "owner": "growth", "status": "active",
     "key_results": [
       {"id": "O2.1", "metric": "Waitlist sign-ups", "baseline": 0, "target": 100, "current": 0},
       {"id": "O2.2", "metric": "Landing page conversion", "unit": "%", "baseline": 0, "target": 8, "current": 0}]}
  ],
  "initiatives": [
    {"id": "I1", "title": "Run 8 Mom Test interviews", "key_result": "O1.1", "owner": "research", "status": "active"},
    {"id": "I2", "title": "Price test in the last 5 minutes of each interview", "key_result": "O1.2", "owner": "research", "status": "active"},
    {"id": "I3", "title": "Landing page with a waitlist", "key_result": "O2.1", "owner": "growth", "status": "active"},
    {"id": "I4", "title": "Two posts a week in studio-owner communities", "key_result": "O2.1", "owner": "growth", "status": "planned"},
    {"id": "I5", "title": "A/B test the hero line", "key_result": "O2.2", "owner": "growth", "status": "planned"}
  ]
}
```

A ticket for it: `python tools/tickets.py new research --title "Book 8 interviews" --goal "8 calls booked" --initiative I1 --by chief-of-staff` carries `initiative:I1` and `goal:O1`.

**Good and bad key results**

| Bad (a task or a vanity number) | Good (an outcome you can measure this cycle) |
| --- | --- |
| Do customer interviews | 5 of 8 interviews show pain and willingness to pay |
| Launch the landing page | 100 waitlist sign-ups at 8% conversion |
| Improve onboarding | 40% of new users finish setup in their first session |
