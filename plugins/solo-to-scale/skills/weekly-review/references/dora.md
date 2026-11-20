# The five DORA metrics, from GitHub and CI data (last 4 weeks)

| Metric | How | Before deploys exist |
| --- | --- | --- |
| Deployment frequency | Successful deploy runs per week (`gh run list --workflow <deploy>`) | n/a until deploys exist |
| Change lead time | PR opened to deployed (or to merged, labelled "to merge", until deploys exist) | Report PR opened to merged |
| Change failure rate | Deploys followed by a rollback or hotfix PR within 7 days | n/a until deploys exist |
| Failed-deployment recovery time | Failed deploy to the next successful deploy | n/a until deploys exist |
| Deployment rework rate | Deploys that are unplanned fixes for a recent deploy | n/a until deploys exist |

Use real numbers or "n/a". Never fill a metric with a guess.
