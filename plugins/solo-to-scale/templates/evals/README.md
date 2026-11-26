# Evals

An eval is a past ticket the team already got right, kept so you can check that a role still gets it right. Re-run a role's evals before you change its model, its prompt or its skills.

## Add a case

Make one file per case at `evals/<role>/<case>.md`. The case name is lower case, digits and hyphens, like `evals/engineer/invoice-export.md`.

```
# Export invoices as CSV

Ticket: #41

## The task
What the ticket asked, in the founder's words.

## A good result
What the merged work did, and the link to its pull request.
```

Pick tickets that were hard, that went wrong once, or that the role does most often. Three to five per role is enough.

## Re-run a case

1. `python tools/heartbeat.py start <role>` prints the role's rubric.
2. Do the task on a branch you throw away. Never merge an eval run.
3. Grade it against the rubric and the good result, then record it:
   `python tools/heartbeat.py end <role> --eval <case> --checks <passed>/<total> --model <model> --usd <cost>`

The dashboard shows each case's last result on the role's page. Eval runs count toward spend but not toward the role's pass rate.
