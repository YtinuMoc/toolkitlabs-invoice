# Start here — 5 minutes

Clone of [PattyBun rauxja](https://pattybun.gumroad.com/l/rauxja) ($14.99 Gumroad checkout).

1. Copy `revenue-log-template.csv` → `my-revenue.csv`
2. Log every sale: date, platform, product, gross
3. Run: `python3 creator_dashboard.py my-revenue.csv`
4. Read stdout: Dashboard · Platform Summary · Product Performance · Tax & Annual Summary

Six-tab promise mapped to CLI sections (PattyBun Gumroad copy):

- **Dashboard** — YTD gross, fees, net, best platform, best product
- **Revenue Log** — your CSV (single source of truth)
- **Platform Summary** — net by platform, monthly rollups
- **Product Performance** — units, gross, net per SKU
- **Launch Tracker** — filter rows where `notes` contains `launch`
- **Tax & Annual Summary** — quarterly net + 25% set-aside estimate (US default)

Free sample: `sample-revenue.csv`
