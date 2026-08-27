# Freelance financial dashboard — setup in five minutes

Clone of [datanestdigital/4l0h](https://dev.to/datanestdigital/freelance-financial-dashboard-4l0h) buyer channel + [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).

Know your numbers without hiring a bookkeeper. datanestdigital ships a Google Sheets dashboard with income logging, expense categories, tax estimates, and monthly charts. Our clone uses CSV + Python — same delivery shape, no Google account.

## Five-minute setup

1. **Download** the free sample CSVs from the [landing page](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) or unzip the paid kit.
2. **Copy** `invoice-log-template.csv` and `expense-log-template.csv` to your working folder.
3. **Log** your first month: one row per client payment in the invoice log, one row per expense.
4. **Configure** your tax set-aside rate (default 25% in the CLI — edit `TAX_BUFFER_PCT` or pass a custom rate).
5. **Run** the dashboard preview:

```bash
python3 freelance_finance_os.py --dashboard invoice-log-sample.csv expense-log-sample.csv
```

## What the dashboard shows

| Metric | Source |
|--------|--------|
| Revenue (paid) | Invoice log — `status=paid` |
| Expenses | Expense log — categorized |
| Net profit | Paid revenue − expenses |
| Tax set-aside | Net profit × your reserve % |
| Take-home | Net profit − tax set-aside |
| Outstanding | Sent invoices not yet paid |
| Overdue | Sent + past due date |

## Expense categories (pre-configured taxonomy)

| Category | Examples | Deductible |
|----------|----------|------------|
| software | Hosting, SaaS, licenses | Yes |
| office | Coworking, home office | Yes |
| marketing | Ads, SEO tools | Yes |
| professional | Courses, conferences | Yes |
| insurance | Liability, health | Yes |
| travel | Client meetings | Yes |
| equipment | Computer, peripherals | Yes |
| subcontractor | Outsourced work | Yes |
| fees | Stripe, wire fees | Yes |
| other | Uncategorized | Review |

## Monthly dashboard block (CLI stdout)

```
═══════════════ JANUARY 2026 ═══════════════
Revenue:        $3,550    (paid invoices)
Expenses:       $214      (categorized)
Net Profit:     $3,336    Margin: 93.9%
Tax Set-Aside:  $834      (25% of net)
Take-Home:      $2,502
Outstanding:    $2,750    (awaiting payment)
```

## Best practices (from datanestdigital/4l0h)

1. **Separate business and personal accounts** — makes categorization automatic.
2. **Log expenses weekly** — Friday afternoon, not April panic.
3. **Reconcile monthly** — compare sheet totals to bank statements.
4. **Review profit margins by client** — some clients cost more than they're worth.
5. **Update tax estimates quarterly** — adjust based on actual income, not projections.
6. **Back up monthly** — download CSV copies at month-end.

## Paid kit

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
