# Cash runway forecast — which month you run dry (agentchip/33mm shape)

Clone of [AgentChip's Freelancer Invoice & Client Tracker ($15)](https://qiliang.gumroad.com/l/ahefab) + [agentchip/33mm](https://dev.to/agentchip/your-spreadsheet-cant-tell-you-the-month-youll-run-out-of-cash-this-can-33mm) buyer channel: P&L is hindsight → forward projection → cash-gap alarm.

## The blind spot for freelancers

Lumpy client payments mean your bank balance lies. The survival question is forward-looking:

> Given payment history, SaaS subscriptions, bills, and debt minimums — **which month does cash go negative?**

## What the CLI forecast does

`freelancer_invoice_tracker.py` builds a **12-month cash runway** from your payment log + fixed obligations:

1. **Rolling forecast** — opening balance, income, expenses, tax set-aside, closing balance per month
2. **Cash-gap alarm** — flags the lowest-balance month; warns if balance goes negative
3. **Three scenarios** — optimistic (income ×1.2), base, pessimistic (×0.8)

```bash
python3 freelancer_invoice_tracker.py clients-sample.csv invoices-sample.csv payments-sample.csv subscriptions-sample.csv bills-sample.csv debt-sample.csv
```

Look for the `CASH RUNWAY FORECAST` block in stdout.

## Inputs

| File | Role |
|------|------|
| `payments-sample.csv` | Payment dates → historical income by month |
| `subscriptions-sample.csv` | Recurring SaaS monthly load (optional) |
| `bills-sample.csv` | Recurring monthly obligations (optional) |
| `debt-sample.csv` | Minimum debt payments (optional) |

Set starting cash in `FINANCE_STARTING_CASH` env var (default: $3,000).

## When to run it

- **Monthly** — after logging new client payments
- **Before a slow season** — pessimistic scenario shows the danger month early
- **Before hiring** — see what a new recurring cost does to the curve

## Paid kit

Full five-sheet workbook: [Freelancer Invoice & Client Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-invoice-tracker/) · EUR 9 one-time · same delivery shape as [AgentChip on Gumroad ($15)](https://qiliang.gumroad.com/l/ahefab).
