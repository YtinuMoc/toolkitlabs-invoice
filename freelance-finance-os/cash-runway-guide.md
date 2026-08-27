# Cash runway forecast — which month you run dry (agentchip/33mm shape)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) + [agentchip/33mm](https://dev.to/agentchip/your-spreadsheet-cant-tell-you-the-month-youll-run-out-of-cash-this-can-33mm) buyer channel: P&L is hindsight → forward projection → cash-gap alarm.

## The blind spot for freelancers

Lumpy client payments mean your bank balance lies. The survival question is forward-looking:

> Given paid income history, recurring bills, and debt minimums — **which month does cash go negative?**

## What the CLI forecast does

`freelance_finance_os.py` builds a **12-month cash runway** from your invoice + expense logs:

1. **Rolling forecast** — opening balance, income, expenses, tax set-aside, closing balance per month
2. **Cash-gap alarm** — flags the lowest-balance month; warns if balance goes negative
3. **Three scenarios** — optimistic (income ×1.2), base, pessimistic (×0.8)

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv subscriptions-sample.csv bills-sample.csv debt-sample.csv
```

Look for the `CASH RUNWAY FORECAST` block in stdout.

## Inputs

| File | Role |
|------|------|
| `invoice-log.csv` | Paid invoices → historical income by month |
| `expense-log.csv` | Categorized expenses by month |
| `bills-sample.csv` | Recurring monthly obligations (optional) |
| `debt-sample.csv` | Minimum debt payments (optional) |

Set starting cash in `FINANCE_STARTING_CASH` env var (default: $3,000).

## When to run it

- **Monthly** — after updating invoice + expense logs
- **Before a slow season** — pessimistic scenario shows the danger month early
- **Before hiring** — see what a new recurring cost does to the curve

## Paid kit

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
