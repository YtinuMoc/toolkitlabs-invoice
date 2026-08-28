# Profit margins at a glance — categorized income & expense

Clone of [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) buyer channel + [saksham82's Freelancer Finance Pack ($9)](https://saksham82.gumroad.com/l/cueko) profit dashboard.

## The problem faisalmq names

Without a clear view of profit margins, you make pricing decisions on guesswork. Is that long-term retainer actually profitable, or are software subscriptions and subcontractor costs eating the margin?

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) sells three outcomes:

1. **Automated summaries** — profit margins at a glance
2. **Tax preparedness** — expenses categorized before filing season
3. **Centralized data** — one log, not emails + bank statements

saksham82's **Profit dashboard** tab is the same promise: log invoices and expenses once, net profit recalculates per month.

## Free CLI preview

```bash
python3 freelancer_finance_pack.py --profit-margins invoices-sample.csv expenses-sample.csv
```

Look for `PROFIT MARGINS AT A GLANCE` in stdout:

```plaintext
=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===
  Active month: 2026-02
    2026-01  income $6,500.00  expense $412.00  net $6,088.00  margin 93.7%
    2026-02  income $0.00  expense $70.40  net $-70.40  margin 0.0% ← selected

  Categorized breakdown (2026-02) — tax preparedness:
    Payment fees: income $0.00  expense $12.40  net $-12.40
    Software: income $0.00  expense $10.00  net $-10.00
    Travel: income $0.00  expense $48.00  net $-48.00

  Per-client income rank (paid invoices) — price the next project:
    Beta LLC: $4,000.00 (62% of collected)
    Acme Corp: $2,500.00 (38% of collected)

  YTD profit margin: 93.0%  ($6,017.60 net on $6,500.00 income)
```

Switch months (workbook dropdown equivalent):

```bash
python3 freelancer_finance_pack.py --profit-margins invoices-sample.csv expenses-sample.csv 2026-01
```

## Why Google Sheets / CSV beats enterprise software

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo): no accounting degree, no bloated subscription. saksham82: shaded cells only — you type in the log, margins calculate themselves.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend after tax buffer
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [self-assessment-guide.md](self-assessment-guide.md) — landolio/5hae monthly tax pot
- [start-here.md](start-here.md) — full seven-sheet pack setup

Full bundle: [Freelancer Finance Pack landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-finance-pack/) — EUR 9 one-time.
