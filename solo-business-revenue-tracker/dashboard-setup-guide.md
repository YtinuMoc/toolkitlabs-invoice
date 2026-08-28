# Solo business financial dashboard — setup in five minutes

Clone of [datanestdigital/4l0h](https://dev.to/datanestdigital/freelance-financial-dashboard-4l0h) buyer channel + [amyragland's Solo Business Revenue & Expense Tracker ($10)](https://amyragland.gumroad.com/l/tckuq).

Know your numbers without hiring a bookkeeper. datanestdigital ships a Google Sheets dashboard with income logging, expense categories, tax estimates, and monthly charts. Our clone uses CSV + Python — same delivery shape, no Google account.

## Five-minute setup

1. **Download** the free sample CSVs from the [landing page](https://ytinumoc.github.io/toolkitlabs-invoice/solo-business-revenue-tracker/) or unzip the paid kit.
2. **Copy** `revenue-template.csv` and `expenses-template.csv` to your working folder.
3. **Log** your first month: one row per client payment, one row per expense.
4. **Configure** your tax set-aside rate (default 25% — pass a custom rate to the CLI).
5. **Run** the dashboard preview:

```bash
python3 solo_business_revenue_tracker.py --dashboard revenue-sample.csv expenses-sample.csv
```

## What the dashboard shows

| Metric | What it answers |
|--------|----------------|
| Revenue | How much did clients actually pay? |
| Expenses | Where is the money going? |
| Net profit | What's left after costs? |
| Tax set-aside | How much to park before spending? |
| Take-home | What's safe to keep? |
| Margin % | Is this month actually profitable? |

## Expense categories (pre-configured taxonomy)

| Category | Examples | Deductible |
|----------|----------|------------|
| Software | Hosting, SaaS, licenses | Yes |
| Marketing | Ads, SEO tools | Yes |
| Office | Coworking, home office | Yes |
| Equipment | Computer, peripherals | Yes |
| Fees | Stripe, wire fees | Yes |
| Other | Uncategorized | Review |

## Monthly dashboard block (CLI stdout)

```
═══════════════ JANUARY 2026 ═══════════════
Revenue:        $3,550.00
Expenses:       $213.99
Net Profit:     $3,336.01    Margin: 93.9%
Tax Set-Aside:  $834.00  (25% of net)
Take-Home:      $2,502.01
```

## Best practices (from datanestdigital/4l0h)

1. **Separate business and personal accounts** — makes categorization automatic.
2. **Log expenses weekly** — Friday afternoon, not April panic.
3. **Reconcile monthly** — compare sheet totals to bank statements.
4. **Review profit margins by client** — some clients cost more than they're worth.
5. **Update tax estimates quarterly** — adjust based on actual income, not projections.
6. **Back up monthly** — download CSV copies at month-end.

## Paid kit

Full solo business revenue tracker: [landing page](https://ytinumoc.github.io/toolkitlabs-invoice/solo-business-revenue-tracker/) · EUR 9 one-time · same delivery shape as [amyragland on Gumroad ($10)](https://amyragland.gumroad.com/l/tckuq).
