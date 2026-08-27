# Side Hustle Income + Expense Tracker

Shameless clone of [PattyBun tdmuz](https://pattybun.gumroad.com/l/tdmuz) ($9.99 Gumroad).

PattyBun ships an 8-tab Google Sheets system. Our clone ships CSV logs + Python CLI:

- Dashboard — all hustles side-by-side, YTD net, best performer, tax estimate
- 8 Hustle Tracker tabs — one `hustle` column per income stream
- Break-Even Calculator — sales/gigs needed to hit target take-home
- Quarterly Tax Planner — Q1–Q4 owed estimates
- Expense log — categories auto-summarized

```bash
python3 side_hustle_dashboard.py income-sample.csv expense-sample.csv
```

See [start-here.md](start-here.md) and [hustle-settings.md](hustle-settings.md).
