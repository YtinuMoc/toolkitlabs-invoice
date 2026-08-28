# Profit margins at a glance — categorized income & expense

Clone of [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) buyer channel + [moonlight573's Freelancer Finance Tracker ($10)](https://moonlight573.gumroad.com/l/unsjlk) live dashboard.

## The problem faisalmq names

Without a clear view of profit margins, you make pricing decisions on guesswork. Is that long-term retainer actually profitable, or are software subscriptions and subcontractor costs eating the margin?

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) sells three outcomes:

1. **Automated summaries** — profit margins at a glance
2. **Tax preparedness** — expenses categorized before filing season
3. **Centralized data** — one log, not emails + bank statements

moonlight573's **live dashboard** is the same promise: log income and expenses once, net profit recalculates per month.

## Free CLI preview

```bash
python3 freelancer_finance_tracker.py --profit-margins income-sample.csv expenses-sample.csv
```

Look for `PROFIT MARGINS AT A GLANCE` in stdout:

```plaintext
=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===
  Active month: 2026-02
    2026-01  income $6,500.00  expense $412.00  net $6,088.00  margin 93.7%
    2026-02  income $3,100.00  expense $70.40  net $3,029.60  margin 97.7% ← selected

  Categorized breakdown (2026-02) — tax preparedness:
    Payment fees: income $0.00  expense $12.40  net $-12.40
    Software: income $0.00  expense $10.00  net $-10.00
    Travel: income $0.00  expense $48.00  net $-48.00

  Per-client income rank (paid income) — price the next project:
    Beta LLC: $4,000.00 (42% of collected)
    Acme Corp: $2,500.00 (26% of collected)
    Gamma Studio: $1,900.00 (20% of collected)
    Delta Inc: $1,200.00 (12% of collected)

  YTD profit margin: 95.0%  ($9,117.60 net on $9,600.00 income)
```

Switch months (workbook dropdown equivalent):

```bash
python3 freelancer_finance_tracker.py --profit-margins income-sample.csv expenses-sample.csv 2026-01
```

## Why Google Sheets / CSV beats enterprise software

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo): no accounting degree, no bloated subscription. moonlight573: shaded cells only — you type in the log, margins calculate themselves.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend after tax buffer
- [tax-set-aside-guide.md](tax-set-aside-guide.md) — faisalmq/4gao deposit-day transfers
- [invoice-panic-guide.md](invoice-panic-guide.md) — faisalmq/43dl overdue invoice flags
- [finance-tracker-guide.md](finance-tracker-guide.md) — faisalmq/gc live dashboard
- [start-here.md](start-here.md) — full tracker setup

Full bundle: [Freelancer Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-finance-tracker/) — EUR 9 one-time.
