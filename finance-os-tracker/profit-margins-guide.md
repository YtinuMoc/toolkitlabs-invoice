# Profit margins at a glance — categorized income & expense

Clone of [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) buyer channel + [heyismail Finance OS Pro ($29+ · 15,254 sales)](https://heyismail.gumroad.com/l/TheUltimateFinanceTracker) profit margin module.

## The problem faisalmq names

Without a clear view of profit margins, you make pricing decisions on guesswork. Is that retainer actually profitable, or are software subscriptions and contractor costs eating the margin?

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) sells three outcomes:

1. **Automated summaries** — profit margins at a glance
2. **Tax preparedness** — expenses categorized before filing season
3. **Centralized data** — one log, not emails + bank statements

heyismail's **Finance OS Pro** includes profit margin tracking in the same income + expense command center.

## Free CLI preview

```bash
python3 finance_os_tracker.py --profit-margins income-sample.csv expenses-sample.csv
```

Look for `PROFIT MARGINS AT A GLANCE` in stdout:

```plaintext
=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===
  Active month: 2026-03
    2026-01  income $5,390.00  expense $1,061.00  net $4,329.00  margin 80.3%
    2026-02  income $4,820.00  expense $164.00  net $4,656.00  margin 96.6%
    2026-03  income $5,740.00  expense $185.00  net $5,555.00  margin 96.8% ← selected

  Categorized breakdown (2026-03) — tax preparedness:
    Marketing: income $0.00  expense $150.00  net $-150.00
    Office: income $0.00  expense $35.00  net $-35.00

  Per-source income rank — price the next offer:
    Client retainer: $13,500.00 (79% of collected)
    Digital product: $2,130.00 (13% of collected)
    Affiliate commission: $320.00 (2% of collected)

  YTD profit margin: 91.0%  ($14,540.00 net on $15,950.00 income)
```

Switch months (workbook dropdown equivalent):

```bash
python3 finance_os_tracker.py --profit-margins income-sample.csv expenses-sample.csv 2026-01
```

## Why CSV beats enterprise software

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo): no accounting degree, no bloated subscription. heyismail Finance OS: one command center for income, expenses, budgets, subscriptions, and net worth.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend after tax buffer
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [invoice-panic-guide.md](invoice-panic-guide.md) — faisalmq/43dl overdue invoice flags
- [self-assessment-guide.md](self-assessment-guide.md) — landolio/5hae monthly P&L
- [merge-ledger-guide.md](merge-ledger-guide.md) — goldenalien/206o unified ledger
- [finance-os-guide.md](finance-os-guide.md) — full command center
- [start-here.md](start-here.md) — full tracker setup

Full bundle: [Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-os-tracker/) — EUR 9 one-time.
