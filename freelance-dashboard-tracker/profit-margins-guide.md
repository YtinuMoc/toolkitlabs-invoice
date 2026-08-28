# Profit margins at a glance — categorized income & expense

Clone of [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) buyer channel + [Anna Hickman's Freelance Dashboard ($97 · 1,251 sales · 69 ratings)](https://cedabranding.gumroad.com/l/pro-dashboard).

## The problem faisalmq names

Without a clear view of profit margins, you price retainers on gut feel. Is that $3,200/month coaching client actually profitable after Notion, ads, and travel — or are you subsidizing them?

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) sells three outcomes:

1. **Automated summaries** — profit margins at a glance
2. **Tax preparedness** — expenses categorized before filing season
3. **Centralized data** — one log, not emails + bank statements

Anna Hickman's **Freelance Dashboard** is the planning layer: log revenue and expenses once, margin % recalculates per month.

## Free CLI preview

```bash
python3 freelance_dashboard_tracker.py --profit-margins revenue-sample.csv expenses-sample.csv
```

Look for `PROFIT MARGINS AT A GLANCE` in stdout:

```plaintext
=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===
  Active month: 2026-03
    2026-01  income $5,000.00  expense $295.00  net $4,705.00  margin 94.1%
    2026-02  income $4,150.00  expense $56.99  net $4,093.01  margin 98.6%
    2026-03  income $3,000.00  expense $28.00  net $2,972.00  margin 99.1% ← selected

  Categorized breakdown (2026-03) — tax preparedness:
    Consulting: income $3,000.00  expense $0.00  net $3,000.00
    Office: income $0.00  expense $28.00  net $-28.00

  Per-client income rank (paid income) — price the next project:
    Acme Coaching: $6,400.00 (46% of collected)
    Beta Consulting: $2,400.00 (17% of collected)

  YTD profit margin: 96.5%  ($11,770.01 net on $12,150.00 income)
```

Switch months (workbook dropdown equivalent):

```bash
python3 freelance_dashboard_tracker.py --profit-margins revenue-sample.csv expenses-sample.csv 2026-01
```

## Why margin % beats gross deposits

Pricing the next project from total deposits — not margin after expenses — is how freelancers undercharge retainers. The dashboard's monthly margin line is the planning metric spreadsheets hide.

## Pair with

- [invoice-panic-guide.md](invoice-panic-guide.md) — faisalmq/43dl overdue invoice flags
- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [freelance-finance-tracker-guide.md](freelance-finance-tracker-guide.md) — faisalmq/5598 income vs expenses
- [daily-check-guide.md](daily-check-guide.md) — wilsonhoe/2kdc 5-minute daily protocol
- [spreadsheet-trap-guide.md](spreadsheet-trap-guide.md) — wilsonhoe/4khk planning layer
- [start-here.md](start-here.md) — full revenue + expense setup

Full bundle: [Freelance Dashboard landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-dashboard-tracker/) — EUR 9 one-time.
