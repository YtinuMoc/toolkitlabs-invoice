# Profit margins at a glance — categorized income & expense (By the Loop clone)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo).

## The problem faisalmq names

Without a clear view of profit margins, you make pricing decisions on guesswork. Are you actually profitable on that long-term project, or are overhead costs eating the margin?

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) sells three outcomes:

1. **Automated summaries** — profit margins at a glance
2. **Tax preparedness** — expenses categorized before filing season
3. **Centralized data** — one log, not emails + bank statements

By the Loop's **Expense + Tax Buffer** tab is the same promise: log once, categorized, net profit recalculates from paid invoices minus expenses.

## Free CLI preview

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Look for `PROFIT MARGINS AT A GLANCE` in stdout:

```plaintext
=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===
  Collected (paid):    $3,550.00
  Expenses YTD:        $313.99
  Net profit:          $3,236.01
  Profit margin:       91.2%
  Categorized breakdown (tax preparedness):
    marketing    $120.00  (3.4% of revenue)
    education    $89.00  (2.5% of revenue)
    software     $69.99  (2.0% of revenue)
    office       $35.00  (1.0% of revenue)
```

**Profit margin** = net profit ÷ collected revenue. If margin drops month over month, subscriptions or underpriced clients are eating you alive — not tax season surprises.

## Why guesswork undercharges you

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo): without margin visibility you undercharge because you don't account for software, transaction fees, and self-employment taxes. By the Loop bundles invoice tracker + expense log + rate calculator + quarterly estimator so margin math stays in one file.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend after tax buffer
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [beginner-guide.md](beginner-guide.md) — faisalmq/2fj6 no-formula onboarding
- [start-here.md](start-here.md) — four-tool bundle setup

Full bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — invoice tracker + expense/tax buffer + rate calculator + quarterly estimator.
